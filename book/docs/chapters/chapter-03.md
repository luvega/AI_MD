# 第 3 章 AI 多组分对接与虚拟筛选

## 本章导读

本章建立虚拟筛选的基础工作流：受体准备、配体准备、box 定义、对接运行、score 排序和 top pose 复核。它是后续 MD、亲和力预测和课题设计的入口。

## 学习目标

- 能设计一个可复现的 docking 记录。
- 能解释 score、rank、pose 和相互作用摘要之间的区别。
- 能说明 docking score 为什么不能直接当作实验亲和力。

## 知识图谱入口

- 章节来源：`01_课程章节索引/章节精读/第03章_AI多组分对接与虚拟筛选精读.md`
- 方法来源：`02_方法笔记/AI多组分对接与虚拟筛选.md`
- 文献来源：`03_文献笔记/分子对接与虚拟筛选.md`
- 证据边界：`07_研究工作台/证据与claims矩阵.md`

## 核心概念

| 概念 | 本章定位 |
|:---|:---|
| receptor preparation | 决定口袋、电荷、缺失区域和辅因子假设 |
| ligand preparation | 决定质子化、互变异构、手性和 3D 构象 |
| docking box | 决定搜索空间和结果可解释性 |
| score/rank | 主要用于同一设置下的候选排序 |
| top pose QC | 防止把非物理姿态写成候选机制 |

## 方法流程

1. 定义任务类型：单靶点筛选、蛋白-肽 docking、多组分体系或反向筛选。
2. 准备受体和配体，记录来源、版本和处理假设。
3. 定义 docking box，说明来自共晶配体、口袋残基还是盲对接。
4. 运行对接，保存软件版本、参数、seed、输入清单和输出路径。
5. 对 top pose 做人工复核，记录保留、淘汰或重跑原因。

## 关键文献与 BibTeX key

- `du_dockey_2023`：大规模 docking/虚拟筛选工具化流程。
- `agrawal_benchmarking_2019`：蛋白-肽 docking benchmark。
- `crampon_machine-learning_2022`：机器学习 docking 和重打分边界。
- `gu_benchmarking_2025`：AI-powered docking benchmark 视角。

完整引用见 [附录 C](../appendices/references.md)。

## 实验/练习入口

- 复制 `04_实验记录/模板_对接虚拟筛选记录.md` 建立练习记录。
- 练习记录 receptor、ligand、box、software、score、rank、pose_path 和 qc_status。
- 对 top 3 pose 写出保留或淘汰理由。

## 使用边界与常见误读

- docking score 只能作为排序信号，不能直接解释为真实 Kd、IC50 或功能活性。
- 不同软件、不同受体准备流程或不同 box 的 score 不应直接横向比较。
- 第八章补充 PDF 中的筛选案例是文献案例，不是本项目已完成筛选结果。

## 延伸阅读与下一步

通过 docking 初筛后，进入 [第 4 章](chapter-04.md) 学习 MD 和采样，或进入 [第 5 章](chapter-05.md) 学习亲和力预测。
