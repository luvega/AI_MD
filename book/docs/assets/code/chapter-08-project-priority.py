import pandas as pd

projects = pd.read_csv('inputs/project_pool.tsv', sep='\t')
projects['priority_score'] = (
    projects['evidence_strength'] * 0.45 +
    projects['method_readiness'] * 0.35 +
    projects['experiment_feasibility'] * 0.20
)
projects.sort_values('priority_score', ascending=False).to_csv('outputs/project_priority.tsv', sep='\t', index=False)
