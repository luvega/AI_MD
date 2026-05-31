import pandas as pd

results = pd.read_csv('inputs/boltz2_results.tsv', sep='\t')
ranked = results.sort_values(['pred_affinity', 'confidence'], ascending=[True, False])
cols = ['candidate_id', 'pred_affinity', 'confidence', 'note']
ranked[cols].to_csv('outputs/boltz2_ranked.tsv', sep='\t', index=False)
print(ranked[cols].head(5).to_string(index=False))
