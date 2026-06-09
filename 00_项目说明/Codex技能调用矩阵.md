---
title: "Codex技能调用矩阵"
created: 2026-06-02
type: project-doc
status: active
topics: [codex-skills, routing, online-book, data-analysis, writing]
source_files: ["00_项目说明/P26_Codex技能集成报告.md", "00_项目说明/P27_Codex项目规则迁移报告.md", "00_项目说明/P28_重点章节Codex审稿报告.md", "00_项目说明/P29_文献与引用补强报告.md", "00_项目说明/P30_图示与版面升级报告.md", "00_项目说明/P31_数据分析与AIDD dry-run报告.md", "00_项目说明/P32_文献候选正式化报告.md", "00_项目说明/P33_Zotero正式锚点补齐报告.md", "CLAUDE.md"]
zotero_items: ["5286JS9F", "T2M6L289", "UIPWC5CR"]
bibtex_keys: []
related: ["插件与Skills调用说明.md", "P26_Codex技能集成报告.md", "P27_Codex项目规则迁移报告.md", "P28_重点章节Codex审稿报告.md", "P29_文献与引用补强报告.md", "P30_图示与版面升级报告.md", "P31_数据分析与AIDD dry-run报告.md", "P32_文献候选正式化报告.md", "P33_Zotero正式锚点补齐报告.md"]
wiki_role: concept
source_count: 9
last_reviewed: 2026-06-02
claims:
  - "AI_MD 下一版更新优先使用全局 Codex skills，而不是向 .claude/skills 添加第三方技能。"
  - "AI_MD 自有项目规则已迁移为 ai-md-* 全局 Codex skills。"
  - "P28 已完成第 3/5/6/8 章高风险 claim 第一轮审稿，可作为 P29-P31 的输入基线。"
  - "P29 已完成第 3/5/6/8 章引用覆盖审计，并识别 Chai-1、RFD3/RFdiffusion3、BindCraft 三个候选补强。"
  - "P30 已完成第 1-8 章 Mermaid 图示增强和 online book Mermaid 校验器增强。"
  - "P31 已完成第 3/5/6/8 章 AIDD dry-run 脚本和实验记录模板字段补强。"
  - "P32 已完成 Chai-1、RFdiffusion3/RFD3 和 BindCraft Nature 2025 候选文献的正式 BibTeX 提升。"
  - "P33 已完成 Chai-1、RFdiffusion3/RFD3 和 BindCraft Nature 2025 的真实 Zotero item key 回写。"
relations:
  - type: extends
    target: "插件与Skills调用说明.md"
  - type: supports
    target: "P28_重点章节Codex审稿报告.md"
  - type: supports
    target: "P29_文献与引用补强报告.md"
  - type: supports
    target: "P30_图示与版面升级报告.md"
  - type: supports
    target: "P31_数据分析与AIDD dry-run报告.md"
  - type: supports
    target: "P32_文献候选正式化报告.md"
  - type: supports
    target: "P33_Zotero正式锚点补齐报告.md"
---
# Codex技能调用矩阵

本矩阵用于 AI_MD 知识库、教材正文和研究工作台更新。旧版内容不完整的 `book/` 已删除；当前工作必须先判断属于 Wiki 轨还是 Book 轨。Codex skills 负责提供专业工作流，AI_MD 项目规则负责限制写入范围、来源边界和验收方式。

## 总原则

| 原则 | 执行方式 |
|:---|:---|
| 本地知识优先 | 先读 `CLAUDE.md`、`index.md`、相关 `_index.md` 和具体笔记，再调用外部技能。 |
| Codex skill 优先 | 项目规则使用 `ai-md-*` 全局 Codex skills；新增外部能力安装到 `C:\Users\xsui\.codex\skills`，不新增第三方 `.claude/skills`。 |
| 来源边界保留 | 原始 PDF、课件、压缩包和 Office 文件只读，不复制进教材正文或未来发布层。 |
| 引用仍走项目元数据 | 正式引用以 `references/references.bib` 和 `references/zotero-map.tsv` 为准。 |
| Wiki/Book 分轨 | Wiki 维护默认不更新 `chapters/chapter-XX/正文.md` 或 `book/`；Book 写作和发布必须由用户明确触发。 |
| 完成前验证 | Wiki 轨运行 LLM Wiki 校验、raw-source 审计和 `tools/graph_health.py`；Book 轨才运行 `sync_online_book.py`、在线书校验和 MkDocs build。 |

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

## Wiki 轨与 Book 轨

| 轨道 | 触发词 | 可写范围 | 禁止项 |
|:---|:---|:---|:---|
| Wiki 轨 | 整理资料、更新 wiki、方法卡、文献笔记、实验记录、`/update-vault`、`wiki-lint` | `00_项目说明/`、`01_课程章节索引/`、`02_方法笔记/`、`03_文献笔记/`、`04_实验记录/`、`05_附件索引/`、`07_研究工作台/`、`references/`、`index.md`、`log.md` | 不改 `chapters/chapter-XX/正文.md`，不改 `book/`，不运行 `sync_online_book.py` |
| Book 轨 | 写章节正文、更新在线书、同步 book、发布层、MkDocs、GitHub Pages | `大纲.md`、`chapters/chapter-XX/本章大纲.md`、`chapters/chapter-XX/正文.md`、`chapters/chapter-XX/assets/`、`book/` | 不从 `book/docs` 反向生成 wiki 或正文；不复制 raw sources |

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
| 化合物处理 | `datamol`、`rdkit` | SMILES/SDF 清洗、描述符、指纹、聚类和构象处理；P31 已落实为第 3 章候选 triage dry-run。 |
| 药物化学筛选 | `medchem` | 成药性规则、结构警报和化合物库 triage；P31 已固化结构警报与过滤理由字段。 |
| MD 与轨迹分析 | `molecular-dynamics` | 体系设置、轨迹指标、代表构象和解释边界。 |
| AI 对接示例 | `diffdock` | pose 预测和虚拟筛选教学流程；不输出亲和力结论，P31 只记录 pose/confidence 边界字段。 |

## 下一版更新建议

1. P28 已完成：`peer-review` 和 `scientific-critical-thinking` 已用于审查第 3/5/6/8 章高风险 claim，基线见 `P28_重点章节Codex审稿报告.md`。
2. P29 已完成：`literature-review` 和 `citation-management` 已用于第 3/5/6/8 章引用覆盖审计，候选补强见 `P29_文献与引用补强报告.md` 和 `references/zotero-candidates-2026-06-02-P29.tsv`。
3. P30 已完成：`markdown-mermaid-writing` 和 `scientific-schematics` 曾用于旧版 8 章 Mermaid source-of-truth 和示意图 prompt；P40 后这些旧发布资源已删除，只保留历史报告。
4. P31 已完成：`datamol`、`rdkit`、`medchem`、`molecular-dynamics`、`diffdock` 已用于补充 dry-run 数据流程和实验记录模板，见 `P31_数据分析与AIDD dry-run报告.md`。
5. P32 已完成：Chai-1、RFdiffusion3/RFD3 和 BindCraft Nature 2025 已正式写入 BibTeX、章节引用区和文献笔记。
6. P33 已完成：真实 Zotero item key 已回写到 `references/zotero-map.tsv`；RFdiffusion3 重复项选择 `T2M6L289` 为 canonical。
7. 下一轮建议进入 P34：把 P31 dry-run 升级为一个真实小样本运行记录，优先选择 Chai-1 或 RFD3/RFdiffusion3。
8. 每轮 Wiki 更新后只运行 LLM Wiki 校验、raw-source 审计和图谱体检；只有用户明确进入 Book 轨，才运行在线书籍校验、MkDocs 构建或 GitHub Pages workflow。
