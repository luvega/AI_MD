# 公开输入与字段练习

`3htb-jz4-noncovalent.yaml` 是独立编写的非共价输入。蛋白序列从 [RCSB 3HTB](https://files.rcsb.org/download/3HTB.pdb) A 链 SEQRES 提取，共 164 个残基，为 T4 lysozyme L99A/M102Q。PDB REMARK 465 标注末端 LEU A164 缺坐标，实际晶体 ATOM 覆盖 A1–A163；完整序列输入与前章对接的坐标覆盖范围相差一残基。配体采用 [CCD JZ4](https://data.rcsb.org/rest/v1/core/chemcomp/JZ4) 的中性 2-propylphenol SMILES `CCCc1ccccc1O`。输入没有共价键约束，没有附加本地课程模板或上传课程原件。

正式 Boltz 单序列结果另存于 [results/3htb-jz4-single](../results/3htb-jz4-single/README.md)。必修练习先读取真实 JSON 与 CIF，再核对 YAML、识别输出字段和处理故意设置的错误。`constructed-output.json` 明确声明 `constructed_field_exercise`，其中数字是人工构造，不能作为 3HTB/JZ4 的模型结果、benchmark 或实验数据。

字段练习运行：

```bash
python code/inspect-affinity.py --input practice/constructed-output.json --out outputs/fields.tsv
```

有合适算力的学生可按 [Boltz 官方预测文档](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md) 配置环境后另行推理。公开 YAML 没有 `msa` 字段；使用 `--use_msa_server` 会把公开蛋白序列发送给 MSA 服务，或先自行生成 MSA 再在 YAML 指明文件。正式预测必须保存软件版本、权重、原始 YAML、MSA 来源、实际命令、运行日志和完整输出。显存不足时保留日志并转用已分配的教学算力；不要把构造 JSON 填入正式结果目录。
