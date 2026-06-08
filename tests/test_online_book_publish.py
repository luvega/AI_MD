from pathlib import Path

from tools.validate_online_book import validate


ROOT = Path(__file__).resolve().parents[1]


def test_online_book_validation_passes() -> None:
    errors = validate()
    assert errors == []


def test_all_chapter_pages_are_generated_from_body_files() -> None:
    for chapter_number in range(1, 13):
        chapter_id = f"chapter-{chapter_number:02d}"
        assert (ROOT / "chapters" / chapter_id / "正文.md").exists()
        assert (ROOT / "book" / "docs" / "chapters" / f"{chapter_id}.md").exists()
