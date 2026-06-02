---
title: "证据与 claims 矩阵"
created: 2026-05-31
type: project-doc
status: active
topics: [type/project, status/active, claim-evidence, evidence-boundary, knowledge-graph]
wiki_role: synthesis
source_count: 11
last_reviewed: 2026-06-02
source_files: ["02_方法笔记/AI多组分对接与虚拟筛选.md", "02_方法笔记/Boltz2亲和力预测.md", "02_方法笔记/亲和力模型综述.md", "02_方法笔记/RFdiffusion与蛋白设计.md", "02_方法笔记/Chai1互作蛋白虚拟筛选.md", "01_课程章节索引/章节精读/章节-文献锚点矩阵.md", "references/zotero-candidates-2026-06-02-P29.tsv", "00_项目说明/P29_文献与引用补强报告.md"]
zotero_items: ["UOUH33GQ", "R2W3SF5S", "57K986LK", "FF4V8LYV", "TPR3JY6N", "V6Y5EEZL", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ"]
bibtex_keys: ["du_dockey_2023", "crampon_machine-learning_2022", "gu_benchmarking_2025", "passaro_boltz-2_2025", "yang_w_past_2026", "zhu_novo_2026", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026"]
related: ["_index.md", "实体索引.md", "研究问题与项目池.md", "AI回归评测集.md", "../00_项目说明/P29_文献与引用补强报告.md"]
claims: [p16_claim_layer_2026_05_31, p29_literature_reinforcement_2026_06_02]
relations:
  - type: depends_on
    target: "实体索引.md"
  - type: supports
    target: "AI回归评测集.md"
  - type: supports
    target: "研究问题与项目池.md"
  - type: supports
    target: "../00_项目说明/P29_文献与引用补强报告.md"
---

# 证据与 claims 矩阵

本页是 P16 的 evidence/claim 层。目标不是把所有正文重写成数据库，而是先把后续研究最容易误用的判断抽出来，明确证据、边界和复核状态。

| claim_id | 判断 | 支持来源 | Zotero/BibTeX | 证据强度 | 使用边界 | 下一次复核 |
|:---|:---|:---|:---|:---|:---|:---|
| `claim:docking-score-ranking-only` | docking score 主要用于同一受体、同一准备流程、同一软件参数下的候选排序，不能直接解释为实验亲和力。 | [AI多组分对接与虚拟筛选](../02_方法笔记/AI多组分对接与虚拟筛选.md), [分子对接与虚拟筛选](../03_文献笔记/分子对接与虚拟筛选.md) | `UOUH33GQ` / `du_dockey_2023`; `R2W3SF5S` / `crampon_machine-learning_2022`; `57K986LK` / `gu_benchmarking_2025` | 中-高 | 不跨软件、不跨受体制备、不替代 top pose 和实验验证 | 2026-08-31 |
| `claim:top-pose-qc-required` | docking top pose 必须检查冲突、关键相互作用、口袋方向、质子化和水/金属/辅因子假设。 | [对接方法卡](../02_方法笔记/AI多组分对接与虚拟筛选.md), [对接记录模板](../04_实验记录/模板_对接虚拟筛选记录.md) | `du_dockey_2023`; `agrawal_benchmarking_2019` | 高 | 适用于小分子和蛋白-肽 docking；蛋白-肽需要额外看肽构象和界面接触 | 2026-08-31 |
| `claim:p14-literature-not-project-results` | 第八章正向虚拟筛选 PDF 和第六章 Nature 综述是教学/文献锚点，不能写成本项目已经完成的运行结果。 | [章节-文献锚点矩阵](../01_课程章节索引/章节精读/章节-文献锚点矩阵.md), [P14 报告](../00_项目说明/知识库维护报告-2026-05-31-P14-文献锚定.md) | `QXKW6K78`, `YUMKNHSK`, `Y4ARSYCQ`, `V6Y5EEZL`, `TPR3JY6N` | 高 | 可借鉴流程、结构化字段和论证方式；不能继承论文结论为本项目证据 | 2026-07-31 |
| `claim:boltz2-affinity-needs-qc` | Boltz2 亲和力输出必须与结构置信度、输入 YAML、链/配体状态和口袋合理性一起解释。 | [Boltz2亲和力预测](../02_方法笔记/Boltz2亲和力预测.md), [Boltz2 结果样例](../04_实验记录/Boltz2结果_l6D9Z7.md) | `FF4V8LYV` / `passaro_boltz-2_2025` | 中 | 不把单次预测值当成实验 Kd；低置信结构或错误配体状态应标记 review | 2026-08-31 |
| `claim:affinity-model-transfer-limit` | 亲和力模型和 docking/ML 重打分适合做候选排序和假设生成，模型外推、靶点域迁移和数据泄漏风险必须单独记录。 | [亲和力模型综述](../02_方法笔记/亲和力模型综述.md), [亲和力文献笔记](../03_文献笔记/亲和力模型与肽结合排序.md) | `95UTFQDM`, `YIV9AVT4`, `CRT8PKH3`, `92GPX1OI`, `VKKT2HE0`, `5GOGPC63` | 中 | 适用于模型筛选、benchmark、排序；不能替代实验测定 | 2026-08-31 |
| `claim:rfdiffusion-output-is-design-candidate` | RFdiffusion/RFD3 生成的结构是设计候选，需要 ProteinMPNN、结构重折叠、界面/功能 QC 和实验验证后才能称为功能 binder。 | [RFdiffusion与蛋白设计](../02_方法笔记/RFdiffusion与蛋白设计.md), [RFD3 第六章精读](../01_课程章节索引/章节精读/第06章_RFD3多组分设计精读.md) | `UKX5E6IB` / `watson_novo_2023`; `ZYFCZKMH` / `ahern_atom_2025`; `TPR3JY6N` / `yang_w_past_2026`; P29 candidate `butcher_novo_2025` 待入库 | 中-高 | 设计结果不等于功能验证；必须保存 motif、contig、链约束、seed 和筛选淘汰原因 | 2026-08-31 |
| `claim:rfd3-record-parameters-required` | RFD3/RFdiffusion 设计记录至少要包含目标复合物、固定 motif、contig/长度、链定义、输入结构、随机种子、扩散参数、输出筛选标准和后续序列设计参数。 | [RFdiffusion 模板](../04_实验记录/模板_RFdiffusion骨架生成记录.md), [ProteinMPNN 模板](../04_实验记录/模板_ProteinMPNN序列设计记录.md) | `watson_novo_2023`, `ahern_atom_2025`, `yang_w_past_2026`; P29 candidate `butcher_novo_2025` 待入库 | 中 | 目前本库尚未发现真实 RFD3 运行输出；该 claim 先作为记录规范 | 2026-08-31 |
| `claim:chai1-aggregate-score-ranking-only` | Chai-1 aggregate score 适合作为批量互作建模的排序/复核信号，不能直接解释为真实结合常数或功能活性。 | [Chai1互作蛋白虚拟筛选](../02_方法笔记/Chai1互作蛋白虚拟筛选.md), [Chai-1 模板](../04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md) | P29 candidate `chai_discovery_chai-1_2024` 待 Zotero/BibTeX 正式入库 | 低-中 | 必须同时看界面接触、链置信度、PAE/局部质量、构象合理性；当前证据主要来自方法卡规则和候选技术报告 | 2026-08-31 |
| `claim:short-md-not-function-proof` | 短时 MD 或单条轨迹主要支持构象稳定性和相互作用持久性判断，不能单独证明药效或功能机制。 | [MD_BioEmu_AI采样](../02_方法笔记/MD_BioEmu_AI采样.md), [MD 模板](../04_实验记录/模板_MD_BioEmu采样记录.md) | `92GPX1OI` / `gu_molecular_2023` | 中 | 需要重复轨迹、对照体系、能量/自由能或实验验证支撑更强结论 | 2026-08-31 |
| `claim:project-pool-needs-user-target-selection` | 研究项目池中的靶点/配体/蛋白面板只有在用户指定真实研究方向、数据来源和可用实验条件后，才能转成正式课题计划。 | [研究问题与项目池](研究问题与项目池.md), [实验队列](实验队列.md) | 视项目而定 | 中 | 当前项目池是研究工作台候选，不是已承诺执行的实验计划 | 2026-07-31 |

## 证据强度约定

| 等级 | 含义 |
|:---|:---|
| 高 | 有正式文献锚点、方法卡和模板共同支撑，且边界清晰 |
| 中 | 有文献或项目方法卡支撑，但仍需要具体项目输入或实际运行记录 |
| 低-中 | 主要来自本项目方法规则或工具输出约定，尚缺正式论文/官方文档锚点 |

## 当前优先补证点

- Chai-1 candidate `chai_discovery_chai-1_2024` 待 Zotero 导入和正式 BibTeX 映射。
- RFD3/RFdiffusion3 candidate `butcher_novo_2025` 待 Zotero 导入；仍需真实运行结果样例，包括失败样例。
- BindCraft candidate `pacesa_bindcraft_2025` 待确认是否升级既有 `pacesa_bindcraft_2024`。
- Boltz2 在本项目真实体系中的输入 YAML、结构置信度和亲和力解释记录。
- docking score 与重打分结果在同一候选集上的一致性/冲突记录。
