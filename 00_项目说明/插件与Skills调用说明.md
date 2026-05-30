---
title: "插件与Skills调用说明"
created: 2026-05-30
type: project-doc
status: active
topics: [plugin-routing, skills, zotero, chrome, life-science-research, workflow]
source_files: ["CLAUDE.md", ".claude/skills"]
zotero_items: []
bibtex_keys: []
related: ["知识库使用说明.md", "../.claude/skills/ai-md-router/SKILL.md"]
---
# 插件与Skills调用说明

这份说明用于让 AI_MD 后续整理任务自动选择必要插件和本地 skill。原则是先用本项目本地索引和规则，只有确实需要外部资料、浏览器状态或 Zotero 库时才调用插件。

## 下一步计划

| 阶段 | 目标 | 产物 | 优先插件/skill |
|:---|:---|:---|:---|
| P3 | 方法卡可执行化 | 第 3-5 章方法卡补输入、命令、输出、质控点和文献锚点 | `ai-md-router`、`takenote`、必要时 `Life Science Research` |
| P4 | 文献候选正式提升 | 从候选表选文献，导出 BibTeX，更新 `zotero-map.tsv` 和文献笔记 | `zotero-literature-link`、`Zotero`、`Life Science Research` |
| P5 | Zotero 暂缓条目收敛 | 复核导出异常条目，必要时用 DOI/Crossref/出版社元数据人工确认 | `zotero-literature-link`、`Zotero`、必要时 `Life Science Research` |
| P6 | Obsidian 使用体验 | 首页、标签、反链、常用查询、模板 | `takenote`、`update-vault` |
| P7 | 自动维护检查 | 一键检查断链、未索引附件、缺失 BibTeX key、OCR/章节覆盖 | `update-vault` |
| P9 | LLM Wiki Agent | 根索引、日志、ingest/query/lint 工作流、本地 Git 版本史 | `ai-md-router`、`ingest-source`、`query-wiki`、`wiki-lint`、`update-vault` |

## 本地Skills

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

## 自动调用流程

1. 先读 `CLAUDE.md` 和本文件。
2. 判断任务属于记录、文献、维护、网页、外部证据、文件提取还是跨模块整理。
3. 选择最小必要集合：本地 skill 优先，插件只在需要外部能力时调用。
4. 写入或更新 Markdown 时同步 `_index.md`。
5. 涉及 Zotero 时同时记录 Zotero item key 和 BibTeX key；候选先进入 `references/zotero-candidates-YYYY-MM-DD.tsv`。
6. 完成前运行验证，并在维护报告中记录通过项和待人工确认项。

## LLM Wiki Agent联用规则

| 场景 | 固定链路 | 说明 |
|:---|:---|:---|
| 新资料进入 | `ai-md-router` -> `ingest-source` -> `takenote` -> `update-vault` | `ingest-source` 只做来源识别和影响面判断，规范写入交给 `takenote`，验收交给 `update-vault`。 |
| 研究问题进入 | `query-wiki` -> 读取索引和笔记 -> 必要时 `takenote` -> `update-vault` | 临时回答不强制写入；有长期价值的综合、比较、开放问题才沉淀。 |
| 周期维护 | `wiki-lint` -> `update-vault` -> 问题清单 | `wiki-lint` 看概念层和关系层，`update-vault` 看索引、链接、附件、BibTeX 和 OCR/章节覆盖。 |
| 文献补强 | `ai-md-router` -> `zotero-literature-link` -> `takenote` -> `update-vault` | 候选文献先进入候选表，确认后再更新 `zotero-map.tsv`、`references.bib` 和文献笔记。 |

## 可复用建库 skill

本项目的 LLM Wiki 建库方法已提炼为全局 Codex skill：

- 位置：`C:/Users/xsui/.codex/skills/building-llm-wiki/`
- 触发场景：把其他项目整理成 LLM Wiki、第二大脑、Obsidian vault、AI 原生知识库，或需要 raw sources / wiki / schema 三层建库、typed relations、Zotero/BibTeX provenance 和本地维护 skill。
- 与本项目关系：AI_MD 继续使用项目内 `.claude/skills/` 作为日常执行入口；`building-llm-wiki` 用于把这套方法迁移到新项目或修复其他知识库 schema。
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
