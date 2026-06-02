"""Dry-run protein design QC table for chapter 06.

This is a record-template helper, not an RFdiffusion/RFD3, ProteinMPNN, or
AlphaFold/Boltz execution script. It shows which fields should be collected
before a generated design is promoted to follow-up analysis.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_ROWS = [
    {
        "design_id": "DES001",
        "backbone_source": "rfdiffusion_dry_run",
        "seed": "101",
        "checkpoint": "teaching_checkpoint",
        "motif_rmsd": "0.8",
        "refold_rmsd": "1.6",
        "interface_contacts": "18",
        "pae_interface": "5.2",
        "sequence_recovery": "0.42",
    },
    {
        "design_id": "DES002",
        "backbone_source": "rfdiffusion_dry_run",
        "seed": "102",
        "checkpoint": "teaching_checkpoint",
        "motif_rmsd": "2.7",
        "refold_rmsd": "4.9",
        "interface_contacts": "6",
        "pae_interface": "18.5",
        "sequence_recovery": "0.21",
    },
]


def load_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return list(DEFAULT_ROWS)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def qc(row: dict[str, str]) -> dict[str, str]:
    motif_rmsd = float(row["motif_rmsd"])
    refold_rmsd = float(row["refold_rmsd"])
    contacts = int(row["interface_contacts"])
    pae = float(row["pae_interface"])
    sequence_recovery = float(row["sequence_recovery"])
    passed = motif_rmsd <= 1.5 and refold_rmsd <= 2.5 and contacts >= 10 and pae <= 10
    reasons = []
    if motif_rmsd > 1.5:
        reasons.append("motif_rmsd")
    if refold_rmsd > 2.5:
        reasons.append("refold_rmsd")
    if contacts < 10:
        reasons.append("interface_contacts")
    if pae > 10:
        reasons.append("pae_interface")
    if sequence_recovery < 0.25:
        reasons.append("sequence_diversity_review")
    return {
        **row,
        "interface_qc_passed": "pass" if passed else "review",
        "discard_reason": ";".join(reasons),
        "next_step": "ProteinMPNN/refold review" if passed else "revise constraints or discard",
        "boundary_note": "Design QC is computational triage, not expression or binding evidence.",
    }


def write_rows(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "design_id",
        "backbone_source",
        "seed",
        "checkpoint",
        "motif_rmsd",
        "refold_rmsd",
        "interface_contacts",
        "pae_interface",
        "sequence_recovery",
        "interface_qc_passed",
        "discard_reason",
        "next_step",
        "boundary_note",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Optional TSV with design QC fields.")
    parser.add_argument("--out", type=Path, default=Path("outputs/chapter-06-design-qc.tsv"))
    args = parser.parse_args()
    rows = [qc(row) for row in load_rows(args.input)]
    write_rows(rows, args.out)
    print(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
