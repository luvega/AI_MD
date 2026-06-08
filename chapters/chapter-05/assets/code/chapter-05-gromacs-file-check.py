#!/usr/bin/env python3
"""Check the minimum file set for a teaching GROMACS MD setup.

This script is a dry-run helper for Chapter 5. It checks whether the files
needed to discuss a basic EM/NVT/NPT/production workflow are present. It does
not run GROMACS and does not produce molecular simulation results.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from tempfile import TemporaryDirectory


REQUIRED_FILES = [
    ("structure", "protein.pdb", "initial protein or complex structure"),
    ("topology", "topol.top", "main topology file"),
    ("parameter", "em.mdp", "energy minimization parameters"),
    ("parameter", "nvt.mdp", "constant-volume equilibration parameters"),
    ("parameter", "npt.mdp", "constant-pressure equilibration parameters"),
    ("parameter", "md.mdp", "production MD parameters"),
]


def ensure_demo_files(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for _, filename, purpose in REQUIRED_FILES:
        path = root / filename
        path.write_text(f"; demo file for {purpose}\n", encoding="utf-8")


def check_files(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for kind, filename, purpose in REQUIRED_FILES:
        path = root / filename
        exists = path.exists()
        rows.append(
            {
                "kind": kind,
                "file": filename,
                "status": "pass" if exists else "missing",
                "purpose": purpose,
                "note": "present" if exists else "add or regenerate before running grompp/mdrun",
            }
        )
    return rows


def write_tsv(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["kind", "file", "status", "purpose", "note"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, str]]) -> str:
    passed = sum(row["status"] == "pass" for row in rows)
    missing = sum(row["status"] == "missing" for row in rows)
    return f"GROMACS setup dry-run: pass={passed} missing={missing}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="directory to check")
    parser.add_argument("--out", type=Path, default=Path("gromacs-file-check.tsv"), help="TSV output path")
    parser.add_argument("--demo", action="store_true", help="create a temporary demo with one missing file")
    args = parser.parse_args()

    if args.demo:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            ensure_demo_files(root)
            rows = check_files(root)
            write_tsv(rows, args.out)
    else:
        rows = check_files(args.root)
        write_tsv(rows, args.out)

    print(f"{summarize(rows)} out={args.out}")
    return 0 if all(row["status"] == "pass" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
