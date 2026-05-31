# 第 8 章 研究思路解析：寻靶、虚拟筛选、PPI 与蛋白设计整合

## 本章导读

本章把前七章方法整合为研究设计路线。重点是从文献案例中学习问题拆解、方法组合和结果边界，而不是把补充 PDF 写成本项目已经完成的结果。

## 学习目标

- 能把 UXS1、APE1、IDO1、BabA 和 Chai-1 PPI 案例拆成研究问题。
- 能说明正向虚拟筛选、互作蛋白筛选和蛋白设计之间的连接方式。
- 能区分文献案例、方法假设、项目结果和下一步实验。

## 知识图谱入口

- 章节来源：`01_课程章节索引/章节精读/第08章_计算思路解析精读.md`
- 方法来源：`02_方法笔记/Chai1互作蛋白虚拟筛选.md`
- 实体索引：`07_研究工作台/实体索引.md`
- claims 边界：`07_研究工作台/证据与claims矩阵.md`
- 项目池：`07_研究工作台/研究问题与项目池.md`

## 核心概念

| 概念 | 本章定位 |
|:---|:---|
| target discovery | 从疾病机制、文献和筛选任务中定义靶点 |
| forward virtual screening | 以靶点和候选库为中心的筛选路线 |
| PPI screening | 用结构预测或复合物建模辅助互作候选排序 |
| de novo binder design | 从目标界面出发设计新 binder |
| project workbench | 把课程案例转成用户自己的研究问题、证据和实验队列 |

## 方法流程

1. 选择研究问题，明确靶点、分子或蛋白面板。
2. 进入实体索引，找到对应方法、文献、模板和 claims。
3. 判断材料属于课程资料、文献证据、本项目结果还是研究假设。
4. 选择实验队列中的最小可执行任务。
5. 输出课件、综述、课题申请或实验记录时保留使用边界。

## 关键文献与 BibTeX key

- `sui_targeting_2026`：UXS1/metformin 文献案例。
- `shen_structure-based_2026`：APE1 结构虚拟筛选案例。
- `tomarchio_reproducible_2026`：IDO1 scaffold-aware ML + docking + MD 可复现框架。
- `zhu_novo_2026`：BabA de novo binder 设计案例。
- `yang_w_past_2026`：de novo protein design 综述。

完整引用见 [附录 C](../appendices/references.md)。

## 实验/练习入口

- 从 [附录 A](../appendices/research-workbench.md) 选择一个项目。
- 从 [附录 B](../appendices/experiment-templates.md) 选择一个模板。
- 先写 dry-run 记录，再决定是否进入真实运行。

## 使用边界与常见误读

- 第八章补充 PDF 是课程范文和文献案例，不是 AI_MD 已完成实验。
- Chai-1 aggregate score 只能作为排序/复核信号，不能当真实 Kd 或功能活性。
- 任何课题计划都需要用户确认真实靶点、数据来源和可用实验条件。

## 延伸阅读与下一步

下一步建议先从 Boltz2 对照样例或 APE1 docking dry-run 中选择一个低风险任务。相关入口见 [附录 A](../appendices/research-workbench.md) 和 [附录 B](../appendices/experiment-templates.md)。
