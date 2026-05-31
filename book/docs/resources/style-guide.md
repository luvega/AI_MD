# P25 中文教材正文风格指南

本指南用于 AI_MD 在线书籍正文润色。它综合 `Research-Paper-Writing-Skills` 的段落功能、reverse outline、claim-evidence alignment，以及 `academic-chinese-style` 的中文生物医学写作边界。

## 适用范围

- 适用于 `book/docs/chapters/` 的教学正文、资源页说明和维护报告摘要。
- 不改写 `<!-- refs:start -->...<!-- refs:end -->` 内的自动引用卡片。
- 不改写代码块、图片链接、DOI/URL、BibTeX key、Zotero item key、文件路径和 manifest 字段。

## 段落规则

- 每段只承担一个功能，第一句说明本段要解决的问题或判断。
- 教学段落优先采用“问题场景 -> 方法动作 -> 证据边界 -> 下一步”的顺序。
- 长流程用表格表达 `输入 | 动作 | 输出 | QC/边界`，不要把所有步骤塞进一个长段落。
- 章节结尾必须指向下一章、研究工作台或实验记录模板。

## 证据边界

| 证据强度 | 推荐动词 | 避免 |
|:---|:---|:---|
| 直接实验或严格验证 | 表明、证实、证明 | 无来源地使用 |
| 多来源一致模式 | 提示、支持、说明 | 写成决定性结论 |
| 模型预测或评分 | 可能提示、可作为排序线索 | 写成 Kd、IC50、结合强度或活性 |
| 文献案例/课程范文 | 可借鉴、可作为案例 | 写成本项目结果 |

## 术语与 provenance

- `docking score`、`predicted affinity`、`confidence`、`aggregate score`、`RFdiffusion/RFD3`、`ProteinMPNN`、`Chai-1` 保持术语一致。
- Zotero item key 和 BibTeX key 必须原样保留，二者不能互换。
- 原始 PDF 和补充材料只作为来源，不直接复制图表到在线书籍。

## P25 来源

- `Research-Paper-Writing-Skills`，commit `9ee5eddc10068cc52590b3a68a827d3a387f5af9`。
- `luvega/codex-skills` 的 `academic-chinese-style`，commit `e7088ef3f476d4ea5720ea56cc72bc8a1cd6eea0`。
