#!/usr/bin/env python3
"""Update online book Nature-style reference sections from BibTeX and Zotero map."""

from __future__ import annotations

import argparse
import csv
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ENTRY_START_RE = re.compile(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,", re.IGNORECASE)
FIELD_RE = re.compile(r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*=\s*(?P<value>.+)")
REF_SECTION_RE = re.compile(
    r"(?ms)^## 关键文献与 BibTeX key\s*\n.*?(?=^## |\Z)",
)


@dataclass
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Nature-style references for the AI_MD online book.")
    parser.add_argument("--map", required=True, dest="map_path", help="Path to book_map.toml.")
    parser.add_argument("--book-root", required=True, help="Path to book/docs.")
    parser.add_argument("--references", required=True, help="Path to references.bib.")
    parser.add_argument("--zotero-map", required=True, help="Path to zotero-map.tsv.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    return parser.parse_args()


def strip_wrapping(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if len(value) >= 2 and ((value[0] == "{" and value[-1] == "}") or (value[0] == '"' and value[-1] == '"')):
        value = value[1:-1]
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    value = value.replace("{", "").replace("}", "")
    return value.strip()


def split_bibtex_entries(text: str) -> list[str]:
    entries: list[str] = []
    index = 0
    while True:
        start = text.find("@", index)
        if start == -1:
            break
        brace = text.find("{", start)
        if brace == -1:
            break
        depth = 0
        end = brace
        while end < len(text):
            char = text[end]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end += 1
                    break
            end += 1
        entries.append(text[start:end])
        index = end
    return entries


def parse_bibtex(path: Path) -> dict[str, BibEntry]:
    entries: dict[str, BibEntry] = {}
    text = path.read_text(encoding="utf-8", errors="replace")
    for raw_entry in split_bibtex_entries(text):
        start_match = ENTRY_START_RE.search(raw_entry)
        if not start_match:
            continue
        entry_type = start_match.group("type")
        key = start_match.group("key")
        body_start = start_match.end()
        body = raw_entry[body_start:].rstrip().removesuffix("}").strip()
        fields = parse_fields(body)
        entries[key] = BibEntry(entry_type=entry_type.lower(), key=key, fields=fields)
    return entries


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    index = 0
    while index < len(body):
        while index < len(body) and body[index] in " \t\r\n,":
            index += 1
        name_start = index
        while index < len(body) and re.match(r"[A-Za-z0-9_-]", body[index]):
            index += 1
        name = body[name_start:index].strip().lower()
        while index < len(body) and body[index].isspace():
            index += 1
        if not name or index >= len(body) or body[index] != "=":
            index += 1
            continue
        index += 1
        while index < len(body) and body[index].isspace():
            index += 1
        if index >= len(body):
            break
        value_start = index
        if body[index] == "{":
            depth = 0
            while index < len(body):
                char = body[index]
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        index += 1
                        break
                index += 1
        elif body[index] == '"':
            index += 1
            while index < len(body):
                if body[index] == '"' and body[index - 1] != "\\":
                    index += 1
                    break
                index += 1
        else:
            while index < len(body) and body[index] != ",":
                index += 1
        fields[name] = strip_wrapping(body[value_start:index])
        while index < len(body) and body[index] != ",":
            index += 1
        if index < len(body) and body[index] == ",":
            index += 1
    return fields


def load_book_map(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_zotero_map(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            key = (row.get("bibtex_key") or row.get("BibTeX key") or "").strip()
            if key:
                rows[key] = row
    return rows


def format_author(author: str) -> str:
    author = author.strip()
    if not author:
        return ""
    if "," in author:
        last, first = [part.strip() for part in author.split(",", 1)]
    else:
        parts = author.split()
        if len(parts) == 1:
            return parts[0]
        last, first = parts[-1], " ".join(parts[:-1])
    initials = " ".join(f"{part[0]}." for part in re.split(r"[\s-]+", first) if part)
    return f"{last}, {initials}".strip()


def format_authors(raw_authors: str) -> str:
    authors = [format_author(part) for part in re.split(r"\s+and\s+", raw_authors) if part.strip()]
    authors = [author for author in authors if author]
    if not authors:
        return "Unknown authors"
    if len(authors) == 1:
        return authors[0]
    if len(authors) > 6:
        return f"{', '.join(authors[:6])} et al."
    return f"{', '.join(authors[:-1])} & {authors[-1]}"


def sentence_case_title(title: str) -> str:
    title = title.strip().rstrip(".")
    return title[0].upper() + title[1:] if title else "Untitled"


def nature_reference(entry: BibEntry) -> str:
    fields = entry.fields
    authors = format_authors(fields.get("author", "")).rstrip(".")
    title = sentence_case_title(fields.get("title", "Untitled"))
    journal = fields.get("journal") or fields.get("journaltitle") or fields.get("booktitle") or fields.get("publisher") or "Source"
    year = fields.get("year") or fields.get("date", "")[:4] or "n.d."
    volume = fields.get("volume", "").strip()
    number = fields.get("number", "").strip()
    pages = fields.get("pages", "").strip().replace("--", "-")
    doi = fields.get("doi", "").strip()
    url = fields.get("url", "").strip()

    if volume and pages:
        source = f"{journal} {volume}, {pages}"
    elif volume:
        source = f"{journal} {volume}"
    elif number:
        source = f"{journal} no. {number}"
    elif pages:
        source = f"{journal}, {pages}"
    else:
        source = journal
    ref = f"{authors}. {title}. {source} ({year})."
    if doi:
        doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
        ref = f"{ref} {doi_url}"
    elif url:
        ref = f"{ref} {url}"
    return ref


def zotero_key_for(bibtex_key: str, zotero_rows: dict[str, dict[str, str]]) -> str:
    row = zotero_rows.get(bibtex_key, {})
    for field in ("zotero_item_key", "item_key", "zotero_key", "Zotero item key"):
        value = row.get(field)
        if value:
            return value.strip()
    return "待补"


def chapter_usage(chapter_title: str, entry: BibEntry) -> str:
    title = entry.fields.get("title", entry.key)
    lowered = title.lower()
    if "alphafold" in lowered:
        return "结构来源、预测模型边界与可视化复核的文献锚点。"
    if "docking" in lowered or "virtual screening" in lowered:
        return "对接/虚拟筛选流程、评分解释和文献案例边界。"
    if "molecular dynamics" in lowered or "peptide" in lowered:
        return "MD/采样或肽结合解释的文献案例，不等同于本项目运行结果。"
    if "boltz" in lowered or "affinity" in lowered:
        return "亲和力预测、置信度和排序解释的模型边界参考。"
    if "diffusion" in lowered or "mpnn" in lowered or "bindcraft" in lowered or "protein design" in lowered:
        return "蛋白设计流程、约束条件和验证标准的文献锚点。"
    if "target" in lowered or "scaffold" in lowered:
        return "第八章研究路线中的文献案例与方法借鉴。"
    return f"{chapter_title} 的方法或证据背景参考。"


def render_refs_block(chapter_title: str, keys: list[str], bib_entries: dict[str, BibEntry], zotero_rows: dict[str, dict[str, str]]) -> str:
    lines = ["## 关键文献与 BibTeX key", "", "<!-- refs:start -->"]
    if not keys:
        lines.extend(
            [
                "",
                "本章暂无正式 required BibTeX key。它承担运行规范、项目目录和可复现记录的基础训练；正式 SCI 文献锚点在后续结构预测、对接、MD、亲和力预测和蛋白设计章节中展开。",
                "",
                "<!-- refs:end -->",
                "",
            ]
        )
        return "\n".join(lines)

    for key in keys:
        entry = bib_entries.get(key)
        if not entry:
            lines.extend(
                [
                    "",
                    f"!!! warning \"缺失引用：`{key}`\"",
                    "    `references/references.bib` 中未找到该 BibTeX key。",
                ]
            )
            continue
        fields = entry.fields
        doi = fields.get("doi", "").strip()
        url = fields.get("url", "").strip()
        locator = doi if doi else url if url else "待补"
        lines.extend(
            [
                "",
                f"!!! quote \"`{key}`\"",
                f"    **Nature 风格引用：** {nature_reference(entry)}",
                "",
                f"    **DOI/URL：** `{locator}`",
                "",
                f"    **BibTeX key：** `{key}`",
                "",
                f"    **Zotero item key：** `{zotero_key_for(key, zotero_rows)}`",
                "",
                f"    **本章用途：** {chapter_usage(chapter_title, entry)}",
            ]
        )
    lines.extend(["", "<!-- refs:end -->", ""])
    return "\n".join(lines)


def replace_ref_section(text: str, rendered_section: str) -> str:
    if REF_SECTION_RE.search(text):
        return REF_SECTION_RE.sub(rendered_section, text, count=1)
    return text.rstrip() + "\n\n" + rendered_section


def render_appendix(data: dict[str, Any], bib_entries: dict[str, BibEntry], zotero_rows: dict[str, dict[str, str]]) -> str:
    chapter_usage_map: dict[str, list[str]] = {}
    for entry in data.get("chapters", []):
        for key in entry.get("required_bibtex_keys", []):
            chapter_usage_map.setdefault(key, []).append(entry.get("title", "未命名章节"))
    appendix_keys: list[str] = []
    for entry in data.get("appendices", []):
        for key in entry.get("required_bibtex_keys", []):
            if key not in appendix_keys:
                appendix_keys.append(key)
    all_keys = list(chapter_usage_map)
    for key in appendix_keys:
        if key not in all_keys:
            all_keys.append(key)

    lines = [
        "# 附录 C Zotero 与 BibTeX 引用表",
        "",
        "本附录由 `tools/update_book_references.py` 从 `references/references.bib` 和 `references/zotero-map.tsv` 生成。正式写作使用 BibTeX key；Zotero item key 只用于本地文献库追踪和 PDF provenance。",
        "",
        "## 按章节索引",
        "",
    ]
    for chapter in data.get("chapters", []):
        keys = chapter.get("required_bibtex_keys", [])
        key_text = "，".join(f"`{key}`" for key in keys) if keys else "暂无正式 BibTeX key"
        lines.append(f"- **{chapter.get('title', '未命名章节')}**：{key_text}")

    lines.extend(["", "## 完整参考文献表", ""])
    for key in all_keys:
        entry = bib_entries.get(key)
        if not entry:
            lines.extend([f"### `{key}`", "", "- 状态：`references/references.bib` 中缺失。", ""])
            continue
        fields = entry.fields
        doi = fields.get("doi", "").strip()
        url = fields.get("url", "").strip()
        locator = doi if doi else url if url else "待补"
        chapters = "；".join(chapter_usage_map.get(key, ["附录引用"]))
        lines.extend(
            [
                f"### `{key}`",
                "",
                f"- **Nature 风格引用：** {nature_reference(entry)}",
                f"- **DOI/URL：** `{locator}`",
                f"- **Zotero item key：** `{zotero_key_for(key, zotero_rows)}`",
                f"- **关联章节/用途：** {chapters}",
                "",
            ]
        )

    lines.extend(
        [
            "## 使用规则",
            "",
            "- 章节正文使用 BibTeX key，例如 `passaro_boltz-2_2025`。",
            "- Zotero item key 只用于本地库追踪，不作为正式引用 key。",
            "- 文献案例、教学范文和本项目结果必须在正文中分层标注。",
            "- DOI/URL 缺失时应回到 Zotero 或原出版页面补齐，不在章节中临时猜测。",
            "",
            "## 来源索引",
            "",
            "- Zotero 映射：`references/zotero-map.tsv`",
            "- BibTeX 文件：`references/references.bib`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    book_map_path = Path(args.map_path).resolve()
    book_root = Path(args.book_root).resolve()
    data = load_book_map(book_map_path)
    bib_entries = parse_bibtex(Path(args.references).resolve())
    zotero_rows = load_zotero_map(Path(args.zotero_map).resolve())

    changed: list[Path] = []
    for chapter in data.get("chapters", []):
        page = chapter.get("page")
        if not page:
            continue
        path = book_root / page
        if not path.exists():
            continue
        keys = [str(key) for key in chapter.get("required_bibtex_keys", [])]
        rendered = render_refs_block(str(chapter.get("title", "")), keys, bib_entries, zotero_rows)
        text = path.read_text(encoding="utf-8")
        new_text = replace_ref_section(text, rendered)
        if new_text != text:
            changed.append(path)
            if not args.dry_run:
                path.write_text(new_text, encoding="utf-8")

    appendix_path = book_root / "appendices" / "references.md"
    appendix_text = render_appendix(data, bib_entries, zotero_rows)
    if appendix_path.exists() and appendix_path.read_text(encoding="utf-8") != appendix_text:
        changed.append(appendix_path)
        if not args.dry_run:
            appendix_path.write_text(appendix_text, encoding="utf-8")

    action = "would update" if args.dry_run else "updated"
    print(f"{action}: {len(changed)} file(s)")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
