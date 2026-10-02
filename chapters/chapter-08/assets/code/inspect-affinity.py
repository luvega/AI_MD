#!/usr/bin/env python3
"""Read clearly labelled constructed or actual Boltz affinity fields."""
from __future__ import annotations
import argparse
import csv
import json
import math
import hashlib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--input', type=Path, help='explicitly labelled exercise JSON')
    inputs.add_argument('--affinity', type=Path, help='raw actual Boltz affinity JSON')
    parser.add_argument('--confidence', type=Path, help='matching raw actual confidence JSON')
    parser.add_argument('--candidate-id', default='3htb_jz4_single')
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    if args.affinity:
        if args.confidence is None:
            parser.error('--confidence is required with raw --affinity')
        affinity = json.loads(args.affinity.read_text(encoding='utf-8'))
        confidence = json.loads(args.confidence.read_text(encoding='utf-8'))
        payload = {'data_status': 'actual_model_output', 'candidates': [{
            'candidate_id': args.candidate_id,
            'affinity_pred_value': affinity['affinity_pred_value'],
            'affinity_probability_binary': affinity['affinity_probability_binary'],
            'confidence_score': confidence['confidence_score'],
            'structure_review': 'inspection_pending', 'control_status': 'none',
        }]}
    else:
        payload = json.loads(args.input.read_text(encoding='utf-8'))
    status = payload.get('data_status')
    if status not in {'constructed_field_exercise', 'actual_model_output'}:
        raise ValueError('declare data_status before interpreting values')
    rows = []
    for candidate in payload['candidates']:
        score = candidate['affinity_pred_value']
        probability = candidate['affinity_probability_binary']
        confidence = candidate['confidence_score']
        if not all(isinstance(x, (float, int)) and math.isfinite(x) for x in [score, probability, confidence]):
            raise ValueError('non-finite or non-numeric field')
        if not 0 <= probability <= 1 or not 0 <= confidence <= 1:
            raise ValueError('probability and confidence must be within [0,1]')
        rows.append({'candidate_id': candidate['candidate_id'], 'data_status': status,
                     'affinity_pred_value': score, 'affinity_probability_binary': probability,
                     'confidence_score': confidence, 'model_scale_IC50_uM': 10 ** score,
                     'pIC50_from_log10_uM': 6 - score,
                     'structure_review': candidate.get('structure_review', 'not_recorded'),
                     'control_status': candidate.get('control_status', 'not_recorded')})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t')
        writer.writeheader(); writer.writerows(rows)
    if args.affinity:
        record = {'data_status': 'actual_model_output', 'affinity_sha256': hashlib.sha256(args.affinity.read_bytes()).hexdigest(),
                  'confidence_sha256': hashlib.sha256(args.confidence.read_bytes()).hexdigest(),
                  'aggregation': 'ensemble affinity_pred_value and affinity_probability_binary; matching confidence_score',
                  'interpretation': 'model scale conversions only; structure review and experimental controls are separate'}
        args.out.with_suffix('.record.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(status, 'rows=', len(rows), 'output=', args.out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
