#!/usr/bin/env python3
"""Generate an aggregate QC SVG for the l6D9Z7 Boltz-2 sample."""

from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path


def load_plddt(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def bar(width: float, max_width: int = 280) -> int:
    return int(max(0, min(max_width, width * max_width)))


def metric_row(y: int, label: str, value: float, fill: str) -> str:
    pct = value if value <= 1 else value / 100
    return (
        f'<text x="36" y="{y}" class="label">{html.escape(label)}</text>'
        f'<rect x="250" y="{y - 12}" width="280" height="14" rx="2" class="track"/>'
        f'<rect x="250" y="{y - 12}" width="{bar(pct)}" height="14" rx="2" fill="{fill}"/>'
        f'<text x="548" y="{y}" class="value">{value:.3f}</text>'
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--plddt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    plddt_rows = load_plddt(args.plddt)
    protein_values = [float(r["plddt"]) for r in plddt_rows if r["asym_id"] == "A"]
    ligand_values = [float(r["plddt"]) for r in plddt_rows if r["asym_id"] != "A"]

    low_conf = sum(1 for v in protein_values if v < 70)
    protein_mean = sum(protein_values) / len(protein_values)
    ligand_mean = sum(ligand_values) / len(ligand_values) if ligand_values else 0.0

    rows = [
        ("confidence", summary["confidence_scores"], "#2c7fb8"),
        ("iptm", summary["iptm_scores"], "#2ca25f"),
        ("complex plddt", summary["complex_plddt_scores"], "#756bb1"),
        ("complex iplddt", summary["complex_iplddt_scores"], "#31a354"),
        ("affinity probability", summary["affinity_LIG_affinity_probability_binary"], "#de2d26"),
        ("protein mean pLDDT", protein_mean, "#3182bd"),
        ("ligand mean pLDDT", ligand_mean, "#e6550d"),
    ]

    metric_svg = "\n".join(metric_row(154 + i * 34, label, value, fill) for i, (label, value, fill) in enumerate(rows))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="470" viewBox="0 0 760 470" role="img" aria-labelledby="title desc">
  <title id="title">l6D9Z7 Boltz-2 output QC summary</title>
  <desc id="desc">Aggregate confidence, affinity and pLDDT fields generated from local summary and pLDDT TSV.</desc>
  <style>
    text {{ font-family: Arial, "Microsoft YaHei", sans-serif; fill: #1f2933; }}
    .small {{ font-size: 13px; fill: #52616b; }}
    .title {{ font-size: 23px; font-weight: 700; }}
    .subtitle {{ font-size: 14px; fill: #52616b; }}
    .label {{ font-size: 14px; }}
    .value {{ font-size: 13px; text-anchor: start; fill: #27323a; }}
    .track {{ fill: #e6edf2; }}
    .panel {{ fill: #f8fafc; stroke: #d7dee5; stroke-width: 1; rx: 6; }}
    .badge {{ fill: #fff7ed; stroke: #fdba74; stroke-width: 1; rx: 5; }}
  </style>
  <rect x="16" y="16" width="728" height="438" class="panel"/>
  <text x="36" y="55" class="title">l6D9Z7 Boltz-2 输出复核摘要</text>
  <text x="36" y="82" class="subtitle">目标身份按序列和课程截图复核为 KRAS G12C；配体为 CCD U4U。原始输入 YAML、seed 和平台仍需正式运行记录确认。</text>
  <rect x="36" y="103" width="670" height="34" class="badge"/>
  <text x="52" y="125" class="small">结构图性质：由 summary.json 和 pLDDT TSV 生成的聚合 QC 图，不替代 3D 口袋与共价键可视化复核。</text>
  {metric_svg}
  <text x="36" y="420" class="small">protein residues: {len(protein_values)}; protein pLDDT &lt;70 residues: {low_conf}; ligand atoms: {len(ligand_values)}; affinity_pic50: {summary["affinity_LIG_affinity_pic50"]:.3f}</text>
  <text x="36" y="442" class="small">Source kept local: 06_原始学习素材/第五章/boltz2在线/boltz2_parsed/</text>
</svg>
'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
