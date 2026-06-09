---
title: "插件与Skills调用说明"
created: 2026-05-30
type: project-doc
status: active
topics: [plugin-routing, skills, zotero, chrome, life-science-research, workflow]
source_files: ["CLAUDE.md", ".claude/skills", "C:/Users/xsui/.codex/skills", "P26_Codex技能集成报告.md"]
zotero_items: []
bibtex_keys: []
related: ["知识库使用说明.md", "Codex技能调用矩阵.md", "P26_Codex技能集成报告.md"]
---
# 插件与Skills调用说明

这份说明用于让 AI_MD 后续整理任务自动选择必要插件、全局 Codex skills 和历史项目内规则。原则是先用本项目本地索引和规则，只有确实需要外部资料、浏览器状态、Zotero 库或专业工作流时才调用外部能力。

## P26当前策略

- 新增第三方专业能力统一安装为全局 Codex skills：`C:/Users/xsui/.codex/skills/`。
- AI_MD 仓库不再向 `.claude/skills/` 添加第三方 skill 副本；该目录只作为历史项目内 LLM Wiki 规则来源。
- P26 已从 `K-Dense-AI/scientific-agent-skills` commit `93124850ef08487e423165554c54f0b333d5631d` 安装 21 个精选 Codex skills。
- P27 已将 AI_MD 自有项目规则生成并安装为 7 个 `ai-md-*` 全局 Codex skills。
- 下一版教材更新的具体调用见 `Codex技能调用矩阵.md`。
- 新安装的全局 skills 需要重启 Codex 后才能稳定出现在会话技能列表中。

## 下一步计划

| 阶段 | 目标 | 产物 | 优先插件/skill |
|:---|:---|:---|:---|
| P27 | AI_MD 自有规则迁移 | 已将既有 `.claude/skills` 项目规则重写并安装为 7 个 `ai-md-*` 全局 Codex skills | `skill-creator`、`building-llm-wiki` |
| P28 | 下一版教材正文审校 | 第 3/5/6/8 章高风险 claim 审稿、文字润色和证据边界收敛 | `scientific-writing`、`peer-review`、`scientific-critical-thinking` |
| P29 | 文献和引用补强 | 从候选文献到正式引用，复核 DOI、引用格式和文献边界 | `literature-review`、`citation-management`、`zotero-literature-link`、`Zotero` |
| P30 | 图示与版面升级 | Mermaid 图、科学示意图、slides 出口和章节版面更新 | `markdown-mermaid-writing`、`scientific-schematics`、`scientific-slides` |
| P31 | 数据分析流程补强 | 化合物、MD、对接和知识图谱 dry-run 流程 | `datamol`、`rdkit`、`medchem`、`molecular-dynamics`、`diffdock`、`networkx` |
| P3 | 方法卡可执行化 | 第 3-5 章方法卡补输入、命令、输出、质控点和文献锚点 | `ai-md-router`、`takenote`、必要时 `Life Science Research` |
| P4 | 文献候选正式提升 | 从候选表选文献，导出 BibTeX，更新 `zotero-map.tsv` 和文献笔记 | `zotero-literature-link`、`Zotero`、`Life Science Research` |
| P5 | Zotero 暂缓条目收敛 | 复核导出异常条目，必要时用 DOI/Crossref/出版社元数据人工确认 | `zotero-literature-link`、`Zotero`、必要时 `Life Science Research` |
| P6 | Obsidian 使用体验 | 首页、标签、反链、常用查询、模板 | `takenote`、`update-vault` |
| P7 | 自动维护检查 | 一键检查断链、未索引附件、缺失 BibTeX key、OCR/章节覆盖 | `update-vault` |
| P9 | LLM Wiki Agent | 根索引、日志、ingest/query/lint 工作流、本地 Git 版本史 | `ai-md-router`、`ingest-source`、`query-wiki`、`wiki-lint`、`update-vault` |

## 全局 Codex skills

| Skill | 触发场景 | 必读文件 | 输出 |
|:---|:---|:---|:---|
| `scientific-writing` | 教材正文、论文式段落、章节长文重写 | `book/docs/resources/style-guide.md`、相关章节 | 教材化正文和段落结构建议 |
| `literature-review` | 章节文献补强、综述线索、研究问题背景 | `references/`、相关文献笔记 | 文献候选和证据边界 |
| `citation-management` | DOI/题名/作者/期刊元数据复核 | `references/references.bib`、`zotero-map.tsv` | 引用元数据和 BibTeX 候选 |
| `peer-review` | 章节审稿、缺口清单、方法风险评估 | 相关章节、方法卡和 claims 矩阵 | 审稿意见和修改建议 |
| `scientific-critical-thinking` | 证据强度、bias、overclaim 检查 | `07_研究工作台/证据与claims矩阵.md` | claim-evidence status 和边界降级 |
| `markdown-mermaid-writing` | 文本化图谱、流程图和章节结构图 | `book/docs/`、`07_研究工作台/实体索引.md` | Mermaid 图和 Markdown 图示 |
| `scientific-schematics` | 科学示意图和 Imagegen/BioRender prompt 设计 | `book/docs/resources/imagegen-prompts.md` | 图示构图和 prompt |
| `datamol`、`rdkit`、`medchem` | 化合物库处理、描述符、筛选规则 | 方法卡、实验模板和输入表 | AIDD dry-run 流程和代码案例 |
| `molecular-dynamics`、`diffdock` | MD/对接教学流程和边界说明 | 第 3/4 章方法卡和实验模板 | dry-run、QC 和结果解释边界 |

## 历史项目内规则

| Skill | 触发场景 | 必读文件 | 输出 |
|:---|:---|:---|:---|
| `ai-md-router` | 用户说“继续整理”“下一步计划”“该用哪个插件/skill”，或任务横跨章节、文献、方法、实验 | `CLAUDE.md`、本文件、相关 `_index.md` | 路由决策和阶段计划 |
| `ingest-source` | 新 PDF、网页、文献、实验结果、附件或维护报告进入项目 | `CLAUDE.md`、`index.md`、`00_项目说明/LLM Wiki运行手册.md`、相关 `_index.md` | 摄入计划、待更新页面、`takenote` 写入建议和 `update-vault` 验收建议 |
| `query-wiki` | 基于知识库提问、跨章节比较、综合方法线、生成可沉淀答案 | `CLAUDE.md`、`index.md`、相关 `_index.md` 和具体笔记 | 引用已有页面的回答；必要时交给 `takenote` 沉淀 |
| `wiki-lint` | 检查 LLM Wiki 健康度、孤立页、重复概念、矛盾候选和待补来源 | `CLAUDE.md`、`index.md`、`00_项目说明/概念关系规范.md`、所有 `_index.md` | LLM Wiki 健康报告，并联动 `update-vault` 机械检查 |
| `takenote` | 记录想法、摘要 PDF/附件、整理运行结果、写方法笔记或实验记录 | `CLAUDE.md`、目标目录 `_index.md` | 正式 Markdown 笔记和索引更新 |
| `zotero-literature-link` | 按主题查 Zotero、建立文献候选、补 BibTeX、更新文献映射 | `references/zotero-map.tsv`、`03_文献笔记/_index.md` | 候选表、正式映射、文献笔记 |
| `update-vault` | 重建索引、检查断链、附件遗漏、OCR/章节覆盖、BibTeX key | 一级目录 `_index.md`、`references/zotero-map.tsv` | 维护报告和问题清单 |

## 插件调用规则

| 插件/skill | 何时调用 | 禁止或限制 |
|:---|:---|:---|
| `Zotero` | 本地文献检索、导出 BibTeX、检查 item key/BibTeX key、生成候选清单 | 不写入 Zotero、不复制 PDF，除非用户明确要求 |
| `Chrome` | 用户点名 `@chrome`，或需要浏览器登录态、页面渲染、远程课程页面截图/检查 | 不读取 cookies、密码或浏览器隐私数据 |
| `Life Science Research` | PubMed/PMC/PDB/UniProt/AlphaFold 等外部生命科学证据交叉验证 | 不把单次数据库命中当成定论，记录来源和限制 |
| `pdf` | PDF 版面检查、OCR、课件全文提取质量复核 | 不覆盖原始 PDF |
| `pptx-extractor` | PPTX 课件转 Markdown | 不移动原始 PPTX |
| `doc` | DOCX 网盘链接、说明文档、实验记录文档提取 | 不改原 DOCX，除非用户要求 |
| `superpowers:verification-before-completion` | 声称完成前 | 必须有新鲜验证输出 |

## AI_MD 全局项目规则

| Codex skill | 来源 | 用途 |
|:---|:---|:---|
| `ai-md-router` | `.claude/skills/ai-md-router` | 宽泛任务路由和阶段推进。 |
| `ai-md-ingest-source` | `.claude/skills/ingest-source` | 新来源摄入和影响面判断。 |
| `ai-md-query-wiki` | `.claude/skills/query-wiki` | 基于知识库回答和沉淀判断。 |
| `ai-md-takenote` | `.claude/skills/takenote` | 正式笔记写入和索引更新。 |
| `ai-md-update-vault` | `.claude/skills/update-vault` | 索引、链接、附件、引用和 raw 边界验收。 |
| `ai-md-wiki-lint` | `.claude/skills/wiki-lint` | 高层健康检查和图谱问题识别。 |
| `ai-md-zotero-literature-link` | `.claude/skills/zotero-literature-link` | Zotero/BibTeX 映射和文献候选。 |

## 自动调用流程

1. 先读 `CLAUDE.md` 和本文件。
2. 判断任务属于记录、文献、维护、网页、外部证据、文件提取还是跨模块整理。
3. 选择最小必要集合：AI_MD 本地索引和历史项目规则优先；需要专业写作、文献、图示或数据流程时调用全局 Codex skills；插件只在需要外部系统或浏览器/Zotero 能力时调用。
4. 先判断 Wiki 轨还是 Book 轨。Wiki 轨写入或更新 Markdown 时同步 `_index.md`，但不更新 `book/` 或 `正文.md`。
5. 涉及 Zotero 时同时记录 Zotero item key 和 BibTeX key；候选先进入 `references/zotero-candidates-YYYY-MM-DD.tsv`。
6. 完成前运行对应轨道验证，并在维护报告中记录通过项和待人工确认项；Book 验证不进入默认 Wiki 维护。

## LLM Wiki Agent联用规则

| 场景 | 固定链路 | 说明 |
|:---|:---|:---|
| 新资料进入 | `ai-md-router` -> `ingest-source` -> `takenote` -> `update-vault` | `ingest-source` 只做来源识别和影响面判断，规范写入交给 `takenote`，验收交给 `update-vault`。 |
| 研究问题进入 | `query-wiki` -> 读取索引和笔记 -> 必要时 `takenote` -> `update-vault` | 临时回答不强制写入；有长期价值的综合、比较、开放问题才沉淀。 |
| 周期维护 | `wiki-lint` -> `update-vault` -> 问题清单 | `wiki-lint` 看概念层和关系层，`update-vault` 看索引、链接、附件、BibTeX 和 OCR/章节覆盖。 |
| 文献补强 | `ai-md-router` -> `zotero-literature-link` -> `takenote` -> `update-vault` | 候选文献先进入候选表，确认后再更新 `zotero-map.tsv`、`references.bib` 和文献笔记。 |
| 在线书更新 | `ai-md-router` -> Book 轨 -> `AGENTs.md` -> `大纲.md`/本章大纲/正文 | 必须由用户明确触发；不属于 `/update-vault` 默认链路。 |

## 可复用建库 skill

本项目的 LLM Wiki 建库方法已提炼为全局 Codex skill：

- 位置：`C:/Users/xsui/.codex/skills/building-llm-wiki/`
- 触发场景：把其他项目整理成 LLM Wiki、第二大脑、Obsidian vault、AI 原生知识库，或需要 raw sources / wiki / schema 三层建库、typed relations、Zotero/BibTeX provenance 和本地维护 skill。
- 与本项目关系：AI_MD 现阶段保留项目内 `.claude/skills/` 作为历史规则来源；新增第三方技能统一安装为全局 Codex skills。`building-llm-wiki` 用于维护 raw/wiki/schema 分层，也可作为后续 P27 迁移项目规则的参考。
- 校验脚本：`C:/Users/xsui/.codex/skills/building-llm-wiki/scripts/validate_llm_wiki.py`

## P3方法卡可执行化建议

优先处理第 3-5 章，因为它们最接近后续实验落地：

- 第 3 章：对接/虚拟筛选方法卡补受体准备、配体准备、box、score、top pose 复核、结果表模板。
- 第 4 章：MD/BioEmu 方法卡补系统准备、轨迹指标、代表构象、AI 采样与物理 MD 的区别。
- 第 5 章：Boltz2/亲和力方法卡补 YAML、输入链/配体、输出文件、置信度、亲和力解释和实验记录模板。

## P5/P6当前策略

- Zotero 本地 API 可读时优先使用 Zotero 自动导出 BibTeX。
- 如果 Zotero item 可确认但 BibTeX 导出异常，可用 DOI、Crossref、PMC 或出版社页面人工确认 BibTeX，并在 `references.bib` 的 `note` 字段和维护报告中标注。
- Obsidian 优化只新增 Markdown 入口和模板，不默认创建 `.obsidian/` 配置。
