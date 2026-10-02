"""Inspect a manifest: file completeness, execution state and requested metrics.

Uses Python standard library only. It never runs a model or assigns biological
success. Relative output paths resolve against --workspace-root (manifest parent
by default). Existing output files are not changed.
"""
from __future__ import annotations
import argparse
import csv
import math
from pathlib import Path

FIELDS = ['task_id','stage','candidate_id','data_kind','run_status','files_found','missing_files','metric_checks','decision','next_action']

def read_rows(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        reader=csv.DictReader(handle)
        required={'task_id','stage','candidate_id','run_status','output_dir','expected_files','data_kind'}
        missing=required-set(reader.fieldnames or [])
        if missing:
            raise ValueError('Missing columns: '+', '.join(sorted(missing)))
        return [{k:(v or '').strip() for k,v in row.items()} for row in reader]

def inspect(row,base):
    status=row['run_status']
    if status not in {'completed','not_run','failed','upstream_output'}:
        raise ValueError('Unknown run_status for '+row['task_id']+': '+status)
    names=[v.strip() for v in row['expected_files'].split(';') if v.strip()]
    folder=base/row['output_dir']
    missing=[name for name in names if not (folder/name).is_file()]
    checks=[]
    for key in [v.strip() for v in row.get('required_metrics','').split(';') if v.strip()]:
        value=row.get(key,'')
        try:
            valid=bool(value) and math.isfinite(float(value))
        except ValueError:
            valid=False
        checks.append(key+('=present' if valid else '=missing_or_invalid'))
    metric_missing=any(v.endswith('=missing_or_invalid') for v in checks)
    if status=='not_run':
        decision,action='pending','run the next stage or record a resource limit'
    elif status=='failed':
        decision,action='failed','read the log before changing the command'
    elif not names or missing or metric_missing:
        decision,action='incomplete','inspect missing files and metric sources'
    else:
        decision,action='ready','inspect the structure or continue to the next stage'
    return {'task_id':row['task_id'],'stage':row['stage'],'candidate_id':row['candidate_id'],'data_kind':row['data_kind'],'run_status':status,'files_found':str(len(names)-len(missing))+'/'+str(len(names)),'missing_files':';'.join(missing),'metric_checks':';'.join(checks) or 'not requested for this stage','decision':decision,'next_action':action}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--summary-csv',type=Path,required=True)
    parser.add_argument('--report-md',type=Path)
    parser.add_argument('--workspace-root',type=Path)
    args=parser.parse_args()
    base=(args.workspace_root or args.manifest.parent).resolve()
    rows=[inspect(row,base) for row in read_rows(args.manifest)]
    args.summary_csv.parent.mkdir(parents=True,exist_ok=True)
    with args.summary_csv.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    if args.report_md:
        lines=['# Batch execution review','','| Candidate | Stage | State | Files | Decision |','|---|---|---|---|---|']
        lines += ['| '+r['candidate_id']+' | '+r['stage']+' | '+r['run_status']+' | '+r['files_found']+' | '+r['decision']+' |' for r in rows]
        lines += ['','This report checks recorded execution and files. A ready row still needs task-specific structural review.']
        args.report_md.parent.mkdir(parents=True,exist_ok=True)
        args.report_md.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for row in rows:
        print(row['candidate_id'],row['stage'],row['decision'],row['files_found'])
    return 0

if __name__=='__main__':
    raise SystemExit(main())
