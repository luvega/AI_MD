---
title: "P28 重点章节Codex审稿报告"
created: 2026-06-02
type: maintenance-report
status: active
topics: [online-book, peer-review, scientific-critical-thinking, scientific-writing, p28]
source_files: ["book/docs/chapters/chapter-03.md", "book/docs/chapters/chapter-05.md", "book/docs/chapters/chapter-06.md", "book/docs/chapters/chapter-08.md", "book/docs/resources/polish-report.md", "00_项目说明/Codex技能调用矩阵.md"]
zotero_items: []
bibtex_keys: []
related: ["P27_Codex项目规则迁移报告.md", "Codex技能调用矩阵.md", "../book/docs/resources/polish-report.md", "../07_研究工作台/证据与claims矩阵.md"]
wiki_role: maintenance
source_count: 6
last_reviewed: 2026-06-02
claims:
  - "第 3/5/6/8 章当前没有把 score、predicted affinity、生成式设计候选或文献案例直接写成实验结论。"
  - "下一版正文更新应继续优先处理 docking score、affinity、RFdiffusion/RFD3、ProteinMPNN 和 Chai-1 aggregate score 的证据边界。"
relations:
  - type: extends
    target: "P27_Codex项目规则迁移报告.md"
  - type: supports
    target: "../book/docs/resources/polish-report.md"
  - type: supports
    target: "../07_研究工作台/证据与claims矩阵.md"
  - type: updates
    target: "Codex技能调用矩阵.md"
---
# P28 重点章节Codex审稿报告

## 审稿范围

本轮按 `peer-review`、`scientific-critical-thinking` 和 `scientific-writing` 的原则，对在线书籍第 3、5、6、8 章进行高风险表述审查。审查对象是正文中的方法解释、代码案例说明、使用边界和文献案例口径，不重写章节、不新增科学事实、不改引用区。

审查重点包括：

| 章节 | 高风险对象 | 主要误读风险 |
|:---|:---|:---|
| 第 3 章 | docking score、pose、rescore、虚拟筛选漏斗 | 把排序分数写成结合自由能、IC50 或实验活性。 |
| 第 5 章 | predicted affinity、confidence、模型评估 | 把模型预测值写成实验 Kd、IC50 或确定性优先级。 |
| 第 6 章 | RFdiffusion/RFD3、ProteinMPNN、回折叠验证 | 把生成结构或序列候选写成可表达、可结合或已验证 binder。 |
| 第 8 章 | 文献案例、Chai-1 aggregate score、项目池 | 把课程范文、补充 PDF 或排序线索写成本项目运行结果。 |

## 总体结论

当前第 3、5、6、8 章已经具备基本的证据边界意识。正文中反复使用“排序线索”“提示”“仍需验证”“不能等同实验值”“文献案例不能写成本项目结果”等表述，未发现需要立即修正的决定性越界结论。

下一版仍应继续补强三个方面：第一，把边界提示从段落说明推进到可执行检查表；第二，把每章的代码案例和实验记录模板连接起来，让读者知道哪些字段必须记录；第三，在 P29-P31 中用文献复核、Mermaid 图和 dry-run 数据流程补足“怎么做”和“怎么验收”的闭环。

## 分章审稿意见

| 章节 | 当前判断 | 风险等级 | 后续修改建议 |
|:---|:---|:---|:---|
| 第 3 章 | `docking score` 被明确限定为排序线索；正文说明不能写成 Kd、IC50、结合自由能或实验活性。 | 中 | 下一版增加“跨软件、跨靶点、跨化学系列不可直接比较”的检查项，并把 `score`、`pose`、`filter_reason` 写入 dry-run manifest 示例。 |
| 第 5 章 | `predicted affinity` 与 `confidence` 已分层；正文说明预测值不能默认等同实验亲和力。 | 中 | 增加模型校准、已知阳性/阴性对照、适用域和失败样本记录字段，避免只按单一预测值排序。 |
| 第 6 章 | RFdiffusion/RFD3 生成结构、ProteinMPNN 序列和回折叠验证均被写成候选证据，不被写成实验成功。 | 中高 | 记录 checkpoint、seed、约束、设计多样性、回折叠指标、界面检查和实验可行性，尤其避免把生成候选称为 binder。 |
| 第 8 章 | 明确第八章补充 PDF 是文献案例和方法借鉴；Chai-1 aggregate score 被限定为排序线索。 | 中高 | 在项目池中增加“证据成熟度”字段，并把“课程范文/文献案例/本项目 dry-run/真实运行结果”作为固定标签。 |

## Claim-Evidence-Risk Matrix

| Claim | Evidence | Risk | Status |
|:---|:---|:---|:---|
| docking score 可用于候选排序。 | 第 3 章方法流程、P25 polish report、研究工作台 claims 矩阵。 | 如果缺少 pose QC 和重评分，容易被误写成活性。 | supported with boundary |
| predicted affinity 可作为候选优先级线索。 | 第 5 章方法流程、Boltz2 解释区、P25 polish report。 | 如果不看 confidence、输入质量和适用域，容易被误写成实验亲和力。 | supported with boundary |
| RFdiffusion/RFD3 输出可进入设计候选池。 | 第 6 章方法流程、ProteinMPNN 和回折叠边界。 | 如果缺少 seed/checkpoint/回折叠/实验可行性记录，容易被误写成成功设计。 | supported with boundary |
| ProteinMPNN 序列可支持序列候选生成。 | 第 6 章核心概念和实验模板。 | 序列候选不等于可表达、稳定或可结合蛋白。 | supported with boundary |
| Chai-1 aggregate score 可作为 PPI 候选排序线索。 | 第 8 章使用边界和 Chai-1 方法卡。 | 容易被误写成实验 PPI 结合强度。 | supported with boundary |
| 文献案例可作为方法借鉴。 | P14 文献锚定、P24/P25 边界说明、第 8 章正文。 | 最常见风险是把 case study 写成本项目结果。 | supported with boundary |

## 审稿人视角的关键意见

1. 方法边界总体合格，但第 3/5/6/8 章都需要更强的“字段化验收”。读者不仅要知道不能过度解释，还要知道在实验记录中必须留下哪些输入、参数、输出和 QC 证据。
2. 第 6 章风险最高，因为生成式蛋白设计的语言很容易从“候选”滑向“成功设计”。后续正文和模板应统一使用“生成候选”“进入验证队列”“待回折叠和实验确认”。
3. 第 8 章应作为全书的证据分层样板。所有从补充 PDF、文献案例或课程范文获得的内容，都应在项目池里显式标注来源类型和证据成熟度。
4. 第 5 章应补一个最小校准案例：已知 ligand、阴性或低活性对照、模型输出、置信度、人工解释。没有校准数据时，只能写“排序建议”。

## P29-P31 交接

| 下一阶段 | 输入 | 目标输出 |
|:---|:---|:---|
| P29 文献与引用补强 | 第 3/5/6/8 章引用区、`references/references.bib`、`references/zotero-map.tsv` | 复核关键文献是否足以支持当前边界；缺口进入候选表，正式结果仍写入 `references/`。 |
| P30 图示与版面升级 | 章节方法流程、知识图谱入口、Imagegen 图像清单 | 为每章设计 Mermaid 结构图和原创示意图 prompt，先形成可审查文本结构。 |
| P31 数据分析与 AIDD dry-run | 代码案例、实验记录模板、研究工作台 claims 矩阵 | 用 `datamol`、`rdkit`、`medchem`、`molecular-dynamics`、`diffdock` 补 dry-run 数据流程和模板字段。 |

## 待作者确认项

- 是否在第 3/5/6/8 章正文中立即加入 P28 建议的检查表，还是等 P29-P31 同步补文献、图示和 dry-run 后一次性改写。
- 第 6 章是否需要把 RFD3 与 RFdiffusion2 的命名、版本和文献边界单独拆成一个小节，避免读者把不同工具链混用。
- 第 8 章项目池是否采用四级证据成熟度：`case-study`、`dry-run`、`validated-computation`、`experimental-result`。
