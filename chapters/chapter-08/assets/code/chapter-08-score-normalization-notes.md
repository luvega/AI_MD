# 第 8 章分数解释边界

不同模型输出不能为了画表而强行归一化到同一尺度。第 8 章正文只做三件事：

1. 记录原始字段名、方向和单位。
2. 在同一模型、同一靶点、同一输入策略和同一批候选内比较排序。
3. 用正/负对照或已知活性系列检查模型信号方向。

## 可同批比较的情况

- 同一 Boltz-2 版本、同一 seed 策略、同一 CLI 参数、同一靶点、同一配体状态定义下的 `affinity_pred_value`。
- 同一 hit-discovery 面板中的 `affinity_probability_binary`，并且正/负对照方向合理。
- 同一 docking 或 pose 重打分流程内的模型分数，前提是 pose 生成和复核标准一致。

## 不应直接比较的情况

- Boltz-2 的 `affinity_probability_binary` 与 `affinity_pred_value`。
- docking score、MM/GBSA、FEP、语言模型 affinity 头和结构 confidence。
- 不同 assay、不同构象来源、不同配体质子化/互变异构状态或不同共价状态下的数值。

## 正文推荐写法

- 可以写：在同批候选中，模型信号支持把该分子列为复核优先级较高的候选。
- 可以写：该结果缺少对照和实验校准，只能作为未校准模型信号。
- 不应写：模型预测证明该分子具有实验 `Kd`、`IC50` 或药效。
