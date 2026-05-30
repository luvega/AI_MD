---
title: "AI_MD LLM Wiki 操作日志"
created: 2026-05-30
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, log]
wiki_role: maintenance
source_count: 2
last_reviewed: 2026-05-30
source_files: ["CLAUDE.md"]
zotero_items: []
bibtex_keys: []
related: ["index.md", "00_项目说明/LLM Wiki运行手册.md"]
claims: [p11_schema_enhancement_2026_05_30]
relations:
  - type: depends_on
    target: "CLAUDE.md"
  - type: updates
    target: "index.md"
---

# AI_MD LLM Wiki 操作日志

本文件为追加式日志。新条目格式固定为：

`## [YYYY-MM-DD] operation | title`

允许的 `operation`：`ingest`、`query`、`update`、`lint`、`zotero`、`ocr`、`git`、`maintenance`。

## [2026-05-30] bootstrap | AI_MD LLM Wiki Agent 落地

- 按 Karpathy LLM Wiki 模式建立 AI_MD 专用第二大脑规则。
- 新增根 `index.md`、根 `log.md`、LLM Wiki 说明、运行手册、概念关系规范。
- 明确 `ai-md-router` 总调度、`takenote` 知识写入、`update-vault` 维护验收的联用关系。

## [2026-05-30] update | 扩展本地 LLM Wiki skills

- 新增 `ingest-source`、`query-wiki`、`wiki-lint`。
- 更新 `ai-md-router`、`takenote`、`update-vault`、`zotero-literature-link`，纳入 LLM Wiki Agent 工作流。

## [2026-05-30] git | 初始化本地版本史

- 执行 `git init` 并做首次本地提交。
- 不配置 remote，不 push。
- `.gitignore` 忽略易变 Obsidian workspace、缓存、临时文件和大型不可变二进制原始资料，不忽略核心 Markdown、BibTeX、TSV、skills 或原始资料索引。

## [2026-05-30] lint | LLM Wiki / update-vault 验收

- 验证根索引、目录索引、skills、BibTeX 映射、Markdown 链接和 Git 状态。
- 结果以本轮最终验证输出为准。

## [2026-05-30] maintenance | P9 LLM Wiki Agent落地报告

- 新增 `00_项目说明/知识库维护报告-2026-05-30-P9-LLM-Wiki-Agent落地.md`。
- 把根 `index.md`、`log.md`、LLM Wiki 说明文档和新增 skills 纳入 `00_项目说明/_index.md`、Obsidian 入口和使用说明。

## [2026-05-30] lint | P10 wiki-lint 健康检查

- 执行 P10 高层健康检查，覆盖 managed Markdown、生成式 PDF 提取页面、附件索引、Markdown 链接和 Zotero/BibTeX 映射。
- 修复 `references/zotero-map.tsv` 和 `references/zotero-candidates-2026-05-30.tsv` 未进入附件清单的问题。
- 维护报告写入 `00_项目说明/知识库维护报告-2026-05-30-P10-wiki-lint健康检查.md`。

## [2026-05-30] update | P11 schema 增强

- 只做 schema 增强，不扩写研究内容。
- 给核心方法卡、文献笔记、LLM Wiki 规则页和 P9/P10 维护报告补 `wiki_role`、`claims` 和 typed `relations`。
- 新增 `00_项目说明/知识库维护报告-2026-05-30-P11-schema增强.md`。
