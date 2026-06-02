---
title: "P27 Codex项目规则迁移报告"
created: 2026-06-02
type: maintenance-report
status: active
topics: [codex-skills, ai-md-project-rules, migration, p27]
source_files: [".claude/skills", "tools/install_ai_md_project_codex_skills.ps1", "00_项目说明/Codex技能调用矩阵.md"]
zotero_items: []
bibtex_keys: []
related: ["Codex技能调用矩阵.md", "P26_Codex技能集成报告.md", "插件与Skills调用说明.md"]
wiki_role: maintenance
source_count: 3
last_reviewed: 2026-06-02
claims:
  - "AI_MD 自有项目规则已生成并安装为全局 Codex skills。"
  - "现有 .claude/skills 保留为历史来源，不再作为新增第三方技能安装位置。"
relations:
  - type: extends
    target: "P26_Codex技能集成报告.md"
  - type: updates
    target: "Codex技能调用矩阵.md"
  - type: updates
    target: "插件与Skills调用说明.md"
---
# P27 Codex项目规则迁移报告

## 迁移结论

P27 已把 AI_MD 自有项目规则从 `.claude/skills/` 迁移为全局 Codex skills。迁移方式不是删除历史目录，而是保留 `.claude/skills` 作为来源和兼容层，同时生成带 `ai-md-*` 前缀的全局 Codex skills。

实际安装位置：

- `C:\Users\xsui\.codex\skills\ai-md-router`
- `C:\Users\xsui\.codex\skills\ai-md-ingest-source`
- `C:\Users\xsui\.codex\skills\ai-md-query-wiki`
- `C:\Users\xsui\.codex\skills\ai-md-takenote`
- `C:\Users\xsui\.codex\skills\ai-md-update-vault`
- `C:\Users\xsui\.codex\skills\ai-md-wiki-lint`
- `C:\Users\xsui\.codex\skills\ai-md-zotero-literature-link`

安装脚本：

- `tools/install_ai_md_project_codex_skills.ps1`

安装后需要重启 Codex，新的项目规则 skills 才会稳定出现在会话技能列表中。

## 迁移映射

| 历史项目规则 | 全局 Codex skill | 用途 |
|:---|:---|:---|
| `.claude/skills/ai-md-router` | `ai-md-router` | 宽泛任务路由，决定 ingest、query、lint、note、Zotero 或 update 路径。 |
| `.claude/skills/ingest-source` | `ai-md-ingest-source` | 新资料、新实验结果、新文献或维护报告的来源识别和影响面判断。 |
| `.claude/skills/query-wiki` | `ai-md-query-wiki` | 基于 AI_MD 知识库回答、综合和判断是否需要沉淀。 |
| `.claude/skills/takenote` | `ai-md-takenote` | 把长期有价值的内容写入正式 Markdown 笔记并维护索引。 |
| `.claude/skills/update-vault` | `ai-md-update-vault` | 维护索引、链接、附件覆盖、引用映射和校验报告。 |
| `.claude/skills/wiki-lint` | `ai-md-wiki-lint` | 检查孤立页、重复概念、过期 claim、矛盾和图谱健康。 |
| `.claude/skills/zotero-literature-link` | `ai-md-zotero-literature-link` | 连接 Zotero、BibTeX、文献候选和章节文献锚点。 |

## 迁移边界

- `.claude/skills/` 本轮不删除，避免破坏历史文档和既有引用。
- 后续新增专业能力继续安装到全局 Codex skills，而不是 `.claude/skills/`。
- AI_MD 项目规则 skills 只在本项目内使用，仍必须先读 `CLAUDE.md`、`index.md` 和相关 `_index.md`。
- 原始资料目录 `06_原始学习素材/` 继续只读，内容不上传 GitHub。

## 对 P28-P31 的影响

- P28 审稿任务先用 `ai-md-router` 定位章节和来源，再调用 `peer-review`、`scientific-critical-thinking`、`scientific-writing`。
- P29 文献任务先用 `ai-md-zotero-literature-link` 和项目引用映射，再调用 `literature-review`、`citation-management`。
- P30 图示任务先用 `ai-md-query-wiki` 确认概念来源，再调用 `markdown-mermaid-writing`、`scientific-schematics`。
- P31 数据流程任务先用 `ai-md-takenote` 或 `ai-md-update-vault` 约束写入和验收，再调用 `datamol`、`rdkit`、`medchem`、`molecular-dynamics`、`diffdock`。

## 验收记录

- 全局 AI_MD 项目规则技能数：7。
- `.claude/skills` 变更策略：保留历史来源，不新增第三方 skill。
- 需重启 Codex：是。
