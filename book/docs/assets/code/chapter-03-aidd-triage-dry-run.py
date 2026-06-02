"""Dry-run ligand triage for chapter 03.

This script is a teaching parser. It tries RDKit/datamol/medchem when they are
available, but it also has a no-dependency fallback so the course example can
run on a clean machine. The output is a TSV manifest for record templates; it is
not a docking, affinity, or activity result.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from rdkit import Chem
    from rdkit.Chem import Crippen, Descriptors, rdMolDescriptors
except Exception:  # pragma: no cover - optional dependency
    Chem = None
    Crippen = None
    Descriptors = None
    rdMolDescriptors = None

try:
    import datamol as dm
except Exception:  # pragma: no cover - optional dependency
    dm = None


@dataclass
class Candidate:
    candidate_id: str
    smiles: str
    source: str


DEFAULT_CANDIDATES = [
    Candidate("LIG001", "CC(=O)OC1=CC=CC=C1C(=O)O", "teaching_aspirin"),
    Candidate("LIG002", "Cn1cnc2n(C)c(=O)n(C)c(=O)c12", "teaching_caffeine"),
    Candidate("LIG003", "C1=CC=INVALID", "teaching_invalid"),
]


def load_candidates(path: Path | None) -> list[Candidate]:
    if path is None:
        return list(DEFAULT_CANDIDATES)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [
            Candidate(
                row.get("candidate_id", "").strip(),
                row.get("smiles", "").strip(),
                row.get("source", "input").strip(),
            )
            for row in reader
        ]


def fallback_metrics(smiles: str) -> dict[str, str]:
    if not smiles or "INVALID" in smiles.upper():
        return {
            "parse_status": "fail",
            "canonical_smiles": "",
            "mw": "",
            "logp": "",
            "tpsa": "",
            "hbd": "",
            "hba": "",
            "rotatable_bonds": "",
            "rule_of_five_pass": "review",
            "alert_status": "not_checked",
            "triage_note": "SMILES could not be parsed without RDKit.",
        }
    heavy_atoms = sum(1 for char in smiles if char.isalpha() and char.isupper())
    return {
        "parse_status": "fallback",
        "canonical_smiles": smiles,
        "mw": str(heavy_atoms * 12),
        "logp": "",
        "tpsa": "",
        "hbd": "",
        "hba": "",
        "rotatable_bonds": "",
        "rule_of_five_pass": "review",
        "alert_status": "not_checked",
        "triage_note": "Fallback estimate only; install RDKit for descriptors.",
    }


def rdkit_metrics(smiles: str) -> dict[str, str]:
    if Chem is None:
        return fallback_metrics(smiles)
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return fallback_metrics("INVALID")
    if dm is not None:
        try:
            mol = dm.fix_mol(mol)
            mol = dm.sanitize_mol(mol)
            mol = dm.standardize_mol(mol)
        except Exception:
            pass
    canonical = Chem.MolToSmiles(mol)
    mw = Descriptors.MolWt(mol)
    logp = Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    hbd = rdMolDescriptors.CalcNumHBD(mol)
    hba = rdMolDescriptors.CalcNumHBA(mol)
    rot = rdMolDescriptors.CalcNumRotatableBonds(mol)
    ro5_pass = mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10
    return {
        "parse_status": "pass",
        "canonical_smiles": canonical,
        "mw": f"{mw:.2f}",
        "logp": f"{logp:.2f}",
        "tpsa": f"{tpsa:.2f}",
        "hbd": str(hbd),
        "hba": str(hba),
        "rotatable_bonds": str(rot),
        "rule_of_five_pass": "pass" if ro5_pass else "review",
        "alert_status": "manual_review",
        "triage_note": "Descriptor triage complete; pose and activity remain pending.",
    }


def build_rows(candidates: Iterable[Candidate]) -> list[dict[str, str]]:
    rows = []
    for candidate in candidates:
        metrics = rdkit_metrics(candidate.smiles)
        filter_reason = ""
        if metrics["parse_status"] == "fail":
            filter_reason = "invalid_smiles"
        elif metrics["rule_of_five_pass"] == "review":
            filter_reason = "descriptor_review"
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "source": candidate.source,
                "smiles": candidate.smiles,
                **metrics,
                "pose_qc_passed": "pending",
                "filter_reason": filter_reason,
            }
        )
    return rows


def write_tsv(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "source",
        "smiles",
        "parse_status",
        "canonical_smiles",
        "mw",
        "logp",
        "tpsa",
        "hbd",
        "hba",
        "rotatable_bonds",
        "rule_of_five_pass",
        "alert_status",
        "pose_qc_passed",
        "filter_reason",
        "triage_note",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Optional TSV with candidate_id, smiles, source.")
    parser.add_argument("--out", type=Path, default=Path("outputs/chapter-03-aidd-triage.tsv"))
    args = parser.parse_args()
    rows = build_rows(load_candidates(args.input))
    write_tsv(rows, args.out)
    print(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
