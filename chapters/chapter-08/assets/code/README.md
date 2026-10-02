# 第 8 章公开练习脚本

从练习下载目录进入 chapter-08/assets 后运行。先用 `inspect-affinity.py` 解析 `results/3htb-jz4-single` 中独立 Boltz2 运行的两个原始 JSON，再用明确标记的构造 JSON 做排序与故障对照。已有真实输出可直接下载，字段解析无需 GPU。

```bash
python code/inspect-affinity.py --affinity results/3htb-jz4-single/affinity_3htb_jz4_single.json --confidence results/3htb-jz4-single/confidence_3htb_jz4_single_model_0.json --out outputs/actual-fields.tsv
```

接着读取构造字段。构造输入的三行数值不代表任何模型运行。

```bash
python code/inspect-affinity.py --input practice/constructed-output.json --out outputs/fields.tsv
```

`practice/3htb-jz4-noncovalent.yaml` 用于非共价输入检查；真实运行采用的单序列输入是 `results/3htb-jz4-single/actual-input.yaml`。两者的 MSA 设置不同，先核对各自说明。真实结果目录还保存 CIF、版本与权重校验值、解析记录和结构检查结果。

解析脚本分别保留概率、原始对数分值、结构置信度与数据状态；`check-actual-pose.py` 用公开 3HTB 坐标检查叠合与几何，`view-actual-pose.pml` 用于可选 PyMOL 结构阅读。命令和文件对应关系见结果目录 README。
