"""Check same-candidate PDL1 sequences and separate fold from interface placement."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import gemmi
import numpy as np


BACKBONE_ATOMS = ("N", "CA", "C", "O")


def fasta_records(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith(">"):
            records.append((line[1:], ""))
        elif line:
            if not records:
                raise ValueError("Sequence precedes FASTA header")
            header, sequence = records[-1]
            records[-1] = (header, sequence + line)
    return records


def protein_chain(structure: gemmi.Structure, name: str) -> gemmi.Chain:
    chain = structure[0].find_chain(name)
    if chain is None:
        raise ValueError(f"Missing chain {name}")
    return chain


def sequence(chain: gemmi.Chain) -> str:
    return "".join(gemmi.find_tabulated_residue(residue.name).one_letter_code for residue in chain)


def backbone(chain: gemmi.Chain) -> np.ndarray:
    coordinates = []
    for residue in chain:
        for name in BACKBONE_ATOMS:
            atoms = [atom for atom in residue if atom.name == name]
            if len(atoms) != 1:
                raise ValueError(f"{chain.name}/{residue.seqid}/{name}: expected exactly one atom")
            coordinates.append(list(atoms[0].pos))
    return np.asarray(coordinates, dtype=float)


def fit(moving: np.ndarray, reference: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return row-vector rigid transform; reflections are forbidden."""
    if moving.shape != reference.shape or moving.shape[0] < 3:
        raise ValueError("Matched coordinate arrays need identical shape and at least three atoms")
    center_moving, center_reference = moving.mean(axis=0), reference.mean(axis=0)
    u, _, vt = np.linalg.svd((moving - center_moving).T @ (reference - center_reference))
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(u @ vt)
    rotation = u @ correction @ vt
    translation = center_reference - center_moving @ rotation
    return rotation, translation


def rmsd(first: np.ndarray, second: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.sum((first - second) ** 2, axis=1))))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--fasta", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError("Use a new analysis directory; existing results are preserved")
    reference = gemmi.read_structure(str(args.reference))
    reference_a, reference_b = protein_chain(reference, "A"), protein_chain(reference, "B")
    reference_a_xyz, reference_b_xyz = backbone(reference_a), backbone(reference_b)
    targets = fasta_records(args.target)
    if len(targets) != 1 or targets[0][1] != sequence(reference_b):
        raise ValueError("Target FASTA must exactly match reference chain B")
    designs = [(header, seq) for header, seq in fasta_records(args.fasta) if "sample=" in header]
    if not designs:
        raise ValueError("No sampled ProteinMPNN sequences found")
    rows = []
    aligned_models = []
    records = []
    configurations = json.loads(args.config.read_text(encoding="utf-8"))
    if len(configurations) != 1:
        raise ValueError("Use the single-task official PDL1 configuration")
    hotspots = next(iter(configurations.values()))["select_hotspots"]
    for header, expected_a in designs:
        sample = header.split("sample=", 1)[1].split(",", 1)[0].strip()
        name = f"pdl1_mpnn_{sample}"
        folder = args.predictions / name
        cif = folder / f"{name}_model_0.cif"
        confidence_path = folder / f"confidence_{name}_model_0.json"
        pae_path = folder / f"pae_{name}_model_0.npz"
        plddt_path = folder / f"plddt_{name}_model_0.npz"
        predicted = gemmi.read_structure(str(cif))
        chain_a, chain_b = protein_chain(predicted, "A"), protein_chain(predicted, "B")
        if [chain.name for chain in predicted[0]] != ["A", "B"]:
            raise ValueError("Expected A then B: this order defines the PAE token blocks")
        if sequence(chain_a) != expected_a or sequence(chain_b) != targets[0][1]:
            raise ValueError(f"{name}: predicted chain identity does not match the actual candidate")
        a, b = backbone(chain_a), backbone(chain_b)
        rotation_a, translation_a = fit(a, reference_a_xyz)
        rotation_b, translation_b = fit(b, reference_b_xyz)
        confidence = json.loads(confidence_path.read_text(encoding="utf-8"))
        with np.load(pae_path, allow_pickle=False) as data:
            pae = data["pae"]
        with np.load(plddt_path, allow_pickle=False) as data:
            plddt = data["plddt"]
        length_a, length_b = len(chain_a), len(chain_b)
        if pae.shape != (length_a + length_b,) * 2 or plddt.shape != (length_a + length_b,):
            raise ValueError("PAE/pLDDT token dimensions do not match these two protein chains")
        if not np.isfinite(pae).all() or not np.isfinite(plddt).all():
            raise ValueError("Non-finite prediction array")
        # Mean of ALL cross-chain token pairs in BOTH directions, not contact-only iPAE.
        cross_pae = np.concatenate((pae[:length_a, length_a:].ravel(), pae[length_a:, :length_a].ravel()))
        binder_heavy = np.asarray([list(atom.pos) for residue in chain_a for atom in residue if atom.element.atomic_number > 1])
        hotspot_distances = {}
        for site, names in hotspots.items():
            if not site.startswith("B"):
                raise ValueError("This PDL1 check expects target B hotspot residues")
            residue = next((residue for residue in chain_b if residue.seqid.num == int(site[1:])), None)
            if residue is None:
                raise ValueError(f"Missing hotspot residue {site}")
            selected = [atom for atom in residue if atom.name in names.split(",")]
            if len(selected) != len(names.split(",")):
                raise ValueError(f"Missing or duplicate selected hotspot atoms at {site}")
            target_atoms = np.asarray([list(atom.pos) for atom in selected])
            minimum = float(np.sqrt(np.sum((binder_heavy[:, None, :] - target_atoms[None, :, :]) ** 2, axis=-1)).min())
            hotspot_distances[site] = minimum
        row = {
            "candidate_id": name,
            "binder_length": length_a,
            "target_length": length_b,
            "complex_plddt_0_to_1": float(confidence["complex_plddt"]),
            "iptm_0_to_1": float(confidence["iptm"]),
            "cross_chain_pae_mean_angstrom": float(cross_pae.mean()),
            "binder_internal_backbone_rmsd_angstrom": rmsd(a @ rotation_a + translation_a, reference_a_xyz),
            "binder_placement_backbone_rmsd_angstrom": rmsd(a @ rotation_b + translation_b, reference_a_xyz),
            "target_fit_backbone_rmsd_angstrom": rmsd(b @ rotation_b + translation_b, reference_b_xyz),
            "binder_backbone_atom_count": int(len(a)),
            "target_backbone_atom_count": int(len(b)),
            "hotspot_residues_with_contact_within_4p5_angstrom": sum(distance <= 4.5 for distance in hotspot_distances.values()),
        }
        if not all(np.isfinite(value) for value in row.values() if isinstance(value, float)):
            raise ValueError("Non-finite summary value")
        rows.append(row)
        records.append({"candidate_id": name, "files_sha256": {path.name: sha256(path) for path in (cif, confidence_path, pae_path, plddt_path)}, "sequence_identity": "A matches sampled ProteinMPNN FASTA; B matches target FASTA and design structure", "hotspot_min_heavy_atom_distances_angstrom": hotspot_distances})
        for chain in predicted[0]:
            for residue in chain:
                for atom in residue:
                    xyz = np.asarray(list(atom.pos)) @ rotation_b + translation_b
                    atom.pos = gemmi.Position(*xyz)
        aligned_models.append((name, predicted))
    args.out.mkdir(parents=True)
    for name, structure in aligned_models:
        structure.write_pdb(str(args.out / f"{name}_target_aligned.pdb"))
    with (args.out / "refold_summary.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "reference_sha256": sha256(args.reference),
        "fasta_sha256": sha256(args.fasta),
        "target_sha256": sha256(args.target),
        "config_sha256": sha256(args.config),
        "atom_matching": "Chain and residue order; N, CA, C, O for every residue, no side chains or hydrogens",
        "internal_rmsd": "Least-squares fit of binder A backbone to design A, then RMSD of the same A atoms",
        "placement_rmsd": "Least-squares fit of target B backbone to design B; apply that transform to binder A and compute A RMSD",
        "cross_chain_pae": "Arithmetic mean over A-to-B and B-to-A blocks, all 2*77*114 directed pairs; not contact-only interface PAE",
        "prediction_scale": "Boltz complex_plddt and iptm are 0-1; PAE and coordinate RMSDs are angstrom",
        "hotspot_contacts": "For each of six configured B residues, minimum distance from its listed hotspot atoms to any A heavy atom; geometric cutoff 4.5 angstrom, not a binding-success criterion",
        "software": {"gemmi": gemmi.__version__, "numpy": np.__version__},
        "candidate_records": records,
        "metrics": rows,
    }
    (args.out / "analysis_record.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
