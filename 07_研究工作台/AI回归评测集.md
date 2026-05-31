---
title: "AI 回归评测集"
created: 2026-05-31
type: project-doc
status: active
topics: [type/project, status/active, ai-eval, regression-test, query-wiki]
wiki_role: synthesis
source_count: 8
last_reviewed: 2026-05-31
source_files: ["index.md", "07_研究工作台/实体索引.md", "07_研究工作台/证据与claims矩阵.md", "07_研究工作台/研究问题与项目池.md", "references/zotero-map.tsv"]
zotero_items: ["TPR3JY6N", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ", "V6Y5EEZL", "FF4V8LYV"]
bibtex_keys: ["yang_w_past_2026", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026", "zhu_novo_2026", "passaro_boltz-2_2025"]
related: ["_index.md", "实体索引.md", "证据与claims矩阵.md", "研究问题与项目池.md"]
claims: [p18_ai_eval_suite_2026_05_31]
relations:
  - type: depends_on
    target: "实体索引.md"
  - type: depends_on
    target: "证据与claims矩阵.md"
  - type: supports
    target: "../00_项目说明/知识库使用说明.md"
---

# AI 回归评测集

本页是 P18 的标准查询任务。每轮大更新后，抽测 3-5 个问题；季度或结构大改后跑全量。合格答案必须同时给出路径、Zotero/BibTeX key、使用边界和待确认项。

| task_id | 标准问题 | 期望读取路径 | 必须包含的 Zotero/BibTeX key | 必须说明的边界 | 通过标准 |
|:---|:---|:---|:---|:---|:---|
| `eval:ch8-vs-literature-boundary` | 第八章正向虚拟筛选有哪些可借鉴但不能当作本项目结果的文献？ | [第08章精读](../01_课程章节索引/章节精读/第08章_计算思路解析精读.md), [章节-文献锚点矩阵](../01_课程章节索引/章节精读/章节-文献锚点矩阵.md), [证据矩阵](证据与claims矩阵.md) | `sui_targeting_2026`, `shen_structure-based_2026`, `tomarchio_reproducible_2026` | 这些是文献案例，不是本项目运行结果 | 列出 3 篇以上，说明可借鉴流程和不可继承结论 |
| `eval:rfd3-record-required` | RFD3 设计记录必须包含哪些参数？ | [RFdiffusion 方法卡](../02_方法笔记/RFdiffusion与蛋白设计.md), [RFdiffusion 模板](../04_实验记录/模板_RFdiffusion骨架生成记录.md), [证据矩阵](证据与claims矩阵.md) | `watson_novo_2023`, `ahern_atom_2025`, `yang_w_past_2026` | 设计候选不等于功能 binder；本库尚无真实 RFD3 输出 | 至少列出 motif、contig、链定义、input、seed、diffusion settings、筛选标准、后续 ProteinMPNN |
| `eval:uxs1-entity-path` | UXS1 关联哪些资料、文献和下一步实验？ | [实体索引](实体索引.md), [研究问题与项目池](研究问题与项目池.md), [阅读队列](阅读队列.md) | `sui_targeting_2026` | metformin/UXS1 是文献案例，不是本项目命中物 | 给出 UXS1、metformin、项目池任务和下一步 dry-run 建议 |
| `eval:chai1-score-boundary` | Chai-1 aggregate score 应该如何解释？ | [Chai-1 方法卡](../02_方法笔记/Chai1互作蛋白虚拟筛选.md), [Chai-1 模板](../04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md), [证据矩阵](证据与claims矩阵.md) | 当前应写“待补正式 Chai-1 锚点” | aggregate score 只能作排序/复核信号，不能当真实 Kd 或功能活性 | 同时提到界面接触、局部置信度、PAE/冲突和待补文献 |
| `eval:boltz2-affinity-qc` | Boltz2 亲和力输出需要哪些 QC 才能写入结论？ | [Boltz2 方法卡](../02_方法笔记/Boltz2亲和力预测.md), [Boltz2 结果样例](../04_实验记录/Boltz2结果_l6D9Z7.md), [证据矩阵](证据与claims矩阵.md) | `passaro_boltz-2_2025` | 单次预测不等于实验 Kd | 至少包含输入 YAML、结构置信度、链/配体状态、口袋合理性、对照和解释边界 |
| `eval:docking-score-use` | docking score 能否直接比较不同软件或不同受体准备流程的候选？ | [对接方法卡](../02_方法笔记/AI多组分对接与虚拟筛选.md), [证据矩阵](证据与claims矩阵.md) | `du_dockey_2023`, `crampon_machine-learning_2022`, `gu_benchmarking_2025` | 不能跨软件/流程直接比较；需 pose QC 和可能的重打分 | 明确 score 是排序信号，不是亲和力 |
| `eval:ape1-project-start` | 如果要把 APE1 文献案例转成用户自己的天然产物筛选项目，第一步做什么？ | [实体索引](实体索引.md), [项目池](研究问题与项目池.md), [实验队列](实验队列.md) | `shen_structure-based_2026` | 先做字段演练，不声明命中 | 建议复制对接模板，定义结构、候选库、box、参数和 top pose QC |
| `eval:ido1-benchmark-fields` | IDO1 scaffold-aware ML + ensemble docking benchmark 应先建哪些字段？ | [研究问题与项目池](研究问题与项目池.md), [实验队列](实验队列.md), [阅读队列](阅读队列.md) | `tomarchio_reproducible_2026` | 在数据集和 split 未确定前不能训练或宣称结果 | 包含数据、scaffold split、ensemble structures、score、MD 指标、失败原因 |
| `eval:baba-design-boundary` | BabA binder 设计案例能给本项目什么，不能给什么？ | [实体索引](实体索引.md), [项目池](研究问题与项目池.md), [输出视图](输出视图.md) | `zhu_novo_2026`, `yang_w_past_2026` | 可借鉴流程和记录规范，不能继承论文 binder 结论 | 同时指向 RFdiffusion/RFD3 模板和 ProteinMPNN 后处理 |
| `eval:project-output-layering` | 写课件或综述时，如何区分课程资料、文献证据和本项目结果？ | [输出视图](输出视图.md), [证据矩阵](证据与claims矩阵.md), [根索引](../index.md) | 视主题引用相关 key | 不把文献案例或教学范文写成项目结果 | 能复述三层分工，并给出至少 2 个例子 |
| `eval:research-workbench-priority` | 当前最值得先做的个人研究工作台任务是哪两个？为什么？ | [研究问题与项目池](研究问题与项目池.md), [实验队列](实验队列.md), [证据矩阵](证据与claims矩阵.md) | `passaro_boltz-2_2025`, `shen_structure-based_2026` 或相关 key | 项目池是候选，不是正式执行计划 | 推荐 Boltz2 对照或 APE1 dry-run，并说明模板完整度和风险较低 |
| `eval:literature-without-bib` | 哪些重要任务还缺 Zotero/BibTeX 锚点？ | [阅读队列](阅读队列.md), [证据矩阵](证据与claims矩阵.md) | 应明确 Chai-1 为待补 | 缺锚点时不能写成正式引用依据 | 列出 Chai-1、FEP/free energy、BioEmu/AI 采样或 Uni-Dock/MSA 的待补状态 |

## 人工验收方法

- 抽测时只给 AI 问题，不给本页答案。
- 合格答案必须有文件路径、Zotero/BibTeX key、边界和下一步。
- 如果回答只复述流程、不引用路径或把文献案例写成项目结果，则判为未通过。
