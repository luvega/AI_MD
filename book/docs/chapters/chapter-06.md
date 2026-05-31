# 第 6 章 RFD3/RFdiffusion、ProteinMPNN 与蛋白设计

## 本章导读

本章把结构生成、序列设计和设计后复核串成蛋白设计工作流。RFdiffusion/RFD3 生成的是设计候选，必须经过 ProteinMPNN、结构重折叠、界面/功能 QC 和实验验证后才能形成强结论。

## 学习目标

- 能说明 RFdiffusion/RFD3 设计记录必须包含的参数。
- 能解释骨架生成、序列设计、重折叠和界面筛选的关系。
- 能区分设计候选、计算筛选通过和功能 binder。

## 知识图谱入口

- 章节来源：`01_课程章节索引/章节精读/第06章_RFD3多组分设计精读.md`
- 方法来源：`02_方法笔记/RFdiffusion与蛋白设计.md`
- 文献来源：`03_文献笔记/RFdiffusion蛋白设计.md`
- 实验模板：`04_实验记录/模板_RFdiffusion骨架生成记录.md`

## 核心概念

| 概念 | 本章定位 |
|:---|:---|
| motif/contig | 约束设计空间和功能区域 |
| backbone generation | 生成候选骨架，不是最终蛋白 |
| ProteinMPNN | 从骨架到序列的设计步骤 |
| refolding | 检查序列是否能回到目标结构 |
| interface QC | 判断 binder 设计是否值得进入实验 |

## 方法流程

1. 定义目标复合物、固定 motif、链、contig 和长度范围。
2. 运行 RFdiffusion/RFD3，记录 seed、diffusion 参数和输出批次。
3. 用 ProteinMPNN 生成序列，记录 temperature、fixed positions 和 chain mask。
4. 对候选序列做结构重折叠和界面质量复核。
5. 只把通过多层 QC 的候选进入后续实验或更高成本计算。

## 关键文献与 BibTeX key

- `watson_novo_2023`：RFdiffusion 蛋白结构与功能 de novo 设计。
- `ahern_atom_2025`：RFdiffusion2 原子级酶活性位点 scaffolding。
- `bennett_atomically_2025`：RFdiffusion 抗体设计。
- `dauparas_robust_2022`：ProteinMPNN 序列设计。
- `pacesa_bindcraft_2024`：BindCraft binder 设计。
- `dauparas_atomic_2025`：LigandMPNN 序列设计。
- `yang_w_past_2026`：de novo protein design 综述。

完整引用见 [附录 C](../appendices/references.md)。

## 实验/练习入口

- 复制 `04_实验记录/模板_RFdiffusion骨架生成记录.md`。
- 复制 `04_实验记录/模板_ProteinMPNN序列设计记录.md`。
- 先做参数记录 dry-run，再决定是否运行真实设计。

## 使用边界与常见误读

- 设计输出不是功能验证。
- 单个漂亮结构图不能证明 binder 成功。
- 本项目当前尚未发现真实 RFD3 运行输出，课程讲义只使用文献案例和记录规范。

## 延伸阅读与下一步

第 8 章会把 BabA binder、RFD3 和正向筛选案例放入研究问题设计语境。[进入第 8 章](chapter-08.md)。
