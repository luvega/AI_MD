---
name: ingest-source
description: 当用户向 AI_MD 添加或要求处理新的 PDF、网页、文献、实验结果、附件、维护报告或提到 ingest/source/摄入 时使用。
---

# ingest-source

把新来源纳入 AI_MD LLM Wiki。核心原则：先识别来源和影响面，再交给 `takenote` 写入，最后交给 `update-vault` 验收。

## 先读什么

1. `CLAUDE.md`
2. `index.md`
3. `00_项目说明/LLM Wiki运行手册.md`
4. 相关目录 `_index.md`

## 流程

1. 判断来源类型：PDF、网页、Zotero 文献、实验结果、表格、压缩包、想法、维护报告。
2. 列出要新建或更新的页面，以及关系类型：`derived_from`、`supports`、`updates`、`applies_to`。
3. 调用或遵循 `takenote` 写入规范 Markdown。
4. 更新对应 `_index.md`、根 `index.md` 和 `log.md`。
5. 调用或建议 `update-vault` 验收。

## 边界

- 不移动、不删除原始资料。
- 不跳过 `takenote` 直接写散乱页面。
- 不把未验证推断写成确定 claim。
- 不把新增来源自动写入教材正文或 `book/`；如来源影响教材，只记录 Book 轨待办。
