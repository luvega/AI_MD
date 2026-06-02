import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "validate_online_book.py"


REQUIRED_SECTIONS = [
    "本章导读",
    "学习目标",
    "知识图谱入口",
    "核心概念",
    "方法流程",
    "代码案例与软件操作",
    "关键文献",
    "实验/练习入口",
    "使用边界与常见误读",
    "延伸阅读与下一步",
]


class ValidateOnlineBookCliTest(unittest.TestCase):
    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

    def make_valid_workspace(self, root: Path) -> tuple[Path, Path]:
        self.write_text(
            root / "references" / "references.bib",
            """
            @article{known_key,
              title = {Known paper}
            }
            """,
        )
        self.write_text(root / "wiki" / "source.md", "# Source\n")
        self.write_text(root / "book" / "docs" / "index.md", "# Home\n\n[Chapter](chapters/chapter-01.md)\n")
        self.write_text(root / "book" / "docs" / "assets" / "screenshots" / "chapter-01.png", "placeholder\n")
        self.write_text(root / "book" / "docs" / "assets" / "imagegen" / "chapter-01-knowledge-map.png", "placeholder\n")
        self.write_text(
            root / "book" / "docs" / "resources" / "imagegen-manifest.tsv",
            """
            id\tchapter\ttype\tfile\tprompt_ref\tsource_basis\talt_text\tstatus
            ch01-map\tchapter-01\tknowledge-map\tassets/imagegen/chapter-01-knowledge-map.png\t#ch01-map\twiki/source.md\tchapter map\taccepted
            """,
        )
        chapter_body = ["# Chapter 1"]
        for section in REQUIRED_SECTIONS:
            body = "- 内容骨架。\n"
            if section == "知识图谱入口":
                body += "\n![chapter map](../assets/imagegen/chapter-01-knowledge-map.png)\n"
            if section == "代码案例与软件操作":
                body += "\n```bash\npython --version\n```\n\n![screenshot](../assets/screenshots/chapter-01.png)\n"
            if section == "关键文献":
                body += "\n<!-- refs:start -->\n\n- Known, A. Known paper. Source (2026).\n\n  **本文内容简介：** 本文介绍示例研究的核心问题、方法和证据边界。\n\n<!-- refs:end -->\n"
            chapter_body.append(f"## {section}\n\n{body}\n")
        chapter_body.append("[Home](../index.md)\n")
        self.write_text(root / "book" / "docs" / "chapters" / "chapter-01.md", "\n".join(chapter_body))
        self.write_text(
            root / "book" / "book_map.toml",
            """
            [[chapters]]
            title = "Chapter 1"
            slug = "chapter-01"
            page = "chapters/chapter-01.md"
            chapter_source = "wiki/source.md"
            method_sources = []
            literature_sources = []
            experiment_sources = []
            workbench_sources = []
            required_bibtex_keys = ["known_key"]
            """,
        )
        return root / "book" / "book_map.toml", root / "book" / "docs"

    def run_validator(
        self,
        book_map: Path,
        book_root: Path,
        cwd: Path,
        *extra_args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--map", str(book_map), "--book-root", str(book_root), *extra_args],
            cwd=cwd,
            text=True,
            capture_output=True,
        )

    def test_accepts_valid_book_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_map, book_root = self.make_valid_workspace(root)
            result = self.run_validator(book_map, book_root, root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("errors: 0", result.stdout)

    def test_rejects_missing_required_section_and_unknown_bibtex_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_map, book_root = self.make_valid_workspace(root)
            chapter = book_root / "chapters" / "chapter-01.md"
            text = chapter.read_text(encoding="utf-8")
            text = text.replace("## 使用边界与常见误读\n\n- 内容骨架。\n", "")
            chapter.write_text(text, encoding="utf-8")
            map_text = book_map.read_text(encoding="utf-8").replace("known_key", "missing_key")
            book_map.write_text(map_text, encoding="utf-8")

            result = self.run_validator(book_map, book_root, root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required section", result.stdout)
        self.assertIn("missing BibTeX key", result.stdout)

    def test_rejects_raw_source_links_and_broken_internal_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_map, book_root = self.make_valid_workspace(root)
            chapter = book_root / "chapters" / "chapter-01.md"
            text = chapter.read_text(encoding="utf-8")
            text += "\n[raw pdf](../../06_原始学习素材/example.pdf)\n[broken](missing.md)\n"
            chapter.write_text(text, encoding="utf-8")

            result = self.run_validator(book_map, book_root, root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("raw source link", result.stdout)
        self.assertIn("broken internal link", result.stdout)

    def test_rejects_chapter_below_requested_character_floor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_map, book_root = self.make_valid_workspace(root)
            result = self.run_validator(book_map, book_root, root, "--min-chapter-chars", "5000")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("chapter too short", result.stdout)

    def test_rejects_missing_imagegen_and_reference_markers_when_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_map, book_root = self.make_valid_workspace(root)
            chapter = book_root / "chapters" / "chapter-01.md"
            text = chapter.read_text(encoding="utf-8")
            text = text.replace("![chapter map](../assets/imagegen/chapter-01-knowledge-map.png)\n", "")
            text = text.replace("<!-- refs:start -->", "").replace("<!-- refs:end -->", "")
            chapter.write_text(text, encoding="utf-8")

            result = self.run_validator(book_map, book_root, root, "--require-nature-refs", "--require-imagegen")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing refs markers", result.stdout)
        self.assertIn("missing Imagegen knowledge map", result.stdout)

    def test_rejects_unregistered_imagegen_asset_when_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_map, book_root = self.make_valid_workspace(root)
            chapter = book_root / "chapters" / "chapter-01.md"
            text = chapter.read_text(encoding="utf-8").replace(
                "chapter-01-knowledge-map.png",
                "chapter-01-unregistered-knowledge-map.png",
            )
            chapter.write_text(text, encoding="utf-8")
            self.write_text(root / "book" / "docs" / "assets" / "imagegen" / "chapter-01-unregistered-knowledge-map.png", "placeholder\n")

            result = self.run_validator(book_map, book_root, root, "--require-imagegen")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unregistered Imagegen asset", result.stdout)


if __name__ == "__main__":
    unittest.main()
