---
title: "P37 图注编号解释合并报告"
created: 2026-06-02
type: resource-report
status: active
topics: [online-book, figures, captions, layout, p37]
source_files: ["book/docs/chapters/", "tools/audit_book_figures.py", "tests/test_audit_book_figures.py", "book/docs/resources/style-guide.md"]
wiki_role: maintenance
source_count: 4
last_reviewed: 2026-06-02
claims:
  - "p37_caption_compaction_2026_06_02"
relations:
  - type: updates
    target: "../../book/docs/chapters/"
  - type: supports
    target: "../../tools/audit_book_figures.py"
---
# P37 图注编号解释合并报告

## Summary

P37 根据版面检查结果，将章节图下方的编号解释表合并进图注。每章的 `图X.1` 知识图谱和 `图X.3` 流程图不再保留独立编号表；节点或流程含义直接写作 `节点编号：1=...` 或 `流程编号：1=...`，放在图注末尾。

本轮不修改图片、不新增科学事实、不新增实验结果，也不改变引用、代码、截图文件和原始素材边界。

## Key Changes

- 移除 8 章知识图谱下方的 `编号 | 正文权威标签` 表格。
- 移除 8 章流程图下方的 `编号 | 流程节点` 表格和“图中编号节点与下表对应”提示。
- 将 16 组编号解释合并到对应图注，保持图注可独立阅读。
- 增强 `tools/audit_book_figures.py`：检查章节中不再残留独立编号表，并要求 `图X.1` / `图X.3` 图注包含内联编号说明。

## Validation Snapshot

| 验收项 | 结果 |
|:---|:---|
| 主章节数量 | 8 |
| 图位总数 | 32 |
| 独立编号解释表 | 0 |
| 图注审计错误 | 0 |

正式验收仍以本轮最终命令输出为准。
