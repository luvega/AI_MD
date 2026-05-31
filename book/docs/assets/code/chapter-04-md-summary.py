from pathlib import Path
import pandas as pd

rmsd = pd.read_csv('inputs/rmsd.tsv', sep='\t')
summary = {
    'frames': len(rmsd),
    'rmsd_mean_nm': round(rmsd['rmsd_nm'].mean(), 3),
    'rmsd_max_nm': round(rmsd['rmsd_nm'].max(), 3),
}
Path('outputs').mkdir(exist_ok=True)
pd.Series(summary).to_csv('outputs/md_qc_summary.tsv', sep='\t', header=False)
