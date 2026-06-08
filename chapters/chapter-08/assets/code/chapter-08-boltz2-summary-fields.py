#!/usr/bin/env python3
"""Extract chapter-safe Boltz-2 summary fields.

The script reads a derived summary JSON and prints a TSV table. It does not copy
raw CIF, PAE, PDE, or model output payloads into the chapter directory.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


FIELD_GROUPS = {
    "runtime": [
        "total_time_seconds",
        "input_preparation_time_seconds",
        "model_inference_time_seconds",
        "affinity_prediction_time_seconds",
    ],
    "structure_confidence": [
        "confidence_scores",
        "ptm_scores",
        "iptm_scores",
        "ligand_iptm_scores",
        "protein_iptm_scores",
        "complex_plddt_scores",
        "complex_iplddt_scores",
        "complex_pde_scores",
        "complex_ipde_scores",
    ],
    "affinity": [
        "affinity_LIG_affinity_pred_value",
        "affinity_LIG_affinity_probability_binary",
        "affinity_LIG_model_1_affinity_pred_value",
        "affinity_LIG_model_1_affinity_probability_binary",
        "affinity_LIG_model_2_affinity_pred_value",
        "affinity_LIG_model_2_affinity_probability_binary",
        "affinity_LIG_affinity_pic50",
    ],
    "plddt_aggregate": [
        "l6D9Z7_model_0_protein_mean_plddt",
        "l6D9Z7_model_0_protein_min_plddt",
        "l6D9Z7_model_0_protein_max_plddt",
        "l6D9Z7_model_0_ligand_mean_plddt",
    ],
}


def normalize_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.6g}"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return "" if value is None else str(value)


def iter_rows(summary: dict[str, Any]):
    for group, fields in FIELD_GROUPS.items():
        for field in fields:
            status = "present" if field in summary else "missing"
            yield {
                "group": group,
                "field": field,
                "value": normalize_value(summary.get(field)),
                "status": status,
            }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, type=Path, help="Path to derived summary JSON.")
    parser.add_argument("--out", type=Path, help="Optional output TSV path. Defaults to stdout.")
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    rows = list(iter_rows(summary))
    fieldnames = ["group", "field", "value", "status"]

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
