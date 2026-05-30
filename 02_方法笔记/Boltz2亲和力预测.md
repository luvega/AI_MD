---
title: "Boltz2 亲和力预测"
created: 2026-05-30
type: method-note
status: complete
topics: [type/method, status/complete, topic/boltz2, topic/affinity, chapter/5]
source_files: ["06_原始学习素材/第05章_亲和力计算/原始PDF/第五章AI多组分亲和力计算.pdf", "06_原始学习素材/第05章_亲和力计算/全文提取/第五章AI多组分亲和力计算/全文.md", "第五章/boltz2在线/boltz2.json", "第五章/boltz2在线/extract_boltz2.py", "第五章/boltz2在线/boltz2_parsed/summary.json"]
zotero_items: ["FF4V8LYV", "CRM22UDT", "PE42AXJX"]
bibtex_keys: ["passaro_boltz-2_2025", "cho_boltzdesign1_2025", "abramson_accurate_2024"]
related: ["../01_课程章节索引/章节精读/第05章_AI多组分亲和力计算精读.md", "../04_实验记录/Boltz2结果_l6D9Z7.md", "../04_实验记录/模板_Boltz2亲和力记录.md", "../03_文献笔记/Boltz2亲和力预测.md", "../03_文献笔记/亲和力模型与肽结合排序.md"]
wiki_role: method
source_count: 8
last_reviewed: 2026-05-30
claims: [passaro_boltz-2_2025, cho_boltzdesign1_2025, abramson_accurate_2024]
relations:
  - type: derived_from
    target: "../06_原始学习素材/第05章_亲和力计算/全文提取/第五章AI多组分亲和力计算/全文.md"
  - type: supports
    target: "../03_文献笔记/Boltz2亲和力预测.md"
  - type: applies_to
    target: "../04_实验记录/模板_Boltz2亲和力记录.md"
  - type: depends_on
    target: "../04_实验记录/Boltz2结果_l6D9Z7.md"
---

# Boltz2 亲和力预测

第五章已有 Boltz2 在线结果和解析脚本，是本知识库最完整的实验记录样例。本方法卡把 Boltz2 任务拆成 YAML 输入、链/配体定义、输出文件、置信度解释和亲和力解释规则。

## 当前已有数据

- 原始输出：`第五章/boltz2在线/boltz2.json`
- 解析脚本：`第五章/boltz2在线/extract_boltz2.py`
- 指标摘要：`第五章/boltz2在线/boltz2_parsed/summary.json`
- 结构模型：`第五章/boltz2在线/boltz2_parsed/l6D9Z7_model_0.cif`
- 残基层面 pLDDT：`第五章/boltz2在线/boltz2_parsed/l6D9Z7_model_0_plddt.tsv`

## 可执行流程

1. 明确任务：结构预测、复合物预测、亲和力预测、候选排序或结果复核。
2. 准备输入：为每条蛋白/核酸链写 ID、序列、MSA、模板；为配体写 ligand ID、SMILES/CCD 或结构文件。
3. 写 YAML：保证链 ID、配体 ID、任务类型和文件路径一致。
4. 运行 Boltz2：记录软件版本、模型版本、运行平台、随机种子和输出目录。
5. 解析输出：保留原始 JSON、summary、CIF、pLDDT/界面指标和亲和力指标。
6. 结构复核：用可视化工具检查链、配体位置、口袋、界面和低置信区域。
7. 解释亲和力：同时读取结构置信度、界面置信度、亲和力读数、二分类概率和适用域。
8. 归档记录：使用 `../04_实验记录/模板_Boltz2亲和力记录.md` 或更新具体实验记录。

## YAML 输入骨架

下面是项目记录用的最小字段模板，实际语法以当前 Boltz2 版本为准；写实验记录时保留真实 YAML 路径。

```yaml
version: 1
sequences:
  - protein:
      id: A
      sequence: "PASTE_PROTEIN_SEQUENCE"
      msa: "path/to/chain_A.a3m"
      templates: []
  - ligand:
      id: LIG
      smiles: "PASTE_SMILES"
properties:
  - affinity:
      binder: LIG
output:
  out_dir: "runs/boltz2_task_id"
```

## 输入字段检查表

| 字段 | 必填记录 | 检查点 |
|:---|:---|:---|
| `protein.id` | 链 ID，例如 A、B | 与输出 CIF 和结果表一致 |
| `protein.sequence` | FASTA 序列 | 无空格、非法字符或截断 |
| `msa` | A3M/空值/自动生成说明 | MSA 来源和覆盖度可追踪 |
| `templates` | 模板路径或空列表 | 模板来源、同源性和是否泄漏答案明确 |
| `ligand.id` | 配体 ID，例如 LIG | 与 affinity binder 一致 |
| `smiles`/`ccd`/结构文件 | 配体表示 | 手性、质子化、电荷和来源明确 |
| `properties.affinity.binder` | 需要预测亲和力的配体 ID | 必须指向已定义配体 |
| `out_dir` | 输出目录 | 不覆盖旧任务 |

## 关键指标解释

- `confidence_scores`：整体置信度。
- `ptm_scores`、`iptm_scores`：结构和界面预测可信度。
- `complex_plddt_scores`、`complex_iplddt_scores`：复合物和界面局部置信度。
- `affinity_LIG_affinity_pic50`：亲和力预测核心读数之一。
- `affinity_LIG_affinity_probability_binary`：结合倾向二分类概率。

## 输出文件规范

| 文件 | 用途 | 是否保留 |
|:---|:---|:---|
| 原始输出 JSON | 完整模型输出和所有指标 | 必须 |
| `summary.json` | 项目内快速读取的指标摘要 | 必须 |
| `*_model_0.cif` | 结构复核和作图 | 必须 |
| `*_plddt.tsv` | 残基层面置信度检查 | 必须 |
| 可视化图片/session | 报告和人工复核 | 建议 |
| 输入 YAML | 复现运行 | 必须 |

## 置信度解释规则

- `confidence_scores` 高只能说明模型整体自洽，不等同实验真实。
- `iptm_scores` 和 `complex_iplddt_scores` 比整体 pLDDT 更接近界面可信度；解释结合模式时优先看界面指标。
- pLDDT 低的 loop、末端或无序区不应直接用于关键相互作用解释。
- 配体附近残基低置信时，亲和力读数必须降级为“候选排序参考”。
- 多模型输出不一致时，保留每个模型指标，不只引用最好的一项。

## 亲和力解释规则

- `affinity_pic50` 可用于同类任务候选排序；不要和 docking score、MM-GBSA 能量或实验 Kd 混在同一数值尺度比较。
- `affinity_probability_binary` 是结合倾向概率，不是实验成功率。
- 亲和力读数必须和结构可信度、界面合理性、输入配体状态、训练分布适用性一起解释。
- 低质量输入上的高亲和力读数应标为 `review`，不能直接推进。
- 如果要换算或比较实验量纲，必须在实验记录中写明公式、单位和温度假设。

## 当前样例判读

- `l6D9Z7` 样例的 `confidence_scores=0.909981`、`iptm_scores=0.959715`、`complex_iplddt_scores=0.864698`，可作为结构和界面较可信的示例。
- `affinity_LIG_affinity_probability_binary=0.921875`、`affinity_LIG_affinity_pic50=8.345176`，可用于第五章亲和力预测讲解和候选排序演示。
- 该样例仍需补充真实输入 YAML、靶点/配体身份、配体状态和结构复核图，才能作为完整实验记录引用。

## 文献依据

- `passaro_boltz-2_2025`：Boltz2 的结构和亲和力预测主文献。
- `cho_boltzdesign1_2025`：Boltz/BoltzDesign 作为设计模型的延伸。
- `abramson_accurate_2024`：AlphaFold3 复合物预测背景。

## 记录模板入口

- 新建 Boltz2 或亲和力实验记录时复制 `../04_实验记录/模板_Boltz2亲和力记录.md`。

