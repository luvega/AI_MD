#!/usr/bin/env python3
"""Compute a real C-alpha DCCM after alignment to the first trajectory frame."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trajectory', required=True, type=Path)
    parser.add_argument('--topology', required=True, type=Path)
    parser.add_argument('--outdir', required=True, type=Path)
    args = parser.parse_args()
    import mdtraj as md
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    trajectory = md.load(str(args.trajectory), top=str(args.topology))
    selected = trajectory.topology.select('protein and name CA')
    if len(selected) < 2 or trajectory.n_frames < 2:
        raise ValueError('need at least two C-alpha atoms and two actual frames')
    trajectory.superpose(trajectory, 0, atom_indices=selected)
    xyz = trajectory.xyz[:, selected, :].astype(np.float64)
    delta = xyz - xyz.mean(axis=0)
    covariance = np.einsum('tic,tjc->ij', delta, delta) / trajectory.n_frames
    denominator = np.sqrt(np.outer(np.diag(covariance), np.diag(covariance)))
    matrix = np.full(covariance.shape, np.nan)
    np.divide(covariance, denominator, out=matrix, where=denominator > 0)
    valid = np.diag(denominator) > 0
    if not np.allclose(matrix, matrix.T, equal_nan=True, atol=1e-10):
        raise ValueError('asymmetric DCCM')
    if not np.allclose(np.diag(matrix)[valid], 1, atol=1e-8):
        raise ValueError('non-unit DCCM diagonal')
    residues = [trajectory.topology.atom(int(index)).residue for index in selected]
    labels = [f'{residue.name}{residue.resSeq}' for residue in residues]
    args.outdir.mkdir(parents=True, exist_ok=True)
    with (args.outdir / 'dccm-ca.tsv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t'); writer.writerow(['residue', *labels])
        for label, row in zip(labels, matrix):writer.writerow([label, *row])
    fig, ax = plt.subplots(figsize=(5.8, 5))
    shown = ax.imshow(np.ma.masked_invalid(matrix), origin='lower', vmin=-1, vmax=1, cmap='RdBu_r')
    tick_positions = np.linspace(0, len(labels) - 1, min(6, len(labels)), dtype=int)
    ax.set_xticks(tick_positions, [labels[i] for i in tick_positions], rotation=45, ha='right')
    ax.set_yticks(tick_positions, [labels[i] for i in tick_positions])
    ax.set(title='1AKI 100 ps teaching data\nAligned C-alpha displacement correlations', xlabel='C-alpha residue', ylabel='C-alpha residue')
    fig.colorbar(shown, ax=ax, label='DCCM'); fig.tight_layout()
    fig.savefig(args.outdir / 'dccm-ca.svg'); fig.savefig(args.outdir / 'dccm-ca.png', dpi=180); plt.close(fig)
    record = {'data_status': 'computed_from_independent_real_MD', 'frames': trajectory.n_frames,
              'C_alpha_atoms': len(selected), 'matrix_shape': list(matrix.shape),
              'trajectory_sha256': hashlib.sha256(args.trajectory.read_bytes()).hexdigest(),
              'topology_sha256': hashlib.sha256(args.topology.read_bytes()).hexdigest(),
              'alignment': 'C-alpha least-squares superposition to first actual frame',
              'formula': '<delta r_i dot delta r_j>/sqrt(<delta r_i^2><delta r_j^2>)',
              'verification': 'symmetric and unit diagonal for nonzero variance',
              'interpretation': 'short-trajectory correlation exercise, not functional coupling evidence'}
    (args.outdir / 'dccm-record.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print('Real frames=', trajectory.n_frames, 'C-alpha atoms=', len(selected), 'DCCM=', matrix.shape)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
