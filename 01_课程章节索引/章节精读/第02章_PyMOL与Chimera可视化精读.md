---
title: "第02章 PyMOL与Chimera可视化精读"
created: 2026-05-30
type: chapter-deep-note
status: draft
topics: [chapter/02, pymol, chimera, visualization]
source_files: ["06_原始学习素材/第02章_PyMOL_Chimera可视化/原始PDF/第二章Pymol与Chimira可视化.pdf", "06_原始学习素材/第02章_PyMOL_Chimera可视化/全文提取/第二章Pymol与Chimira可视化/全文.md"]
zotero_items: ["UYRXX2U2", "PE42AXJX"]
bibtex_keys: ["jumper_highly_2021", "abramson_accurate_2024"]
related: ["../../02_方法笔记/PyMOL与Chimera可视化.md", "../../03_文献笔记/AlphaFold结构预测.md", "../../06_原始学习素材/PDF OCR质量收敛报告.md"]
---
# 第02章 PyMOL与Chimera可视化精读

## 本章定位

这一章解决“看结构、解释结构、输出结构图”的问题。PyMOL 更适合高质量展示和脚本化出图，Chimera/ChimeraX 更适合结构处理、叠合、密度/表面和交互式分析。

## 核心概念

- 表示方式决定你看到什么：cartoon 看二级结构，sticks 看配体和关键残基，surface 看口袋和整体形状，mesh/volume 看密度或空间占据。
- 结构图不是截图，应该可复现：颜色、背景、光线、标签、选择集和视角都应能通过命令重建。
- `.pymolrc` 是长期复用的默认配置入口，适合写背景、渲染、抗锯齿、颜色别名和常用宏。
- 结构叠合需要先明确比较对象：全局骨架、活性口袋、配体附近残基还是突变区域。

## 可执行流程

1. 加载结构文件，先检查链、配体、水分子、金属离子和缺失残基。
2. 选择展示层级：整体结构用 cartoon，活性位点用 sticks/spheres，口袋用 surface。
3. 统一视觉规则：背景、配色、透明度、标签和图片尺寸。
4. 做分析图：距离、氢键、疏水接触、静电表面、结构叠合 RMSD。
5. 导出图片前记录命令或 session，确保可以重新生成。

## 易错点

- 没有隐藏水分子或无关链，导致图面复杂且误导。
- 用全局 RMSD 解释局部口袋变化，或反过来用局部叠合解释整体构象。
- 出图只靠手动旋转，没有保存视角和脚本，后续无法复现。
- 混淆 Chimera、ChimeraX 和 PyMOL 的命令体系。

## 本项目落地

- 对接、MD、Boltz2 或 RFdiffusion 结果都应至少保留一张结构复核图和对应会话/命令。
- 章节笔记只记录判断逻辑，具体作图命令归入 `02_方法笔记/PyMOL与Chimera可视化.md`。

## 文献锚点

- `UYRXX2U2` / `jumper_highly_2021`：AlphaFold2 单体结构预测背景，用于解释可视化对象常来自预测结构而非实验结构。
- `PE42AXJX` / `abramson_accurate_2024`：AlphaFold3 复合物预测背景，用于解释后续多组分结构图和相互作用图的可信度边界。
- 当前 Zotero 检索未找到 PyMOL 或 Chimera/ChimeraX 专门条目；软件操作仍以课件、方法卡和官方文档为主。

## 来源定位

| 主题 | 来源页 |
|:---|:---|
| PyMOL 安装与启动 | [page-004.md](../../06_原始学习素材/第02章_PyMOL_Chimera可视化/全文提取/第二章Pymol与Chimira可视化/pages/page-004.md) |
| .pymolrc 默认设置 | [page-005.md](../../06_原始学习素材/第02章_PyMOL_Chimera可视化/全文提取/第二章Pymol与Chimira可视化/pages/page-005.md) |
| 作图渲染参数 | [page-006.md](../../06_原始学习素材/第02章_PyMOL_Chimera可视化/全文提取/第二章Pymol与Chimira可视化/pages/page-006.md) |
| OCR 复核页 | [page-001.ocr.md](../../06_原始学习素材/第02章_PyMOL_Chimera可视化/全文提取/第二章Pymol与Chimira可视化/ocr/page-001.ocr.md) |
