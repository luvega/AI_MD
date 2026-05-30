---
name: update-vault
description: 当用户想维护 AI_MD 知识库、重建索引、检查断链、检查附件遗漏、检查 Zotero 映射或提到 /update-vault 时使用。
---

# update-vault

维护 AI_MD 知识库的索引、链接和引用一致性。它是 LLM Wiki Agent 的维护验收器，不负责生成研究内容。

## 先读什么

1. 读取 `CLAUDE.md`。
2. 读取根 `index.md` 和 `log.md`。
3. 读取所有一级知识库目录下的 `_index.md`。
4. 读取 `references/zotero-map.tsv`。
5. 扫描原始资料目录：`06_原始学习素材/`、根目录、`第三章/`、`第四章/`、`第五章/`、`第六章/`。

## 检查项

1. 附件遗漏：确认 PDF、RAR、ZIP、DOCX、TXT、XLSX、HTML、PY、JSON、TSV、CIF 都在 `05_附件索引/附件清单.md` 中出现。
2. 索引一致性：确认每个新增 Markdown 文件出现在所在目录 `_index.md`。
3. 文献一致性：确认 `references/zotero-map.tsv` 中的 BibTeX key 出现在 `references/references.bib`。
4. 断链检查：确认 Markdown 中的相对链接指向存在文件。
5. PDF 全文提取：确认每份规范 PDF 都有 `全文.md`、`pages/page-001.md` 和 `extraction-report.md`，并记录页数、抽取质量和是否建议 OCR。
6. OCR 补充：确认低文本页在 `ocr/page-xxx.ocr.md` 中有补充文本、`OCR quality` 分级和 `Action`，并已追加到对应 `全文.md`。
7. 章节精读覆盖：确认 `01_课程章节索引/章节精读/` 覆盖第 1-5 章，每篇包含本章定位、核心概念、可执行流程、易错点、本项目落地和来源定位。
8. 重复资料提示：只报告，不删除；重复 PDF 放在 `06_原始学习素材/重复PDF待确认/`。
9. LLM Wiki 根索引：确认新增 Markdown 出现在目录 `_index.md` 和根 `index.md`。
10. 日志检查：确认重要 ingest、query、update、lint、zotero、ocr、git、maintenance 操作已追加到 `log.md`。

## 输出报告

维护完成后，在 `00_项目说明/` 新增或更新维护报告，包含：

- 索引更新情况。
- 附件覆盖率。
- PDF 全文提取覆盖率和质量结果。
- OCR 补充覆盖率、语言包和引擎版本。
- OCR 质量分级统计和需要人工整理的页面数量。
- 第 1-5 章结构化精读笔记覆盖情况。
- 缺失或异常 BibTeX key。
- 断链列表。
- 重复或待人工确认资料。
- `index.md` 和 `log.md` 更新情况。
- 需要交回 `takenote` 的内容性缺口。

## 安全规则

- 不删除原始文件。
- 不移动非 PDF 原始资料；PDF 课件可在用户确认后统一归档到 `06_原始学习素材/`。
- 允许检查 Git 状态；只有用户明确要求时才初始化或提交。
- 不写入 Zotero，除非用户明确要求。
- 不生成研究内容；如发现内容缺口，只报告给 LLM Wiki Agent，再由 `takenote` 处理。
