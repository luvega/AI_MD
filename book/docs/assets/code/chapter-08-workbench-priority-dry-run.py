"""Dry-run project priority table for chapter 08.

The script separates literature cases, dry-runs, validated computation, and
experimental results so project planning does not promote borrowed case studies
into local findings.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_ROWS = [
    {
        "project_id": "PPI001",
        "question": "PPI screening route",
        "evidence_maturity": "case-study",
        "method_readiness": "3",
        "data_readiness": "2",
        "experiment_feasibility": "2",
        "expected_output": "reading note and dry-run plan",
    },
    {
        "project_id": "VS001",
        "question": "small-molecule virtual screening",
        "evidence_maturity": "dry-run",
        "method_readiness": "4",
        "data_readiness": "3",
        "experiment_feasibility": "3",
        "expected_output": "candidate manifest and docking record",
    },
    {
        "project_id": "DES001",
        "question": "binder design route",
        "evidence_maturity": "validated-computation",
        "method_readiness": "3",
        "data_readiness": "3",
        "experiment_feasibility": "2",
        "expected_output": "design QC table and validation queue",
    },
]

MATURITY_WEIGHT = {
    "case-study": 1,
    "dry-run": 2,
    "validated-computation": 3,
    "experimental-result": 4,
}


def load_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return list(DEFAULT_ROWS)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def score(row: dict[str, str]) -> dict[str, str]:
    maturity = MATURITY_WEIGHT.get(row["evidence_maturity"], 0)
    method = int(row["method_readiness"])
    data = int(row["data_readiness"])
    feasibility = int(row["experiment_feasibility"])
    priority = maturity * 0.35 + method * 0.25 + data * 0.20 + feasibility * 0.20
    if row["evidence_maturity"] == "case-study":
        status = "do_not_report_as_local_result"
    elif priority >= 3.0:
        status = "ready_for_experiment_queue"
    else:
        status = "needs_more_evidence"
    return {
        **row,
        "priority_score": f"{priority:.2f}",
        "decision": status,
        "boundary_note": "Keep literature cases, dry-runs, validated computation, and experiments separate.",
    }


def write_rows(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "project_id",
        "question",
        "evidence_maturity",
        "method_readiness",
        "data_readiness",
        "experiment_feasibility",
        "expected_output",
        "priority_score",
        "decision",
        "boundary_note",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Optional TSV with project priority fields.")
    parser.add_argument("--out", type=Path, default=Path("outputs/chapter-08-workbench-priority.tsv"))
    args = parser.parse_args()
    rows = [score(row) for row in load_rows(args.input)]
    rows.sort(key=lambda item: float(item["priority_score"]), reverse=True)
    write_rows(rows, args.out)
    print(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
