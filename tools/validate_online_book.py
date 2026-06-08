from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
DOCS_DIR = BOOK_DIR / "docs"
CHAPTERS_DIR = ROOT / "chapters"
CHAPTER_COUNT = 12

BANNED_CONTENT = (
    "本章大纲.md",
    "06_原始学习素材",
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


def validate() -> list[str]:
    errors: list[str] = []
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

    asset_markdown = list((DOCS_DIR / "assets").rglob("*.md"))
    if asset_markdown:
        errors.append("Markdown files under book/docs/assets are not part of the published text layer: " + ", ".join(map(str, asset_markdown)))

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
        if published_file.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf"}:
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
