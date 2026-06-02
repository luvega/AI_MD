import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "audit_book_figures.py"


class AuditBookFiguresCliTest(unittest.TestCase):
    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

    def run_audit(self, root: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--book-root",
                str(root),
                "--min-caption-chars",
                "30",
                *extra_args,
            ],
            text=True,
            capture_output=True,
        )

    def test_accepts_numbered_image_and_mermaid_captions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            self.write_text(
                book_root / "chapters" / "chapter-01.md",
                """
                # Chapter 1

                ![图1.1 test map](../assets/imagegen/chapter-01.png)

                **图1.1 测试知识图谱。** 本图为教学示意图，用于说明节点关系；编号只用于定位，不承载精确参数，以正文为准。节点编号：1=输入；2=输出。

                ```mermaid
                flowchart LR
                    a["A"] --> b["B"]
                ```

                **图1.2 测试结构图。** 本图为 Mermaid 教学示意图，用于说明流程关系；箭头代表阅读顺序，以正文为准。
                """,
            )

            result = self.run_audit(book_root, "--min-figures-per-chapter", "2")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("errors: 0", result.stdout)
        self.assertIn("figures: 2", result.stdout)

    def test_rejects_wrong_caption_number_and_outside_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            self.write_text(
                book_root / "chapters" / "chapter-01.md",
                """
                # Chapter 1

                ![missing number](../assets/imagegen/chapter-01.png)

                **图1.2 错号知识图谱。** 本图为教学示意图，用于说明节点关系；编号只用于定位，不承载精确参数，以正文为准。

                图中编号节点与下表对应：

                | 编号 | 流程节点 |
                |:---:|:---|
                | 1 | Input |
                """,
            )
            self.write_text(
                book_root / "resources" / "index.md",
                "![outside](../assets/screenshots/outside.png)\n",
            )

            result = self.run_audit(book_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("figure number mismatch", result.stdout)
        self.assertIn("image alt missing figure number", result.stdout)
        self.assertIn("image outside chapter figure flow", result.stdout)
        self.assertIn("standalone figure number table remains", result.stdout)


if __name__ == "__main__":
    unittest.main()
