"""Inventory teaching inputs without exposing user accounts or machine paths."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not args.inputs.is_dir():
        parser.error("Input directory not found. Check your current directory and --inputs.")
    paths = sorted(p for p in args.inputs.iterdir() if p.is_file())
    if not paths:
        parser.error("Input directory contains no files.")
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in paths:
        data = path.read_bytes()
        lines = data.decode("utf-8", errors="replace").splitlines()
        rows.append({"file": path.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "ATOM_records": sum(line.startswith("ATOM  ") for line in lines), "HETATM_records": sum(line.startswith("HETATM") for line in lines), "inspection": "record counts only; inspect chemistry separately"})
    with (args.out / "input_inventory.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "environment.json").write_text(json.dumps({"python": platform.python_version(), "system": platform.system(), "script": "check_files.py", "arguments": {"inputs": "INPUTS", "out": "OUTPUTS"}}, indent=2), encoding="utf-8")
    print(f"Recorded {len(rows)} file(s): input_inventory.tsv and environment.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
