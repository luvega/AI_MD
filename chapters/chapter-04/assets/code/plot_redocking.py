"""Plot actual reference/docked ligand coordinates, without structural fitting."""
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Draw
import numpy as np


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    ref = Chem.SDMolSupplier(str(args.inputs / "jz4_reference.sdf"))[0]
    docked = Chem.SDMolSupplier(str(args.results / "JZ4_poses.sdf"))[0]
    if ref is None or docked is None:
        raise ValueError("Reference or first docked pose cannot be read")
    fig = plt.figure(figsize=(7, 5.6))
    ax = fig.add_subplot(projection="3d")
    all_xyz = []
    for mol, color, label in [(ref, "#777777", "Crystal JZ4"), (docked, "#1d6fb8", "Vina top pose")]:
        xyz = mol.GetConformer().GetPositions()
        all_xyz.append(xyz)
        for bond in mol.GetBonds():
            i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
            ax.plot(*xyz[[i, j]].T, color=color, linewidth=2.5)
        ax.scatter(*xyz.T, color=color, s=32, label=label)
        oxygen = [i for i, atom in enumerate(mol.GetAtoms()) if atom.GetAtomicNum() == 8]
        ax.scatter(*xyz[oxygen].T, color="#c73636", s=50)
    xyz = np.vstack(all_xyz)
    midpoint = (xyz.max(0) + xyz.min(0)) / 2
    radius = max(np.ptp(xyz, axis=0)) / 2 + 0.7
    for dimension, setter in enumerate([ax.set_xlim, ax.set_ylim, ax.set_zlim]):
        setter(midpoint[dimension] - radius, midpoint[dimension] + radius)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("x (angstrom)")
    ax.set_ylabel("y (angstrom)")
    ax.set_zlabel("z (angstrom)")
    ax.legend(loc="upper left")
    ax.set_title("3HTB / JZ4: same crystal coordinate frame")
    fig.tight_layout()
    fig.savefig(args.out / "jz4_redocking_overlay.png", dpi=180)
    plt.close(fig)
    molecules = [Chem.SDMolSupplier(str(args.inputs / f"{name}_ideal.sdf"))[0] for name in ["JZ4", "IPH", "BNZ"]]
    for mol in molecules:
        Chem.rdDepictor.Compute2DCoords(mol)
    svg = Draw.MolsToGridImage(molecules, molsPerRow=3, subImgSize=(260, 180), legends=["JZ4: 2-propylphenol", "IPH: phenol", "BNZ: benzene"], useSVG=True)
    (args.out / "three_ccd_ligands.svg").write_text(svg, encoding="utf-8")
    print("Created coordinate overlay PNG and three-ligand SVG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
