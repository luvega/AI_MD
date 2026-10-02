# 3HTB 三分子批处理任务说明

请在已经完成第 4 章 JZ4 单分子 re-docking 的工作目录中，整理并运行同一协议下的 JZ4、IPH、BNZ 三分子批次。先读现有文件和脚本，再给出简短执行计划。

## 已有输入

- `inputs/3htb/3htb_receptor.pdbqt` 与 `box.json`，沿用第 3 章准备结果。
- `inputs/3htb/JZ4.pdbqt`、`IPH.pdbqt`、`BNZ.pdbqt` 和 `jz4_reference.sdf`。
- 第 4 章 `run_vina_case.py`，用 `--vina` 显式传入本机 Vina 可执行文件。
- Python 环境已包含 RDKit、Meeko、NumPy 和 SciPy；不要另建名称不明的环境。

## 执行步骤

1. 检查输入是否齐全，读取受体、网格、配体状态和已有运行记录。
2. 先运行 JZ4 单分子任务，使用新输出目录。检查返回码、log、pose 和重原子 RMSD。
3. 单分子流程通过后，用原脚本运行 JZ4、IPH、BNZ。固定 `--cpu 2 --seed 20261002 --exhaustiveness 16`，保持受体、网格和打分函数一致。
4. 保留每个 log 和 pose；汇总 `ligand_id`、`status`、`vina_score_kcal_mol`、`pose_file`、`pose_review`。
5. 遇到失败，报告出错命令和日志位置。每次只改变一个条件，再使用新输出目录重跑。
6. 最后给出一张执行表和一个仍需人工检查的 pose 列表。

## 验收

- 每个输入都有对应输出状态。分数来自 log 中的真实模式 1 记录。
- JZ4 有晶体坐标系内、无拟合、考虑对称性的重原子 RMSD；不能把配体先拟合再称为 pose 复现。
- 报告记录 Vina 版本、seed、CPU 数、exhaustiveness 和网格参数。
- 既有输入、已完成结果和原始日志完整保留；新结果写入新目录。
- 不调用外部收费服务，不读取账号凭据，不修改系统设置。

## 交付说明

这三分子批次用于练习同协议自动化。Vina score 是计算排序字段，JZ4 RMSD 用于检查已知 pose；实验结合和功能验证另列为后续任务。
