---
title: "P33 Zotero正式锚点补齐报告"
created: 2026-06-02
type: maintenance-report
status: active
topics: [zotero, references, citation-management, p33]
source_files: ["references/literature-upgrades-2026-06-02-P32.tsv", "references/zotero-upgrades-2026-06-02-P33.tsv", "references/zotero-map.tsv", "references/references.bib", "03_文献笔记/Chai1方法与PPI筛选.md", "03_文献笔记/RFdiffusion蛋白设计.md", "03_文献笔记/BindCraft与LigandMPNN.md"]
zotero_items: ["5286JS9F", "T2M6L289", "UIPWC5CR"]
bibtex_keys: ["chai_discovery_chai-1_2024", "butcher_novo_2025", "pacesa_bindcraft_2025"]
related: ["P32_文献候选正式化报告.md", "../references/zotero-map.tsv", "../references/zotero-upgrades-2026-06-02-P33.tsv"]
wiki_role: maintenance
source_count: 7
last_reviewed: 2026-06-02
claims:
  - "P33 已把 P32 留下的 Chai-1、RFdiffusion3/RFD3 和 BindCraft Nature 2025 Zotero item key 补齐。"
  - "RFdiffusion3/RFD3 在 Zotero 中存在重复条目；AI_MD 选择 T2M6L289 作为 canonical，不把重复项写入 zotero-map.tsv。"
relations:
  - type: extends
    target: "P32_文献候选正式化报告.md"
  - type: updates
    target: "../references/zotero-map.tsv"
  - type: updates
    target: "../references/references.bib"
  - type: supports
    target: "../07_研究工作台/证据与claims矩阵.md"
---
# P33 Zotero正式锚点补齐报告

## 更新结论

P33 启动本机 Zotero Desktop 后，本地 API 与 Connector 均恢复可用。P32 中暂记为 `待补正式锚点` 的 3 条文献已补齐真实 Zotero item key，并同步写入 `references/zotero-map.tsv`、`references/references.bib`、P32/P33 TSV、相关文献笔记和 claims 矩阵。

## Zotero 状态

| 项 | 结果 |
|:---|:---|
| Zotero 路径 | `E:\Program Files\Zotero\zotero.exe` |
| Zotero 版本 | 9.0.4 |
| Local API | `http://127.0.0.1:23119` 可用 |
| Connector | 可用 |
| 目标集合 | `WOJHNDDE` / `AI药物设计_蛋白与多肽` |

## 正式锚点

| 文献 | BibTeX key | Zotero item key | 处理 |
|:---|:---|:---|:---|
| Chai-1: Decoding the molecular interactions of life | `chai_discovery_chai-1_2024` | `5286JS9F` | 原库未检索到，已通过 Connector 导入到 `AI药物设计_蛋白与多肽`。 |
| De novo Design of All-atom Biomolecular Interactions with RFdiffusion3 | `butcher_novo_2025` | `T2M6L289` | Zotero 中已有两个重复项；选择 `T2M6L289` 为 canonical，`5IA9AEAN` 不进入正式映射。 |
| One-shot design of functional protein binders with BindCraft | `pacesa_bindcraft_2025` | `UIPWC5CR` | Zotero 中已有 Nature 2025 正式条目；旧 preprint `QCD2DXXI` 保留给 `pacesa_bindcraft_2024`。 |

## 边界说明

- AI_MD 继续保留本地正式 BibTeX key，不自动改成 Zotero 导出的 key；这样可以保持在线书籍引用区稳定。
- Chai-1 和 RFdiffusion3/RFD3 仍按 preprint/posted-content 方法锚点处理，不写成本项目实验结果。
- 下一步可进入 P34：把 Chai-1 或 RFD3 的一个最小可运行样例转成真实实验记录，补齐输入、参数、输出、失败项和 QC。

## 验收结果

| 校验 | 结果 |
|:---|:---|
| `python -m unittest discover -s tests` | 12 tests passed |
| `python tools\validate_online_book.py --map book\book_map.toml --book-root book\docs --min-chapter-chars 5000 --require-nature-refs --require-imagegen --require-mermaid` | errors: 0 |
| `python C:\Users\xsui\.codex\skills\building-llm-wiki\scripts\validate_llm_wiki.py . --raw-dir 06_原始学习素材` | warnings: 0, errors: 0 |
| `python -m mkdocs build -f book\mkdocs.yml --strict` | build passed |
| `python tools\graph_health.py . --json --stale-days 180` | `zotero_keys_missing_in_bib: 0`; `literature_pages_missing_zotero_or_bibtex` 仅剩 Obsidian 模板页 |
