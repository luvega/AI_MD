# 官方真实 MM/GBSA 输出练习

`gb_delta_total.csv` 原样取自 [gmx_MMPBSA 官方 API 示例](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/tree/5fe49f88eb6db7341e98f56803814473c0266d8d/examples/API)。上游 README 说明，它由官方蛋白–配体单轨迹示例的真实计算结果导出，包含 10 帧 `GB delta TOTAL` 和汇总行，单位为 kcal/mol，示例温度为 298.15 K。

固定版本为 `5fe49f88eb6db7341e98f56803814473c0266d8d`。原始 CSV 与同版本 GPL-3.0 许可证一起保存。没有运行或反序列化上游 compact/pickle 文件。教学统计和图形由本章 `read-official-gb.py` 从数值行独立重算。

它是外部真实 MM/GBSA 示例，不是 3HTB/JZ4 的重算，不是 MM/PBSA 输出，也不是本项目实验结果。当前工作机未配置 AmberTools；本章采用可在普通 Windows Python 环境运行的读取与时间窗比较作为必修实践，完整重新计算另列选学。

在下载包的本章 assets 目录运行。

```bash
python code/read-official-gb.py --input practice/official-gb/gb_delta_total.csv --outdir outputs/full
python code/read-official-gb.py --input practice/official-gb/gb_delta_total.csv --startframe 6 --endframe 10 --outdir outputs/last-five
```

完整 10 帧的平均值为 -15.017773104 kcal/mol，population SD 为 1.686022904 kcal/mol。脚本将帧行与 `Average`、`SD`、`SEM` 分开；不能把汇总行当成三次额外观测。`naive_sem` 是按帧数代入公式的结果，未处理帧间相关性。
