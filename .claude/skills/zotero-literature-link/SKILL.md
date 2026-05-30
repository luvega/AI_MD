---
name: zotero-literature-link
description: 当用户想按主题检索 Zotero、为 AI_MD 课程章节补文献、生成文献笔记、更新 references.bib 或维护 zotero-map.tsv 时使用。
---

# zotero-literature-link

按主题把 Zotero 文献连接到 AI_MD 项目。它负责文献检索、候选、BibTeX 和映射；内容写入仍遵守 `takenote` 和 LLM Wiki 关系规范。

## 先读什么

1. 读取 `CLAUDE.md`。
2. 读取根 `index.md`。
3. 读取 `references/zotero-map.tsv`，避免重复映射。
4. 读取 `03_文献笔记/_index.md`，判断是否已有文献笔记。

## Zotero 检索

使用本地 Zotero helper：

```powershell
python "C:\Users\xsui\.codex\plugins\cache\openai-curated\zotero\fef63ecf\skills\zotero\scripts\zotero.py" status --json
python "C:\Users\xsui\.codex\plugins\cache\openai-curated\zotero\fef63ecf\skills\zotero\scripts\zotero.py" search "<query>" --with-bibtex-keys --json
```

如果 Windows 控制台出现编码问题，先设置：

```powershell
$env:PYTHONIOENCODING='utf-8'
```

## 处理流程

1. 根据主题检索 Zotero。
2. 先判断是“候选补强”还是“正式入库”。
3. 候选补强：写入 `references/zotero-candidates-YYYY-MM-DD.tsv` 和 `03_文献笔记/Zotero文献补强候选.md`，不改 `references.bib` 和 `zotero-map.tsv`。
4. 正式入库：选择与课程章节最相关的 3-10 条文献。
5. 导出或补充 BibTeX 到 `references/references.bib`。
6. 在 `references/zotero-map.tsv` 增加映射行。
7. 在 `03_文献笔记/` 新建或更新文献笔记。
8. 更新 `03_文献笔记/_index.md`、必要时更新根 `index.md`。
9. 向 `log.md` 追加 `zotero` 或 `update` 记录。
10. 用 `update-vault` 验证 `references.bib`、`zotero-map.tsv`、候选表和文献笔记一致性。

## 输出要求

- 明确区分 Zotero item key 和 BibTeX key。
- 如果 Zotero 导出的 BibTeX key 重复或错误，使用本项目本地 alias，并在笔记中说明。
- 不导入新文献到 Zotero，除非用户明确要求。
- 不复制 Zotero PDF，除非用户明确要求。
- 不跳过 `takenote` 的笔记格式要求。
