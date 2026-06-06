---
title: "在线书籍阶段报告索引"
created: 2026-06-02
type: project-doc
status: active
topics: [online-book, maintenance, reports]
source_files: ["polish-report.md", "p34-readability-report.md", "p35-detemplate-report.md", "p36-figure-caption-report.md", "p37-caption-compaction-report.md", "p39-reviewer-revision-report.md"]
wiki_role: maintenance
source_count: 6
last_reviewed: 2026-06-06
claims:
  - "p38_reports_removed_from_book_content_2026_06_02"
  - "p39_reviewer_revision_2026_06_06"
relations:
  - type: supports
    target: "../../book/docs/index.md"
  - type: supports
    target: "../../book/mkdocs.yml"
  - type: supports
    target: "p39-reviewer-revision-report.md"
---
# 在线书籍阶段报告索引

本目录保存 P25 之后的在线书籍阶段性维护报告。它们用于项目审计和后续 Agent 交接，不作为 MkDocs 在线教材内容发布。

| 阶段 | 报告 | 说明 |
|:---|:---|:---|
| P25 | [正文润色报告](polish-report.md) | 记录 reverse outline、claim-evidence map 和正文润色边界。 |
| P34 | [中文教材可读性增强报告](p34-readability-report.md) | 记录中等扩写、教材讲解风格和可读性审计。 |
| P35 | [去模板化报告](p35-detemplate-report.md) | 记录章节专属化修订和重复句审计。 |
| P36 | [图注出版规范化报告](p36-figure-caption-report.md) | 记录图号、图注、alt text 和图示边界。 |
| P37 | [图注编号解释合并报告](p37-caption-compaction-report.md) | 记录编号解释并入图注和版式压缩。 |
| P39 | [审稿导向教材修订报告](p39-reviewer-revision-report.md) | 记录 academic-research-suite 审稿框架下的章节去模板化、文献使用说明、案例走读和 P39 审计器。 |

## 边界

- 本目录可以被根索引和项目说明索引引用。
- 本目录不得加入 `book/mkdocs.yml` 课程资源导航。
- 不把本目录报告复制到 `book/docs/resources/`。
