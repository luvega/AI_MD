---
title: "07_研究工作台索引"
created: 2026-05-31
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, research-workbench, knowledge-graph]
wiki_role: synthesis
source_count: 8
last_reviewed: 2026-05-31
source_files: ["index.md", "00_项目说明/项目背景.md", "01_课程章节索引/章节精读/章节-文献锚点矩阵.md", "references/zotero-map.tsv"]
zotero_items: ["TPR3JY6N", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ", "V6Y5EEZL"]
bibtex_keys: ["yang_w_past_2026", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026", "zhu_novo_2026"]
related: ["../index.md", "实体索引.md", "证据与claims矩阵.md", "研究问题与项目池.md", "AI回归评测集.md"]
claims: [p15_entity_layer_2026_05_31, p16_claim_layer_2026_05_31, p17_research_workbench_2026_05_31, p18_ai_eval_suite_2026_05_31, p19_output_views_2026_05_31]
relations:
  - type: depends_on
    target: "../index.md"
  - type: supports
    target: "实体索引.md"
  - type: supports
    target: "证据与claims矩阵.md"
  - type: supports
    target: "研究问题与项目池.md"
  - type: supports
    target: "AI回归评测集.md"
---

# 07_研究工作台索引

本目录把课程资料库推进为个人研究工作台：实体索引负责“查对象”，claims 矩阵负责“查证据和边界”，项目池和队列负责“把材料转成下一步实验”，AI 回归评测集负责“检查后续 Agent 是否真的能用这个知识库”。

| 文件 | 类型 | 一句话说明 | 关联原始文件 | 关联 Zotero 条目 |
|:---|:---|:---|:---|:---|
| [实体索引.md](实体索引.md) | project-doc | 轻量实体层，覆盖第 3/5/6/8 章的靶点、分子、方法、软件、论文、实验模板和章节。 | 章节精读、方法笔记、文献映射 | 多个 |
| [证据与claims矩阵.md](证据与claims矩阵.md) | project-doc | 把容易误读的判断抽成 claim，记录证据、边界、强度和复核日期。 | 方法笔记、章节精读、文献笔记 | 多个 |
| [研究问题与项目池.md](研究问题与项目池.md) | project-doc | 面向用户个人研究，把课程线索转成问题、假设、证据、缺口、下一步实验和输出物。 | 第 3/5/6/8 章资料 | 多个 |
| [阅读队列.md](阅读队列.md) | project-doc | 按研究价值和缺口优先级排列后续阅读与文献补锚任务。 | `references/zotero-map.tsv` | 多个 |
| [实验队列.md](实验队列.md) | project-doc | 把项目池拆成可执行实验记录任务，并指向已有模板。 | `04_实验记录/` | 多个 |
| [输出视图.md](输出视图.md) | project-doc | 按课件、综述、课题申请和实验记录等出口重组现有资料。 | 全项目 | 多个 |
| [AI回归评测集.md](AI回归评测集.md) | project-doc | 12 个标准查询任务，用于每轮更新后验收 AI 回答的路径、引用、边界和待确认项。 | 全项目 | 多个 |

## 使用顺序

1. 查对象：先读 [实体索引](实体索引.md)，定位靶点、方法、软件、论文和模板。
2. 查判断：再读 [证据与 claims 矩阵](证据与claims矩阵.md)，确认哪些结论只是排序信号、教学范例或待验证假设。
3. 做研究：进入 [研究问题与项目池](研究问题与项目池.md) 和 [实验队列](实验队列.md)，选择下一步可执行任务。
4. 做输出：按 [输出视图](输出视图.md) 重组课件、综述、课题申请或实验记录。
5. 验收 AI：用 [AI 回归评测集](AI回归评测集.md) 检查回答是否包含路径、Zotero/BibTeX key、使用边界和待确认项。
