import unittest

from tools.polish_book_chapters import overclaim_hits, protected_tokens, replace_section


class PolishBookChaptersTest(unittest.TestCase):
    def test_replace_section_preserves_neighbor_heading_spacing(self) -> None:
        text = "# Title\n\n## 本章导读\n\nold\n\n## 学习目标\n\nkeep\n"
        updated = replace_section(text, "本章导读", "new")
        self.assertIn("## 本章导读\n\nnew\n\n## 学习目标", updated)

    def test_protected_tokens_include_reference_code_and_images(self) -> None:
        text = """![图](../assets/imagegen/example.png)

```bash
echo 10.1000/example
```

<!-- refs:start -->
`known_key` https://doi.org/10.1000/example
<!-- refs:end -->
"""
        tokens = protected_tokens(text)
        self.assertIn("../assets/imagegen/example.png", tokens)
        self.assertTrue(any("refs:start" in token for token in tokens))
        self.assertTrue(any("echo 10.1000/example" in token for token in tokens))

    def test_overclaim_scan_allows_negated_prove_language(self) -> None:
        self.assertEqual(overclaim_hits("该结果不能证明机制成立。"), [])
        self.assertTrue(overclaim_hits("该结果证明机制成立。"))


if __name__ == "__main__":
    unittest.main()
