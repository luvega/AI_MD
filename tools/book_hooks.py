"""Preserve allowlisted Markdown downloads alongside MkDocs' readable pages."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.sync_online_book import public_assets, DOCS_DIR


def on_post_build(config):
    site = Path(config['site_dir']).resolve()
    for _, published in public_assets():
        if published.suffix == '.md':
            target = site / published.relative_to(DOCS_DIR)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(published, target)
