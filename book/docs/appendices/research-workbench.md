# 附录 A 研究问题与项目池

本附录把课程讲义与个人研究工作台连接起来。它面向课程讲义读者，帮助读者理解如何从课程案例走向可执行研究任务。

## 项目池

| project_id | 研究问题 | 推荐入口 | 当前状态 |
|:---|:---|:---|:---|
| `proj:uxs1-metformin-transfer` | UXS1/metformin 机制与虚拟筛选思路能否迁移到代谢相关课题？ | [第 8 章](../chapters/chapter-08.md) | 文献案例，需确认真实课题对象 |
| `proj:ape1-natural-product-screen` | APE1 结构口袋虚拟筛选能否作为天然产物筛选模板？ | [第 3 章](../chapters/chapter-03.md) | 适合先做 docking dry-run |
| `proj:ido1-reproducible-vs` | IDO1 ML + ensemble docking + MD 能否作为可复现筛选 benchmark？ | [第 3 章](../chapters/chapter-03.md) | 需要数据集和 split 设计 |
| `proj:baba-binder-design` | BabA binder 设计案例能否转成 RFD3/RFdiffusion 训练任务？ | [第 6 章](../chapters/chapter-06.md) | 适合先做参数记录规范 |
| `proj:chai1-ppi-panel` | Chai-1 能否从候选蛋白面板中优先筛选互作伙伴？ | [第 8 章](../chapters/chapter-08.md) | 缺正式 Chai-1 文献锚点 |
| `proj:boltz2-affinity-triage` | Boltz2 是否适合做候选小分子/肽亲和力 triage？ | [第 5 章](../chapters/chapter-05.md) | 适合先做正/负对照样例 |

## 推荐首个执行任务

优先选择 `proj:boltz2-affinity-triage` 或 `proj:ape1-natural-product-screen`。这两个方向模板完整、边界清楚，能快速形成真实记录，同时不需要先承诺大规模课题。

## 来源索引

- 研究问题来源：`07_研究工作台/研究问题与项目池.md`
- 实体来源：`07_研究工作台/实体索引.md`
- 实验队列来源：`07_研究工作台/实验队列.md`

## 边界提示

项目池是候选研究方向，不是已经执行的实验计划。任何项目进入真实执行前，都必须明确靶点、候选库、数据来源、软件版本、实验条件和可产出物。
