# 附录 D AI 回归评测任务

本附录用于验收后续 AI Agent 是否能从在线书籍和 AI_MD 知识库中答出正确路径、引用、边界和下一步。

## 核心评测任务

| task_id | 标准问题 | 应读章节 | 合格答案必须包含 |
|:---|:---|:---|:---|
| `eval:ch8-vs-literature-boundary` | 第八章正向虚拟筛选有哪些可借鉴但不能当作本项目结果的文献？ | [第 8 章](../chapters/chapter-08.md) | `sui_targeting_2026`、`shen_structure-based_2026`、`tomarchio_reproducible_2026` 和文献案例边界 |
| `eval:rfd3-record-required` | RFD3 设计记录必须包含哪些参数？ | [第 6 章](../chapters/chapter-06.md) | motif、contig、链定义、input、seed、diffusion settings、ProteinMPNN 后处理 |
| `eval:chai1-score-boundary` | Chai-1 aggregate score 应该如何解释？ | [第 8 章](../chapters/chapter-08.md) | 排序/复核信号、不能当真实 Kd、需要界面 QC 和正式锚点 |
| `eval:boltz2-affinity-qc` | Boltz2 亲和力输出需要哪些 QC？ | [第 5 章](../chapters/chapter-05.md) | 输入 YAML、结构置信度、链/配体状态、口袋合理性和对照 |
| `eval:docking-score-use` | docking score 能否直接比较不同软件或不同受体准备流程？ | [第 3 章](../chapters/chapter-03.md) | 不能直接比较、需要 top pose QC、score 只是排序信号 |

## 验收规则

- 回答必须给出章节入口、AI_MD 来源路径、BibTeX key 和使用边界。
- 只复述流程、不说明边界，判为未通过。
- 把文献案例写成本项目结果，判为未通过。

## 来源索引

- AI 回归评测集：`07_研究工作台/AI回归评测集.md`
- 图谱体检工具：`tools/graph_health.py`
- 在线书籍校验工具：`tools/validate_online_book.py`
