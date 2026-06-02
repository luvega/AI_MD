---
title: "Zotero 文献补强候选"
created: 2026-05-30
type: literature-note
status: active
topics: [zotero, literature-candidates, docking, molecular-dynamics, affinity, protein-design]
source_files: ["references/zotero-candidates-2026-05-30.tsv", "references/zotero-candidates-2026-06-02-P29.tsv", "references/zotero-map.tsv"]
zotero_items: ["T2M6L289", "P7DSJ8TH", "LQED22TC", "2FEDHKRQ", "R2W3SF5S", "57K986LK", "92GPX1OI", "95UTFQDM", "YIV9AVT4", "CRT8PKH3", "VKKT2HE0", "5GOGPC63", "6Q8ACPUP"]
bibtex_keys: ["crampon_machine-learning_2022", "gu_benchmarking_2025", "wang_deepdtaf_2021", "romero-molina_ppi-affinity_2022", "chang_ranking_2023", "gu_molecular_2023", "mcdonald_benchmarking_2023", "akdel_structural_2022"]
related: ["../01_课程章节索引/章节精读/章节-文献锚点矩阵.md", "../references/zotero-candidates-2026-05-30.tsv", "../references/zotero-candidates-2026-06-02-P29.tsv", "../00_项目说明/P29_文献与引用补强报告.md"]
---
# Zotero 文献补强候选

本页记录本轮从本地 Zotero 检索得到的补强候选及 P4/P5 处理状态。已正式提升或人工确认提升的条目已经写入 `references/zotero-map.tsv` 和 `references/references.bib`。

## 推荐优先级

1. 第三章已正式提升：`R2W3SF5S`、`57K986LK`，用于补机器学习 docking 和 AI-powered virtual screening benchmark。
2. 第五章已正式提升：`95UTFQDM`、`YIV9AVT4`、`CRT8PKH3`，用于补深度学习亲和力、蛋白-肽/PPI 亲和力和 AlphaFold 肽 binder 排序。
3. 第二/四/五章人工确认提升：`92GPX1OI`、`VKKT2HE0`、`5GOGPC63`，原因是本轮 Zotero BibTeX 导出返回 HTTP 502，已改用 DOI/Crossref/出版社元数据确认。
4. 第六章后续：`T2M6L289`、`P7DSJ8TH`、`LQED22TC`、`2FEDHKRQ`、`6Q8ACPUP`，用于 RFdiffusion3、binder improvement 和 ProteinMPNN 扩展。

## 本轮检索结论

- Zotero 本地 API 可用，版本为 `9.0.4`，本轮只读检索，不写入 Zotero。
- `Boltz`、`RFdiffusion`、`ProteinMPNN`、`AlphaFold`、`molecular docking`、`molecular dynamics`、`binding affinity` 和 `virtual screening` 都有可用候选。
- `PyMOL`、`Chimera`、`Uni-Dock`、`BioEmu` 在本地 Zotero 本轮检索无直接命中。
- Life Science Research/NCBI Entrez 交叉检查：RFdiffusion3 查询命中 PubMed ID `41000976`；BioEmu 查询遇到 NCBI 429 限流，需后续单独补查；AI-powered docking benchmark 以当前查询未命中 PubMed。
- P4 正式提升 5 条：`R2W3SF5S`、`57K986LK`、`95UTFQDM`、`YIV9AVT4`、`CRT8PKH3`。
- P5 人工确认提升 3 条：`92GPX1OI`、`VKKT2HE0`、`5GOGPC63`；原因是 Zotero 本地 BibTeX 导出返回 HTTP 502，人工确认来源已写入 `references.bib` 的 `note` 字段。

## P29 补强候选

P29 复核第 3/5/6/8 章后，新增 3 条候选，详见 `references/zotero-candidates-2026-06-02-P29.tsv`：

| 候选 BibTeX key | 用途 | 当前状态 |
|:---|:---|:---|
| `chai_discovery_chai-1_2024` | 第 8 章 Chai-1 方法锚点，支持输入、输出、restraints、MSA 和工具引用边界。 | 待 Zotero 导入，不进入正式章节引用区。 |
| `butcher_novo_2025` | 第 6 章 RFD3/RFdiffusion3 特异性方法锚点。 | 待 Zotero 导入，不替代现有 RFdiffusion/RFdiffusion2 正式条目。 |
| `pacesa_bindcraft_2025` | 将既有 BindCraft bioRxiv 条目升级为 Nature 2025 正式发表版本。 | 待确认是否更新既有 Zotero 条目或建立 published-version alias。 |

## 使用规则

- 只有在具体章节或方法卡需要它时，才把候选文献提升到 `zotero-map.tsv`。
- 提升前必须导出并确认 BibTeX key；如果导出 key 过长或重复，建立项目本地 alias。
- 如果 Zotero 导出失败但 DOI/出版社元数据可确认，可以标为“人工确认提升”，但必须记录原因和来源。
- 已提升条目在候选表中保留处理状态，正式引用以 `references/zotero-map.tsv` 和对应文献笔记为准。
