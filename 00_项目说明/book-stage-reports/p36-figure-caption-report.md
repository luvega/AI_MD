---
title: "P36 图注规范化报告"
created: 2026-06-02
type: resource-report
status: active
topics: [online-book, figures, captions, p36]
source_files: ["book/docs/chapters/", "book/docs/resources/screenshot-index.md", "tools/audit_book_figures.py", "tests/test_audit_book_figures.py"]
wiki_role: maintenance
source_count: 4
last_reviewed: 2026-06-02
claims:
  - "p36_figure_caption_standard_2026_06_02"
relations:
  - type: updates
    target: "../P40_旧版在线图书删除记录.md"
  - type: supports
    target: "../P40_旧版在线图书删除记录.md"
---
# P36 图注规范化报告

## Summary

P36 将在线书籍 8 个主章节中的图像与图示统一纳入出版式图注规则。每章保留 4 类图位：Imagegen 知识图谱、Mermaid 结构图、Imagegen 流程解释图和软件操作截图；每张图均改为 `图X.Y` 编号，并在图下方给出可独立阅读的详细图注。

本轮不新增科学事实、不新增文献、不新增实验结果，也不重做 Imagegen 图。图注只负责解释图中信息、阅读顺序和证据边界；真实参数、术语、代码和 QC 标准仍以正文、表格和代码块为准。

## Figure System

| 图位 | 范围 | 图注重点 |
|:---|:---|:---|
| 图X.1 | 每章 Imagegen 知识图谱 | 说明中心概念、编号节点、知识入口和不承载精确参数的边界。 |
| 图X.2 | 每章 Mermaid 结构图 | 说明箭头代表阅读或记录依赖，不替代真实运行或实验验证。 |
| 图X.3 | 每章 Imagegen 流程图 | 说明操作顺序、关键节点和记录交接，不代表实验结果。 |
| 图X.4 | 每章软件截图 | 说明 dry-run 界面、文件或表格字段，避免把截图误读成项目结果。 |

## Key Changes

- 更新 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md`，为 32 个图位补齐编号、标题、图下注释和来源边界。
- 调整所有章节图片 alt text，使其包含对应 `图X.Y` 编号和图题。
- 将 `book/docs/resources/screenshot-index.md` 从图片预览表改为文件链接表，避免资源页出现未编号图片。
- 新增 `tools/audit_book_figures.py`，检查图号顺序、图注格式、图注长度、边界词、图片 alt text 和章节外图片。
- 新增 `tests/test_audit_book_figures.py`，覆盖有效图注、错号图注、缺编号 alt text 和章节外图片四类场景。

## Validation Snapshot

| 验收项 | 结果 |
|:---|:---|
| 主章节数量 | 8 |
| 图位总数 | 32 |
| 每章最少图位 | 4 |
| 图注审计错误 | 0 |

正式验收仍以本轮最终命令输出为准。

## Boundary

Imagegen 图和 Mermaid 图是教学示意图，不作为精确数据图。软件截图为本地 dry-run 或教学界面截图，用于说明操作入口和记录字段，不代表实验结果。章节图注不得扩大 docking score、predicted affinity、RFdiffusion/RFD3、Chai-1 aggregate score 或文献案例的证据强度。
