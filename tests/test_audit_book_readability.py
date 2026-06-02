import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.audit_book_readability import prose_char_count, repeated_sentences, split_sections


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "audit_book_readability.py"


class AuditBookReadabilityTest(unittest.TestCase):
    def write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")

    def test_prose_count_excludes_tables_code_images_and_refs(self) -> None:
        markdown = """
        ## 本章导读

        这一段用于解释教材场景，并帮助读者理解后续判断。

        | 列 | 值 |
        |:---|:---|
        | A | B |

        ![map](../assets/imagegen/map.png)

        ```bash
        echo should_not_count
        ```

        <!-- refs:start -->
        - Reference text should not count.
        <!-- refs:end -->
        """
        sections = split_sections(textwrap.dedent(markdown))
        count = prose_char_count(sections["本章导读"])
        self.assertGreater(count, 20)
        self.assertLess(count, len(sections["本章导读"]))

    def test_cli_rejects_short_priority_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter = root / "chapters" / "chapter-01.md"
            body = ["# Chapter"]
            for section in ["本章导读", "核心概念", "方法流程", "使用边界与常见误读", "延伸阅读与下一步"]:
                body.append(f"## {section}\n\n短段落。\n")
            self.write_text(chapter, "\n".join(body))

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--book-root",
                    str(root),
                    "--min-prose-chars-per-chapter",
                    "200",
                    "--min-priority-section-chars",
                    "50",
                ],
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("priority section too short", result.stdout)

    def test_repeated_sentences_uses_prose_only(self) -> None:
        shared_heading = "\u6838\u5fc3\u6982\u5ff5"
        shared_table = "\u91cd\u590d\u8868\u683c\u53e5\u5b50\u4e0d\u5e94\u7edf\u8ba1\u4e3a\u6b63\u6587\u91cd\u590d\u5ba1\u8ba1\u7ed3\u679c\u3002"
        shared_list = "\u91cd\u590d\u5217\u8868\u53e5\u5b50\u4e0d\u5e94\u7edf\u8ba1\u4e3a\u6b63\u6587\u91cd\u590d\u5ba1\u8ba1\u7ed3\u679c\u3002"
        shared_prose = "\u91cd\u590d\u6b63\u6587\u53e5\u5b50\u5e94\u8be5\u8fdb\u5165\u91cd\u590d\u53e5\u5ba1\u8ba1\u7ed3\u679c\u5e76\u88ab\u62a5\u544a\u51fa\u6765\u3002"
        chapter_texts = {
            f"chapter-{idx:02d}.md": textwrap.dedent(
                f"""
                ## {shared_heading}

                {shared_prose}

                | A | B |
                |:---|:---|
                | {shared_table} | x |

                1. {shared_list}
                """
            )
            for idx in range(1, 5)
        }

        repeated = repeated_sentences(chapter_texts)

        self.assertIn(shared_prose, repeated)
        self.assertNotIn(shared_table, repeated)
        self.assertNotIn(shared_list, repeated)


if __name__ == "__main__":
    unittest.main()
