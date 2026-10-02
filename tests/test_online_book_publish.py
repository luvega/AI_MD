from pathlib import Path

from tools.validate_online_book import validate
from tools.sync_online_book import public_assets, render_chapter, rewrite_paths
import csv
import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_online_book_validation_passes() -> None:
    errors = validate()
    assert errors == []


def test_all_chapter_pages_are_generated_from_body_files() -> None:
    for chapter_number in range(1, 13):
        chapter_id = f"chapter-{chapter_number:02d}"
        assert (ROOT / "chapters" / chapter_id / "正文.md").exists()
        assert (ROOT / "book" / "docs" / "chapters" / f"{chapter_id}.md").exists()
        assert (ROOT / "book" / "docs" / "chapters" / f"{chapter_id}.md").read_text(encoding="utf-8") == render_chapter(chapter_number)[2]


@pytest.mark.parametrize("path,source_type", [("../06_原始学习素材/slides.png", "public_structure"), ("chapter-01/assets/../lecture.html", "official_example"), ("chapter-01/assets/course.pdf", "official_example"), ("chapter-01/assets/missing.tsv", "lecture_slide")])
def test_public_assets_reject_unreviewed_or_escaped_files(tmp_path, path, source_type):
    manifest = tmp_path / "assets.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file_path", "source_type"], delimiter="\t")
        writer.writeheader()
        writer.writerow({"file_path": path, "source_type": source_type})
    with pytest.raises(ValueError):
        public_assets(manifest)


def test_student_markdown_prompt_is_allowlisted_and_published():
    assets = public_assets()
    prompts = [(s, d) for s, d in assets if s.name == "vina_batch_docking_skill_prompt.md"]
    assert len(prompts) == 1
    assert prompts[0][1].read_bytes() == prompts[0][0].read_bytes()


def test_publication_rewrites_cross_chapter_links_and_keeps_commands():
    source = "[input](../chapter-03/assets/data/3htb/3htb.pdb)\n```\npython chapters/chapter-04/assets/code/run_vina_case.py --help\n```"
    rendered = rewrite_paths(source, "chapter-11")
    assert "[input](../assets/chapter-03/data/3htb/3htb.pdb)" in rendered
    assert "python chapters/chapter-04/assets/code/run_vina_case.py --help" in rendered
