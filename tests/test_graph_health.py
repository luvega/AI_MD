import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "graph_health.py"


class GraphHealthCliTest(unittest.TestCase):
    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

    def test_reports_core_graph_health_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_text(
                root / "references" / "references.bib",
                """
                @article{known_key,
                  title = {Known paper}
                }
                """,
            )
            self.write_text(
                root / "references" / "zotero-map.tsv",
                """
                zotero_item_key\tbibtex_key\ttitle
                ITEM1\tknown_key\tKnown paper
                ITEM2\tmissing_key\tMissing paper
                """,
            )
            self.write_text(
                root / "good.md",
                """
                ---
                title: "Good"
                type: method-note
                wiki_role: method
                last_reviewed: 2026-05-01
                zotero_items: ["ITEM1"]
                bibtex_keys: ["known_key"]
                relations:
                  - type: supports
                    target: "evidence.md"
                ---

                # Good
                """,
            )
            self.write_text(
                root / "evidence.md",
                """
                ---
                title: "Evidence"
                type: project-doc
                wiki_role: synthesis
                last_reviewed: 2026-05-01
                ---

                # Evidence
                """,
            )
            self.write_text(
                root / "stale.md",
                """
                ---
                title: "Stale"
                type: project-doc
                wiki_role: synthesis
                last_reviewed: 2024-01-01
                ---

                # Stale
                """,
            )
            self.write_text(
                root / "literature-missing-keys.md",
                """
                ---
                title: "Literature Missing Keys"
                type: literature-note
                wiki_role: literature
                last_reviewed: 2026-05-01
                ---

                # Literature Missing Keys
                """,
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--json", "--stale-days", "120"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            payload = json.loads(result.stdout)

        self.assertEqual(payload["summary"]["markdown_files"], 4)
        self.assertEqual(payload["summary"]["frontmatter_pages"], 4)
        self.assertEqual(payload["relation_types"]["supports"], 1)
        self.assertEqual(payload["summary"]["zotero_rows"], 2)
        self.assertEqual(payload["summary"]["zotero_keys_missing_in_bib"], 1)
        self.assertGreaterEqual(payload["summary"]["isolated_pages"], 1)
        self.assertGreaterEqual(payload["summary"]["stale_pages"], 1)
        self.assertEqual(payload["summary"]["literature_pages_missing_zotero_or_bibtex"], 1)

        missing = payload["issues"]["zotero_keys_missing_in_bib"]
        self.assertEqual(missing[0]["bibtex_key"], "missing_key")
        stale_paths = {item["path"] for item in payload["issues"]["stale_pages"]}
        self.assertIn("stale.md", stale_paths)


if __name__ == "__main__":
    unittest.main()
