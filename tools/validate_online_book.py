from __future__ import annotations

import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.sync_online_book import public_assets, render_chapter, practice_dependencies, practice_archive_members
BOOK_DIR = ROOT / "book"
DOCS_DIR = BOOK_DIR / "docs"
CHAPTERS_DIR = ROOT / "chapters"
CHAPTER_COUNT = 12
DOWNLOADS_DIR = DOCS_DIR / "downloads"

BANNED_CONTENT = (
    "本章大纲.md",
    "06_原始学习素材",
    "08_实战教程",
    "book/docs",
    "book/site",
    "polish_book_chapters.py",
    "阶段报告",
    "维护报告",
    "待作者确认",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def local_links(markdown: str) -> list[str]:
    links = []
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", markdown):
        href = match.group(1).strip()
        if not href or href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        links.append(href.split("#", 1)[0])
    return links


def validate_practice_archives(approved: list[tuple[Path, Path]],
                               downloads_dir: Path | None = None) -> list[str]:
    downloads_dir = downloads_dir or DOWNLOADS_DIR
    errors = []
    expected_paths = {downloads_dir / f"chapter-{number:02d}.zip" for number in range(1, CHAPTER_COUNT + 1)}
    actual_paths = {path for path in downloads_dir.rglob("*") if path.is_file()}
    for path in sorted(actual_paths - expected_paths):
        errors.append(f"Unexpected practice archive file: {path}")
    dependencies = practice_dependencies(approved)
    for number in range(1, CHAPTER_COUNT + 1):
        path = downloads_dir / f"chapter-{number:02d}.zip"
        if not path.is_file():
            errors.append(f"Missing chapter practice archive: {path}")
            continue
        members = practice_archive_members(approved, number, dependencies)
        try:
            with zipfile.ZipFile(path) as archive:
                infos = archive.infolist()
                names = [info.filename for info in infos]
                if len(names) != len(set(names)):
                    errors.append(f"{path}: duplicate ZIP member")
                if set(names) != set(members):
                    errors.append(f"{path}: ZIP members differ from approved chapter files")
                for info in infos:
                    relative = PurePosixPath(info.filename)
                    if relative.is_absolute() or ".." in relative.parts or "\\" in info.filename or ":" in info.filename or not re.fullmatch(r"AI_MD_practice/chapter-\d{2}/assets/.+", info.filename):
                        errors.append(f"{path}: unsafe ZIP member path: {info.filename}")
                        continue
                    if info.is_dir() or stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1:
                        errors.append(f"{path}: ZIP member must be a regular unencrypted file: {info.filename}")
                        continue
                    source = members.get(info.filename)
                    if source is None:
                        continue
                    data = source.read_bytes()
                    if info.file_size != len(data):
                        errors.append(f"{path}: ZIP member size differs from reviewed source: {info.filename}")
                    # Reading verifies the member CRC as well as its complete bytes.
                    elif archive.read(info) != data:
                        errors.append(f"{path}: ZIP member differs from reviewed source: {info.filename}")
        except (OSError, zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
            errors.append(f"Invalid practice archive {path}: {exc}")
    return errors


def validate_resource_cards(markdown: str) -> list[str]:
    cards = re.findall(r'<div class="resource-card" markdown="1">(.*?)</div>', markdown, flags=re.DOTALL)
    errors = []
    if len(cards) != CHAPTER_COUNT or markdown.count('<div class="resource-grid" markdown="1">') != 1:
        errors.append("Resources page must contain one grid with 12 chapter cards")
    for number, card in enumerate(cards, 1):
        chapter_id = f"chapter-{number:02d}"
        expected = [f"downloads/{chapter_id}.zip", f"chapters/{chapter_id}.md"]
        if local_links(card) != expected or card.count("[下载本章资源]") != 1 or card.count("[阅读本章]") != 1:
            errors.append(f"Resources card {chapter_id} must link to its single ZIP and chapter page")
        if "压缩包大小：" not in card:
            errors.append(f"Resources card {chapter_id} is missing its compressed size")
        if f'download="{chapter_id}.zip"' not in card:
            errors.append(f"Resources card {chapter_id} must preserve its chapter ZIP filename")
    if local_links(markdown) != [link for number in range(1, CHAPTER_COUNT + 1) for link in (f"downloads/chapter-{number:02d}.zip", f"chapters/chapter-{number:02d}.md")]:
        errors.append("Resources page must not contain individual-file download lists")
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    file_names = {path.relative_to(DOCS_DIR).as_posix() for path in DOCS_DIR.rglob("*") if path.is_file()}
    mkdocs_path = BOOK_DIR / "mkdocs.yml"
    if not mkdocs_path.exists():
        return ["Missing book/mkdocs.yml"]

    config = yaml.load(read_text(mkdocs_path), Loader=yaml.UnsafeLoader)
    if config.get("theme", {}).get("palette", {}).get("primary") != "blue":
        errors.append("MkDocs theme primary palette must be blue")
    extra_css = config.get("extra_css") or []
    if "stylesheets/blue-white.css" not in extra_css:
        errors.append("Missing blue-white stylesheet in extra_css")

    outline_files = list(BOOK_DIR.rglob("本章大纲.md"))
    if outline_files:
        errors.append("Outline files must not be copied into book/: " + ", ".join(map(str, outline_files)))

    try:
        approved = public_assets()
        expected = {dest.resolve() for _, dest in approved}
        actual = {path.resolve() for path in (DOCS_DIR / "assets").rglob("*") if path.is_file()}
        for extra in actual - expected:
            errors.append(f"Unlisted published asset: {extra}")
        for source, dest in approved:
            if not dest.is_file():
                errors.append(f"Missing approved asset: {dest}")
            elif source.read_bytes() != dest.read_bytes():
                errors.append(f"Published asset differs from reviewed source: {dest}")
        errors.extend(validate_practice_archives(approved))
    except (ValueError, FileNotFoundError, KeyError) as exc:
        errors.append(str(exc))

    index_path = DOCS_DIR / "index.md"
    if not index_path.exists():
        errors.append("Missing book/docs/index.md")
    else:
        index_text = read_text(index_path)
        for banned in BANNED_CONTENT:
            if banned in index_text:
                errors.append(f"{index_path}: banned content found: {banned}")

    for published_file in DOCS_DIR.rglob("*"):
        if not published_file.is_file():
            continue
        if published_file.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".zip"}:
            continue
        try:
            published_text = read_text(published_file)
        except UnicodeDecodeError:
            continue
        for banned in BANNED_CONTENT:
            if banned in published_text:
                errors.append(f"{published_file}: banned content found: {banned}")

    for chapter_number in range(1, CHAPTER_COUNT + 1):
        chapter_id = f"chapter-{chapter_number:02d}"
        source_path = CHAPTERS_DIR / chapter_id / "正文.md"
        out_path = DOCS_DIR / "chapters" / f"{chapter_id}.md"
        if not source_path.exists():
            errors.append(f"Missing source chapter: {source_path}")
            continue
        if not out_path.exists():
            errors.append(f"Missing published chapter: {out_path}")
            continue

        source_title = first_heading(read_text(source_path))
        out_text = read_text(out_path)
        if out_text != render_chapter(chapter_number)[2]:
            errors.append(f"{out_path}: published text differs from current chapter source")
        if first_heading(out_text) != source_title:
            errors.append(f"{out_path}: published title does not match source title")

        for banned in BANNED_CONTENT:
            if banned in out_text:
                errors.append(f"{out_path}: banned content found: {banned}")

        for href in local_links(out_text):
            target = (out_path.parent / href).resolve()
            try:
                target.relative_to(DOCS_DIR.resolve())
            except ValueError:
                errors.append(f"{out_path}: local link escapes docs dir: {href}")
                continue
            if not target.exists():
                errors.append(f"{out_path}: missing local link target: {href}")
            elif target.relative_to(DOCS_DIR.resolve()).as_posix() not in file_names:
                errors.append(f"{out_path}: link case differs from published filename: {href}")

    for page in (DOCS_DIR / "index.md", DOCS_DIR / "resources.md"):
        if not page.is_file():
            errors.append(f"Missing student entry page: {page}")
            continue
        if page.name == "resources.md":
            errors.extend(validate_resource_cards(read_text(page)))
        for href in local_links(read_text(page)):
            target = (page.parent / href).resolve()
            if DOCS_DIR.resolve() not in target.parents or not target.is_file():
                errors.append(f"{page}: invalid local link: {href}")
    for file in DOCS_DIR.rglob("*"):
        if file.is_file() and file.suffix.lower() in {".pdf", ".mp4", ".ppt", ".pptx", ".zip", ".rar", ".html"}:
            if file.parent == DOWNLOADS_DIR and re.fullmatch(r"chapter-(?:0[1-9]|1[0-2])\.zip", file.name):
                continue  # Only generated chapter archives pass the member checks above.
            errors.append(f"Course archives or embedded HTML may not publish: {file}")

    css_path = DOCS_DIR / "stylesheets" / "blue-white.css"
    if not css_path.exists():
        errors.append("Missing blue-white CSS file")
    else:
        css = read_text(css_path)
        for color in ("#ffffff", "#0b5ed7", "#eff6ff"):
            if color not in css:
                errors.append(f"blue-white CSS missing expected color {color}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Online book validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
