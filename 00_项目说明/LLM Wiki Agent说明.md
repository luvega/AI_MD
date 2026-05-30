---
title: "LLM Wiki Agent 说明"
created: 2026-05-30
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, agent]
wiki_role: concept
source_count: 1
last_reviewed: 2026-05-30
source_files: ["CLAUDE.md", "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"]
zotero_items: []
bibtex_keys: []
related: ["LLM Wiki运行手册.md", "概念关系规范.md", "../index.md", "../log.md"]
---

# LLM Wiki Agent 说明

AI_MD 的 LLM Wiki Agent 采用 Karpathy LLM Wiki 思路：原始资料是不可变 source of truth，Markdown wiki 是持续累积的中间知识层，`CLAUDE.md` 和本地 skills 是约束 Agent 行为的 schema。

## 三层架构

| 层 | 本项目落点 | 规则 |
|:---|:---|:---|
| Raw sources | `06_原始学习素材/`、`第三章/`、`第四章/`、`第五章/`、`第六章/`、`references/` | 原始资料只读，不移动、不删除、不重命名，除非用户明确确认 |
| Wiki | `00_项目说明/`、`01_课程章节索引/`、`02_方法笔记/`、`03_文献笔记/`、`04_实验记录/`、`05_附件索引/`、根 `index.md` 和 `log.md` | LLM 负责创建、更新、交叉引用、维护一致性 |
| Schema | `CLAUDE.md`、`.claude/skills/`、`00_项目说明/LLM Wiki运行手册.md` | 规定写作格式、索引规则、Zotero 联动、ingest/query/lint 流程 |

## Agent 分工

| 组件 | 角色 | 不负责 |
|:---|:---|:---|
| `ai-md-router` | 总调度器，判断任务类型和需要的 skill | 直接写所有内容 |
| `takenote` | 原子写入器，创建或更新规范 Markdown 笔记 | 全库验收 |
| `update-vault` | 维护验收器，检查索引、断链、附件、BibTeX、PDF/OCR 覆盖 | 生成研究内容 |
| `ingest-source` | 新来源摄入流程 | 跳过 `takenote` 或 `update-vault` |
| `query-wiki` | 基于 wiki 的问答与可沉淀输出 | 无依据扩写 |
| `wiki-lint` | 高层健康检查和机械验收调度 | 自动删除或移动资料 |

## 工作原则

- 新资料进入时，不只做检索索引；要把关键内容整合进已有章节、方法、文献或实验页面。
- 回答复杂问题时，先读 `index.md` 和相关 `_index.md`，再综合具体页面。
- 有长期价值的回答要沉淀回 wiki，由 `takenote` 写入，再由 `update-vault` 验收。
- 重要操作必须追加到 `log.md`。
- 发现矛盾、重复概念或过期内容时，不直接覆盖旧结论；先记录关系和待确认项。
