#!/usr/bin/env python3
"""Plot real two-column PCA projections and a finite-frame frequency exercise."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--outdir', required=True, type=Path)
    parser.add_argument('--bins', type=int, default=8)
    parser.add_argument('--temperature', type=float, default=300)
    args = parser.parse_args()
    if args.bins < 2 or args.temperature <= 0:
        parser.error('bins >=2 and temperature >0 are required')
    points = []
    for line in args.input.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith(('#', '@')):
            continue
        row = [float(value) for value in line.split()]
        if len(row) != 2 or not all(math.isfinite(x) for x in row):
            raise ValueError('PCA 2D input must have two projections and no time column')
        points.append(row)
    if len(points) < 2:
        raise ValueError('not enough real projected frames')
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    array = np.asarray(points)
    counts, xedges, yedges = np.histogram2d(array[:, 0], array[:, 1], bins=args.bins)
    if int(counts.sum()) != len(points):
        raise ValueError('histogram discarded projected frames')
    relative = np.full(counts.shape, np.nan)
    occupied = counts > 0
    relative[occupied] = -0.008314462618 * args.temperature * np.log(counts[occupied] / counts.max())
    args.outdir.mkdir(parents=True, exist_ok=True)
    with (args.outdir / 'pca-frequency-grid.tsv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t')
        writer.writerow(['x_low', 'x_high', 'y_low', 'y_high', 'frame_count', 'relative_kJ_mol'])
        for i in range(args.bins):
            for j in range(args.bins):
                writer.writerow([xedges[i], xedges[i + 1], yedges[j], yedges[j + 1], int(counts[i, j]),
                                 relative[i, j] if occupied[i, j] else 'unsampled'])
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    axes[0].scatter(array[:, 0], array[:, 1], s=12, alpha=0.7, color='#167a9b')
    axes[0].set_title('Actual projected frames')
    a = axes[1].pcolormesh(xedges, yedges, counts.T, cmap='viridis')
    axes[1].set_title(f'Frame counts ({args.bins} x {args.bins})'); fig.colorbar(a, ax=axes[1], label='Frame count')
    b = axes[2].pcolormesh(xedges, yedges, np.ma.masked_invalid(relative.T), cmap='magma_r')
    axes[2].set_title('Frequency-derived relative value'); fig.colorbar(b, ax=axes[2], label='Relative value (kJ/mol)')
    for ax in axes:
        ax.set(xlabel='PC1 projection (nm)', ylabel='PC2 projection (nm)')
        ax.spines[['top', 'right']].set_visible(False)
    fig.suptitle('1AKI 100 ps teaching data: unsampled bins remain blank', fontsize=11)
    fig.tight_layout(); fig.savefig(args.outdir / 'pca-frequency.svg'); fig.savefig(args.outdir / 'pca-frequency.png', dpi=180)
    plt.close(fig)
    record = {'data_status': 'derived_from_independent_real_MD_projections', 'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'frames': len(points), 'bins': args.bins, 'temperature_K': args.temperature,
              'gas_constant_kJ_mol_K': 0.008314462618, 'formula': '-RT ln(count/max_count)',
              'empty_bins': 'unsampled, not zero energy; no pseudocount or interpolation',
              'note': 'finite-frame frequency exercise; this plot is independently recomputed, not the GROMACS XPM color map'}
    (args.outdir / 'pca-frequency-record.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print('Real projected frames=', len(points), 'occupied bins=', int(occupied.sum()))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
