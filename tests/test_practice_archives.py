import csv
import hashlib
import json
from pathlib import Path
import warnings
import zipfile

import pytest

from tools import sync_online_book as sync
from tools.validate_online_book import validate_practice_archives, validate_resource_cards


@pytest.fixture
def reviewed_assets(tmp_path, monkeypatch):
    chapters = tmp_path / "chapters"
    docs = tmp_path / "docs"
    monkeypatch.setattr(sync, "CHAPTERS_DIR", chapters)
    monkeypatch.setattr(sync, "ASSETS_OUT", docs / "assets")
    monkeypatch.setattr(sync, "DOCS_DIR", docs)
    docs.mkdir()
    rows = []
    for number in range(1, 13):
        relative = f"chapter-{number:02d}/assets/data/example.txt"
        path = chapters / relative
        path.parent.mkdir(parents=True)
        path.write_bytes(f"chapter {number}\r\n原始字节\n".encode())
        rows.append({"file_path": relative, "source_type": "teaching_template", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "validation_status": "checked"})
    relative = "shared/assets/practice-downloads.json"
    dependencies = chapters / relative
    dependencies.parent.mkdir(parents=True)
    dependencies.write_text(json.dumps({"dependencies": {"2": [3], "3": [1], "4": [1, 3], "9": [10], "11": [4, 10]}, "files": []}), encoding="utf-8")
    rows.append({"file_path": relative, "source_type": "independent_script", "sha256": hashlib.sha256(dependencies.read_bytes()).hexdigest(), "validation_status": "checked"})
    manifest = chapters / "public_assets.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    # A real unlisted file must stay out, even when it lives beside approved data.
    (chapters / "chapter-11/assets/data/unreviewed.txt").write_text("do not publish", encoding="utf-8")
    return sync.public_assets(manifest), manifest, docs


def test_archives_preserve_bytes_and_include_recursive_dependencies(reviewed_assets):
    approved, _, docs = reviewed_assets
    archives = sync.publish_practice_archives(approved, docs / "downloads")
    assert len(archives) == 12
    assert validate_practice_archives(approved, docs / "downloads") == []
    with zipfile.ZipFile(archives["chapter-11"]) as archive:
        assert {name.split("/")[1] for name in archive.namelist()} == {"chapter-01", "chapter-03", "chapter-04", "chapter-10", "chapter-11"}
        assert not any("unreviewed" in name for name in archive.namelist())
        archive.extractall(docs / "extracted")
    for source, _ in approved:
        relative = source.relative_to(sync.CHAPTERS_DIR)
        extracted = docs / "extracted/AI_MD_practice" / relative
        if extracted.is_file():
            assert extracted.read_bytes() == source.read_bytes()
    first_bytes = archives["chapter-11"].read_bytes()
    assert sync.publish_practice_archives(approved, docs / "downloads")["chapter-11"].read_bytes() == first_bytes


@pytest.mark.parametrize("change", ["changed", "missing", "extra", "unsafe", "duplicate", "symlink"])
def test_archive_validation_rejects_changed_or_unsafe_members(reviewed_assets, change):
    approved, _, docs = reviewed_assets
    path = sync.publish_practice_archives(approved, docs / "downloads")["chapter-01"]
    name = "AI_MD_practice/chapter-01/assets/data/example.txt"
    entries = [(name, (sync.CHAPTERS_DIR / "chapter-01/assets/data/example.txt").read_bytes())]
    if change == "changed":
        original = entries[0][1]
        entries[0] = (name, b"X" + original[1:])
    elif change == "missing":
        entries = []
    elif change == "extra":
        entries.append(("AI_MD_practice/chapter-01/assets/data/unreviewed.txt", b"extra"))
    elif change == "unsafe":
        entries.append(("AI_MD_practice/../private.txt", b"unsafe"))
    elif change == "duplicate":
        entries.append(entries[0])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(path, "w") as archive:
            for member, data in entries:
                info = zipfile.ZipInfo(member)
                if change == "symlink":
                    info.create_system = 3
                    info.external_attr = 0o120777 << 16
                archive.writestr(info, data)
    assert validate_practice_archives(approved, docs / "downloads")


def test_archive_validation_requires_all_12_and_no_extra_archives(reviewed_assets):
    approved, _, docs = reviewed_assets
    archives = sync.publish_practice_archives(approved, docs / "downloads")
    archives["chapter-12"].unlink()
    (docs / "downloads/course.zip").write_bytes(b"raw archive")
    errors = validate_practice_archives(approved, docs / "downloads")
    assert any("Missing chapter practice archive" in error for error in errors)
    assert any("Unexpected practice archive file" in error for error in errors)


def test_original_zip_is_still_rejected_by_asset_allowlist(reviewed_assets):
    _, manifest, _ = reviewed_assets
    relative = "chapter-01/assets/data/course.zip"
    path = sync.CHAPTERS_DIR / relative
    path.write_bytes(b"raw course archive")
    with manifest.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file_path", "source_type", "sha256", "validation_status"], delimiter="\t")
        writer.writerow({"file_path": relative, "source_type": "official_example", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "validation_status": "checked"})
    with pytest.raises(ValueError, match="Unsupported public asset type"):
        sync.public_assets(manifest)


def test_resources_page_has_one_zip_per_card(reviewed_assets):
    approved, _, docs = reviewed_assets
    archives = sync.publish_practice_archives(approved, docs / "downloads")
    chapters = [(f"chapter-{number:02d}", f"第 {number} 章") for number in range(1, 13)]
    sync.write_resources(chapters, archives)
    markdown = (docs / "resources.md").read_text(encoding="utf-8")
    assert validate_resource_cards(markdown) == []
    assert "C:/coursework/AI_MD_practice" in markdown
    assert "assets/data/example.txt" not in markdown
    assert validate_resource_cards(markdown + "\n[file](assets/chapter-01/data/example.txt)\n")


@pytest.mark.parametrize("dependencies", [{"13": [1]}, {"1": [0]}, {"1": [True]}, {"1": "2"}])
def test_dependency_manifest_rejects_invalid_chapters(reviewed_assets, dependencies):
    approved, _, _ = reviewed_assets
    (sync.CHAPTERS_DIR / "shared/assets/practice-downloads.json").write_text(json.dumps({"dependencies": dependencies}), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid dependenc"):
        sync.practice_dependencies(approved)
