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
    r"(?ms)^## 关键文献(?:与 BibTeX key)?\s*\n.*?(?=^## |\Z)",
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
        if not first:
            return last
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


def article_brief(entry: BibEntry) -> str:
    title = entry.fields.get("title", entry.key)
    lowered = title.lower()
    rules = [
        ("highly accurate protein structure prediction with alphafold", "本文介绍 AlphaFold 在蛋白结构预测中的模型设计、CASP14 验证和结构生物学应用。"),
        ("alphafold 3", "本文介绍 AlphaFold 3 对蛋白、核酸、小分子和修饰残基复合物结构的统一预测框架。"),
        ("community assessment of alphafold2", "本文评估 AlphaFold2 在结构生物学中的应用范围、可靠性边界和社区使用经验。"),
        ("dockey", "本文介绍 Dockey 平台在大规模分子对接、虚拟筛选和结果管理中的集成流程。"),
        ("protein-peptide docking", "本文比较多种蛋白-多肽对接方法的性能，为肽结合体系的模型选择提供基准。"),
        ("ligand–protein molecular docking", "本文综述机器学习方法在配体-蛋白分子对接中的建模策略、特征和应用限制。"),
        ("ai-powered docking", "本文从虚拟筛选角度评测 AI 驱动对接方法，比较排序能力、适用场景和局限。"),
        ("target specific peptide inhibitors", "本文结合生成式深度学习、柔性肽对接和分子动力学设计靶向肽抑制剂。"),
        ("molecular dynamics simulations improve", "本文讨论分子动力学模拟能否提升机器学习预测蛋白-配体亲和力的效果。"),
        ("boltz-2", "本文介绍 Boltz-2 在复合物结构和结合亲和力预测中的模型设计、性能与开放资源。"),
        ("boltzdesign1", "本文提出反向使用全原子结构预测模型进行广义生物分子结合体设计的方法。"),
        ("deepdtaf", "本文提出 DeepDTAF 深度学习模型，用于预测蛋白-配体结合亲和力。"),
        ("ppi-affinity", "本文介绍 PPI-Affinity 网络工具，用于预测并优化蛋白-肽和蛋白-蛋白结合亲和力。"),
        ("ranking peptide binders", "本文探讨利用 AlphaFold 相关结构信息按亲和力排序肽结合体的策略。"),
        ("rfdiffusion2", "本文介绍 RFdiffusion2 在原子级酶活性位点支架设计中的建模和实验验证。"),
        ("rfdiffusion3", "本文介绍 RFdiffusion3 用于全原子生物分子相互作用设计的预印本方法。"),
        ("antibodies with rfdiffusion", "本文展示结合 RFdiffusion2 和筛选实验从头设计表位特异性抗体的流程。"),
        ("rfdiffusion", "本文介绍 RFdiffusion 通过扩散模型从分子约束生成蛋白结构和功能设计方案。"),
        ("proteinmpnn", "本文提出 ProteinMPNN 深度学习序列设计方法，并用结构和功能实验验证其性能。"),
        ("bindcraft", "本文介绍 BindCraft 一步式蛋白结合体设计管线及其多靶点实验成功率。"),
        ("ligandmpnn", "本文介绍 LigandMPNN 在小分子、核苷酸和金属环境下进行蛋白序列设计的方法。"),
        ("past, present and future", "本文综述从头蛋白设计的发展脉络、当前能力和未来研究方向。"),
        ("uxs1-dependent glucuronate detoxification", "本文研究 UXS1 依赖的葡萄糖醛酸解毒通路与二甲双胍抗肿瘤效应的关系。"),
        ("ape1", "本文通过结构基础虚拟筛选发现靶向 APE1 内切酶活性位点的小分子抑制剂。"),
        ("hierarchical virtual screening", "本文提出整合骨架感知机器学习、集合对接和分子动力学的可复现虚拟筛选框架。"),
        ("helicobacter pylori adhesin baba", "本文报道靶向幽门螺杆菌黏附素 BabA 的从头蛋白结合体设计。"),
        ("chai-1", "本文介绍 Chai-1 对生物分子相互作用进行统一结构预测和约束建模的方法。"),
    ]
    for pattern, brief in rules:
        if pattern in lowered:
            return clamp_brief(brief)
    return clamp_brief("本文围绕该主题提供方法背景、模型依据或案例证据，需结合正文边界理解。")


def clamp_brief(text: str, limit: int = 100) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip("，。；、 ") + "。"


def render_refs_block(chapter_title: str, keys: list[str], bib_entries: dict[str, BibEntry], zotero_rows: dict[str, dict[str, str]]) -> str:
    lines = ["## 关键文献", "", "<!-- refs:start -->"]
    if not keys:
        lines.extend(
            [
                "",
                "本章暂无正式关键文献列表。它承担运行规范、项目目录和可复现记录的基础训练；正式 SCI 文献锚点在后续章节中展开。",
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
                    "!!! warning \"缺失引用\"",
                    "    `references/references.bib` 中未找到对应的内部引用键。",
                ]
            )
            continue
        lines.extend(
            [
                "",
                f"- {nature_reference(entry)}",
                "",
                f"  **本文内容简介：** {article_brief(entry)}",
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
        "# 附录 C 参考文献表",
        "",
        "本附录由 `tools/update_book_references.py` 从内部引用映射生成。页面只展示可读参考文献列表；引用键和本地文献库条目保留在项目元数据中。",
        "",
        "## 按章节索引",
        "",
    ]
    for chapter in data.get("chapters", []):
        keys = chapter.get("required_bibtex_keys", [])
        key_text = f"{len(keys)} 篇关键文献" if keys else "暂无正式关键文献"
        lines.append(f"- **{chapter.get('title', '未命名章节')}**：{key_text}")

    lines.extend(["", "## 完整参考文献表", ""])
    for index, key in enumerate(all_keys, start=1):
        entry = bib_entries.get(key)
        if not entry:
            lines.extend([f"### 参考文献 {index}", "", "- 状态：内部引用映射缺失对应条目。", ""])
            continue
        chapters = "；".join(chapter_usage_map.get(key, ["附录引用"]))
        lines.extend(
            [
                f"### 参考文献 {index}",
                "",
                f"- {nature_reference(entry)}",
                f"- **本文内容简介：** {article_brief(entry)}",
                f"- **关联章节：** {chapters}",
                "",
            ]
        )

    lines.extend(
        [
            "## 使用规则",
            "",
            "- 章节正文只展示参考文献和 100 字以内的本文内容简介。",
            "- 内部引用键和本地文献库条目只用于生成、校验和 provenance 追踪，不在读者页面展示。",
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
