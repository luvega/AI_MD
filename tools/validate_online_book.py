#!/usr/bin/env python3
"""Validate the AI_MD MkDocs online book skeleton."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_CHAPTER_SECTIONS = [
    "本章导读",
    "学习目标",
    "知识图谱入口",
    "核心概念",
    "方法流程",
    "关键文献与 BibTeX key",
    "实验/练习入口",
    "使用边界与常见误读",
    "延伸阅读与下一步",
]

SOURCE_LIST_FIELDS = [
    "method_sources",
    "literature_sources",
    "experiment_sources",
    "workbench_sources",
]

RAW_SOURCE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]*06_原始学习素材[^)]*)\)|\[[^\]]+\]\(([^)]*06_原始学习素材[^)]*)\)")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
BIBTEX_ENTRY_PATTERN = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


@dataclass
class Issue:
    kind: str
    path: str
    detail: str

    def format(self) -> str:
        return f"{self.kind}: {self.path}: {self.detail}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate AI_MD online book files.")
    parser.add_argument("--map", required=True, dest="map_path", help="Path to book_map.toml.")
    parser.add_argument("--book-root", required=True, help="Path to book/docs.")
    parser.add_argument(
        "--min-chapter-chars",
        type=int,
        default=0,
        help="Require each chapter Markdown file to contain at least this many characters.",
    )
    return parser.parse_args()


def load_book_map(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_bibtex_keys(repo_root: Path) -> set[str]:
    bib_path = repo_root / "references" / "references.bib"
    if not bib_path.exists():
        return set()
    return set(BIBTEX_ENTRY_PATTERN.findall(bib_path.read_text(encoding="utf-8", errors="replace")))


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return target


def is_external_link(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)) or target.startswith("mailto:")


def check_sources(entry: dict[str, Any], repo_root: Path, issues: list[Issue]) -> None:
    title = str(entry.get("title", "<untitled>"))
    source_fields = ["chapter_source", *SOURCE_LIST_FIELDS]
    for field in source_fields:
        values = as_list(entry.get(field))
        for value in values:
            if not value:
                continue
            source_path = repo_root / str(value)
            if not source_path.exists():
                issues.append(Issue("missing source path", title, f"{field} -> {value}"))


def check_bibtex_keys(entry: dict[str, Any], bibtex_keys: set[str], issues: list[Issue]) -> None:
    title = str(entry.get("title", "<untitled>"))
    for key in as_list(entry.get("required_bibtex_keys")):
        key = str(key).strip()
        if key and key not in bibtex_keys:
            issues.append(Issue("missing BibTeX key", title, key))


def check_chapter_sections(
    entry: dict[str, Any],
    book_root: Path,
    issues: list[Issue],
    min_chapter_chars: int = 0,
) -> None:
    page = str(entry.get("page", "")).strip()
    title = str(entry.get("title", "<untitled>"))
    if not page:
        issues.append(Issue("missing page", title, "chapter entry has no page field"))
        return
    page_path = book_root / page
    if not page_path.exists():
        issues.append(Issue("missing page", title, page))
        return
    text = page_path.read_text(encoding="utf-8", errors="replace")
    if min_chapter_chars > 0 and len(text) < min_chapter_chars:
        issues.append(Issue("chapter too short", page, f"{len(text)} < {min_chapter_chars} characters"))
    for section in REQUIRED_CHAPTER_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, flags=re.MULTILINE):
            issues.append(Issue("missing required section", page, section))


def iter_markdown_files(book_root: Path) -> list[Path]:
    return sorted(book_root.rglob("*.md"))


def check_raw_source_links(book_root: Path, issues: list[Issue]) -> None:
    for path in iter_markdown_files(book_root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in RAW_SOURCE_PATTERN.finditer(text):
            target = match.group(1) or match.group(2) or ""
            issues.append(Issue("raw source link", path.relative_to(book_root).as_posix(), target))


def check_internal_links(book_root: Path, issues: list[Issue]) -> None:
    for path in iter_markdown_files(book_root):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel_path = path.relative_to(book_root).as_posix()
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            target = normalize_link_target(match.group(1))
            if not target or target.startswith("#") or is_external_link(target):
                continue
            if target.startswith("/"):
                candidate = book_root / target.lstrip("/")
            else:
                candidate = path.parent / target
            if not candidate.exists():
                issues.append(Issue("broken internal link", rel_path, match.group(1)))


def validate(book_map_path: Path, book_root: Path, min_chapter_chars: int = 0) -> list[Issue]:
    repo_root = book_map_path.resolve().parents[1]
    data = load_book_map(book_map_path)
    bibtex_keys = load_bibtex_keys(repo_root)
    issues: list[Issue] = []

    for entry in as_list(data.get("chapters")):
        if not isinstance(entry, dict):
            continue
        check_sources(entry, repo_root, issues)
        check_bibtex_keys(entry, bibtex_keys, issues)
        check_chapter_sections(entry, book_root, issues, min_chapter_chars=min_chapter_chars)

    for entry in as_list(data.get("appendices")):
        if not isinstance(entry, dict):
            continue
        check_sources(entry, repo_root, issues)
        check_bibtex_keys(entry, bibtex_keys, issues)
        page = str(entry.get("page", "")).strip()
        if page and not (book_root / page).exists():
            issues.append(Issue("missing page", str(entry.get("title", "<untitled>")), page))

    check_raw_source_links(book_root, issues)
    check_internal_links(book_root, issues)
    return issues


def main() -> int:
    args = parse_args()
    book_map_path = Path(args.map_path).resolve()
    book_root = Path(args.book_root).resolve()
    issues = validate(book_map_path, book_root, min_chapter_chars=args.min_chapter_chars)
    print(f"checked map: {book_map_path}")
    print(f"checked book root: {book_root}")
    print(f"errors: {len(issues)}")
    for issue in issues:
        print(f"- {issue.format()}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
