#!/usr/bin/env python3
"""Plot selected real Amber tutorial residue summaries without inventing frames."""
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
    args = parser.parse_args()
    terms = ['internal', 'vdw', 'electrostatic', 'polar_solvation', 'nonpolar_solvation']
    with args.input.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle, delimiter='\t'))
    if not rows:
        raise ValueError('no residue summaries')
    for row in rows:
        if row['data_status'] != 'external_real_Amber_tutorial_summary':
            raise ValueError('unexpected data status')
        for term in [*terms, 'total']:
            for suffix in ['mean', 'reported_sd']:
                key = term + '_' + suffix
                row[key] = float(row[key])
                if not math.isfinite(row[key]) or (suffix == 'reported_sd' and row[key] < 0):
                    raise ValueError('invalid numeric residue summary')
        difference = sum(row[t + '_mean'] for t in terms) - row['total_mean']
        if abs(difference) > 0.0021:
            raise ValueError('mean components do not sum to total within source rounding')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels = [row['component'] + ':' + row['residue_name'] + row['component_residue'] for row in rows]
    fig, axes = plt.subplots(2, 1, figsize=(8, 6.8), sharex=True)
    xs = range(len(rows))
    axes[0].bar(xs, [r['total_mean'] for r in rows], color='#167a9b')
    axes[0].errorbar(xs, [r['total_mean'] for r in rows], yerr=[r['total_reported_sd'] for r in rows],
                     fmt='none', color='#32414a', capsize=3, label='reported SD (historical upstream output)')
    axes[0].set(ylabel='GB residue TOTAL (kcal/mol)', title='Amber Ras-Raf: selected R residues, true summary values')
    axes[0].axhline(0, color='#777777', linewidth=0.7); axes[0].legend(frameon=False, fontsize=8)
    axes[1].plot(xs, [r['electrostatic_mean'] for r in rows], 'o-', color='#167a9b', label='Electrostatic mean')
    axes[1].plot(xs, [r['polar_solvation_mean'] for r in rows], 's-', color='#d47c28', label='Polar solvation mean')
    axes[1].set(ylabel='Component mean (kcal/mol)', xlabel='Selected receptor residue (upstream numbering)')
    axes[1].axhline(0, color='#777777', linewidth=0.7); axes[1].legend(frameon=False, fontsize=8)
    axes[1].set_xticks(list(xs), labels, rotation=60, ha='right')
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout(); args.outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.outdir / 'residue-contributions.svg'); fig.savefig(args.outdir / 'residue-contributions.png', dpi=180)
    plt.close(fig)
    record = {'data_status': 'external_real_Amber_tutorial_summary', 'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'residues': labels, 'n_residues': len(rows), 'unit': 'kcal/mol',
              'dispersion': 'upstream reported SD, not SEM; no raw-frame reconstruction',
              'mean_component_sum_tolerance': 0.0021}
    (args.outdir / 'plot-record.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print('Verified and plotted', len(rows), 'real residue summaries')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
