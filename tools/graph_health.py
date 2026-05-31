#!/usr/bin/env python3
"""Diagnostic health checks for the AI_MD LLM Wiki graph layer."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".obsidian",
    ".pytest_cache",
    "__pycache__",
    "06_原始学习素材",
}

PLACEHOLDER_KEYS = {"", "-", "na", "n/a", "none", "null", "待补", "待确认", "待补正式锚点"}


@dataclass
class Page:
    path: Path
    rel_path: str
    frontmatter: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check LLM Wiki graph health.")
    parser.add_argument("root", nargs="?", default=".", help="Wiki root directory.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--stale-days", type=int, default=180, help="Days after last_reviewed before a page is stale.")
    parser.add_argument("--include-raw", action="store_true", help="Include 06_原始学习素材 in Markdown scans.")
    parser.add_argument("--as-of", default=None, help="Reference date in YYYY-MM-DD form. Defaults to today.")
    return parser.parse_args()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [strip_quotes(part.strip()) for part in split_inline_list(inner)]
    return strip_quotes(value)


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def split_inline_list(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    for char in value:
        if char in {'"', "'"}:
            quote = None if quote == char else char if quote is None else quote
        if char == "," and quote is None:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return parts


def parse_block_list(lines: list[str]) -> Any:
    if not lines:
        return []
    relations: list[dict[str, str]] = []
    simple_items: list[str] = []
    current: dict[str, str] | None = None
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if ":" in item and not item.startswith(('"', "'")):
                key, value = item.split(":", 1)
                current = {key.strip(): strip_quotes(value.strip())}
                relations.append(current)
            else:
                current = None
                simple_items.append(strip_quotes(item))
            continue
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = strip_quotes(value.strip())
    if relations:
        return relations
    return simple_items


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, flags=re.DOTALL)
    if not match:
        return {}
    frontmatter = match.group(1)
    lines = frontmatter.splitlines()
    data: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "\t", "- ")):
            i += 1
            continue
        if ":" not in raw:
            i += 1
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = parse_scalar(value)
            i += 1
            continue
        block: list[str] = []
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if next_line and not next_line.startswith((" ", "\t", "-")) and ":" in next_line:
                break
            block.append(next_line)
            i += 1
        data[key] = parse_block_list(block)
    return data


def should_skip(path: Path, root: Path, excluded_dirs: set[str]) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in excluded_dirs for part in rel_parts)


def iter_markdown(root: Path, include_raw: bool) -> list[Path]:
    excluded = set(DEFAULT_EXCLUDED_DIRS)
    if include_raw:
        excluded.discard("06_原始学习素材")
    return sorted(path for path in root.rglob("*.md") if not should_skip(path, root, excluded))


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def listify(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [] if value.strip() in {"", "[]"} else [value]
    return [value]


def clean_key(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().strip('"').strip("'")


def is_real_key(value: Any) -> bool:
    key = clean_key(value)
    return key.lower() not in PLACEHOLDER_KEYS and not key.startswith("待")


def parse_date(value: Any) -> date | None:
    text = clean_key(value)
    if not text:
        return None
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def load_pages(root: Path, include_raw: bool) -> tuple[list[Path], list[Page]]:
    markdown_files = iter_markdown(root, include_raw)
    pages: list[Page] = []
    for path in markdown_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        frontmatter = parse_frontmatter(text)
        if frontmatter:
            pages.append(Page(path=path, rel_path=rel(path, root), frontmatter=frontmatter))
    return markdown_files, pages


def normalize_target(source: Page, target: str, root: Path) -> str | None:
    if not target or "://" in target:
        return None
    target = target.split("#", 1)[0]
    if not target.endswith(".md"):
        return None
    target_path = (source.path.parent / target).resolve()
    try:
        return target_path.relative_to(root).as_posix()
    except ValueError:
        return None


def graph_signals(root: Path, pages: list[Page]) -> tuple[Counter[str], dict[str, set[str]], dict[str, set[str]]]:
    relation_types: Counter[str] = Counter()
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)
    page_paths = {page.rel_path for page in pages}

    for page in pages:
        relations = [item for item in listify(page.frontmatter.get("relations")) if isinstance(item, dict)]
        for relation in relations:
            relation_type = clean_key(relation.get("type"))
            if relation_type:
                relation_types[relation_type] += 1
            normalized = normalize_target(page, clean_key(relation.get("target")), root)
            if normalized:
                outgoing[page.rel_path].add(normalized)
                if normalized in page_paths:
                    incoming[normalized].add(page.rel_path)
        for related in listify(page.frontmatter.get("related")):
            normalized = normalize_target(page, clean_key(related), root)
            if normalized:
                outgoing[page.rel_path].add(normalized)
                if normalized in page_paths:
                    incoming[normalized].add(page.rel_path)

    return relation_types, outgoing, incoming


def load_bib_keys(root: Path) -> set[str]:
    bib_path = root / "references" / "references.bib"
    if not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", text))


def load_zotero_rows(root: Path) -> list[dict[str, str]]:
    zmap = root / "references" / "zotero-map.tsv"
    if not zmap.exists():
        return []
    with zmap.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        if "\t" not in sample:
            return []
        reader = csv.DictReader(handle, delimiter="\t")
        rows = []
        for row in reader:
            if row and any((value or "").strip() for value in row.values()):
                rows.append({(key or "").strip(): (value or "").strip() for key, value in row.items()})
    return rows


def bibtex_key_from_row(row: dict[str, str]) -> str:
    candidates = [
        "bibtex_key",
        "bibtex",
        "BibTeX key",
        "BibTeX",
        "citation_key",
        "key",
    ]
    lower_map = {key.lower(): value for key, value in row.items()}
    for candidate in candidates:
        if candidate in row:
            return clean_key(row[candidate])
        if candidate.lower() in lower_map:
            return clean_key(lower_map[candidate.lower()])
    values = list(row.values())
    return clean_key(values[1]) if len(values) > 1 else ""


def count_entities(root: Path) -> int:
    entity_index = root / "07_研究工作台" / "实体索引.md"
    if not entity_index.exists():
        return 0
    text = entity_index.read_text(encoding="utf-8", errors="replace")
    count = 0
    for line in text.splitlines():
        if re.match(r"^\|\s*`[^`]+:[^`]+`\s*\|", line):
            count += 1
    return count


def build_report(root: Path, include_raw: bool, stale_days: int, as_of: date) -> dict[str, Any]:
    markdown_files, pages = load_pages(root, include_raw)
    page_paths = {page.rel_path for page in pages}
    relation_types, outgoing, incoming = graph_signals(root, pages)

    stale_pages = []
    missing_last_reviewed = []
    for page in pages:
        reviewed = parse_date(page.frontmatter.get("last_reviewed"))
        if reviewed is None:
            missing_last_reviewed.append({"path": page.rel_path})
            continue
        age = (as_of - reviewed).days
        if age > stale_days:
            stale_pages.append({"path": page.rel_path, "last_reviewed": reviewed.isoformat(), "age_days": age})

    isolated_pages = []
    for page in pages:
        if not outgoing.get(page.rel_path) and not incoming.get(page.rel_path):
            isolated_pages.append({"path": page.rel_path, "title": clean_key(page.frontmatter.get("title"))})

    literature_missing_keys = []
    for page in pages:
        if clean_key(page.frontmatter.get("type")) != "literature-note":
            continue
        zotero_keys = [item for item in listify(page.frontmatter.get("zotero_items")) if is_real_key(item)]
        bibtex_keys = [item for item in listify(page.frontmatter.get("bibtex_keys")) if is_real_key(item)]
        if not zotero_keys or not bibtex_keys:
            literature_missing_keys.append({"path": page.rel_path, "zotero_items": zotero_keys, "bibtex_keys": bibtex_keys})

    bib_keys = load_bib_keys(root)
    zmap_rows = load_zotero_rows(root)
    missing_bib = []
    for row in zmap_rows:
        bibtex_key = bibtex_key_from_row(row)
        if is_real_key(bibtex_key) and bibtex_key not in bib_keys:
            missing_bib.append(
                {
                    "bibtex_key": bibtex_key,
                    "zotero_item_key": row.get("zotero_item_key") or row.get("item_key") or row.get("zotero_key") or "",
                    "title": row.get("title") or row.get("Title") or "",
                }
            )

    relation_targets_missing = []
    for page in pages:
        for relation in [item for item in listify(page.frontmatter.get("relations")) if isinstance(item, dict)]:
            target = clean_key(relation.get("target"))
            normalized = normalize_target(page, target, root)
            if normalized and normalized not in page_paths and not (root / normalized).exists():
                relation_targets_missing.append({"path": page.rel_path, "target": target})

    issues = {
        "stale_pages": sorted(stale_pages, key=lambda item: (-item["age_days"], item["path"])),
        "missing_last_reviewed": sorted(missing_last_reviewed, key=lambda item: item["path"]),
        "isolated_pages": sorted(isolated_pages, key=lambda item: item["path"]),
        "zotero_keys_missing_in_bib": sorted(missing_bib, key=lambda item: item["bibtex_key"]),
        "literature_pages_missing_zotero_or_bibtex": sorted(literature_missing_keys, key=lambda item: item["path"]),
        "relation_targets_missing": sorted(relation_targets_missing, key=lambda item: (item["path"], item["target"])),
    }

    recommendations = []
    if issues["zotero_keys_missing_in_bib"]:
        recommendations.append("补齐 references.bib 中缺失的 BibTeX key，或从 zotero-map.tsv 移出未正式提升条目。")
    if issues["literature_pages_missing_zotero_or_bibtex"]:
        recommendations.append("文献笔记应同时记录 Zotero item key 和 BibTeX key；未确认时写入候选表。")
    if issues["stale_pages"]:
        recommendations.append("优先复核过期页面的 last_reviewed，尤其是方法卡、claims 和实验模板。")
    if issues["isolated_pages"]:
        recommendations.append("为孤立页面补 related 或 typed relations，或确认其是否应归档。")
    if not recommendations:
        recommendations.append("图谱体检未发现优先级较高的结构问题。")

    summary = {
        "root": str(root),
        "markdown_files": len(markdown_files),
        "frontmatter_pages": len(pages),
        "entity_count": count_entities(root),
        "typed_relations": sum(relation_types.values()),
        "pages_with_relations_or_related": sum(1 for page in pages if outgoing.get(page.rel_path)),
        "isolated_pages": len(issues["isolated_pages"]),
        "stale_pages": len(issues["stale_pages"]),
        "missing_last_reviewed": len(issues["missing_last_reviewed"]),
        "zotero_rows": len(zmap_rows),
        "bibtex_entries": len(bib_keys),
        "zotero_keys_missing_in_bib": len(issues["zotero_keys_missing_in_bib"]),
        "literature_pages_missing_zotero_or_bibtex": len(issues["literature_pages_missing_zotero_or_bibtex"]),
        "relation_targets_missing": len(issues["relation_targets_missing"]),
        "as_of": as_of.isoformat(),
        "stale_days": stale_days,
    }

    return {
        "summary": summary,
        "relation_types": dict(sorted(relation_types.items())),
        "issues": issues,
        "recommendations": recommendations,
    }


def print_text_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print("AI_MD graph health")
    print("==================")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print()
    print("relation_types:")
    if report["relation_types"]:
        for key, value in report["relation_types"].items():
            print(f"- {key}: {value}")
    else:
        print("- none")
    print()
    print("recommendations:")
    for item in report["recommendations"]:
        print(f"- {item}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date() if args.as_of else date.today()
    report = build_report(root=root, include_raw=args.include_raw, stale_days=args.stale_days, as_of=as_of)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
