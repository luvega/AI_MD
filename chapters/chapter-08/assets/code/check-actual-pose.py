#!/usr/bin/env python3
"""Check the supplied actual 3HTB/JZ4 structure against public crystal coordinates."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True, type=Path)
    parser.add_argument('--reference', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    import gemmi
    import numpy as np
    model, reference = gemmi.read_structure(str(args.model))[0], gemmi.read_structure(str(args.reference))[0]

    def ca(chain):
        points = {}
        for residue in chain:
            for atom in residue:
                if atom.name == 'CA' and atom.element.name == 'C':
                    points[residue.seqid.num] = np.array([atom.pos.x, atom.pos.y, atom.pos.z])
        return points

    pred, ref = ca(model['A']), ca(reference['A'])
    keys = sorted(set(pred) & set(ref))
    if len(keys) != 163:
        raise ValueError('expected public 3HTB matching A1-163 C-alpha atoms')
    p, q = np.array([pred[k] for k in keys]), np.array([ref[k] for k in keys])
    pc, qc = p.mean(0), q.mean(0)
    u, _, vt = np.linalg.svd((p - pc).T @ (q - qc))
    sign = np.eye(3); sign[2, 2] = np.linalg.det(u @ vt)
    rotation = u @ sign @ vt
    aligned = (p - pc) @ rotation + qc
    ligand = np.array([[a.pos.x, a.pos.y, a.pos.z] for r in model['LIG'] for a in r if a.element.name != 'H'])
    crystal = np.array([[a.pos.x, a.pos.y, a.pos.z] for r in reference['A'] if r.name == 'JZ4' for a in r if a.element.name != 'H'])
    if ligand.shape != (10, 3) or crystal.shape != (10, 3):
        raise ValueError('expected 10-heavy-atom JZ4 in each structure')
    protein = np.array([[a.pos.x, a.pos.y, a.pos.z] for r in model['A'] for a in r if a.element.name != 'H'])
    distances = np.linalg.norm(ligand[:, None, :] - protein[None, :, :], axis=2)
    record = {'data_status': 'derived_from_actual_model_structure',
              'protein_alignment': 'matched A-chain C-alpha residue numbers1-163, Kabsch fit',
              'matched_CA_atoms': len(keys), 'CA_RMSD_Angstrom': float(np.sqrt(((aligned - q) ** 2).sum() / len(keys))),
              'ligand_heavy_atoms': len(ligand), 'crystal_ligand_heavy_atoms': len(crystal),
              'aligned_ligand_centroid_shift_Angstrom': float(np.linalg.norm(((ligand - pc) @ rotation + qc).mean(0) - crystal.mean(0))),
              'minimum_model_ligand_protein_heavy_distance_Angstrom': float(distances.min()),
              'model_sha256': hashlib.sha256(args.model.read_bytes()).hexdigest(),
              'reference_sha256': hashlib.sha256(args.reference.read_bytes()).hexdigest(),
              'note': 'centroid shift is not ligand atom-mapped RMSD or evidence of binding; deposited crystal lacks LEU164'}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print('CA RMSD (A)=', record['CA_RMSD_Angstrom'], 'centroid shift (A)=', record['aligned_ligand_centroid_shift_Angstrom'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
