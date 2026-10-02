"""Read a teaching configuration or an existing RFD3 output using Python only."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import re


def inspect_config(path: Path) -> list[dict[str, str]]:
    tasks = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(tasks, dict) or not tasks:
        raise ValueError("The JSON must contain at least one named task")
    rows = []
    for name, task in tasks.items():
        if not isinstance(task, dict):
            raise ValueError(f"{name}: task must be an object")
        if "length" not in task and "contig" not in task:
            raise ValueError(f"{name}: provide length or contig")
        if "length" in task:
            length = task["length"]
            if isinstance(length, int) and not isinstance(length, bool):
                valid = length > 0
            elif isinstance(length, str) and re.fullmatch(r"\d+-\d+", length):
                lower, upper = map(int, length.split("-"))
                valid = 0 < lower <= upper
            else:
                valid = False
            if not valid:
                raise ValueError(f"{name}: length must be a positive integer or ascending range")
        if "contig" in task and (not isinstance(task["contig"], str) or not task["contig"].strip()):
            raise ValueError(f"{name}: contig must be a nonempty string")
        source = task.get("input")
        status = "recorded"
        if source and not (path.parent / source).resolve().is_file():
            status = "input_missing"
        rows.append({"object": name, "field": "task", "value": str(task.get("contig", task.get("length"))), "status": status})
        for residue, atoms in task.get("select_hotspots", {}).items():
            rows.append({"object": name, "field": "hotspot", "value": f"{residue}:{atoms}", "status": "recorded"})
    return rows


def inspect_pdb(path: Path) -> list[dict[str, str]]:
    chains: dict[str, set[tuple[str, str]]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("ATOM"):
            chains.setdefault(line[21], set()).add((line[22:27].strip(), line[17:20]))
    if not chains:
        raise ValueError("No ATOM records found")
    return [{"object": chain, "field": "residue_count", "value": str(len(residues)), "status": "read_from_coordinates"} for chain, residues in sorted(chains.items())]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--pdb", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if not any((args.config, args.pdb, args.metadata)):
        parser.error("provide --config, --pdb, or --metadata")
    rows: list[dict[str, str]] = []
    if args.config:
        rows.extend(inspect_config(args.config))
    if args.pdb:
        rows.extend(inspect_pdb(args.pdb))
    if args.metadata:
        data = json.loads(args.metadata.read_text(encoding="utf-8"))
        for key in ("num_residues", "n_chainbreaks", "non_loop_fraction", "radius_of_gyration"):
            value = data.get("metrics", {}).get(key)
            rows.append({"object": args.metadata.stem, "field": key, "value": "" if value is None else str(value), "status": "upstream_metadata" if value is not None else "not_present"})
    for row in rows:
        print("\t".join(row.values()))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["object", "field", "value", "status"], delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
    return 1 if any(row["status"] == "input_missing" for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
