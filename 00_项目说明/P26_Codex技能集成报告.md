---
title: "P26 Codex技能集成报告"
created: 2026-06-02
type: maintenance-report
status: active
topics: [codex-skills, scientific-agent-skills, routing, p26]
source_files: ["CLAUDE.md", "00_项目说明/插件与Skills调用说明.md", "tools/install_ai_md_codex_skills.ps1"]
zotero_items: []
bibtex_keys: []
related: ["Codex技能调用矩阵.md", "插件与Skills调用说明.md"]
wiki_role: maintenance
source_count: 3
last_reviewed: 2026-06-02
claims:
  - "AI_MD P26 采用全局 Codex skills 安装，不向 .claude/skills 添加第三方 skill 副本。"
  - "精选 scientific-agent-skills 固定到 commit 93124850ef08487e423165554c54f0b333d5631d。"
relations:
  - type: updates
    target: "插件与Skills调用说明.md"
  - type: updates
    target: "../CLAUDE.md"
---
# P26 Codex技能集成报告

## 集成结论

P26 已将第三方技能集成方式从项目内 `.claude/skills/` 改为全局 Codex skills。实际安装位置为 `C:\Users\xsui\.codex\skills`；AI_MD 仓库只记录调用矩阵、安装脚本和维护报告，不提交第三方技能源码。

外部来源固定为：

- 仓库：`K-Dense-AI/scientific-agent-skills`
- commit：`93124850ef08487e423165554c54f0b333d5631d`
- 安装脚本：`C:\Users\xsui\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py`

安装后需要重启 Codex，新的全局 skills 才会稳定出现在会话可用技能列表中。

## 已安装 Codex skills

| 分组 | 技能 | AI_MD 用途 |
|:---|:---|:---|
| 专业内容撰写与文字修正 | `scientific-writing` | 下一版教材正文、段落结构和学术写作出口。 |
| 专业内容撰写与文字修正 | `literature-review` | 第 3/5/6/8 章文献补强和综述线索。 |
| 专业内容撰写与文字修正 | `citation-management` | DOI、参考文献元数据和引用准确性复核。 |
| 专业内容撰写与文字修正 | `peer-review` | 章节级审稿、方法边界和缺口清单。 |
| 专业内容撰写与文字修正 | `scientific-critical-thinking` | claim-evidence map、证据强度和过度表述降级。 |
| 专业内容撰写与文字修正 | `hypothesis-generation` | 研究问题与项目池的假设、预测和实验设计。 |
| 专业内容撰写与文字修正 | `research-grants` | 课题申请、研究意义和创新性出口视图。 |
| 内容组织与版面设计 | `markdown-mermaid-writing` | Markdown 章节结构、Mermaid 图和文本化流程图。 |
| 内容组织与版面设计 | `scientific-schematics` | 科学示意图和流程图设计提示。 |
| 内容组织与版面设计 | `scientific-slides` | 课程讲义到组会/课堂幻灯片出口。 |
| 内容组织与版面设计 | `venue-templates` | 论文、会议、海报和基金格式要求参考。 |
| 内容组织与版面设计 | `markitdown` | 新增 Office/PDF/网页资料转 Markdown 的候选入口。 |
| 数据分析与 AIDD 流程 | `exploratory-data-analysis` | 对 SDF/CSV/TSV/轨迹摘要等数据做结构和质量初筛。 |
| 数据分析与 AIDD 流程 | `statistical-analysis` | 统计检验选择、假设检查和报告措辞。 |
| 数据分析与 AIDD 流程 | `scientific-visualization` | 发表级多面板图、配色和图注规范。 |
| 数据分析与 AIDD 流程 | `networkx` | 知识图谱、实体关系和引用网络分析。 |
| 数据分析与 AIDD 流程 | `datamol` | 标准药物发现 SMILES/SDF 处理和描述符计算。 |
| 数据分析与 AIDD 流程 | `rdkit` | 进阶化学信息学、指纹、子结构和构象处理。 |
| 数据分析与 AIDD 流程 | `medchem` | 成药性规则、PAINS/结构警报和化合物库筛选。 |
| 数据分析与 AIDD 流程 | `molecular-dynamics` | MD 设置、轨迹分析和结果边界说明。 |
| 数据分析与 AIDD 流程 | `diffdock` | 扩散对接流程、pose 预测和虚拟筛选示例；不用于亲和力结论。 |

## 跳过项

| 技能 | 跳过原因 |
|:---|:---|
| `docx`、`pptx`、`pdf`、`xlsx` | 本机已有 Codex `doc`、`pdf`、`pptx-extractor` 等能力；不重复引入同类专有许可证技能。 |
| `pyzotero` | AI_MD 当前使用 Zotero 插件、本地 `references.bib` 和 `zotero-map.tsv`；不引入 Zotero Web API key 依赖。 |
| `infographics` | 依赖额外外部图像服务；P26 只安装低风险、可直接服务知识库更新的技能。 |

## 使用边界

- 第三方 Codex skills 是辅助能力，不替代 AI_MD 的 raw/wiki/schema 三层结构。
- 原始资料仍在 `06_原始学习素材/` 本地保留，内容不上传 GitHub。
- 在线书籍只写整理后的教学内容，不复制原始 PDF 图表，不把文献案例写成本项目结果。
- 正式引用仍以 `references/references.bib` 和 `references/zotero-map.tsv` 为准。
- AI_MD 自有 `.claude/skills` 的全局 Codex skills 迁移已在 P27 完成；历史目录继续保留为来源和兼容层。

## 验收记录

- 全局技能目录检查：21 个精选技能均位于 `C:\Users\xsui\.codex\skills`。
- 仓库边界：未向 `.claude/skills/` 添加第三方 skill 副本。
- 需重启 Codex：是。
