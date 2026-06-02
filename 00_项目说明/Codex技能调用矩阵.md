---
title: "Codex技能调用矩阵"
created: 2026-06-02
type: project-doc
status: active
topics: [codex-skills, routing, online-book, data-analysis, writing]
source_files: ["00_项目说明/P26_Codex技能集成报告.md", "00_项目说明/P27_Codex项目规则迁移报告.md", "00_项目说明/P28_重点章节Codex审稿报告.md", "00_项目说明/P29_文献与引用补强报告.md", "00_项目说明/P30_图示与版面升级报告.md", "CLAUDE.md"]
zotero_items: []
bibtex_keys: []
related: ["插件与Skills调用说明.md", "P26_Codex技能集成报告.md", "P27_Codex项目规则迁移报告.md", "P28_重点章节Codex审稿报告.md", "P29_文献与引用补强报告.md", "P30_图示与版面升级报告.md"]
wiki_role: concept
source_count: 6
last_reviewed: 2026-06-02
claims:
  - "AI_MD 下一版更新优先使用全局 Codex skills，而不是向 .claude/skills 添加第三方技能。"
  - "AI_MD 自有项目规则已迁移为 ai-md-* 全局 Codex skills。"
  - "P28 已完成第 3/5/6/8 章高风险 claim 第一轮审稿，可作为 P29-P31 的输入基线。"
  - "P29 已完成第 3/5/6/8 章引用覆盖审计，并识别 Chai-1、RFD3/RFdiffusion3、BindCraft 三个候选补强。"
  - "P30 已完成第 1-8 章 Mermaid 图示增强和 online book Mermaid 校验器增强。"
relations:
  - type: extends
    target: "插件与Skills调用说明.md"
  - type: supports
    target: "P28_重点章节Codex审稿报告.md"
  - type: supports
    target: "P29_文献与引用补强报告.md"
  - type: supports
    target: "P30_图示与版面升级报告.md"
---
# Codex技能调用矩阵

本矩阵用于下一版 AI_MD 在线教材和研究工作台更新。Codex skills 负责提供专业工作流；AI_MD 项目规则负责限制写入范围、来源边界和验收方式。

## 总原则

| 原则 | 执行方式 |
|:---|:---|
| 本地知识优先 | 先读 `CLAUDE.md`、`index.md`、相关 `_index.md` 和具体笔记，再调用外部技能。 |
| Codex skill 优先 | 项目规则使用 `ai-md-*` 全局 Codex skills；新增外部能力安装到 `C:\Users\xsui\.codex\skills`，不新增第三方 `.claude/skills`。 |
| 来源边界保留 | 原始 PDF、课件、压缩包和 Office 文件只读，不复制进在线书籍。 |
| 引用仍走项目元数据 | 正式引用以 `references/references.bib` 和 `references/zotero-map.tsv` 为准。 |
| 完成前验证 | 内容、图谱、在线书籍和 GitHub Pages 相关更新必须运行对应校验。 |

## AI_MD 项目规则

| 场景 | 优先 Codex skill | 输出 |
|:---|:---|:---|
| 宽泛任务、阶段推进、跨模块选择 | `ai-md-router` | 路由到 ingest、query、takenote、Zotero、lint 或 update。 |
| 新来源摄入 | `ai-md-ingest-source` | 来源类型、影响面、目标页面和验收建议。 |
| 基于知识库回答 | `ai-md-query-wiki` | 基于索引和具体笔记的回答；必要时建议沉淀。 |
| 长期内容写入 | `ai-md-takenote` | 正式 Markdown 笔记、frontmatter 和索引更新。 |
| 维护验收 | `ai-md-update-vault` | 索引、链接、引用、附件和 raw 边界检查。 |
| 高层健康检查 | `ai-md-wiki-lint` | 孤立页、重复概念、过期 claim 和图谱问题。 |
| 文献映射 | `ai-md-zotero-literature-link` | 文献候选、BibTeX、Zotero 映射和文献笔记。 |

## 教材正文与文字修正

| 场景 | 优先 Codex skill | 输出 |
|:---|:---|:---|
| 章节正文重写、教材化长文 | `scientific-writing` | 章节导读、概念解释、方法流程和学习路径。 |
| 章节审稿与风险清单 | `peer-review` | 问题清单、缺口、可读性和方法边界建议。 |
| claim-evidence 自检 | `scientific-critical-thinking` | Claim、Evidence、Status 和过强表述降级建议。 |
| 研究假设与下一步实验 | `hypothesis-generation` | 假设、预测、验证实验和待确认项。 |
| 课题申请出口 | `research-grants` | 研究意义、创新性、可行性和输出视图。 |

## 文献复核与引用

| 场景 | 优先 Codex skill | 输出 |
|:---|:---|:---|
| 章节文献补强 | `literature-review` | 文献候选、主题综述、证据边界。 |
| DOI/元数据核对 | `citation-management` | 参考文献元数据、引用格式和 BibTeX 候选。 |
| 本地 Zotero 映射 | `zotero-literature-link`、Zotero 插件 | `zotero-map.tsv`、`references.bib` 和文献笔记。 |

## 内容组织、版面和图示

| 场景 | 优先 Codex skill | 输出 |
|:---|:---|:---|
| 文本化流程图和结构图 | `markdown-mermaid-writing` | Mermaid 图、章节结构图和工作流图。 |
| 科学示意图设计 | `scientific-schematics` | Imagegen/BioRender/原创示意图的 prompt 和构图规则。 |
| 课程幻灯片出口 | `scientific-slides` | 讲义到课堂/组会 slides 的结构建议。 |
| 投稿/海报/基金格式参考 | `venue-templates` | 输出格式、版面和投稿规范参考。 |
| 新素材转 Markdown | `markitdown` | 转换草稿；正式内容仍需回到 AI_MD wiki 层整理。 |

## 数据分析与 AIDD 流程

| 场景 | 优先 Codex skill | 输出 |
|:---|:---|:---|
| 数据结构和质量初筛 | `exploratory-data-analysis` | 数据摘要、质量问题和后续分析建议。 |
| 统计检验与结果措辞 | `statistical-analysis` | 假设检验、报告句式和边界提示。 |
| 发表级图表 | `scientific-visualization` | 多面板图、配色、图注和导出规范。 |
| 知识图谱分析 | `networkx` | 节点、边、中心性、孤立节点和社区结构。 |
| 化合物处理 | `datamol`、`rdkit` | SMILES/SDF 清洗、描述符、指纹、聚类和构象处理。 |
| 药物化学筛选 | `medchem` | 成药性规则、结构警报和化合物库 triage。 |
| MD 与轨迹分析 | `molecular-dynamics` | 体系设置、轨迹指标、代表构象和解释边界。 |
| AI 对接示例 | `diffdock` | pose 预测和虚拟筛选教学流程；不输出亲和力结论。 |

## 下一版更新建议

1. P28 已完成：`peer-review` 和 `scientific-critical-thinking` 已用于审查第 3/5/6/8 章高风险 claim，基线见 `P28_重点章节Codex审稿报告.md`。
2. P29 已完成：`literature-review` 和 `citation-management` 已用于第 3/5/6/8 章引用覆盖审计，候选补强见 `P29_文献与引用补强报告.md` 和 `references/zotero-candidates-2026-06-02-P29.tsv`。
3. P30 已完成：`markdown-mermaid-writing` 和 `scientific-schematics` 已用于每章 Mermaid source-of-truth 和示意图 prompt，见 `book/docs/resources/mermaid-schematics.md`。
4. P31 下一步：用 `datamol`、`rdkit`、`medchem`、`molecular-dynamics`、`diffdock` 补充 dry-run 数据流程和实验记录模板。
5. 每轮更新后运行在线书籍校验、MkDocs 构建、LLM Wiki 校验和图谱体检。
