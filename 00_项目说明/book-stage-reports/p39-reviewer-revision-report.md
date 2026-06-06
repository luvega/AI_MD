---
title: "P39 审稿导向教材修订报告"
created: 2026-06-06
type: maintenance-report
status: active
topics: [online-book, peer-review, readability, evidence-boundary, p39]
source_files: ["book/docs/chapters/chapter-01.md", "book/docs/chapters/chapter-08.md", "tools/audit_book_review_readiness.py", "tools/audit_book_readability.py"]
wiki_role: maintenance
source_count: 4
last_reviewed: 2026-06-06
claims:
  - "p39_reviewer_revision_2026_06_06"
relations:
  - type: updates
    target: "../../book/docs/chapters/chapter-01.md"
  - type: updates
    target: "../../book/docs/chapters/chapter-08.md"
  - type: supports
    target: "../../tools/audit_book_review_readiness.py"
  - type: supports
    target: "../../book/book_map.toml"
---
# P39 审稿导向教材修订报告

P39 使用 `academic-research-suite / academic-paper-reviewer` 的多视角审稿框架，对在线教材第 1-8 章做了一轮 Major Revision 级正文修订。修订目标不是新增科学事实，而是把 P34/P35 后仍残留的模板化表达改成章节专属叙事，并让文献、dry-run、案例走读和证据边界更容易被读者连续理解。

## 修改范围

- 8 个主章节保留原有一级结构，重写 `本章导读`、`学习目标`、`核心概念`、`方法流程`、`关键文献`、`使用边界与常见误读` 和 `延伸阅读与下一步` 的解释性正文。
- 每章 `关键文献` 增加 `文献使用说明`，说明文献在本章中支撑方法、benchmark、边界或案例；正式引用列表仍只展示可读参考文献和 100 字以内内容简介。
- 第 3/5/6/8 章新增 `案例走读`，分别覆盖 docking shortlist、predicted affinity 解释、RFdiffusion/RFD3 设计 QC 和 claim-evidence-boundary 项目池决策。
- 新增 `tools/audit_book_review_readiness.py` 与对应单元测试，检查模板句残留、文献使用说明、重点章节案例走读、高风险 claim 边界和阶段报告未进入在线教材资源层。

## 审稿要点处理

| 审稿视角 | P39 处理 |
|:---|:---|
| EIC | 减少维护说明式语言，把章节导读改为读者问题场景。 |
| 方法审稿 | 增加章节级执行链、失败点、交接条件和 P39 审计器。 |
| 领域审稿 | 第 3/5/6/8 章继续保护 `docking score`、`predicted affinity`、`RFdiffusion/RFD3`、`Chai-1 aggregate score` 等边界。 |
| 跨学科教学 | 将图、代码、截图和 dry-run 组织为案例走读任务。 |
| Devil's Advocate | 移除 P34/P35 残留模板句，避免教材读起来像批量替换文本。 |

## 边界

- 本轮不新增原始素材，不重做 Imagegen 图，不新增实验结果。
- 不手工改写 `<!-- refs:start -->...<!-- refs:end -->` 内的正式参考文献条目。
- 不在在线教材页面显示 BibTeX key 或 Zotero item key。
- 阶段报告继续保存在 `00_项目说明/book-stage-reports/`，不进入 `book/docs/resources/` 或 MkDocs 导航。

## 验收命令

```powershell
python -m unittest discover -s tests
python tools\audit_book_review_readiness.py --book-root book\docs
python tools\audit_book_readability.py --book-root book\docs --min-prose-chars-per-chapter 3500 --min-priority-section-chars 350
python tools\validate_online_book.py --map book\book_map.toml --book-root book\docs --min-chapter-chars 5000 --require-nature-refs --require-imagegen --require-mermaid
python -m mkdocs build -f book\mkdocs.yml --strict
python C:\Users\xsui\.codex\skills\building-llm-wiki\scripts\validate_llm_wiki.py . --raw-dir 06_原始学习素材
python tools\graph_health.py . --json --stale-days 180
```

## 验收结果

| 项目 | 结果 |
|:---|:---|
| 单元测试 | 20 tests, OK |
| P39 审稿就绪审计 | chapters 8, report files in book resources 0, errors 0 |
| 可读性审计 | min prose chars 4011, min priority section chars 350, errors 0 |
| 图注审计 | chapters 8, figures 32, errors 0 |
| 在线书籍校验 | errors 0 |
| MkDocs strict build | build 成功；Material for MkDocs 显示 MkDocs 2.0 未来兼容性提示，不影响本次构建 |
| LLM Wiki 校验 | warnings 0, errors 0 |
| 图谱体检 | exit 0；relation_targets_missing 0；仍保留历史 missing `last_reviewed` 和孤立模板页建议 |

## 下一步

下一轮建议进入 P40 文献复核或真实小样本运行二选一。若优先公开教材质量，应先复核参考文献元数据和 DOI；若优先研究工作台，应从第 3/5/6/8 章选择一个 dry-run 升级为正式实验记录。
