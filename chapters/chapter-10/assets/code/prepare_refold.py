"""Convert actual ProteinMPNN FASTA records into Boltz complex inputs and a queue."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import re


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records = []
    header = None
    parts: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(parts)))
            header, parts = line[1:], []
        elif line:
            parts.append(line)
    if header is not None:
        records.append((header, "".join(parts)))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fasta", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    target_records = read_fasta(args.target)
    if len(target_records) != 1:
        raise ValueError("Target FASTA must have one sequence")
    target = target_records[0][1]
    if not re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", target):
        raise ValueError("Target must contain standard amino acids only")
    rows = []
    args.out.mkdir(parents=True, exist_ok=True)
    design_records = read_fasta(args.fasta)
    seed = re.search(r"seed=(\d+)", " ".join(header for header, _ in design_records))
    for header, sequence in design_records:
        if "sample=" not in header:
            continue
        if not re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", sequence):
            raise ValueError("Each design record must contain one standard-amino-acid chain")
        sample = re.search(r"sample=(\d+)", header).group(1)
        name = f"pdl1_mpnn_{sample}"
        # Designed chains have no precomputed MSA; use explicit single-sequence mode.
        # This teaching run uses explicit single-sequence inputs for BOTH chains.
        yaml = f"version: 1\nsequences:\n  - protein:\n      id: A\n      sequence: {sequence}\n      msa: empty\n  - protein:\n      id: B\n      sequence: {target}\n      msa: empty\n"
        (args.out / f"{name}.yaml").write_text(yaml, encoding="utf-8")
        score = re.search(r"(?<!global_)score=([0-9.]+)", header)
        rows.append({"candidate_id": name, "backbone_source": "foundry_official_pdl1", "sequence_source": "ProteinMPNN_CPU" + ("_seed" + seed.group(1) if seed else ""), "binder_length": len(sequence), "mpnn_score": score.group(1) if score else "", "refold_input": f"{name}.yaml", "refold_status": "not_run", "complex_plddt_0_to_1": "", "cross_chain_pae_mean_angstrom": "", "binder_internal_backbone_rmsd_angstrom": "", "binder_placement_backbone_rmsd_angstrom": "", "decision": "pending_refold"})
    if not rows:
        raise ValueError("No sampled ProteinMPNN records found")
    with (args.out / "candidate_queue.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared {len(rows)} actual-sequence inputs; refold_status=not_run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
