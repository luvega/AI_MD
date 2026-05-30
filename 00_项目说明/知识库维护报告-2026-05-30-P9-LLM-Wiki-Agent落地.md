---
title: "知识库维护报告-2026-05-30-P9-LLM-Wiki-Agent落地"
created: 2026-05-30
type: maintenance-report
status: active
topics: [llm-wiki, wiki-agent, skills, git, maintenance]
source_files: ["CLAUDE.md", "index.md", "log.md", ".claude/skills"]
zotero_items: []
bibtex_keys: []
related: ["LLM Wiki Agent说明.md", "LLM Wiki运行手册.md", "概念关系规范.md", "../index.md", "../log.md"]
wiki_role: maintenance
source_count: 4
last_reviewed: 2026-05-30
claims: []
relations:
  - type: updates
    target: "知识库维护报告-2026-05-30-P7-update-vault全库验收.md"
  - type: derived_from
    target: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
---

# P9 LLM Wiki Agent 落地报告

## 本轮目标

在不移动、不删除、不重命名原始学习资料的前提下，把 AI_MD 从“课程资料知识库”升级为可持续维护的 LLM Wiki 第二大脑：

- 保留现有 Obsidian 入口、Zotero 映射和本地 skills。
- 补齐 raw sources / wiki / schema 三层规则。
- 新增根 `index.md` 和 `log.md`。
- 让 `ai-md-router` 成为总调度，联动 `ingest-source`、`query-wiki`、`wiki-lint`、`takenote`、`zotero-literature-link` 和 `update-vault`。
- 启用本地 Git 版本史；Git 默认记录 Markdown wiki、schema、skills、BibTeX、TSV、脚本和结构化文本，不记录 PDF/RAR/ZIP/Office 等大型不可变原始资料；不配置 remote，不 push。

## 新增内容

| 文件 | 作用 |
|:---|:---|
| `index.md` | 内容型总索引，优先作为 LLM Wiki 和 Obsidian 的项目入口。 |
| `log.md` | 追加式时间线，记录 ingest、query、update、lint、zotero、ocr、git、maintenance 操作。 |
| `00_项目说明/LLM Wiki Agent说明.md` | 说明 AI_MD 如何落实 Karpathy LLM Wiki 模式。 |
| `00_项目说明/LLM Wiki运行手册.md` | 固化 ingest、query、lint、update、zotero 和 git 流程。 |
| `00_项目说明/概念关系规范.md` | 固化 typed relations 和 claim 记录方式。 |
| `.claude/skills/ingest-source/SKILL.md` | 新来源摄入 workflow。 |
| `.claude/skills/query-wiki/SKILL.md` | 基于 wiki 的问答和沉淀 workflow。 |
| `.claude/skills/wiki-lint/SKILL.md` | 高层健康检查 workflow。 |
| `.gitignore` | 忽略本地缓存、临时文件、易变 Obsidian workspace 文件和大型不可变原始二进制资料。 |

## 更新内容

| 文件 | 更新点 |
|:---|:---|
| `CLAUDE.md` | 强化为 LLM Wiki Agent schema，加入三层结构、skill 联用、日志、typed relations 和本地 Git 规则。 |
| `.claude/skills/ai-md-router/SKILL.md` | 升级为总调度入口。 |
| `.claude/skills/takenote/SKILL.md` | 明确只负责规范写入，不负责全库验收。 |
| `.claude/skills/update-vault/SKILL.md` | 明确只负责验收和维护报告，不生成研究内容。 |
| `.claude/skills/zotero-literature-link/SKILL.md` | 明确文献补强需交给 `takenote` 写入、由 `update-vault` 验收。 |
| `00_项目说明/_index.md` | 加入 LLM Wiki 三份说明文档和本报告。 |
| `00_项目说明/知识库使用说明.md` | 加入根索引、日志和 LLM Wiki 入口。 |
| `00_项目说明/插件与Skills调用说明.md` | 加入 ingest/query/lint 三个新增 skill 的联用规则。 |
| `00_项目说明/Obsidian入口.md` | 加入根 `index.md`、`log.md` 和 LLM Wiki 文档入口。 |

## Skill 联用结论

| 场景 | 主流程 |
|:---|:---|
| 新资料进入 | `ai-md-router` -> `ingest-source` -> `takenote` -> `update-vault` -> `log.md` |
| 研究问题进入 | `query-wiki` -> 读取索引和笔记 -> 必要时 `takenote` 沉淀 -> `update-vault` 验收 |
| 周期维护 | `wiki-lint` -> `update-vault` -> 问题清单 -> 必要时回到 `takenote` 或 `zotero-literature-link` |
| 文献补强 | `ai-md-router` -> `zotero-literature-link` -> `takenote` -> `update-vault` |

## 验收结果

| 检查项 | 结果 |
|:---|:---|
| 必要文件 | 11 个必需文件存在，包括根 `index.md`、`log.md`、三份 LLM Wiki 文档、三份新增 skill 和本报告。 |
| 根索引 | `index.md` 已覆盖项目入口、章节索引、方法线索引、文献与 Zotero、实验记录、维护报告、综合与开放问题、最近日志摘要和待确认项。 |
| 目录索引 | `00_项目说明/_index.md` 已加入 LLM Wiki 三份说明文档和本报告。 |
| Skill smoke test | 7 个本地 skill 均有 `name`、`description` 和可执行流程；`ingest-source`、`query-wiki`、`wiki-lint` 已明确联动 `takenote` 与 `update-vault`。 |
| Zotero/BibTeX | `references/zotero-map.tsv` 的 21 行 BibTeX key 均存在于 `references/references.bib`。 |
| Markdown 链接 | 本轮修改的 11 个核心 Markdown 文件相对链接检查通过。 |
| Git | 已初始化本地 Git 并创建首次提交；`git status --short` 为空；未配置 remote。 |
| 大型原始资料 | PDF/RAR/ZIP/Office 等大型不可变原始资料未进入 Git，由 Markdown 索引继续追踪。 |

## 待人工确认

- 后续如果要把 Obsidian Dataview、Web Clipper、固定附件目录写进 `.obsidian/` 配置，需要单独确认，避免覆盖本地偏好。
- 当前只启用本地 Git 版本史，不配置 remote；如需 GitHub 同步，需要另开一步确认 remote、隐私和大文件策略。
- 原始 PDF/RAR/ZIP/Office 资料不进入 Git，依赖 `05_附件索引/附件清单.md` 和 `06_原始学习素材/PDF全文提取总览.md` 追踪。
