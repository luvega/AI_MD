#!/usr/bin/env python3
"""Validate the AI_MD MkDocs online book skeleton."""

from __future__ import annotations

import argparse
import csv
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
    "代码案例与软件操作",
    "关键文献",
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
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
BIBTEX_ENTRY_PATTERN = re.compile(r"@\w+\s*\{\s*([^,\s]+)")
FENCED_CODE_PATTERN = re.compile(r"^\s*```", re.MULTILINE)
REFS_SECTION_PATTERN = re.compile(r"(?ms)^##\s+关键文献(?:与 BibTeX key)?\s*\n(?P<body>.*?)(?=^## |\Z)")


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
    parser.add_argument(
        "--require-nature-refs",
        action="store_true",
        help="Require refs:start/refs:end blocks and Nature-style reference entries inside the reference section.",
    )
    parser.add_argument(
        "--require-imagegen",
        action="store_true",
        help="Require chapter Imagegen knowledge maps and a resources/imagegen-manifest.tsv.",
    )
    parser.add_argument(
        "--require-mermaid",
        action="store_true",
        help="Require each chapter to include a Mermaid diagram with accTitle and accDescr.",
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
    require_nature_refs: bool = False,
    require_imagegen: bool = False,
    imagegen_files: set[str] | None = None,
    require_mermaid: bool = False,
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
    if not FENCED_CODE_PATTERN.search(text):
        issues.append(Issue("missing fenced code block", page, "each chapter must include at least one copyable code block"))
    if "assets/screenshots/" not in text:
        issues.append(Issue("missing screenshot", page, "代码案例与软件操作 must reference one screenshot asset"))

    if require_nature_refs:
        match = REFS_SECTION_PATTERN.search(text)
        if not match:
            issues.append(Issue("missing refs section", page, "关键文献"))
        else:
            refs_body = match.group("body")
            if "<!-- refs:start -->" not in refs_body or "<!-- refs:end -->" not in refs_body:
                issues.append(Issue("missing refs markers", page, "expected refs:start and refs:end"))
            if entry.get("required_bibtex_keys") and not re.search(r"(?m)^-\s+\S", refs_body):
                issues.append(Issue("missing reference list", page, "expected Markdown bullet reference entries"))
            if entry.get("required_bibtex_keys") and "本文内容简介" not in refs_body:
                issues.append(Issue("missing article summary", page, "本文内容简介"))
            for summary in re.findall(r"\*\*本文内容简介：\*\*\s*([^\n]+)", refs_body):
                if len(summary.strip()) > 100:
                    issues.append(Issue("article summary too long", page, f"{len(summary.strip())} > 100 characters"))

    if require_imagegen:
        images = [normalize_link_target(match.group(1)) for match in MARKDOWN_IMAGE_PATTERN.finditer(text)]
        knowledge_maps = [image for image in images if "assets/imagegen/" in image and "knowledge-map" in image]
        if not knowledge_maps:
            issues.append(Issue("missing Imagegen knowledge map", page, "expected assets/imagegen/*knowledge-map*"))
        for image in images:
            if "assets/imagegen/" not in image:
                continue
            candidate = (page_path.parent / image).resolve()
            try:
                rel = candidate.relative_to(book_root.resolve()).as_posix()
            except ValueError:
                rel = image
            if imagegen_files is not None and rel not in imagegen_files:
                issues.append(Issue("unregistered Imagegen asset", page, rel))

    if require_mermaid:
        mermaid_blocks = re.findall(r"(?ms)^\s*```mermaid\s*\n(.*?)^\s*```", text)
        if not mermaid_blocks:
            issues.append(Issue("missing Mermaid diagram", page, "expected at least one ```mermaid fenced block"))
        for block in mermaid_blocks:
            if "accTitle:" not in block or "accDescr:" not in block:
                issues.append(Issue("inaccessible Mermaid diagram", page, "expected accTitle and accDescr"))


def load_imagegen_manifest(book_root: Path, issues: list[Issue]) -> set[str]:
    manifest_path = book_root / "resources" / "imagegen-manifest.tsv"
    files: set[str] = set()
    if not manifest_path.exists():
        issues.append(Issue("missing Imagegen manifest", "resources/imagegen-manifest.tsv", "required by --require-imagegen"))
        return files
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        expected = {"id", "chapter", "type", "file", "prompt_ref", "source_basis", "alt_text", "status"}
        if not reader.fieldnames or not expected.issubset(set(reader.fieldnames)):
            issues.append(Issue("invalid Imagegen manifest", "resources/imagegen-manifest.tsv", "missing required columns"))
            return files
        for row in reader:
            file_value = (row.get("file") or "").strip()
            if not file_value:
                issues.append(Issue("invalid Imagegen manifest", "resources/imagegen-manifest.tsv", "empty file field"))
                continue
            files.add(file_value)
            if not (book_root / file_value).exists():
                issues.append(Issue("missing Imagegen asset", "resources/imagegen-manifest.tsv", file_value))
            if not (row.get("alt_text") or "").strip():
                issues.append(Issue("missing Imagegen alt text", "resources/imagegen-manifest.tsv", file_value))
    return files


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
        for pattern in (MARKDOWN_LINK_PATTERN, MARKDOWN_IMAGE_PATTERN):
            for match in pattern.finditer(text):
                check_one_markdown_target(book_root, path, rel_path, match.group(1), issues)


def check_one_markdown_target(book_root: Path, path: Path, rel_path: str, raw_target: str, issues: list[Issue]) -> None:
    target = normalize_link_target(raw_target)
    if not target or target.startswith("#") or is_external_link(target):
        return
    if target.startswith("/"):
        candidate = book_root / target.lstrip("/")
    else:
        candidate = path.parent / target
    if not candidate.exists():
        issues.append(Issue("broken internal link", rel_path, raw_target))


def validate(
    book_map_path: Path,
    book_root: Path,
    min_chapter_chars: int = 0,
    require_nature_refs: bool = False,
    require_imagegen: bool = False,
    require_mermaid: bool = False,
) -> list[Issue]:
    repo_root = book_map_path.resolve().parents[1]
    data = load_book_map(book_map_path)
    bibtex_keys = load_bibtex_keys(repo_root)
    issues: list[Issue] = []
    imagegen_files = load_imagegen_manifest(book_root, issues) if require_imagegen else None

    for entry in as_list(data.get("chapters")):
        if not isinstance(entry, dict):
            continue
        check_sources(entry, repo_root, issues)
        check_bibtex_keys(entry, bibtex_keys, issues)
        check_chapter_sections(
            entry,
            book_root,
            issues,
            min_chapter_chars=min_chapter_chars,
            require_nature_refs=require_nature_refs,
            require_imagegen=require_imagegen,
            imagegen_files=imagegen_files,
            require_mermaid=require_mermaid,
        )

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
    issues = validate(
        book_map_path,
        book_root,
        min_chapter_chars=args.min_chapter_chars,
        require_nature_refs=args.require_nature_refs,
        require_imagegen=args.require_imagegen,
        require_mermaid=args.require_mermaid,
    )
    print(f"checked map: {book_map_path}")
    print(f"checked book root: {book_root}")
    print(f"errors: {len(issues)}")
    for issue in issues:
        print(f"- {issue.format()}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
