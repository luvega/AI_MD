---
title: "RFdiffusion 蛋白设计文献"
created: 2026-05-30
type: literature-note
status: complete
topics: [type/literature, status/complete, topic/rfdiffusion, topic/protein-design, chapter/6]
source_files: ["references/references.bib", "references/zotero-map.tsv", "references/literature-upgrades-2026-06-02-P32.tsv", "references/zotero-upgrades-2026-06-02-P33.tsv"]
zotero_items: ["UKX5E6IB", "ZYFCZKMH", "EBQ7CNVI", "TPR3JY6N", "V6Y5EEZL", "T2M6L289"]
bibtex_keys: ["watson_novo_2023", "ahern_atom_2025", "butcher_novo_2025", "bennett_atomically_2025", "yang_w_past_2026", "zhu_novo_2026"]
related: ["../02_方法笔记/RFdiffusion与蛋白设计.md"]
wiki_role: literature
source_count: 7
last_reviewed: 2026-06-02
claims: [watson_novo_2023, ahern_atom_2025, butcher_novo_2025, bennett_atomically_2025, yang_w_past_2026, zhu_novo_2026, p32_literature_upgrade_2026_06_02, p33_zotero_anchoring_2026_06_02]
relations:
  - type: supports
    target: "../02_方法笔记/RFdiffusion与蛋白设计.md"
  - type: applies_to
    target: "../01_课程章节索引/章节精读/第06章_RFD3多组分设计精读.md"
  - type: applies_to
    target: "../01_课程章节索引/章节精读/第08章_计算思路解析精读.md"
  - type: depends_on
    target: "../references/zotero-map.tsv"
---

# RFdiffusion 蛋白设计文献

## 核心条目

- `UKX5E6IB` / `watson_novo_2023`：RFdiffusion 主文献，支撑第六章蛋白骨架生成。
- `ZYFCZKMH` / `ahern_atom_2025`：RFdiffusion2 活性位点 scaffolding，适合连接酶活性位点设计。
- `T2M6L289` / `butcher_novo_2025`：RFdiffusion3/RFD3 预印本方法锚点，用于把第六章 RFD3 特异性 claim 从 RFdiffusion2/综述中拆出来；Zotero 重复项 `5IA9AEAN` 不进入正式映射。
- `EBQ7CNVI` / `bennett_atomically_2025`：RFdiffusion 抗体设计，适合扩展到抗体和表位特异性 binder。
- `TPR3JY6N` / `yang_w_past_2026`：de novo protein design 综述，作为第六章新增 Nature PDF 的正式锚点，用于把 Rosetta、AlphaFold/RoseTTAFold、RFdiffusion、ProteinMPNN、binder/酶设计和未来方向放在同一条方法谱系中。
- `V6Y5EEZL` / `zhu_novo_2026`：第八章 BabA binder 设计范文，作为 RFdiffusion3 + ProteinMPNN + 回折叠/对接/MD 漏斗的课程案例锚点；当前只作为范文和流程参照，不等同于本项目已有运行结果。

## 项目落点

第六章压缩包中的 RFdiffusion/RFD3 资料，应在解压或运行后补充：输入约束、骨架生成策略、序列设计步骤、筛选指标、可视化结构和失败案例。

## P14 补充边界

- Nature 综述的 Zotero 库中存在重复条目 `TPR3JY6N` 和 `G3TSIVRB`；本项目只把 `TPR3JY6N` 写入 `references/zotero-map.tsv`，避免后续映射重复。
- BabA 预印本在 Zotero 中以 `document` 类型导入，BibTeX 使用 `@misc{zhu_novo_2026}`；正式引用时要标注其 posted-content/preprint 属性。
- 第八章蛋白设计 PDF 可用于教学拆解流程：热点定义、RFdiffusion3 骨架生成、ProteinMPNN 序列设计、回折叠、对接和 MD。不能把其中候选 binder 当作 AI_MD 已验证候选。

## P32 补强

- `butcher_novo_2025` 已作为 RFdiffusion3/RFD3 方法锚点写入 `references/references.bib` 和第六章关键文献区。
- 该条目仍按 bioRxiv posted-content/preprint 处理；没有真实 AI_MD RFD3 运行输出前，只能支撑方法背景和记录字段，不能支撑本项目结果。

## P33 Zotero 锚定

- P33 启动 Zotero Desktop 后检索到两个 RFdiffusion3 重复项：`T2M6L289` 和 `5IA9AEAN`。
- 两者导出 BibTeX key 均为 `butcher_j_novo_2025`，本项目保留本地正式 BibTeX key `butcher_novo_2025`，并选择 `T2M6L289` 作为 canonical Zotero item key。
