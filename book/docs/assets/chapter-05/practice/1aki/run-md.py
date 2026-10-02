#!/usr/bin/env python3
"""Run the independent 1AKI CPU teaching workflow. No warnings are bypassed."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import re
import shutil
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gmx', default='gmx', help='gmx executable or absolute path')
    parser.add_argument('--work', required=True, type=Path, help='new output directory')
    parser.add_argument('--threads', type=int, default=4)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    work = args.work.resolve()
    if work.exists() and any(work.iterdir()):
        parser.error('output directory is not empty; choose a new run directory')
    work.mkdir(parents=True, exist_ok=True)
    text = (source / 'input' / '1aki.pdb').read_text()
    atoms = [line[:16] + ' ' + line[17:] for line in text.splitlines()
             if line.startswith('ATOM  ') and line[21:22] == 'A'
             and line[16:17] in (' ', 'A')]
    if not atoms:
        parser.error('1AKI chain A has no ATOM records')
    (work / 'protein.pdb').write_text('\n'.join(atoms) + '\nTER\nEND\n')
    for path in (source / 'mdp').glob('*.mdp'):
        shutil.copyfile(path, work / path.name)
    steps = [
        ('version', ['--version'], None),
        ('topology', ['pdb2gmx', '-f', 'protein.pdb', '-o', 'protein.gro', '-p', 'topol.top', '-ignh', '-ff', 'amber99sb', '-water', 'tip3p'], None),
        ('box', ['editconf', '-f', 'protein.gro', '-o', 'box.gro', '-d', '1.0', '-bt', 'dodecahedron'], None),
        ('water', ['solvate', '-cp', 'box.gro', '-cs', 'spc216.gro', '-o', 'solv.gro', '-p', 'topol.top'], None),
        ('ion-input', ['grompp', '-f', 'ions.mdp', '-c', 'solv.gro', '-p', 'topol.top', '-o', 'ions.tpr'], None),
        ('ions', ['genion', '-s', 'ions.tpr', '-o', 'system.gro', '-p', 'topol.top', '-pname', 'NA', '-nname', 'CL', '-neutral', '-conc', '0.15', '-seed', '20261002'], 'SOL\n'),
        ('em-input', ['grompp', '-f', 'em.mdp', '-c', 'system.gro', '-p', 'topol.top', '-o', 'em.tpr'], None),
        ('em', ['mdrun', '-deffnm', 'em', '-ntmpi', '1', '-ntomp', str(args.threads), '-nb', 'cpu'], None),
        ('nvt-input', ['grompp', '-f', 'nvt.mdp', '-c', 'em.gro', '-r', 'em.gro', '-p', 'topol.top', '-o', 'nvt.tpr'], None),
        ('nvt', ['mdrun', '-deffnm', 'nvt', '-ntmpi', '1', '-ntomp', str(args.threads), '-nb', 'cpu'], None),
        ('npt-input', ['grompp', '-f', 'npt.mdp', '-c', 'nvt.gro', '-r', 'em.gro', '-t', 'nvt.cpt', '-p', 'topol.top', '-o', 'npt.tpr'], None),
        ('npt', ['mdrun', '-deffnm', 'npt', '-ntmpi', '1', '-ntomp', str(args.threads), '-nb', 'cpu'], None),
        ('md-input', ['grompp', '-f', 'md.mdp', '-c', 'npt.gro', '-t', 'npt.cpt', '-p', 'topol.top', '-o', 'md.tpr'], None),
        ('md', ['mdrun', '-deffnm', 'md', '-ntmpi', '1', '-ntomp', str(args.threads), '-nb', 'cpu'], None),
        ('trajectory-check', ['check', '-f', 'md.xtc'], None),
    ]
    with (work / 'command-log.tsv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle, delimiter='\t')
        writer.writerow(['step', 'command', 'selection_input', 'exit_code', 'log'])
        thread_mpi_enabled = False
        for name, flags, selection in steps:
            if flags[0] == 'mdrun' and not thread_mpi_enabled:
                # -ntmpi applies only to builds with internal thread-MPI.
                position = flags.index('-ntmpi')
                flags = flags[:position] + flags[position + 2:]
            command = [args.gmx, *flags]
            print(name, ' '.join(command), flush=True)
            result = subprocess.run(command, cwd=work, input=selection, text=True,
                                    encoding='utf-8', errors='replace',
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log = name + '.stdout.log'
            (work / log).write_text(result.stdout, encoding='utf-8')
            writer.writerow([name, ' '.join(command), repr(selection), result.returncode, log])
            handle.flush()
            if result.returncode:
                print('Stopped. Inspect', work / log)
                return result.returncode
            if name == 'version':
                thread_mpi_enabled = bool(re.search(r'MPI\s+library\s*:\s*thread_mpi', result.stdout, re.IGNORECASE))
    print('Finished: 20 ps NVT, 20 ps NPT and 100 ps MD. Outputs:', work)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
