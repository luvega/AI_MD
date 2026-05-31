# 第 5 章 亲和力预测、Boltz2 与模型评估

## 本章导读

本章讨论从结构到亲和力预测的桥梁。Boltz2、DeepDTAF、PPI-Affinity 和 AlphaFold 相关排序方法可以帮助候选 triage，但输出必须结合输入质量、置信度和适用域解释。

## 学习目标

- 能说明 Boltz2 输入 YAML、链定义、配体状态和输出指标的记录要求。
- 能区分结构置信度、亲和力预测值和实验亲和力。
- 能识别模型外推、数据泄漏和适用域问题。

## 知识图谱入口

- 章节来源：`01_课程章节索引/章节精读/第05章_AI多组分亲和力计算精读.md`
- 方法来源：`02_方法笔记/Boltz2亲和力预测.md`
- 综述来源：`02_方法笔记/亲和力模型综述.md`
- 实验样例：`04_实验记录/Boltz2结果_l6D9Z7.md`

## 核心概念

| 概念 | 本章定位 |
|:---|:---|
| affinity prediction | 用模型估计结合强弱或排序信号 |
| confidence | 判断结构和界面预测是否可用 |
| positive/negative control | 检查模型输出方向是否合理 |
| applicability domain | 判断训练数据和目标体系是否匹配 |
| triage | 为后续实验或更高成本计算筛选候选 |

## 方法流程

1. 明确任务是小分子、肽、PPI 还是多组分体系。
2. 准备输入 YAML、链、配体、序列和结构来源。
3. 运行预测并保存版本、参数、seed、输出和日志。
4. 对结构置信度、界面质量和亲和力输出做联合解释。
5. 结合 docking、MD 或实验对照判断是否进入下一步。

## 关键文献与 BibTeX key

- `passaro_boltz-2_2025`：Boltz2 亲和力预测。
- `cho_boltzdesign1_2025`：BoltzDesign binder 设计背景。
- `wang_deepdtaf_2021`：DeepDTAF 蛋白-配体亲和力预测。
- `romero-molina_ppi-affinity_2022`：PPI-Affinity 工具。
- `chang_ranking_2023`：AlphaFold peptide binder 排序。

完整引用见 [附录 C](../appendices/references.md)。

## 实验/练习入口

- 复制 `04_实验记录/模板_Boltz2亲和力记录.md`。
- 选择一个有已知正/负对照的体系。
- 记录输入质量、结构置信度、亲和力预测和解释边界。

## 使用边界与常见误读

- 单次 Boltz2 输出不等于实验 Kd。
- 低质量输入结构或错误配体状态会让亲和力输出失去解释意义。
- PPI、肽和小分子的模型边界不同，不能混用阈值。

## 延伸阅读与下一步

如果下一步是设计新 binder 或蛋白骨架，进入 [第 6 章](chapter-06.md)。如果下一步是研究问题整合，进入 [第 8 章](chapter-08.md)。
