"""Prepare a small public 3HTB/CCD teaching case; no course files are read.

Run from a working directory of your choice:
  python prepare_3htb.py --out inputs/3htb
Requires RDKit, Meeko, Gemmi, NumPy and SciPy. The output retains the original
PDB/CCD data and the exact commands used for preparation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import Request, urlopen


SOURCES = {
    "3htb.pdb": "https://files.rcsb.org/download/3HTB.pdb",
    "jz4_reference.sdf": "https://models.rcsb.org/v1/3htb/ligand?auth_asym_id=A&auth_seq_id=167&encoding=sdf",
    "JZ4_ideal.sdf": "https://files.rcsb.org/ligands/download/JZ4_ideal.sdf",
    "IPH_ideal.sdf": "https://files.rcsb.org/ligands/download/IPH_ideal.sdf",
    "BNZ_ideal.sdf": "https://files.rcsb.org/ligands/download/BNZ_ideal.sdf",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, help="Use already downloaded public files instead of the network")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    from rdkit import Chem
    from meeko import MoleculePreparation, PDBQTWriterLegacy

    downloads = []
    for filename, url in SOURCES.items():
        path = out / filename
        if args.source_dir:
            content = (args.source_dir / filename).read_bytes()
        else:
            with urlopen(Request(url, headers={"User-Agent": "AI_MD-public-teaching-case/1.0"}), timeout=60) as response:
                content = response.read()
        path.write_bytes(content)
        downloads.append({"file": filename, "source_url": url, "sha256": hashlib.sha256(content).hexdigest(), "license": "CC0-1.0 (wwPDB archive data)"})

    pdb = (out / "3htb.pdb").read_text()
    atoms = [line for line in pdb.splitlines() if line.startswith("ATOM  ") and line[21] == "A"]
    if not atoms:
        raise ValueError("No protein ATOM records for auth chain A")
    (out / "3htb_receptor.pdb").write_text("\n".join(atoms) + "\nTER\nEND\n")
    reference = Chem.SDMolSupplier(str(out / "jz4_reference.sdf"), removeHs=False)[0]
    if reference is None or reference.GetNumHeavyAtoms() != 10:
        raise ValueError("Expected one JZ4 reference with 10 heavy atoms")
    xyz = Chem.RemoveHs(reference).GetConformer().GetPositions()
    center = xyz.mean(axis=0)
    box = [18.0, 18.0, 18.0]
    receptor_cmd = [sys.executable, "-m", "meeko.cli.mk_prepare_receptor", "--read_pdb", "3htb_receptor.pdb", "--default_altloc", "A", "-o", "3htb_receptor", "-p", "-v", "--box_center", *[f"{v:.3f}" for v in center], "--box_size", *[str(v) for v in box]]
    result = subprocess.run(receptor_cmd, cwd=out, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / "receptor_preparation.log").write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError("Receptor preparation failed; read receptor_preparation.log")

    rows = []
    for component in ["JZ4", "IPH", "BNZ"]:
        mol = Chem.SDMolSupplier(str(out / f"{component}_ideal.sdf"), removeHs=False)[0]
        if mol is None:
            raise ValueError(f"Cannot read CCD {component}")
        mol = Chem.AddHs(mol, addCoords=True)
        setup = MoleculePreparation().prepare(mol)[0]
        pdbqt, ok, error = PDBQTWriterLegacy.write_string(setup)
        if not ok:
            raise ValueError(error)
        (out / f"{component}.pdbqt").write_text(pdbqt)
        rows.append({"ligand_id": component, "source_sdf": f"{component}_ideal.sdf", "prepared_pdbqt": f"{component}.pdbqt", "heavy_atoms": mol.GetNumHeavyAtoms(), "formal_charge": Chem.GetFormalCharge(mol), "state_assumption": "neutral CCD state; not pH enumeration", "qc_status": "RDKit sanitized; Meeko preparation completed"})

    with (out / "ligand_manifest.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    (out / "box.json").write_text(json.dumps({"pdb_id": "3HTB", "reference": "JZ4 auth chain A residue 167", "center": center.tolist(), "size_angstrom": box, "center_basis": "mean of crystal reference ligand heavy-atom coordinates", "receptor_policy": "chain A ATOM records; Meeko alternate-location A; waters/PO4/BME/JZ4 removed for this dry rigid-receptor teaching protocol"}, indent=2), encoding="utf-8")
    (out / "download_sources.json").write_text(json.dumps(downloads, indent=2), encoding="utf-8")
    (out / "preparation_commands.json").write_text(json.dumps({"receptor_command": ["python", *receptor_cmd[2:]], "ligand_preparation": "RDKit SDMolSupplier/AddHs then Meeko MoleculePreparation and PDBQTWriterLegacy"}, indent=2), encoding="utf-8")
    print(f"Prepared {len(atoms)} receptor heavy-atom records and 3 ligands in {args.out}")
    print("Box center (A):", ", ".join(f"{x:.3f}" for x in center))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
