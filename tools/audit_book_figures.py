#!/usr/bin/env python3
"""Audit publication-style figure numbering and captions in AI_MD online book."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]*)\)(?P<attrs>\{[^}]*\})?")
CAPTION_RE = re.compile(r"^\*\*图(?P<chapter>\d+)\.(?P<number>\d+)\s+(?P<title>[^。]+)。\*\*(?P<body>.*)$")
BOUNDARY_TOKENS = [
    "教学示意图",
    "截图",
    "dry-run",
    "不代表实验结果",
    "不承载",
    "不替代",
    "以正文为准",
]


@dataclass
class FigureRecord:
    chapter_file: str
    figure_no: str
    kind: str
    line: int
    caption_line: int | None
    caption_chars: int
    title: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit AI_MD online book figure captions.")
    parser.add_argument("--book-root", required=True, help="Path to book/docs.")
    parser.add_argument("--min-caption-chars", type=int, default=80)
    parser.add_argument("--min-figures-per-chapter", type=int, default=0)
    parser.add_argument("--json", action="store_true", help="Print JSON payload.")
    return parser.parse_args()


def clean_caption(text: str) -> str:
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\[[^\]]+\]\([^)]*\)", "", text)
    return re.sub(r"\s+", "", text)


def next_nonempty_line(lines: list[str], start_index: int) -> tuple[int | None, str | None]:
    for idx in range(start_index, len(lines)):
        if lines[idx].strip():
            return idx, lines[idx].strip()
    return None, None


def find_figures(lines: list[str]) -> list[tuple[str, int, str | None]]:
    figures: list[tuple[str, int, str | None]] = []
    in_mermaid = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            continue
        if in_mermaid and stripped == "```":
            figures.append(("mermaid", idx, None))
            in_mermaid = False
            continue
        if not in_mermaid:
            match = IMAGE_RE.search(stripped)
            if match:
                figures.append(("image", idx, match.group("alt")))
    return figures


def chapter_number_from_path(path: Path) -> int | None:
    match = re.search(r"chapter-(\d+)\.md$", path.name)
    return int(match.group(1)) if match else None


def audit_chapter(path: Path, min_caption_chars: int, min_figures: int) -> tuple[list[FigureRecord], list[str]]:
    chapter_no = chapter_number_from_path(path)
    if chapter_no is None:
        return [], [f"invalid chapter filename: {path.name}"]
    lines = path.read_text(encoding="utf-8").splitlines()
    figures = find_figures(lines)
    records: list[FigureRecord] = []
    errors: list[str] = []
    if min_figures and len(figures) < min_figures:
        errors.append(f"too few figures: {path.name}: {len(figures)} < {min_figures}")
    for expected_no, (kind, fig_idx, alt) in enumerate(figures, start=1):
        figure_no = f"图{chapter_no}.{expected_no}"
        caption_idx, caption = next_nonempty_line(lines, fig_idx + 1)
        if caption_idx is None or caption is None:
            errors.append(f"missing caption: {path.name}: {figure_no}: line {fig_idx + 1}")
            continue
        match = CAPTION_RE.match(caption)
        if not match:
            errors.append(f"invalid caption format: {path.name}: expected {figure_no}: line {caption_idx + 1}")
            continue
        actual_no = f"图{match.group('chapter')}.{match.group('number')}"
        if actual_no != figure_no:
            errors.append(f"figure number mismatch: {path.name}: expected {figure_no}, got {actual_no}")
        caption_chars = len(clean_caption(caption))
        if caption_chars < min_caption_chars:
            errors.append(
                f"caption too short: {path.name}: {figure_no}: {caption_chars} < {min_caption_chars}"
            )
        if not any(token in caption for token in BOUNDARY_TOKENS):
            errors.append(f"caption lacks source/boundary token: {path.name}: {figure_no}")
        if kind == "image" and alt and figure_no not in alt:
            errors.append(f"image alt missing figure number: {path.name}: {figure_no}: line {fig_idx + 1}")
        records.append(
            FigureRecord(
                chapter_file=path.name,
                figure_no=figure_no,
                kind=kind,
                line=fig_idx + 1,
                caption_line=caption_idx + 1,
                caption_chars=caption_chars,
                title=match.group("title") if match else "",
            )
        )
    return records, errors


def find_nonchapter_images(book_root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(book_root.rglob("*.md")):
        if path.parent.name == "chapters" and re.match(r"chapter-\d+\.md$", path.name):
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if IMAGE_RE.search(line):
                rel = path.relative_to(book_root).as_posix()
                errors.append(f"image outside chapter figure flow: {rel}: line {line_no}")
    return errors


def build_payload(book_root: Path, min_caption_chars: int, min_figures: int) -> dict[str, object]:
    chapter_root = book_root / "chapters"
    all_records: list[FigureRecord] = []
    errors: list[str] = []
    for path in sorted(chapter_root.glob("chapter-*.md")):
        records, chapter_errors = audit_chapter(path, min_caption_chars, min_figures)
        all_records.extend(records)
        errors.extend(chapter_errors)
    errors.extend(find_nonchapter_images(book_root))
    return {
        "book_root": str(book_root),
        "chapters": len(list(chapter_root.glob("chapter-*.md"))),
        "figures": [asdict(record) for record in all_records],
        "figure_count": len(all_records),
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    book_root = Path(args.book_root).resolve()
    payload = build_payload(book_root, args.min_caption_chars, args.min_figures_per_chapter)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"checked book root: {book_root}")
        print(f"chapters: {payload['chapters']}")
        print(f"figures: {payload['figure_count']}")
        print(f"errors: {len(payload['errors'])}")
        for error in payload["errors"]:
            print(f"- {error}")
    return 1 if payload["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
