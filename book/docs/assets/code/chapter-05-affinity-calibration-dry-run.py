"""Dry-run affinity interpretation table for chapter 05.

The script reads or creates prediction-like rows and converts them into a
bounded interpretation table. It does not run Boltz2 and does not convert model
scores into experimental Kd, IC50, or activity.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_ROWS = [
    {
        "candidate_id": "CAND_A",
        "pred_affinity": "7.2",
        "confidence": "0.82",
        "control_type": "known_positive_like",
    },
    {
        "candidate_id": "CAND_B",
        "pred_affinity": "5.1",
        "confidence": "0.41",
        "control_type": "unknown",
    },
    {
        "candidate_id": "CAND_C",
        "pred_affinity": "6.3",
        "confidence": "0.74",
        "control_type": "negative_control_like",
    },
]


def load_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return list(DEFAULT_ROWS)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rank_bucket(pred_affinity: float, confidence: float) -> str:
    if confidence < 0.5:
        return "review_low_confidence"
    if pred_affinity >= 7:
        return "high_priority_signal"
    if pred_affinity >= 6:
        return "medium_priority_signal"
    return "low_priority_signal"


def interpret(row: dict[str, str]) -> dict[str, str]:
    pred = float(row["pred_affinity"])
    conf = float(row["confidence"])
    bucket = rank_bucket(pred, conf)
    calibration_available = "yes" if row.get("control_type", "unknown") != "unknown" else "no"
    if bucket == "review_low_confidence":
        note = "Model output requires input and structure review before ranking."
    elif calibration_available == "yes":
        note = "Use as a relative ranking signal against matched controls."
    else:
        note = "Use only as an uncalibrated model signal."
    return {
        **row,
        "calibration_available": calibration_available,
        "rank_bucket": bucket,
        "interpretation": note,
        "boundary_note": "Predicted affinity is not experimental Kd, IC50, or activity.",
    }


def write_rows(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "pred_affinity",
        "confidence",
        "control_type",
        "calibration_available",
        "rank_bucket",
        "interpretation",
        "boundary_note",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Optional TSV with candidate_id, pred_affinity, confidence.")
    parser.add_argument("--out", type=Path, default=Path("outputs/chapter-05-affinity-calibration.tsv"))
    args = parser.parse_args()
    rows = [interpret(row) for row in load_rows(args.input)]
    rows.sort(key=lambda item: (item["rank_bucket"], -float(item["confidence"])))
    write_rows(rows, args.out)
    print(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
