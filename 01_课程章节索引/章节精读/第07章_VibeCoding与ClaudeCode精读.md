---
title: "第07章 VibeCoding与Claude Code精读"
created: 2026-05-31
type: chapter-deep-note
status: draft
topics: [chapter/07, vibe-coding, claude-code, codex, skills, llm-wiki]
source_files: ["06_原始学习素材/第六章/第六七章RFD3多组分设计.pdf", "06_原始学习素材/第六章/补充资料/claude.txt", "06_原始学习素材/第六章/补充资料/github_skills地址.txt", "06_原始学习素材/第六章/补充资料/ssh.txt"]
zotero_items: []
bibtex_keys: []
related: ["../../00_项目说明/LLM Wiki运行手册.md", "../../00_项目说明/插件与Skills调用说明.md", "../../00_项目说明/LLM Wiki Agent说明.md"]
wiki_role: synthesis
source_count: 4
last_reviewed: 2026-05-31
claims: [p12_chapter_7_ingest_2026_05_31]
relations:
  - type: derived_from
    target: "../../06_原始学习素材/第六章/第六七章RFD3多组分设计.pdf"
  - type: applies_to
    target: "../../00_项目说明/LLM Wiki运行手册.md"
---

# 第07章 VibeCoding与Claude Code精读

## 本章定位

第七章是工具链和 Agent 工作流章节，主题从 RFD3 设计切到 VibeCoding、Claude Code、插件/Skills、项目模式和远程环境。它不直接产生药物设计结论，但会影响本项目后续如何把课程资料、代码、运行结果和知识库维护流程连接起来。

## 核心概念

- VibeCoding 的价值不在“让 AI 直接替代工程判断”，而在把需求、架构、实现、测试、文档和复盘组织成可审查的工作流。
- Claude Code/Codex 这类 Agent 应优先读取项目规则、索引和本地 skills，再决定是否写入知识库或运行工具。
- Skills 适合把稳定工作流沉淀成可复用入口，例如 `ingest-source`、`takenote`、`update-vault` 和 `wiki-lint`。
- SSH、远程 GPU/服务器、GitHub skills 地址等内容属于环境与工具链资料，应作为原始资料索引，不应混入课程方法结论。

## 可执行流程

1. 明确任务是资料摄入、wiki 查询、代码实现、环境配置还是远程运行。
2. 先读 `CLAUDE.md`、`index.md` 和相关 `_index.md`，再决定调用本地 skills。
3. 对稳定流程写入 `.claude/skills/<skill>/SKILL.md`；对项目规则写入 `CLAUDE.md` 或 `00_项目说明/LLM Wiki运行手册.md`。
4. 涉及 SSH、GitHub 地址或账号环境时，只记录路径和用途，不在 wiki 中暴露密钥、token 或私密凭据。
5. 每次 ingest/update 后追加 `log.md`，再运行 `update-vault` 验收。

## 易错点

- 直接把聊天建议当作项目事实写入，而没有原始资料、路径或日志记录。
- 复制网络教程却没有区分本机路径、远程路径、环境变量和账号权限。
- 把技能说明写成泛泛提示词，没有明确输入、输出、边界和验收步骤。
- 在包含 SSH 或账号资料时把私密信息写入 Markdown。

## 本项目落地

- 本项目已经有 `.claude/skills/ai-md-router`、`ingest-source`、`takenote`、`update-vault`、`wiki-lint` 等本地 skills。
- 第七章后续应优先沉淀为“课程工具链/Agent 工作流”说明，而不是药物设计方法卡。
- `06_原始学习素材/第六章/补充资料/claude.txt`、`github_skills地址.txt`、`ssh.txt` 只作为原始工具链附件保留；如需公开或提交，必须先做私密信息检查。

## 来源定位

| 主题 | 来源页 |
|:---|:---|
| VibeCoding 范式转换 | [page-102.md](../../06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-102.md) |
| VibeCoding 工具形态 | [page-107.md](../../06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-107.md) |
| Claude Code 安装/配置/项目模式 | [page-118.md](../../06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-118.md) |
| 插件与 Skills | [page-130.md](../../06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-130.md) |
