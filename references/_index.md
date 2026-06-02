# references - 索引

| 文件 | 类型 | 一句话说明 | 关联原始文件 | 关联 Zotero 条目 |
|:---|:---|:---|:---|:---|
| [references.bib](references.bib) | bibliography | 从 Zotero 筛出的本项目核心文献 BibTeX 条目。 | Zotero local API | 多个 |
| [zotero-map.tsv](zotero-map.tsv) | reference-map | 主题、Zotero item key、BibTeX key、文献笔记和章节的映射表。 | Zotero local API | 多个 |
| [zotero-candidates-2026-05-30.tsv](zotero-candidates-2026-05-30.tsv) | candidate-map | 本轮 Zotero 检索候选及 P4/P5 正式提升、人工确认提升状态。 | Zotero local API、Crossref/出版社元数据 | 多个候选 |
| [zotero-candidates-2026-05-31-P14.tsv](zotero-candidates-2026-05-31-P14.tsv) | candidate-map | P14 第六章 Nature 综述和第八章补充 PDF 的 Zotero/BibTeX 锚定记录。 | Zotero local API、Crossref/DOI 元数据 | `TPR3JY6N`, `QXKW6K78`, `YUMKNHSK`, `Y4ARSYCQ`, `V6Y5EEZL` |
| [literature-audit-2026-06-02-P29.tsv](literature-audit-2026-06-02-P29.tsv) | reference-audit | P29 第 3/5/6/8 章 book_map 引用覆盖审计表。 | `book/book_map.toml`, `references/references.bib`, `references/zotero-map.tsv` | 多个 |
| [zotero-candidates-2026-06-02-P29.tsv](zotero-candidates-2026-06-02-P29.tsv) | candidate-map | P29 Chai-1、RFD3/RFdiffusion3 和 BindCraft 正式版本补强候选；P32/P33 已正式化。 | GitHub、PubMed/PMC、Nature/DOI 元数据 | `5286JS9F`, `T2M6L289`, `UIPWC5CR` |
| [literature-upgrades-2026-06-02-P32.tsv](literature-upgrades-2026-06-02-P32.tsv) | reference-upgrade | P32 把 Chai-1、RFD3/RFdiffusion3 和 BindCraft Nature 2025 写入正式 BibTeX；P33 已回写真实 Zotero key。 | CrossRef/DOI 元数据、Zotero local API | `5286JS9F`, `T2M6L289`, `UIPWC5CR` |
| [zotero-upgrades-2026-06-02-P33.tsv](zotero-upgrades-2026-06-02-P33.tsv) | reference-map | P33 Zotero 正式锚点补齐表，记录 Chai-1 导入、RFdiffusion3 重复项 canonical 选择和 BindCraft 2025 已有条目。 | Zotero local API、Zotero Connector | `5286JS9F`, `T2M6L289`, `UIPWC5CR` |
