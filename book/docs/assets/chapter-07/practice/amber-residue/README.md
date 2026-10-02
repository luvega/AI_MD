# 真实残基分解阅读练习

数据来自 [Amber 官方 Ras–Raf 教程 3.6](https://ambermd.org/tutorials/advanced/tutorial3/py_script/section6.htm)公开的 [FINAL_DECOMP_MMPBSA_perres.dat](https://ambermd.org/tutorials/advanced/tutorial3/py_script/files/FINAL_DECOMP_MMPBSA_perres.dat)。上游是 2010 年 Amber MMPBSA.py 的真实 50 帧结果。本目录只抽取其中第一段 GB、DELTAS、Total 的 R 侧 LYS5 和 30–40 位点，共 12 个残基；没有复制教程文字、截图或课堂素材。

这是第二套外部真实体系，与 `official-gb` 的 gmx_MMPBSA 蛋白–配体案例不同，也不是 3HTB/JZ4。`source-record.json` 记录原文件校验值、结果时间和参数。上游使用 `igb=5`、盐浓度 0.100 M、`idecomp=1`，并提示半径设置需要复核；本练习只读取旧输出，不把这套历史配置当作推荐参数。

TSV 保存各分项均值和原文件所报 SD。SD 不是 SEM，也不是本章重新计算的独立重复误差。没有从这些汇总值重建逐帧数据。五个分项均值之和与 TOTAL 在源文件舍入范围内相符。

```bash
python code/read-residue.py --input practice/amber-residue/ras-selected-residue.tsv --outdir outputs/residue
```

图只包括选中的 12 个残基。比较静电与极性溶剂化分项时，应一起看 TOTAL；不能把其中一个有利分项直接称为“关键残基”。
