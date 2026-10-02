"""Run real CPU Vina for one public teaching receptor and three CCD ligands.

  python run_vina_case.py --vina path/to/vina --inputs inputs/3htb --out outputs/run-01
Creates one log/PDBQT per molecule, a result TSV, a command record and JZ4 pose
SDF plus crystal-frame heavy-atom RMSD. Existing outputs are never overwritten.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import subprocess
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vina", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--ligands", nargs="+", default=["JZ4", "IPH", "BNZ"], choices=["JZ4", "IPH", "BNZ"])
    parser.add_argument("--cpu", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument("--exhaustiveness", type=int, default=16)
    parser.add_argument("--center-shift", type=float, nargs=3, default=[0.0, 0.0, 0.0], metavar=("DX", "DY", "DZ"), help="Shift the search box center in angstrom for the comparison exercise")
    args = parser.parse_args()
    inputs, out, vina = args.inputs.resolve(), args.out.resolve(), args.vina.resolve()
    if not vina.is_file():
        raise FileNotFoundError(vina)
    if out.exists():
        raise FileExistsError("Use a new --out directory to preserve earlier runs")
    if args.cpu < 1 or args.exhaustiveness < 1:
        raise ValueError("CPU and exhaustiveness must be positive")
    out.mkdir(parents=True)
    box = json.loads((inputs / "box.json").read_text())
    box["original_center"] = list(box["center"])
    box["center"] = [value + shift for value, shift in zip(box["center"], args.center_shift)]
    box["center_shift_angstrom"] = args.center_shift
    version = subprocess.check_output([str(vina), "--version"], text=True).strip()
    commands, rows = [], []
    for ligand in args.ligands:
        command = [str(vina), "--receptor", str(inputs / "3htb_receptor.pdbqt"), "--ligand", str(inputs / f"{ligand}.pdbqt"), "--out", str(out / f"{ligand}_out.pdbqt"), "--cpu", str(args.cpu), "--seed", str(args.seed), "--exhaustiveness", str(args.exhaustiveness), "--num_modes", "9"]
        for name, value in zip(["center_x", "center_y", "center_z"], box["center"]):
            command += ["--" + name, f"{value:.3f}"]
        for name, value in zip(["size_x", "size_y", "size_z"], box["size_angstrom"]):
            command += ["--" + name, str(value)]
        start = time.perf_counter()
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elapsed = time.perf_counter() - start
        public_log = result.stdout.replace(str(inputs), "INPUTS").replace(str(out), "OUTPUTS")
        (out / f"{ligand}.log").write_text(public_log, encoding="utf-8")
        match = re.search(r"^\s*1\s+(-?\d+(?:\.\d+)?)\s+", result.stdout, re.MULTILINE)
        status = "completed" if result.returncode == 0 and match else "failed"
        rows.append({"ligand_id": ligand, "status": status, "vina_score_kcal_mol": match.group(1) if match else "", "seconds": f"{elapsed:.3f}", "seed": args.seed, "exhaustiveness": args.exhaustiveness, "cpu": args.cpu, "pose_file": f"{ligand}_out.pdbqt", "pose_review": "pending human inspection", "next_step": "inspect pose and compare JZ4 crystal reference"})
        # Store portable arguments, never the user's absolute paths.
        commands.append({"ligand_id": ligand, "arguments": ["vina", "--receptor", "INPUTS/3htb_receptor.pdbqt", "--ligand", f"INPUTS/{ligand}.pdbqt", "--out", f"OUTPUTS/{ligand}_out.pdbqt", *command[7:]]})
        print(ligand, status, rows[-1]["vina_score_kcal_mol"], f"{elapsed:.1f}s")

    with (out / "docking_results.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    (out / "run_parameters.json").write_text(json.dumps({"vina_version": version, "box": box, "commands": commands, "score_function": "Vina default; no AutoDock4 maps", "protocol": "rigid dry receptor; neutral CCD ligand states; CPU; one seed per ligand"}, indent=2), encoding="utf-8")

    if any(row["status"] == "failed" for row in rows):
        return 1
    if "JZ4" in args.ligands:
        from rdkit import Chem
        from rdkit.Chem import rdMolAlign
        from meeko import PDBQTMolecule, RDKitMolCreate
        docked = RDKitMolCreate.from_pdbqt_mol(PDBQTMolecule.from_file(str(out / "JZ4_out.pdbqt"), skip_typing=True))[0]
        reference = Chem.SDMolSupplier(str(inputs / "jz4_reference.sdf"))[0]
        heavy = Chem.RemoveHs(docked)
        values = []
        writer = Chem.SDWriter(str(out / "JZ4_poses.sdf"))
        for cid in range(heavy.GetNumConformers()):
            # No fitting: receptor and ligand are already in the crystal frame.
            rmsd = rdMolAlign.CalcRMS(heavy, reference, prbId=cid, refId=0)
            values.append({"pose": cid + 1, "heavy_atom_rmsd_angstrom": round(rmsd, 4)})
            writer.write(docked, confId=cid)
        writer.close()
        (out / "JZ4_redocking_rmsd.json").write_text(json.dumps({"comparison": "symmetry-aware heavy-atom RMSD, crystal coordinate frame, no fitting", "reference": "3HTB JZ4 auth chain A residue 167", "poses": values}, indent=2), encoding="utf-8")
        print("JZ4 top-pose RMSD (A):", values[0]["heavy_atom_rmsd_angstrom"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
