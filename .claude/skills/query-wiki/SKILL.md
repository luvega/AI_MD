---
name: query-wiki
description: 当用户基于 AI_MD 知识库提问、要求综合分析、跨章节比较、生成可沉淀答案或提到 query/wiki/第二大脑 时使用。
---

# query-wiki

基于 AI_MD LLM Wiki 回答问题。核心原则：先查 wiki，再综合；有长期价值的答案沉淀回 wiki。

## 先读什么

1. `CLAUDE.md`
2. `index.md`
3. 与问题相关的目录 `_index.md`
4. 具体方法、文献、实验或维护报告页面

## 流程

1. 判断问题是临时回答还是值得沉淀。
2. 搜索相关页面，优先使用 `rg` 和根 `index.md`。
3. 回答时引用已有页面、原始路径、Zotero item key 或 BibTeX key。
4. 如果答案有长期价值，交给 `takenote` 形成综合笔记、方法补充或开放问题。
5. 写入后更新 `log.md`，并由 `update-vault` 验收。

## 边界

- 不凭空造链接。
- 不用未核验信息覆盖旧结论。
- 临时回答不强制写文件。
