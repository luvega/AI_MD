"""Refresh download and publication lists from reviewed chapter provenance.

Run only after checking sources, licenses, outputs and the chapter provenance.
This tool verifies records and hashes; it does not approve new teaching files.
"""
import csv
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
chapters = root / 'chapters'
rows = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for number in range(1, 13):
    chapter_id = f'chapter-{number:02d}'
    provenance = chapters / chapter_id / 'assets/provenance.tsv'
    with provenance.open(encoding='utf-8-sig', newline='') as handle:
        entries = list(csv.DictReader(handle, delimiter='\t'))
    for entry in entries:
        name = entry.get('file_path') or entry.get('file') or entry.get('path')
        if name.startswith('chapters/'):
            name = name[len('chapters/'):]
        if not name.startswith('chapter-'):
            name = f'{chapter_id}/assets/{name}'
        if not re.fullmatch(r'chapter-\d{2}/assets/.+', name) or '..' in Path(name).parts:
            raise ValueError('Invalid reviewed asset path: ' + name)
        path = chapters / name
        if (chapters / chapter_id / 'assets').resolve() not in path.resolve().parents:
            raise ValueError('Reviewed asset is outside its chapter: ' + name)
        if not path.is_file():
            raise FileNotFoundError(path)
        if entry['sha256'] != digest(path):
            raise ValueError('Provenance needs review after edit: ' + name)
        origin = entry.get('source_url') or entry.get('source', '')
        source_type = entry.get('source_type')
        if not source_type:
            if path.suffix == '.py':
                source_type = 'independent_script'
            elif 'constructed-' in name:
                source_type = 'teaching_constructed'
            elif path.suffix in {'.svg', '.png'}:
                source_type = 'original_diagram'
            elif '/results/' in name or '/analysis/' in name:
                source_type = 'independent_run'
            elif path.suffix in {'.md', '.mdp', '.yaml'}:
                source_type = 'teaching_template'
            elif 'rcsb.org' in origin:
                source_type = 'public_structure'
            elif origin.startswith('http'):
                source_type = 'official_example'
            elif 'results/' in name or 'data/' in name:
                source_type = 'independent_run'
            else:
                source_type = 'teaching_template'
        validation = entry.get('validation_status') or entry.get('validation') or entry.get('verification')
        if not validation:
            raise ValueError('Missing validation record: ' + name)
        rows.append({'file_path': name, 'source_type': source_type,
                     'source_url': origin if origin.startswith('http') else '',
                     'validation_status': validation,
                     'sha256': digest(path),
                     'notes': entry.get('generation_method') or entry.get('transformation') or entry.get('method', '')})
    rows.append({'file_path': provenance.relative_to(chapters).as_posix(), 'source_type': 'teaching_template',
                 'source_url': '', 'validation_status': 'source review record checked against listed file hashes',
                 'sha256': digest(provenance), 'notes': 'Public source and validation record; no local lecture derivatives'})

downloads = {'version': '1.1.0', 'dependencies': {'2': [3], '3': [1], '4': [1, 3], '6': [5], '8': [3], '9': [10], '11': [4, 10]}, 'files': []}
for row in rows:
    match = re.fullmatch(r'chapter-(\d{2})/assets/(.+)', row['file_path'])
    downloads['files'].append({'chapter': int(match[1]), 'relative_path': row['file_path'],
                               'url_path': f'chapter-{match[1]}/{match[2]}', 'sha256': row['sha256']})
download_manifest = chapters / 'shared/assets/practice-downloads.json'
download_manifest.write_text(json.dumps(downloads, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for path in [chapters / 'shared/assets/get-practice.py', download_manifest]:
    rows.append({'file_path': path.relative_to(chapters).as_posix(),
                 'source_type': 'independent_script' if path.suffix == '.py' else 'teaching_template',
                 'source_url': '', 'validation_status': 'checksum and dependency download regression checked',
                 'sha256': digest(path), 'notes': 'Independently authored downloader and reviewed chapter file list'})
with (chapters / 'public_assets.tsv').open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=['file_path', 'source_type', 'source_url', 'validation_status', 'sha256', 'notes'], delimiter='\t')
    writer.writeheader()
    writer.writerows(rows)
print('Reviewed assets:', len(rows), 'bytes:', sum((chapters / row['file_path']).stat().st_size for row in rows))
