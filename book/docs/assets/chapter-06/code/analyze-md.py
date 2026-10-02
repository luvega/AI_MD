#!/usr/bin/env python3
"""Extract real XVG/PCA outputs from the independently generated 1AKI run."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gmx', default='gmx')
    parser.add_argument('--run', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--tpr', type=Path, help='optional analysis TPR rebuilt with the locally installed GROMACS; keep original production TPR')
    parser.add_argument('--native-secondary', action='store_true', help='also use modern native hbond and dssp interfaces (verified with GROMACS 2025.5)')
    args = parser.parse_args()
    run, out = args.run.resolve(), args.out.resolve()
    needed = ['md.xtc', 'nvt.edr', 'npt.edr', 'protein.gro']
    for filename in needed:
        if not (run / filename).is_file():
            parser.error(f'missing real run input: {run / filename}')
    if out.exists() and any(out.iterdir()):
        parser.error('choose a new empty analysis directory')
    tpr_path = (args.tpr if args.tpr is not None else run / 'md.tpr').resolve()
    if not tpr_path.is_file():
        parser.error(f'missing matched analysis TPR: {tpr_path}')
    out.mkdir(parents=True, exist_ok=True)
    tpr, xtc = str(tpr_path), str(run / 'md.xtc')
    journal = []

    def execute(name, flags, selection=None):
        command = [args.gmx, *flags]
        result = subprocess.run(command, cwd=out, input=selection, text=True,
                                encoding='utf-8', errors='replace',
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = name + '.stdout.log'
        (out / log).write_text(result.stdout, encoding='utf-8')
        journal.append({'step': name, 'command': ' '.join(command),
                        'selection_input': repr(selection), 'exit_code': result.returncode, 'log': log})
        with (out / 'analysis-commands.tsv').open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(journal[0]), delimiter='\t')
            writer.writeheader(); writer.writerows(journal)
        if result.returncode:
            raise RuntimeError(f'{name} failed; read {out / log}')
        return result.stdout

    execute('version', ['--version'])
    execute('check-raw', ['check', '-f', xtc])
    execute('whole', ['trjconv', '-s', tpr, '-f', xtc, '-o', 'md-whole.xtc', '-pbc', 'mol'], 'System\n')
    execute('center', ['trjconv', '-s', tpr, '-f', 'md-whole.xtc', '-o', 'md-center.xtc', '-center', '-pbc', 'mol'], 'Protein\nSystem\n')
    execute('fit', ['trjconv', '-s', tpr, '-f', 'md-center.xtc', '-o', 'md-fit.xtc', '-fit', 'rot+trans'], 'Backbone\nSystem\n')
    execute('reference0', ['trjconv', '-s', tpr, '-f', 'md-center.xtc', '-o', 'md-reference0.pdb', '-dump', '0'], 'System\n')
    execute('reference-last', ['trjconv', '-s', tpr, '-f', 'md-center.xtc', '-o', 'md-last.pdb', '-dump', '100'], 'System\n')
    execute('rmsd-ca', ['rms', '-s', tpr, '-f', 'md-center.xtc', '-o', 'rmsd-ca.xvg', '-tu', 'ps'], 'C-alpha\nC-alpha\n')
    execute('rmsd-backbone', ['rms', '-s', tpr, '-f', 'md-center.xtc', '-o', 'rmsd-backbone.xvg', '-tu', 'ps'], 'Backbone\nBackbone\n')
    execute('rmsd-lastref', ['rms', '-s', 'md-last.pdb', '-f', 'md-center.xtc', '-o', 'rmsd-ca-lastref.xvg', '-tu', 'ps'], 'C-alpha\nC-alpha\n')
    execute('rmsf-ca', ['rmsf', '-s', tpr, '-f', 'md-center.xtc', '-o', 'rmsf-ca.xvg', '-res'], 'C-alpha\n')
    gyrate_help = execute('gyrate-help', ['gyrate', '-h'])
    gyrate_args = ['gyrate', '-s', tpr, '-f', 'md-center.xtc', '-o', 'gyrate.xvg']
    if '-sel ' in gyrate_help:
        gyrate_args.extend(['-sel', 'group "Protein"'])
        execute('gyrate', gyrate_args)
    else:
        execute('gyrate', gyrate_args, 'Protein\n')
    execute('sasa', ['sasa', '-s', tpr, '-f', 'md-center.xtc', '-o', 'sasa.xvg',
                     '-surface', 'group "Protein"', '-output', 'group "Protein"'])
    if args.native_secondary:
        execute('hbond-protein', ['hbond', '-s', tpr, '-f', 'md-center.xtc', '-r', 'group "Protein"',
                                 '-t', 'group "Protein"', '-num', 'hbond-protein.xvg',
                                 '-dan', 'hbond-donors-acceptors.xvg', '-dist', 'hbond-distances.xvg',
                                 '-ang', 'hbond-angles.xvg', '-o', 'hbond-protein.ndx'])
        execute('dssp', ['dssp', '-s', tpr, '-f', 'md-center.xtc', '-sel', 'group "Protein"',
                        '-o', 'dssp.dat', '-num', 'dssp-count.xvg'])
    protein_gro = (run / 'protein.gro').read_text().splitlines()
    expected = {35: 'GLU', 52: 'ASP'}
    observed = {}
    for line in protein_gro[2:-1]:
        if line[10:15].strip() == 'CA' and int(line[:5]) in expected:
            observed[int(line[:5])] = line[5:10].strip()
    if observed != expected:
        raise RuntimeError(f'1AKI C-alpha distance residues differ: {observed}')
    distance_selection = '(group "Protein" and resnr 35 and name CA) plus (group "Protein" and resnr 52 and name CA)'
    execute('distance-glu35-asp52', ['distance', '-s', tpr, '-f', 'md-center.xtc',
                                   '-select', distance_selection, '-oall', 'distance-glu35-asp52.xvg'])
    execute('nvt-temperature', ['energy', '-f', str(run / 'nvt.edr'), '-o', 'nvt-temperature.xvg'], 'Temperature\n0\n')
    execute('npt-pressure-density', ['energy', '-f', str(run / 'npt.edr'), '-o', 'npt-pressure-density.xvg'], 'Pressure\nDensity\n0\n')
    execute('npt-pressure', ['energy', '-f', str(run / 'npt.edr'), '-o', 'npt-pressure.xvg'], 'Pressure\n0\n')
    execute('npt-density', ['energy', '-f', str(run / 'npt.edr'), '-o', 'npt-density.xvg'], 'Density\n0\n')
    execute('covariance', ['covar', '-s', tpr, '-f', 'md-fit.xtc', '-o', 'eigenvalues.xvg',
                           '-v', 'eigenvectors.trr', '-av', 'pca-average.pdb'], 'C-alpha\nC-alpha\n')
    execute('pca-projection', ['anaeig', '-s', tpr, '-f', 'md-fit.xtc', '-v', 'eigenvectors.trr',
                              '-first', '1', '-last', '2', '-proj', 'pca-projection.xvg', '-2d', 'pca-2d.xvg'], 'C-alpha\nC-alpha\n')
    execute('cluster', ['cluster', '-s', tpr, '-f', 'md-fit.xtc', '-method', 'gromos',
                        '-cutoff', '0.10', '-g', 'cluster.log', '-dist', 'cluster-rmsd-distribution.xvg',
                        '-o', 'cluster-rmsd.xpm', '-sz', 'cluster-sizes.xvg', '-cl', 'cluster-representatives.pdb'],
            'C-alpha\nProtein\n')
    execute('sham', ['sham', '-f', 'pca-2d.xvg', '-notime', '-ngrid', '8', '8', '8',
                     '-tsham', '300', '-ls', 'fel.xpm', '-g', 'sham.log'])
    representatives = (out / 'cluster-representatives.pdb').read_text()
    first_model, active = [], False
    if 'MODEL ' in representatives:
        for line in representatives.splitlines():
            if line.startswith('MODEL'):
                if active:
                    break
                active = True
            if active:
                first_model.append(line)
            if active and line.startswith('ENDMDL'):
                break
    else:
        first_model = representatives.splitlines()
    if not any(line.startswith('ATOM  ') for line in first_model):
        raise RuntimeError('cluster output contains no first representative atoms')
    if sum(line.startswith('ATOM  ') for line in first_model) != int(protein_gro[1]):
        raise RuntimeError('cluster representative does not contain the complete Protein output group')
    (out / 'representative-first-cluster.pdb').write_text('\n'.join(first_model) + '\nEND\n')
    execute('check-centered', ['check', '-f', 'md-center.xtc'])
    metadata = {'data_status': 'independent_real_GROMACS_run', 'system': '1AKI chain A',
                'analysis_note': '100 ps format and selection exercise; PCA is exploratory, not converged state sampling',
                'run_inputs': {name: {'file_name': name,
                                     'sha256': hashlib.sha256((run / name).read_bytes()).hexdigest()} for name in needed},
                'analysis_tpr': {'file_name': tpr_path.name, 'sha256': hashlib.sha256(tpr_path.read_bytes()).hexdigest(),
                                 'locally_rebuilt': args.tpr is not None},
                'rmsd': {'ca': ['C-alpha', 'C-alpha'], 'backbone': ['Backbone', 'Backbone'],
                         'last_reference': 'md-last.pdb at 100 ps'},
                'pca_atoms': 'C-alpha', 'trajectory_output_group': 'System'}
    metadata['cluster'] = {'method': 'gromos', 'cutoff_nm': 0.10, 'rmsd_group': 'C-alpha', 'output_group': 'Protein'}
    metadata['distance'] = {'residues_checked': observed, 'atoms': 'C-alpha', 'selection': distance_selection}
    metadata['native_secondary_structure'] = args.native_secondary
    metadata['sham'] = {'input_has_time_column': False, 'grid': [8, 8], 'temperature_K': 300,
                        'interpretation': 'projected finite-frame frequency exercise, not converged basins'}
    (out / 'analysis-record.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print('Real analysis outputs:', out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
