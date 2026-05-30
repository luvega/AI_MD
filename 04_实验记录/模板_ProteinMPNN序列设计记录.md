---
title: "模板：ProteinMPNN 序列设计记录"
created: 2026-05-30
type: experiment-record
status: draft
topics: [type/experiment, status/draft, topic/protein-design, chapter/6]
source_files: ["02_方法笔记/RFdiffusion与蛋白设计.md"]
zotero_items: ["V2WLND5M"]
bibtex_keys: ["dauparas_robust_2022"]
related: ["../02_方法笔记/RFdiffusion与蛋白设计.md", "../03_文献笔记/ProteinMPNN序列设计.md"]
---

# 模板：ProteinMPNN 序列设计记录

## 任务定义

- 任务 ID：待填。
- 输入骨架来源：RFdiffusion / 实验结构 / 人工设计。
- 输入结构路径：待填。
- 固定残基或功能位点：待填。

## 参数

| 参数 | 值 | 说明 |
|:---|:---|:---|
| ProteinMPNN 版本 | 待填 | 代码版本或 commit |
| temperature | 待填 | 控制序列多样性 |
| num_seq_per_target | 待填 | 每个骨架生成序列数 |
| fixed_positions | 待填 | 固定 motif、活性位点或界面残基 |
| omit_AA / bias_AA | 待填 | 排除或偏置氨基酸 |
| seed | 待填 | 可复现 |

## 输出和筛选

| design_id | sequence_id | fasta_path | score | recovery_or_identity | fixed_residue_ok | qc_status | next_step |
|:---|:---|:---|---:|---:|:---|:---|:---|
| 待填 | 待填 | 待填 | 待填 | 待填 | pass/review/fail | pass/review/fail | 回折叠/淘汰 |

## 回折叠验证

| sequence_id | model_path | plddt | ptm_iptm | motif_rmsd | interface_ok | decision |
|:---|:---|---:|---:|---:|:---|:---|
| 待填 | 待填 | 待填 | 待填 | 待填 | pass/review/fail | 保留/淘汰 |

## 结论

- 推荐序列：待填。
- 失败模式：待填。
- 下一步：LigandMPNN / BindCraft / Boltz2 / MD / 实验。
