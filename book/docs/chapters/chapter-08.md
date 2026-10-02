# 第 8 章 AI 亲和力预测与模型评估

## 本章导读

面对一张 AI 结果表，先不要按最大的数字排序。模型可能输出结合概率、对数亲和力或结构置信度，方向和用途并不相同。本章先核对公开的非共价输入，读取一次真实 Boltz 输出，再用明确构造的错误字段做对照。

主输入继续使用公开 3HTB/JZ4。T4 lysozyme L99A/M102Q 与中性 2-propylphenol。必修练习不依赖课程 Boltz 原件，也不要求 GPU。正式模型推理为选学，必修可以直接读取已提供的真实 JSON 和 CIF。构造字段单独用于故障与排序练习。

| 必修操作 | 你要得到什么 | 核对方法 |
|---|---|---|
| 检查非共价 YAML | 输入组分、ID、序列与 MSA 方案 | 对照公开来源 |
| 读取字段练习 | 概率、分值与置信度分列 | 检查方向与单位 |
| 排查结构错误 | 数值好但位置错误的候选 | 记录结构复核状态 |
| 制作下一步表 | 缺失输入、对照与任务 | 每项有对应文件或待办 |

## 练习目录

从[练习资源页](https://luvega.github.io/AI_MD/resources/)下载本章压缩包，解压到 `C:/coursework`。以下命令从 `C:/coursework/AI_MD_practice` 开始。先进入本章目录，后续 Python 命令都从这里运行，结果写入 `outputs`。

```bash
cd chapter-08/assets
```

## 8.1 AI 亲和力预测任务定义

先给一次预测写任务卡。你要从大量分子中识别可能结合者，还是比较已有活性分子的细微差别？两种问题可能使用不同输出。不要先选软件，再把它能输出的数字当成研究问题。

| 任务卡字段 | 填写示例 | 需要亲手核对的地方 |
|---|---|---|
| prediction unit | 一个蛋白–小分子组合 | 是否包含多个配体或其他组分 |
| input | 序列、SMILES、结构或 pose | 是否来自同一化学状态 |
| label / output | 结合概率、log10(IC50/μM) 或其他评分 | 模型文档的实际定义 |
| direction | 大更强或小更强 | 用一个已知数值例子检查 |
| comparison scope | 同靶点、同系列、同方案 | 对照与模型版本是否一致 |

用第 4 章的 docking score、第 7 章的 `GB delta TOTAL` 和本章的概率字段各填一行字段定义，分别写出体系与来源。第 7 章官方能量来自其他体系，这里只借用列定义，不能填入 3HTB/JZ4 候选行。

## 8.2 PLANET、GAABind、Interformer、BALM 等模型

比较模型先比较输入，而不是比较论文中的最高相关系数。下面四个例子用来识别任务差别；下载代码和选择模型时仍需回到对应版本说明。

| 模型 | 输入侧重点 | 输出侧重点 | 准备时先问什么 |
|---|---|---|---|
| PLANET | 3D 口袋与配体 2D 化学图 | 亲和力及接触/距离信息 | 是否已有可靠口袋结构 |
| GAABind | 已知口袋与未结合配体构象 | 距离、pose 与亲和力 | 配体构象和原子对应是否正确 |
| Interformer | 结合位点与配体 3D/pose | 互作相关评分、pose 与亲和力 | pose 从哪来，是否经过检查 |
| BALM | 蛋白与配体的语言模型输入 | 亲和力预测 | 标签与数据划分怎样定义 |

对应论文为 [PLANET](https://doi.org/10.1021/acs.jcim.3c00253)、[GAABind](https://doi.org/10.1093/bib/bbad462)、[Interformer](https://doi.org/10.1038/s41467-024-54440-6) 和 [BALM 的原始预印本](https://doi.org/10.1101/2024.11.01.621495)。作业选择一篇，找到输入字段、训练标签和测试划分，填写任务卡；不要求同时安装四个模型。

对照练习。把同一个蛋白序列与一个 docking pose 分别作为输入设想，指出哪类模型还需要额外的 3D 口袋或配体原子图。缺少输入时写缺失项，不以改扩展名代替格式转换。

## 8.3 Boltz-2 输入、输出与运行方式

下载 [3htb-jz4-noncovalent.yaml](../assets/chapter-08/practice/3htb-jz4-noncovalent.yaml)，用文本编辑器打开。先看 protein 与 ligand 的 ID，再看 `properties.affinity.binder`。配体 ID 为 `LIG`，亲和力任务也必须指向 `LIG`。其核心结构如下，运行时使用下载的完整 YAML。

```yaml
version: 1
sequences:
  - protein:
      id: A
      sequence: MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPDLNAAKSELDKAIGRNCNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRCAAINQVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPDRAKRVITTFRTGTWDAYKNL
  - ligand:
      id: LIG
      smiles: 'CCCc1ccccc1O'
properties:
  - affinity:
      binder: LIG
```

| 检查项 | 本练习应是什么 | 故意改错后检查什么 |
|---|---|---|
| 蛋白序列 | 3HTB A 链 SEQRES，164 aa | 少一个残基后是否仍与来源对应 |
| 配体 | JZ4，中性 2-propylphenol | 改 SMILES 是否改变了化学结构 |
| ligand ID | LIG | binder 改成未定义 ID 会怎样 |
| 化学表示 | 单独使用 smiles | 同时写 ccd 与 smiles 是否冲突 |
| 共价键 | 无 bond 约束 | 不要从共价案例复制连接定义 |
| MSA | 选择外部服务或本地预计算文件 | 没有 MSA 时用哪条运行路线 |

公开 YAML 未提供 MSA。使用 `--use_msa_server` 会把公开蛋白序列发送给 MSA 服务；也可以先生成自己的 MSA，再在 YAML 填本地路径。单序列模式 `msa: empty` 是不同输入方案，应记录并单独评估，不能当作补齐 MSA。

选学在已配置环境运行，先查看本机帮助与版本。

```bash
boltz predict --help
python -m pip show boltz
boltz predict practice/3htb-jz4-noncovalent.yaml --use_msa_server --out_dir outputs/3htb-jz4-run
```

命令使用独立输出目录。正式运行保存原始 YAML、版本、权重、随机种子设置、MSA 来源、日志与完整输出。先用默认样本量完成一个输入，不要求为了课堂练习大量增加 diffusion samples；显存不足时保留报错并转用教学算力。

| 正式输出 | 打开后读什么 |
|---|---|
| model_0.cif 等结构 | 配体位置、接触、几何与组分 |
| confidence JSON | confidence_score、iptm、ligand_iptm、pLDDT 等 |
| affinity JSON | affinity_pred_value 与 affinity_probability_binary |
| 原始日志与 processed | 实际参数、输入处理与运行状态 |

本次已附的正式运行采用单序列输入 `msa: empty`，1 recycle、结构与亲和力各 100 sampling steps/1 sample，seed 20261002。见 [实际输入](../assets/chapter-08/results/3htb-jz4-single/actual-input.yaml) 与 [运行记录](../assets/chapter-08/results/3htb-jz4-single/run-record.json)。它与上面使用 MSA 的准备方案分别记录，不能混成同一组参数。

## 8.4 predicted affinity 与 confidence 解读

先读取真实结果包。无需安装 Boltz 或使用 GPU，从本章 assets 目录运行：

```bash
python code/inspect-affinity.py --affinity results/3htb-jz4-single/affinity_3htb_jz4_single.json --confidence results/3htb-jz4-single/confidence_3htb_jz4_single_model_0.json --out outputs/actual-fields.tsv
```

| 真实输出字段 | 本次 3HTB/JZ4 单序列运行 |
|---|---:|
| affinity_pred_value | 2.300788 |
| affinity_probability_binary | 0.204868 |
| confidence_score | 0.966183 |
| complex_plddt | 0.971745 |
| iptm | 0.943934 |

解析脚本直接从两个原始 JSON 取集合亲和力读数与 confidence，不改变原始文件。结果显示结构置信度与结合者概率可以明显不同。打开 CIF 后，还要检查配体和蛋白的几何关系。

[结构核对记录](../assets/chapter-08/results/3htb-jz4-single/structure-check.json)按 A1–A163 的 C-alpha 叠合，RMSD 为 0.582 Å；叠合后模型与晶体配体质心相差 0.619 Å。质心差不是配体按原子映射计算的 RMSD。可在 PyMOL 从本章 assets 目录执行 [view-actual-pose.pml](../assets/chapter-08/code/view-actual-pose.pml)，查看橙色预测配体与绿色晶体配体。

先打开 [constructed-output.json](../assets/chapter-08/practice/constructed-output.json)。第一项 `data_status` 是 `constructed_field_exercise`；数字为人工构造，仅用于字段和错误对照，不是 3HTB/JZ4 预测。

| 字段 | 本章读取规则 | 先核对哪一点 |
|---|---|---|
| affinity_probability_binary | 预测结合者概率，0–1 | 任务偏向识别结合者/诱饵 |
| affinity_pred_value | 模型 log10(IC50/μM) 尺度，越低越强 | 比较对象与适用范围 |
| confidence_score | 结构预测综合置信字段 | 与配体位置、界面一起看 |
| iptm / ligand_iptm 等 | 相应界面置信字段 | 具体界面与输出文件 |

运行字段解析。

```bash
python code/inspect-affinity.py --input practice/constructed-output.json --out outputs/fields.tsv
```

脚本要求明确数据状态，并检查概率和置信度是否在 0–1。它将 `10**y` 标为模型尺度 μM 数值，将 `6-y` 标为无量纲 pIC50 代数换算，保留原始分值；这里不把它换写成物理 kcal/mol。

| 构造候选 | y | 10^y / μM | 6−y | 结构/对照信息 |
|---|---:|---:|---:|---|
| field_A | -0.3 | 0.501 | 6.3 | 配体在预期口袋外；无对照 |
| field_B | 1.2 | 15.849 | 4.8 | 尚未检查结构；无对照 |
| field_C | 0.4 | 2.512 | 5.6 | 尚未检查结构；无对照 |

先按 y 排序，再按 probability 排序，再检查结构列。field_A 数字更有利，但已经带有结构问题；field_C 的 confidence 高也不会自动补齐结构与对照。作业写出三者各自还缺哪项复核，暂不选“获胜分子”。

## 8.5 结构预测、亲和力预测和实验值之间的边界

这一节把三个文件放在一起核对。模型 CIF、affinity JSON、实验记录。先看是否是同一个蛋白构建体、同一个配体状态和同一套测量条件。

| 信息 | 具体核对任务 | 发现差别后怎样记录 |
|---|---|---|
| 结构 | 配体是否位于合理区域，是否严重冲突 | 残基、原子与检查图 |
| 模型分值 | 原始字段、方向、版本、适用范围 | 原始 JSON 与解析表 |
| 实验 | Kd/Ki/IC50 类型、单位、条件和重复 | 原始 readout 与来源 |

对照题。一份模型表是 log10(IC50/μM)，另一份实验表是 Kd/nM。先完成各自的单位与定义记录，指出哪些差异不能只靠乘 1000 消除。IC50 与 Kd 之间还涉及测定条件与反应模型，不能直接互换表头。

## 8.6 模型 benchmark、校准和误差来源

拿到一篇模型论文，先找训练和测试如何分开。随机按样本拆分，可能让相似靶点或同系列配体同时出现在两侧；新靶点测试与新骨架测试提出的是不同问题。

| 评估设计 | 你要查什么 | 给课堂案例的任务 |
|---|---|---|
| random split | 近重复与相似分子是否跨组 | 指出潜在信息重叠 |
| target split | 测试靶点是否在训练出现 | 说明与新靶点任务的对应 |
| scaffold split | 配体骨架怎样定义和分组 | 检查是否仍有近似骨架 |
| 时间划分或外部测试 | 日期、筛选规则与来源 | 判断是否贴近实际前瞻使用 |
| 标定 | 已知活性/低活性对照与同一 assay | 先定对照，不先调阈值 |

读 benchmark 时，先把指标与任务对应。不同 readout 和数据划分的指标不能直接拼成排行榜。

| 指标 | 回答什么问题 | 读取时注意什么 |
|---|---|---|
| MAE | 预测与标签的平均绝对差 | 单位或对数尺度要一致 |
| RMSE | 平方误差汇总后的偏差 | 对大偏差更敏感 |
| Pearson 相关 | 是否呈线性共变 | 高相关仍可能存在整体偏移 |
| Spearman / 排序指标 | 候选顺序是否一致 | 不表示数值已经标定 |
| AUROC | 跨分类阈值区分阳性与阴性 | 同时核对类别组成 |
| AP / precision–recall | 正例检出与结果精度 | 受阳性比例影响 |
| EF（指定前百分比） | 顶部命中相对随机基线富集多少 | 报出截取比例和正例基线 |

课堂构造字段没有标签，不能拿来计算模型准确率。真正做 benchmark 时还需保存样本 ID、标签、单位、预测版本与划分；分类问题再计算相应分类指标，排序任务使用相应排序指标。

## 8.7 生成式采样与亲和力解释

一个输入可能生成多个构象。先把样本 ID 与各自结构置信度对应，再检查配体接触是否一致。不要只保存最高分那张图，其他样本可能暴露输入或构象不确定性。

| 要比较的内容 | 操作方式 | 保存结果 |
|---|---|---|
| 结构差异 | 叠合蛋白后看配体与局部区域 | 样本 ID、叠合组与图 |
| 字段差异 | 保留每个样本及聚合方式 | 原始 JSON 与汇总规则 |
| 跨运行差异 | 保持输入、记录随机设置 | 运行目录与完整日志 |

选学先生成少量样本，核对资源和输出，再决定是否增加取样。构造字段练习没有结构文件，也不是生成式样本；本章真实 3HTB/JZ4 输出则附有 CIF。作业应分别记录两类材料。

## 8.8 从预测排序到实验队列

同一候选行只填这个候选实际得到的结果。3HTB/JZ4 可以填第 4 章 pose 与本章模型字段、结构检查；MM/GBSA、MM/PBSA 列留空，注明未计算。第 7 章两套官方示例只提供列定义与阅读练习，不能把 -15.017773104 kcal/mol 放入 JZ4 行。下一步按缺项安排结构检查、对照、计算或实验。

| 当前状态 | 表中怎么写 | 下一步任务 |
|---|---|---|
| 输入不一致 | 标明序列、配体状态或 ID 差异 | 先修正输入 |
| 已有结构问题 | 链接检查图，记录问题位置 | 修复或排除该建模方案 |
| 输入合格但缺结果 | 结果留空 | 执行指定运行 |
| 只有模型读数 | 分别保留字段与版本 | 加入对照与结构检查 |
| 有实验与计算 | 保留不同 readout | 在同任务内比较与标定 |

章末提交公开 YAML 的检查表、带数据状态的解析 TSV、三份构造候选的待办，以及一个正式运行计划。第 9 章进入候选生成；本章表格可继续用来复核生成结果。

## 本章方法范围

模型读数描述的是特定输入、权重和训练任务下的预测。结构置信度、结合概率和对数亲和力承担不同功能，不能替代实验 Kd、Ki、IC50、药效或机制验证。构造字段只用于阅读练习，未执行的输入只算准备完成；正式结果需要完整运行记录、结构复核、适用域与相应对照。预测比较只有在任务、输入和方法口径一致时才有意义。
