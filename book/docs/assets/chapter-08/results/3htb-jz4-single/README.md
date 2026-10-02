# 独立真实 Boltz-2 结果

本结果从公开 3HTB A 链完整 SEQRES（164 aa）和 JZ4 中性 SMILES 独立运行，未使用课程 Boltz 原件。晶体坐标缺 LEU164，而本次模型包含该残基。实际输入为 `actual-input.yaml`，明确采用 `msa: empty`，与另一个需要 MSA 的公开准备 YAML 属于不同运行方案。

Boltz 2.2.1、Python 3.13、Torch 2.6.0+cu124，使用 RTX 3070 8 GB。设置为 seed 20261002、1 recycling step、结构 100 sampling steps/1 sample、亲和力 100 steps/1 sample，`no_kernels`、`num_workers=0`。完整版本与权重校验值见 `run-record.json`。

`3htb_jz4_single_model_0.cif`、`confidence_3htb_jz4_single_model_0.json` 与 `affinity_3htb_jz4_single.json` 是原始正式输出。`parsed-fields.tsv` 由本章脚本从两个 JSON 聚合，未改写原始数值。`structure-check.json` 记录 A1–A163 的 C-alpha 叠合与配体质心位置检查；质心差不等于按原子映射得到的配体 RMSD。

从下载包的 chapter-08/assets 目录运行。

```bash
python code/inspect-affinity.py --affinity results/3htb-jz4-single/affinity_3htb_jz4_single.json --confidence results/3htb-jz4-single/confidence_3htb_jz4_single_model_0.json --out outputs/actual-fields.tsv
```

这次真实模型读数约为 y=2.300788、结合者概率 0.204868、confidence 0.966183。换算的 `10**y` 是模型尺度数值，不是一次实验测定。单序列与少量取样只用于课堂可复现实践，不能代表默认 MSA 方案或模型性能评估。

需要重算结构核对时，从同一 assets 目录运行。

```bash
python -m pip install numpy gemmi
python code/check-actual-pose.py --model results/3htb-jz4-single/3htb_jz4_single_model_0.cif --reference ../../chapter-03/assets/data/3htb/3htb.pdb --out outputs/structure-check.json
```
