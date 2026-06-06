import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.audit_book_review_readiness import audit_chapter, split_sections


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "audit_book_review_readiness.py"


class AuditBookReviewReadinessTest(unittest.TestCase):
    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

    def test_split_sections_reads_key_literature_body(self) -> None:
        sections = split_sections(
            textwrap.dedent(
                """
                ## 关键文献

                文献使用说明：本章文献用于说明方法和边界。

                <!-- refs:start -->
                <!-- refs:end -->

                ## 下一节
                text
                """
            )
        )
        self.assertIn("关键文献", sections)
        self.assertIn("文献使用说明", sections["关键文献"])

    def test_chapter_audit_flags_template_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter-03.md"
            self.write_text(
                path,
                """
                # 第 3 章

                ## 本章导读

                关键问题不是单个命令或界面能够解决。受体、配体库、box 和 pose 是本章对象。

                ## 关键文献

                文献使用说明：本章文献用于说明 docking score 的 benchmark 与边界。

                <!-- refs:start -->
                <!-- refs:end -->

                ## 方法流程

                ### 案例走读

                receptor ligand box shortlist。

                ## 使用边界与常见误读

                docking score 不能写成 Kd 或 IC50。
                """,
            )

            audit = audit_chapter(path)

        self.assertIn("关键问题不是单个命令或界面能够解决", audit.forbidden_template_hits)
        self.assertTrue(audit.has_literature_use_note)

    def test_cli_rejects_stage_reports_in_book_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_text(root / "chapters" / "chapter-01.md", "# Ch\n\n## 关键文献\n\n文献使用说明：暂无。\n")
            self.write_text(root / "resources" / "p39-report.md", "# report")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--book-root", str(root)],
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stage reports must not be in book resources", result.stdout)


if __name__ == "__main__":
    unittest.main()
