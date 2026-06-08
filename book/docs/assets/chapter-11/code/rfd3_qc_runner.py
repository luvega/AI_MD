#!/usr/bin/env python3
"""
RFD3 / ProteinMPNN QC manifest summarizer for Chapter 11.

This script is a teaching example. It does not run RFD3, ProteinMPNN, Boltz2,
Vina, or any external service. It reads a batch manifest, checks expected output
files when they exist, applies transparent example thresholds, and writes a QC
summary table. Thresholds are placeholders for workflow training and must not be
treated as universal scientific criteria.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Thresholds:
    plddt_min: float = 70.0
    ipae_max: float = 10.0
    rmsd_max: float = 2.5
    interface_contacts_min: int = 8
    motif_rmsd_max: float = 1.5


SUMMARY_FIELDS = [
    "task_id",
    "stage",
    "candidate_id",
    "tool",
    "output_dir",
    "expected_files_found",
    "metric_warnings",
    "decision",
    "fallback",
    "evidence_boundary",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize an RFD3 / ProteinMPNN teaching manifest into a QC table."
    )
    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="CSV manifest with candidate rows and optional QC metrics.",
    )
    parser.add_argument(
        "--summary-csv",
        required=True,
        type=Path,
        help="Output CSV path for the QC summary.",
    )
    parser.add_argument(
        "--report-md",
        type=Path,
        help="Optional Markdown report path.",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=None,
        help="Base directory for resolving relative paths. Defaults to the manifest directory.",
    )
    return parser.parse_args()


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def as_float(row: dict[str, str], field: str) -> float | None:
    value = row.get(field, "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def as_int(row: dict[str, str], field: str) -> int | None:
    value = row.get(field, "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def resolve_path(base: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return base / path


def expected_files_found(row: dict[str, str], base: Path) -> tuple[bool, list[str]]:
    expected = [item.strip() for item in row.get("expected_files", "").split(";") if item.strip()]
    output_dir = row.get("output_dir", "")
    if not expected or not output_dir:
        return False, ["missing expected_files or output_dir"]

    out_path = resolve_path(base, output_dir)
    missing = [name for name in expected if not (out_path / name).exists()]
    return not missing, missing


def metric_warnings(row: dict[str, str], thresholds: Thresholds) -> list[str]:
    warnings: list[str] = []

    checks: list[tuple[str, float | int | None, str]] = [
        ("plddt", as_float(row, "plddt"), f"< {thresholds.plddt_min}"),
        ("ipae", as_float(row, "ipae"), f"> {thresholds.ipae_max}"),
        ("rmsd", as_float(row, "rmsd"), f"> {thresholds.rmsd_max}"),
        (
            "interface_contacts",
            as_int(row, "interface_contacts"),
            f"< {thresholds.interface_contacts_min}",
        ),
        ("motif_rmsd", as_float(row, "motif_rmsd"), f"> {thresholds.motif_rmsd_max}"),
    ]

    for field, value, rule in checks:
        if value is None:
            warnings.append(f"{field}=missing")
            continue
        if field == "plddt" and value < thresholds.plddt_min:
            warnings.append(f"{field}{rule}")
        elif field == "ipae" and value > thresholds.ipae_max:
            warnings.append(f"{field}{rule}")
        elif field == "rmsd" and value > thresholds.rmsd_max:
            warnings.append(f"{field}{rule}")
        elif field == "interface_contacts" and value < thresholds.interface_contacts_min:
            warnings.append(f"{field}{rule}")
        elif field == "motif_rmsd" and value > thresholds.motif_rmsd_max:
            warnings.append(f"{field}{rule}")

    return warnings


def decide(files_ok: bool, missing_files: list[str], warnings: list[str]) -> str:
    if missing_files and "missing expected_files or output_dir" not in missing_files:
        return "fail"
    if not files_ok or warnings:
        return "review"
    return "pass"


def summarize_rows(rows: Iterable[dict[str, str]], base: Path) -> list[dict[str, str]]:
    thresholds = Thresholds()
    summary: list[dict[str, str]] = []

    for row in rows:
        files_ok, missing = expected_files_found(row, base)
        warnings = metric_warnings(row, thresholds)
        decision = decide(files_ok, missing, warnings)
        fallback = row.get("fallback", "")
        if decision == "fail" and not fallback:
            fallback = "rerun_or_inspect_missing_outputs"
        elif decision == "review" and not fallback:
            fallback = "manual_qc_review"

        summary.append(
            {
                "task_id": row.get("task_id", ""),
                "stage": row.get("stage", ""),
                "candidate_id": row.get("candidate_id", ""),
                "tool": row.get("tool", ""),
                "output_dir": row.get("output_dir", ""),
                "expected_files_found": "yes" if files_ok else "no: " + ";".join(missing),
                "metric_warnings": ";".join(warnings) if warnings else "none",
                "decision": decision,
                "fallback": fallback,
                "evidence_boundary": (
                    "Computational QC only; predictions and scores require structural, "
                    "biochemical, or functional validation before scientific claims."
                ),
            }
        )

    return summary


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total = len(rows)
    counts = {label: sum(1 for row in rows if row["decision"] == label) for label in ["pass", "review", "fail"]}
    lines = [
        "# RFD3 / ProteinMPNN QC Summary",
        "",
        "This report is generated from a teaching manifest. It is not an experimental result.",
        "",
        f"- Total rows: {total}",
        f"- Pass: {counts['pass']}",
        f"- Review: {counts['review']}",
        f"- Fail: {counts['fail']}",
        "",
        "| Candidate | Stage | Tool | Decision | Warnings | Fallback |",
        "|:---|:---|:---|:---|:---|:---|",
    ]
    for row in rows:
        lines.append(
            "| {candidate_id} | {stage} | {tool} | {decision} | {metric_warnings} | {fallback} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "",
            "This summary only checks files and example metrics. It does not prove binding, activity, stability, selectivity, low off-target risk, or clinical relevance.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    manifest = args.manifest.resolve()
    base = (args.workspace_root or manifest.parent).resolve()
    rows = read_manifest(manifest)
    summary = summarize_rows(rows, base)
    write_summary(args.summary_csv, summary)
    if args.report_md:
        write_report(args.report_md, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
