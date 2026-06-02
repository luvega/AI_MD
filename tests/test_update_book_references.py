import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "update_book_references.py"


class UpdateBookReferencesCliTest(unittest.TestCase):
    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

    def test_updates_single_line_bibtex_into_nature_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_text(
                root / "references" / "references.bib",
                """
                @article{known_key, title={Known method paper}, volume={7}, journal={Nature Methods}, author={Doe, Jane and Smith, John}, year={2026}, pages={12-19}, DOI={10.1000/example}}
                """,
            )
            self.write_text(
                root / "references" / "zotero-map.tsv",
                """
                zotero_item_key\tbibtex_key
                ABC123\tknown_key
                """,
            )
            self.write_text(
                root / "book" / "book_map.toml",
                """
                [[chapters]]
                title = "Chapter"
                slug = "chapter-01"
                page = "chapters/chapter-01.md"
                required_bibtex_keys = ["known_key"]
                """,
            )
            self.write_text(
                root / "book" / "docs" / "chapters" / "chapter-01.md",
                """
                # Chapter

                ## 关键文献

                old content
                """,
            )
            self.write_text(root / "book" / "docs" / "appendices" / "references.md", "# old\n")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--map",
                    str(root / "book" / "book_map.toml"),
                    "--book-root",
                    str(root / "book" / "docs"),
                    "--references",
                    str(root / "references" / "references.bib"),
                    "--zotero-map",
                    str(root / "references" / "zotero-map.tsv"),
                ],
                cwd=root,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            chapter = (root / "book" / "docs" / "chapters" / "chapter-01.md").read_text(encoding="utf-8")
            self.assertIn("Doe, J. & Smith, J. Known method paper. Nature Methods 7, 12-19 (2026).", chapter)
            self.assertIn("https://doi.org/10.1000/example", chapter)
            self.assertIn("本文内容简介", chapter)
            self.assertNotIn("BibTeX key", chapter)
            self.assertNotIn("Zotero item key", chapter)


if __name__ == "__main__":
    unittest.main()
