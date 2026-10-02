#!/usr/bin/env python3
"""Plot numeric XVG data without smoothing, and retain input checksums."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics


def read_xvg(path: Path):
    labels = {'title': path.stem, 'xaxis': 'x (unit unspecified)', 'yaxis': 'y (unit unspecified)'}
    legends, data = {}, []
    for number, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            for key, pattern in [('title', r'@\s+title\s+"(.*)"'), ('xaxis', r'@\s+xaxis\s+label\s+"(.*)"'), ('yaxis', r'@\s+yaxis\s+label\s+"(.*)"')]:
                match = re.match(pattern, line)
                if match:
                    labels[key] = match.group(1)
            match = re.match(r'@\s+s(\d+)\s+legend\s+"(.*)"', line)
            if match:
                legends[int(match.group(1))] = match.group(2)
            continue
        if line == '&':
            raise ValueError(f'{path}:{number}: multiple XVG datasets require separate files')
        row = [float(value) for value in line.split()]
        if len(row) < 2 or not all(math.isfinite(value) for value in row):
            raise ValueError(f'{path}:{number}: invalid numeric row')
        if data and len(row) != len(data[0]):
            raise ValueError(f'{path}:{number}: inconsistent column count')
        data.append(row)
    if not data:
        raise ValueError(f'{path}: no numeric rows')
    return labels, legends, data


def grace_label(value: str) -> str:
    """Translate the Grace escapes used by these genuine GROMACS files."""
    for raw, displayed in [(r'\S2\N', '²'), (r'\S3\N', '³'),
                           (r'\s10\N', '₁₀'), (r'\sII\N', 'II'),
                           (r'\xp\f{}', 'π'), (r'\xb\f{}', 'β'),
                           (r'\xa\f{}', 'α'), ('Rg/sX/N', 'Rgₓ'),
                           ('Rg/sY/N', 'Rgᵧ'), ('Rg/sZ/N', 'Rg_z')]:
        value = value.replace(raw, displayed)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', type=Path, nargs='+')
    parser.add_argument('--outdir', type=Path, default=Path('xvg-plots'))
    parser.add_argument('--xmin', type=float)
    parser.add_argument('--xmax', type=float)
    args = parser.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    args.outdir.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(len(args.inputs), 1, figsize=(8.5, 2.7 * len(args.inputs)), squeeze=False)
    colors = list(plt.get_cmap('tab10').colors)
    metadata, summary = [], []
    for index, path in enumerate(args.inputs):
        labels, legends, raw_data = read_xvg(path)
        display_labels = {key: grace_label(value) for key, value in labels.items()}
        display_legends = {key: grace_label(value) for key, value in legends.items()}
        data = [row for row in raw_data if (args.xmin is None or row[0] >= args.xmin)
                and (args.xmax is None or row[0] <= args.xmax)]
        if not data:
            raise ValueError(f'{path}: requested window contains no rows')
        ax = axes[index, 0]
        for column in range(1, len(data[0])):
            values = [row[column] for row in data]
            label = display_legends.get(column - 1, f'column {column + 1}')
            ax.plot([row[0] for row in data], values, color=colors[(column - 1) % len(colors)], linewidth=1.2, label=label)
            summary.append({'input': path.name, 'column': column + 1, 'n': len(values),
                            'x_min': min(row[0] for row in data), 'x_max': max(row[0] for row in data),
                            'mean': statistics.fmean(values), 'population_sd': statistics.pstdev(values),
                            'minimum': min(values), 'maximum': max(values), 'y_label': display_labels['yaxis']})
        ax.set(title=display_labels['title'], xlabel=display_labels['xaxis'], ylabel=display_labels['yaxis'])
        ax.spines[['top', 'right']].set_visible(False)
        if len(data[0]) > 2:
            ax.legend(frameon=False, loc='upper left', bbox_to_anchor=(1.01, 1), fontsize=8)
        metadata.append({'input': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'original_rows': len(raw_data), 'plotted_rows': len(data), 'labels': labels,
                         'display_labels': display_labels,
                         'original_legends': legends, 'display_legends': display_legends,
                         'xmin': args.xmin, 'xmax': args.xmax, 'smoothing': 'none'})
    figure.tight_layout()
    figure.savefig(args.outdir / 'xvg-panels.svg')
    figure.savefig(args.outdir / 'xvg-panels.png', dpi=180)
    plt.close(figure)
    with (args.outdir / 'summary.tsv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]), delimiter='\t')
        writer.writeheader(); writer.writerows(summary)
    (args.outdir / 'plot-record.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Saved raw-data plots and records:', args.outdir)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
