#!/usr/bin/env python3
"""Recalculate frame statistics from a real official gmx_MMPBSA CSV export."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--outdir', type=Path, default=Path('gb-analysis'))
    parser.add_argument('--startframe', type=int, default=1)
    parser.add_argument('--endframe', type=int, default=10)
    args = parser.parse_args()
    frames, supplied = [], {}
    with args.input.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ['Frames', 'GB delta TOTAL']:
            raise ValueError('expected official CSV header: Frames,GB delta TOTAL')
        for row in reader:
            label, value = row['Frames'], float(row['GB delta TOTAL'])
            if not math.isfinite(value):
                raise ValueError('non-finite energy')
            if label.isdigit():
                frame = int(label)
                if args.startframe <= frame <= args.endframe:
                    frames.append((frame, value))
            else:
                supplied[label] = value
    if len(frames) < 2:
        raise ValueError('select at least two numeric frame rows')
    values = [value for _, value in frames]
    mean, sd = statistics.fmean(values), statistics.pstdev(values)
    result = {'data_status': 'external_real_gmx_MMPBSA_example', 'method': 'MM/GBSA',
              'source_commit': '5fe49f88eb6db7341e98f56803814473c0266d8d',
              'source_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'energy_unit': 'kcal/mol', 'temperature_K_from_upstream_readme': 298.15,
              'selected_frames': [frame for frame, _ in frames], 'mean': mean,
              'population_sd': sd, 'sample_sd': statistics.stdev(values),
              'naive_sem': sd / math.sqrt(len(values)), 'provided_summary': supplied,
              'interpretation': 'frame dispersion; correlated frames are not independent experimental replicates'}
    if len(frames) == 10 and args.startframe == 1 and args.endframe == 10:
        if not math.isclose(mean, supplied['Average'], abs_tol=1e-10):
            raise ValueError('numeric-frame mean does not match upstream summary')
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / 'summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.plot([frame for frame, _ in frames], values, 'o-', color='#167a9b', linewidth=1.2)
    ax.axhline(mean, color='#d47c28', linestyle='--', label=f'mean = {mean:.4f}')
    ax.set(xlabel='Selected trajectory frame', ylabel='GB delta TOTAL (kcal/mol)', title='Official MM/GBSA example: numeric frame rows')
    ax.spines[['top', 'right']].set_visible(False); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(args.outdir / 'gb-frames.svg'); fig.savefig(args.outdir / 'gb-frames.png', dpi=180)
    plt.close(fig)
    print(f'n={len(values)} mean={mean:.6f} population_sd={sd:.6f}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
