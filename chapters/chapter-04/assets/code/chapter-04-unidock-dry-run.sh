#!/usr/bin/env bash
set -euo pipefail

# Teaching dry-run only. This script creates reproducible record tables for
# Chapter 4; it does not call UniDock and does not produce real docking results.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="${1:-"${SCRIPT_DIR}/../dry-run-output"}"

mkdir -p "${RUN_DIR}/inputs" "${RUN_DIR}/outputs" "${RUN_DIR}/logs"

cat > "${RUN_DIR}/inputs/box.tsv" <<'BOX'
center_x	center_y	center_z	size_x	size_y	size_z	box_basis
30.346	43.402	53.131	30	30	30	reference_ligand_or_pocket_residues
BOX

cat > "${RUN_DIR}/inputs/ligand_library_manifest.tsv" <<'LIGANDS'
ligand_id	source	input_format	prepared_path	protonation_state	qc_status
LIG001	teaching_example	SDF	inputs/ligand/LIG001.pdbqt	pH_7.4_assumption	review
LIG002	teaching_example	SDF	inputs/ligand/LIG002.pdbqt	pH_7.4_assumption	review
LIG003	teaching_example	SDF	inputs/ligand/LIG003.pdbqt	pH_7.4_assumption	review
LIGANDS

cat > "${RUN_DIR}/outputs/docking_manifest.tsv" <<'RESULTS'
ligand_id	rank	score_placeholder	pose_path	pose_qc_passed	filter_reason	next_step
LIG001	1	mock_-7.6	outputs/result1/LIG001_pose1.pdbqt	pending	teaching_placeholder	visual_pose_qc
LIG002	2	mock_-6.9	outputs/result1/LIG002_pose1.pdbqt	pending	teaching_placeholder	visual_pose_qc
LIG003	3	mock_-5.4	outputs/result1/LIG003_pose1.pdbqt	pending	teaching_placeholder	visual_pose_qc
RESULTS

cat > "${RUN_DIR}/outputs/top_pose_qc.tsv" <<'QC'
ligand_id	rank	score_placeholder	clash_check	key_interaction	conformation_check	decision
LIG001	1	mock_-7.6	pending	pending	pending	review_before_shortlist
LIG002	2	mock_-6.9	pending	pending	pending	review_before_shortlist
LIG003	3	mock_-5.4	pending	pending	pending	review_before_shortlist
QC

cat > "${RUN_DIR}/logs/unidock-dry-run.log" <<LOG
[chapter-04 dry-run]
mode=teaching_record_only
receptor=inputs/receptor.pdbqt
ligand_dir=inputs/ligand
box=inputs/box.tsv
search_mode=fast
note=No docking executable was called. Mock scores are placeholders for table training.
LOG

printf 'Dry-run files written to %s\n' "${RUN_DIR}"
