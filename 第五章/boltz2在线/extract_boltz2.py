#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
from pathlib import Path
from statistics import mean


def safe_first(x, default=None):
    """
    Boltz2 json 里很多值是 list，比如 [0.9]。
    这个函数用于安全取第一个值。
    """
    if isinstance(x, list) and len(x) > 0:
        return x[0]
    return x if x is not None else default


def parse_mmcif_plddt_from_ma_qa(cif_text):
    """
    从 mmCIF 中解析 _ma_qa_metric_local 表里的 pLDDT。

    返回列表：
    [
        {
            "asym_id": "A",
            "seq_id": 1,
            "comp_id": "MET",
            "plddt": 84.329
        },
        ...
    ]

    这个解析器针对你给的 Boltz2/ModelCIF 格式足够用。
    """
    lines = cif_text.splitlines()
    results = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 找到 loop_
        if line == "loop_":
            headers = []
            j = i + 1

            # 收集 header
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith("_"):
                    headers.append(s)
                    j += 1
                else:
                    break

            # 判断是不是 _ma_qa_metric_local 这个 loop
            if any(h.startswith("_ma_qa_metric_local.") for h in headers):
                # 需要的列
                required = [
                    "_ma_qa_metric_local.label_asym_id",
                    "_ma_qa_metric_local.label_seq_id",
                    "_ma_qa_metric_local.label_comp_id",
                    "_ma_qa_metric_local.metric_value",
                ]

                header_index = {h: idx for idx, h in enumerate(headers)}

                missing = [h for h in required if h not in header_index]
                if missing:
                    raise ValueError(f"ma_qa_metric_local 缺少字段: {missing}")

                # 读取数据行，直到 # 或新 loop
                while j < len(lines):
                    s = lines[j].strip()

                    if not s:
                        j += 1
                        continue

                    if s == "#" or s.startswith("loop_") or s.startswith("_"):
                        break

                    parts = s.split()

                    # 防御性判断
                    if len(parts) >= len(headers):
                        asym_id = parts[header_index["_ma_qa_metric_local.label_asym_id"]]
                        seq_id = parts[header_index["_ma_qa_metric_local.label_seq_id"]]
                        comp_id = parts[header_index["_ma_qa_metric_local.label_comp_id"]]
                        metric_value = parts[header_index["_ma_qa_metric_local.metric_value"]]

                        # ligand 的 seq_id 可能也是 1，这里统一处理
                        try:
                            seq_id_int = int(seq_id)
                        except ValueError:
                            seq_id_int = None

                        try:
                            plddt_float = float(metric_value)
                        except ValueError:
                            plddt_float = None

                        results.append({
                            "asym_id": asym_id,
                            "seq_id": seq_id_int,
                            "comp_id": comp_id,
                            "plddt": plddt_float,
                        })

                    j += 1

                i = j
                continue

        i += 1

    return results


def parse_atom_site_bfactor_as_plddt(cif_text):
    """
    备用方法：
    从 _atom_site 里解析每个原子的 B_iso_or_equiv。
    在 AlphaFold/Boltz 类输出中，这通常也是 pLDDT。
    返回 atom-level 信息。

    注意：
    这里是原子级别，不是 residue 级别。
    """
    lines = cif_text.splitlines()
    atoms = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line == "loop_":
            headers = []
            j = i + 1

            while j < len(lines):
                s = lines[j].strip()
                if s.startswith("_"):
                    headers.append(s)
                    j += 1
                else:
                    break

            if any(h.startswith("_atom_site.") for h in headers):
                header_index = {h: idx for idx, h in enumerate(headers)}

                required = [
                    "_atom_site.group_PDB",
                    "_atom_site.label_atom_id",
                    "_atom_site.label_comp_id",
                    "_atom_site.label_seq_id",
                    "_atom_site.label_asym_id",
                    "_atom_site.Cartn_x",
                    "_atom_site.Cartn_y",
                    "_atom_site.Cartn_z",
                    "_atom_site.B_iso_or_equiv",
                ]

                if not all(h in header_index for h in required):
                    i = j
                    continue

                while j < len(lines):
                    s = lines[j].strip()

                    if not s:
                        j += 1
                        continue

                    if s == "#" or s.startswith("loop_") or s.startswith("_"):
                        break

                    parts = s.split()

                    if len(parts) >= len(headers):
                        def get(h):
                            return parts[header_index[h]]

                        try:
                            seq_id = int(get("_atom_site.label_seq_id"))
                        except ValueError:
                            seq_id = None

                        try:
                            bfactor = float(get("_atom_site.B_iso_or_equiv"))
                        except ValueError:
                            bfactor = None

                        atoms.append({
                            "group": get("_atom_site.group_PDB"),
                            "asym_id": get("_atom_site.label_asym_id"),
                            "seq_id": seq_id,
                            "comp_id": get("_atom_site.label_comp_id"),
                            "atom_id": get("_atom_site.label_atom_id"),
                            "x": float(get("_atom_site.Cartn_x")),
                            "y": float(get("_atom_site.Cartn_y")),
                            "z": float(get("_atom_site.Cartn_z")),
                            "bfactor_or_plddt": bfactor,
                        })

                    j += 1

                i = j
                continue

        i += 1

    return atoms


def extract_summary(data):
    """
    提取 JSON 顶层指标。
    """
    summary = {}

    # 时间指标
    metrics = data.get("metrics", {})
    for k, v in metrics.items():
        summary[k] = v

    # 常见 score
    score_keys = [
        "confidence_scores",
        "ptm_scores",
        "iptm_scores",
        "ligand_iptm_scores",
        "protein_iptm_scores",
        "complex_plddt_scores",
        "complex_iplddt_scores",
        "complex_pde_scores",
        "complex_ipde_scores",
    ]

    for key in score_keys:
        summary[key] = safe_first(data.get(key))

    # chains pTM
    chains_ptm = data.get("chains_ptm_scores")
    if isinstance(chains_ptm, list):
        for idx, val in enumerate(chains_ptm):
            summary[f"chain_{idx}_ptm"] = val

    # pair chain ipTM 原样保留到 json summary 中
    summary["pair_chains_iptm_scores"] = data.get("pair_chains_iptm_scores")

    # affinity
    affinities = data.get("affinities", {})
    for lig_name, lig_data in affinities.items():
        prefix = f"affinity_{lig_name}"

        for k, v in lig_data.items():
            summary[f"{prefix}_{k}"] = safe_first(v)

    return summary


def write_tsv_dict(path, data):
    """
    写一个 key-value tsv。
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("key\tvalue\n")
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v, ensure_ascii=False)
            f.write(f"{k}\t{v}\n")


def write_plddt_tsv(path, plddt_rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("asym_id\tseq_id\tcomp_id\tplddt\n")
        for r in plddt_rows:
            f.write(
                f"{r['asym_id']}\t"
                f"{r['seq_id']}\t"
                f"{r['comp_id']}\t"
                f"{r['plddt']}\n"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Parse Boltz2 JSON result file, extract scores, affinities, mmCIF, and pLDDT."
    )
    parser.add_argument(
        "-i", "--input",
        default="boltz2.json",
        help="Input Boltz2 JSON file. Default: boltz2.json"
    )
    parser.add_argument(
        "-o", "--outdir",
        default="boltz2_parsed",
        help="Output directory. Default: boltz2_parsed"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. summary
    summary = extract_summary(data)

    # 2. 保存 structure mmCIF
    structures = data.get("structures", [])
    saved_cif_paths = []

    for idx, s in enumerate(structures):
        cif_text = s.get("structure", "")
        fmt = s.get("format", "mmcif")
        source = s.get("source", f"structure_{idx}.cif")

        if not cif_text:
            continue

        # 优先用 source 名称
        cif_name = Path(source).name
        if not cif_name.endswith(".cif"):
            cif_name = f"structure_{idx}.cif"

        cif_path = outdir / cif_name
        with open(cif_path, "w", encoding="utf-8") as f:
            f.write(cif_text)

        saved_cif_paths.append(str(cif_path))

        # 解析 pLDDT
        plddt_rows = parse_mmcif_plddt_from_ma_qa(cif_text)

        if plddt_rows:
            plddt_path = outdir / f"{Path(cif_name).stem}_plddt.tsv"
            write_plddt_tsv(plddt_path, plddt_rows)

            protein_plddt = [
                r["plddt"] for r in plddt_rows
                if r["asym_id"] != "LIG" and r["plddt"] is not None
            ]
            ligand_plddt = [
                r["plddt"] for r in plddt_rows
                if r["asym_id"] == "LIG" and r["plddt"] is not None
            ]

            if protein_plddt:
                summary[f"{Path(cif_name).stem}_protein_mean_plddt"] = mean(protein_plddt)
                summary[f"{Path(cif_name).stem}_protein_min_plddt"] = min(protein_plddt)
                summary[f"{Path(cif_name).stem}_protein_max_plddt"] = max(protein_plddt)

            if ligand_plddt:
                summary[f"{Path(cif_name).stem}_ligand_mean_plddt"] = mean(ligand_plddt)

    summary["saved_cif_files"] = saved_cif_paths

    # 3. 输出 summary json
    summary_json_path = outdir / "summary.json"
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # 4. 输出 summary tsv
    summary_tsv_path = outdir / "summary.tsv"
    write_tsv_dict(summary_tsv_path, summary)

    # 5. 命令行打印关键信息
    print("解析完成")
    print(f"输入文件: {input_path}")
    print(f"输出目录: {outdir}")
    print(f"summary JSON: {summary_json_path}")
    print(f"summary TSV : {summary_tsv_path}")

    print("\n关键结果:")
    important_keys = [
        "confidence_scores",
        "ptm_scores",
        "iptm_scores",
        "ligand_iptm_scores",
        "complex_plddt_scores",
        "complex_iplddt_scores",
        "complex_pde_scores",
        "complex_ipde_scores",
    ]

    for k in important_keys:
        if k in summary:
            print(f"  {k}: {summary[k]}")

    # affinity 打印
    for k, v in summary.items():
        if k.startswith("affinity_"):
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
