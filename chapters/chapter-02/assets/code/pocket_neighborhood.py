"""Count protein residues near crystal JZ4 using auth PDB IDs and altloc A."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdb", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    protein, ligand = [], []
    for line in args.pdb.read_text().splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        if line[21] != "A" or line[16] not in " A":
            continue
        xyz = tuple(float(line[a:b]) for a, b in [(30, 38), (38, 46), (46, 54)])
        if line.startswith("ATOM  "):
            protein.append(((line[21], line[22:26].strip(), line[17:20]), xyz))
        elif line[17:20] == "JZ4" and line[22:26].strip() == "167":
            ligand.append(xyz)
    if not protein or len(ligand) != 10:
        raise ValueError("Expected protein auth A and JZ4 A167 with ten atoms")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["radius_angstrom", "residue_count", "auth_residues", "selection_policy"], delimiter="\t")
        writer.writeheader()
        for radius in [3.0, 5.0, 7.0]:
            selected = sorted({res for res, point in protein if any(sum((a - b) ** 2 for a, b in zip(point, other)) <= radius ** 2 for other in ligand)}, key=lambda row: int(row[1]))
            writer.writerow({"radius_angstrom": radius, "residue_count": len(selected), "auth_residues": ";".join(f"{c}:{r}:{name}" for c, r, name in selected), "selection_policy": "auth chain A; blank/A alternate locations; any protein atom within radius of crystal JZ4"})
    print("Saved residue-neighborhood counts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
