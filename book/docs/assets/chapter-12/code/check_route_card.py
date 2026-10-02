"""Check route-card fields and practical next actions; no scientific scoring."""
import argparse
import json
from pathlib import Path
REQUIRED=('task_id','question','starting_evidence','hypothesis','cpu_action','outputs','metrics','current_status','next_validation','resource_limit','stop_condition')
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('card',type=Path); a=p.parse_args()
    cards=json.loads(a.card.read_text(encoding='utf-8'))
    if not isinstance(cards,list) or not cards:
        raise ValueError('Expected a nonempty list of route cards')
    errors=[]; seen=set()
    for i,card in enumerate(cards,1):
        absent=[key for key in REQUIRED if not card.get(key)]
        name=card.get('task_id') or 'row'+str(i)
        if name in seen: errors.append(name+': duplicate task_id')
        seen.add(name)
        if absent: errors.append(name+': missing '+', '.join(absent))
        else: print(name+': fields complete; read the evidence and actions before execution')
    for error in errors: print(error)
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
