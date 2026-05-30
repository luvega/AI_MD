---
name: wiki-lint
description: 当用户要求检查 AI_MD LLM Wiki 健康度、孤立页、重复概念、矛盾、过期声明、待补来源或提到 lint/wiki-lint 时使用。
---

# wiki-lint

检查 AI_MD LLM Wiki 的高层健康度，并联动 `update-vault` 做机械一致性验收。

## 先读什么

1. `CLAUDE.md`
2. `index.md`
3. `00_项目说明/概念关系规范.md`
4. 所有一级目录 `_index.md`
5. `references/zotero-map.tsv`

## 检查项

- 孤立页：未出现在根 `index.md` 或目录 `_index.md`。
- 重复概念：同一方法或文献以不同名称出现。
- 矛盾候选：新旧页面对同一方法边界、适用性、结果解释有冲突。
- 缺少来源：明确 claim 没有 BibTeX key、Zotero item key 或原始资料路径。
- 过期声明：候选状态、Zotero 异常、OCR 状态与最新维护报告不一致。
- 机械一致性：调用或复用 `update-vault` 检查附件、断链、BibTeX、PDF/OCR 和章节覆盖。

## 输出

- 只报告问题和建议，不删除、不移动原始资料。
- 内容缺口交给 `takenote`。
- 文献缺口交给 `zotero-literature-link`。
