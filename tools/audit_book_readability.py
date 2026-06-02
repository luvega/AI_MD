#!/usr/bin/env python3
"""Audit readability-oriented prose coverage in AI_MD online book chapters."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path


CHAPTER_PATTERN = "chapter-*.md"
PRIORITY_SECTIONS = [
    "本章导读",
    "核心概念",
    "方法流程",
    "使用边界与常见误读",
    "延伸阅读与下一步",
]
OVERCLAIM_TERMS = [
    "突破性",
    "革命性",
    "颠覆性",
    "决定性",
    "最佳",
    "全面揭示",
    "彻底阐明",
    "广泛适用",
    "普遍机制",
]

FENCED_BLOCK_RE = re.compile(r"(?ms)^```.*?^```")
REF_BLOCK_RE = re.compile(r"(?ms)<!-- refs:start -->.*?<!-- refs:end -->")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)(?:\{[^}]*\})?")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
SECTION_RE = re.compile(r"(?ms)^##\s+(.+?)\s*\n(.*?)(?=^##\s+|\Z)")
SENTENCE_RE = re.compile(r"[^。！？!?]+[。！？!?]")


@dataclass
class ChapterReadability:
    chapter: str
    prose_chars: int
    table_lines: int
    list_lines: int
    priority_section_chars: dict[str, int]
    overclaim_terms: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit AI_MD online book readability coverage.")
    parser.add_argument("--book-root", required=True, help="Path to book/docs.")
    parser.add_argument(
        "--min-prose-chars-per-chapter",
        type=int,
        default=0,
        help="Minimum prose characters per chapter after excluding refs, code, tables, lists, and image links.",
    )
    parser.add_argument(
        "--min-priority-section-chars",
        type=int,
        default=0,
        help="Minimum prose characters for each priority teaching section.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON payload.")
    return parser.parse_args()


def strip_protected(text: str) -> str:
    text = REF_BLOCK_RE.sub("", text)
    text = FENCED_BLOCK_RE.sub("", text)
    text = IMAGE_RE.sub("", text)
    text = LINK_RE.sub(r"\1", text)
    return text


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def is_list_line(line: str) -> bool:
    stripped = line.strip()
    return bool(re.match(r"^(-|\*|\+)\s+", stripped) or re.match(r"^\d+\.\s+", stripped))


def prose_lines(markdown: str) -> list[str]:
    text = strip_protected(markdown)
    prose_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("!!!") or stripped.startswith("==="):
            continue
        if is_table_line(stripped) or is_list_line(stripped):
            continue
        prose_lines.append(stripped)
    return prose_lines


def prose_char_count(markdown: str) -> int:
    lines = prose_lines(markdown)
    prose = re.sub(r"\s+", "", "".join(lines))
    return len(prose)


def split_sections(markdown: str) -> dict[str, str]:
    return {heading.strip(): body for heading, body in SECTION_RE.findall(markdown)}


def table_line_count(markdown: str) -> int:
    return sum(1 for line in strip_protected(markdown).splitlines() if is_table_line(line))


def list_line_count(markdown: str) -> int:
    return sum(1 for line in strip_protected(markdown).splitlines() if is_list_line(line))


def overclaim_hits(markdown: str) -> list[str]:
    text = strip_protected(markdown)
    hits = sorted({term for term in OVERCLAIM_TERMS if term in text})
    for match in re.finditer("证明", text):
        context = text[max(0, match.start() - 14) : match.end() + 14]
        if not any(token in context for token in ("不能", "不等于", "不写成", "不应", "除非")):
            hits.append(f"证明:{context}")
    return hits


def repeated_sentences(chapter_texts: dict[str, str]) -> dict[str, list[str]]:
    sentence_sources: dict[str, set[str]] = defaultdict(set)
    for chapter, text in chapter_texts.items():
        clean = "\n".join(prose_lines(text))
        for sentence in SENTENCE_RE.findall(clean):
            normalized = re.sub(r"\s+", "", sentence)
            if len(normalized) >= 24:
                sentence_sources[normalized].add(chapter)
    repeated = {
        sentence: sorted(sources)
        for sentence, sources in sentence_sources.items()
        if len(sources) >= 4
    }
    return dict(sorted(repeated.items(), key=lambda item: (-len(item[1]), item[0])))


def audit_chapter(path: Path) -> ChapterReadability:
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    priority_counts = {
        section: prose_char_count(sections.get(section, ""))
        for section in PRIORITY_SECTIONS
    }
    return ChapterReadability(
        chapter=path.name,
        prose_chars=prose_char_count(text),
        table_lines=table_line_count(text),
        list_lines=list_line_count(text),
        priority_section_chars=priority_counts,
        overclaim_terms=overclaim_hits(text),
    )


def build_payload(book_root: Path) -> dict[str, object]:
    chapter_root = book_root / "chapters"
    chapters = [audit_chapter(path) for path in sorted(chapter_root.glob(CHAPTER_PATTERN))]
    chapter_texts = {path.name: path.read_text(encoding="utf-8") for path in sorted(chapter_root.glob(CHAPTER_PATTERN))}
    prose_values = [chapter.prose_chars for chapter in chapters]
    priority_values = [
        count
        for chapter in chapters
        for count in chapter.priority_section_chars.values()
    ]
    return {
        "book_root": str(book_root),
        "chapter_count": len(chapters),
        "min_prose_chars": min(prose_values) if prose_values else 0,
        "avg_prose_chars": round(sum(prose_values) / len(prose_values), 1) if prose_values else 0,
        "min_priority_section_chars": min(priority_values) if priority_values else 0,
        "chapters": [asdict(chapter) for chapter in chapters],
        "repeated_sentences": repeated_sentences(chapter_texts),
    }


def validate_payload(
    payload: dict[str, object],
    min_prose_chars_per_chapter: int,
    min_priority_section_chars: int,
) -> list[str]:
    errors: list[str] = []
    for chapter in payload["chapters"]:  # type: ignore[index]
        chapter_name = chapter["chapter"]  # type: ignore[index]
        prose_chars = chapter["prose_chars"]  # type: ignore[index]
        if prose_chars < min_prose_chars_per_chapter:
            errors.append(f"chapter prose too short: {chapter_name}: {prose_chars} < {min_prose_chars_per_chapter}")
        for section, count in chapter["priority_section_chars"].items():  # type: ignore[index, union-attr]
            if count < min_priority_section_chars:
                errors.append(f"priority section too short: {chapter_name}: {section}: {count} < {min_priority_section_chars}")
    return errors


def print_text_report(payload: dict[str, object], errors: list[str]) -> None:
    print(f"checked book root: {payload['book_root']}")
    print(f"chapters: {payload['chapter_count']}")
    print(f"min prose chars: {payload['min_prose_chars']}")
    print(f"avg prose chars: {payload['avg_prose_chars']}")
    print(f"min priority section chars: {payload['min_priority_section_chars']}")
    for chapter in payload["chapters"]:  # type: ignore[index]
        overclaims = chapter["overclaim_terms"]  # type: ignore[index]
        if overclaims:
            print(f"overclaim terms: {chapter['chapter']}: {', '.join(overclaims)}")
    repeated = payload["repeated_sentences"]  # type: ignore[index]
    if repeated:
        print(f"repeated sentences across >=4 chapters: {len(repeated)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(error)


def main() -> int:
    args = parse_args()
    book_root = Path(args.book_root).resolve()
    payload = build_payload(book_root)
    errors = validate_payload(payload, args.min_prose_chars_per_chapter, args.min_priority_section_chars)
    if args.json:
        print(json.dumps({"payload": payload, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        print_text_report(payload, errors)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
