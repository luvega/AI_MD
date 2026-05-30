---
title: "AlphaFold 结构预测文献"
created: 2026-05-30
type: literature-note
status: complete
topics: [type/literature, status/complete, topic/protein-design, chapter/2, chapter/5]
source_files: ["references/references.bib", "references/zotero-map.tsv"]
zotero_items: ["UYRXX2U2", "PE42AXJX", "VKKT2HE0", "5GOGPC63"]
bibtex_keys: ["jumper_highly_2021", "abramson_accurate_2024", "mcdonald_benchmarking_2023", "akdel_structural_2022"]
related: ["../02_方法笔记/PyMOL与Chimera可视化.md", "../02_方法笔记/Boltz2亲和力预测.md", "亲和力模型与肽结合排序.md"]
---

# AlphaFold 结构预测文献

## 核心条目

- `UYRXX2U2` / `jumper_highly_2021`：AlphaFold2 单体结构预测背景。
- `PE42AXJX` / `abramson_accurate_2024`：AlphaFold3 生物分子相互作用结构预测背景。
- `VKKT2HE0` / `mcdonald_benchmarking_2023`：AlphaFold2 肽结构预测 benchmark，用于补充肽结构预测的可靠性和失败模式。
- `5GOGPC63` / `akdel_structural_2022`：AlphaFold2 应用的结构生物学社区评估，用于补充第二章结构解释时的应用边界。

## 项目落点

- 第二章可视化时用于解释结构模型来源和可信度。
- 第五章 Boltz2/复合物预测时用于对比结构预测模型的能力边界。
- 涉及肽结构时，应同时检查 pLDDT、构象类别、二硫键/转角等局部结构，不能只看整体模型排名。
- 使用 AlphaFold2 数据库或预测模型做口袋、突变、PPI 或对接解释时，应把低置信区和应用场景写入方法卡或实验记录。

## P5 处理说明

`VKKT2HE0` 和 `5GOGPC63` 的 Zotero 本地 BibTeX 导出在本轮返回 HTTP 502，因此 `references.bib` 中的 `mcdonald_benchmarking_2023` 与 `akdel_structural_2022` 为 Crossref/出版社元数据人工确认条目，Zotero item key 保留在 `references/zotero-map.tsv`。
