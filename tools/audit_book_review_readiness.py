#!/usr/bin/env python3
"""Audit reviewer-facing quality gates for the AI_MD online book."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


CHAPTER_PATTERN = "chapter-*.md"
FORBIDDEN_TEMPLATE_PHRASES = [
    "关键问题不是单个命令或界面能够解决",
    "如果明天需要把这一步交给同组同学复核",
    "不是孤立的工具说明，而是后续章节继续工作的接口层",
    "边界判断并不是削弱",
    "完成这种转换后",
]

CASE_WALKTHROUGH_REQUIREMENTS = {
    "chapter-03.md": ["### 案例走读", "receptor", "ligand", "box", "shortlist"],
    "chapter-05.md": ["### 案例走读", "predicted affinity", "confidence", "校准"],
    "chapter-06.md": ["### 案例走读", "motif", "contig", "seed", "回折叠"],
    "chapter-08.md": ["### 案例走读", "claim-evidence-boundary", "文献案例", "项目池"],
}

HIGH_RISK_BOUNDARY_REQUIREMENTS = {
    "chapter-03.md": ["docking score", "不能写成", "Kd", "IC50"],
    "chapter-05.md": ["predicted affinity", "不能写成", "实验"],
    "chapter-06.md": ["RFdiffusion/RFD3", "不能写成", "成功 binder"],
    "chapter-08.md": ["Chai-1 aggregate score", "文献案例", "不能写成"],
}

CHAPTER_TERMS = {
    "chapter-01.md": ["环境", "路径", "日志", "实验记录"],
    "chapter-02.md": ["结构来源", "链", "配体", "口袋"],
    "chapter-03.md": ["受体", "配体库", "box", "pose"],
    "chapter-04.md": ["轨迹", "RMSD", "RMSF", "代表构象"],
    "chapter-05.md": ["predicted affinity", "confidence", "校准", "排序"],
    "chapter-06.md": ["RFdiffusion/RFD3", "ProteinMPNN", "回折叠", "界面"],
    "chapter-07.md": ["brief", "执行日志", "验收", "沉淀"],
    "chapter-08.md": ["研究问题", "文献案例", "claim-evidence-boundary", "项目池"],
}

SECTION_RE = re.compile(r"(?ms)^##\s+(.+?)\s*\n(.*?)(?=^##\s+|\Z)")


@dataclass
class ChapterReviewAudit:
    chapter: str
    forbidden_template_hits: list[str]
    missing_terms: list[str]
    has_literature_use_note: bool
    missing_case_walkthrough_tokens: list[str]
    missing_high_risk_boundary_tokens: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit P39 reviewer-facing book quality gates.")
    parser.add_argument("--book-root", required=True, help="Path to book/docs.")
    parser.add_argument("--json", action="store_true", help="Print JSON payload.")
    return parser.parse_args()


def split_sections(markdown: str) -> dict[str, str]:
    return {heading.strip(): body for heading, body in SECTION_RE.findall(markdown)}


def audit_chapter(path: Path) -> ChapterReviewAudit:
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    key_lit = sections.get("关键文献", "")
    expected_terms = CHAPTER_TERMS.get(path.name, [])
    case_tokens = CASE_WALKTHROUGH_REQUIREMENTS.get(path.name, [])
    risk_tokens = HIGH_RISK_BOUNDARY_REQUIREMENTS.get(path.name, [])
    return ChapterReviewAudit(
        chapter=path.name,
        forbidden_template_hits=[phrase for phrase in FORBIDDEN_TEMPLATE_PHRASES if phrase in text],
        missing_terms=[term for term in expected_terms if term not in text],
        has_literature_use_note="文献使用说明" in key_lit,
        missing_case_walkthrough_tokens=[token for token in case_tokens if token not in text],
        missing_high_risk_boundary_tokens=[token for token in risk_tokens if token not in text],
    )


def build_payload(book_root: Path) -> dict[str, object]:
    chapters = [
        audit_chapter(path)
        for path in sorted((book_root / "chapters").glob(CHAPTER_PATTERN))
    ]
    report_files_in_book = sorted(
        path.relative_to(book_root).as_posix()
        for path in (book_root / "resources").glob("*report*.md")
    )
    return {
        "book_root": str(book_root),
        "chapter_count": len(chapters),
        "chapters": [asdict(chapter) for chapter in chapters],
        "report_files_in_book_resources": report_files_in_book,
    }


def validate_payload(payload: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for chapter in payload["chapters"]:  # type: ignore[index]
        name = chapter["chapter"]  # type: ignore[index]
        if chapter["forbidden_template_hits"]:  # type: ignore[index]
            errors.append(f"forbidden template phrase: {name}: {chapter['forbidden_template_hits']}")
        if chapter["missing_terms"]:  # type: ignore[index]
            errors.append(f"missing chapter-specific terms: {name}: {chapter['missing_terms']}")
        if not chapter["has_literature_use_note"]:  # type: ignore[index]
            errors.append(f"missing literature use note: {name}")
        if chapter["missing_case_walkthrough_tokens"]:  # type: ignore[index]
            errors.append(f"missing case walkthrough tokens: {name}: {chapter['missing_case_walkthrough_tokens']}")
        if chapter["missing_high_risk_boundary_tokens"]:  # type: ignore[index]
            errors.append(f"missing high-risk boundary tokens: {name}: {chapter['missing_high_risk_boundary_tokens']}")
    if payload["report_files_in_book_resources"]:  # type: ignore[index]
        errors.append(f"stage reports must not be in book resources: {payload['report_files_in_book_resources']}")
    return errors


def print_text_report(payload: dict[str, object], errors: list[str]) -> None:
    print(f"checked book root: {payload['book_root']}")
    print(f"chapters: {payload['chapter_count']}")
    print(f"report files in book resources: {len(payload['report_files_in_book_resources'])}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(error)


def main() -> int:
    args = parse_args()
    payload = build_payload(Path(args.book_root).resolve())
    errors = validate_payload(payload)
    if args.json:
        print(json.dumps({"payload": payload, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        print_text_report(payload, errors)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
