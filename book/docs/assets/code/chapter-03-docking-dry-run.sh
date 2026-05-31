set -euo pipefail
mkdir -p outputs logs
cat > inputs/box.tsv <<'BOX'
cx	cy	cz	sx	sy	sz
12.4	-3.2	8.6	22	22	22
BOX
unidock --receptor inputs/receptor.pdbqt --ligand_index inputs/ligands.txt \
  --center_x 12.4 --center_y -3.2 --center_z 8.6 \
  --size_x 22 --size_y 22 --size_z 22 \
  --dir outputs > logs/unidock-dry-run.log 2>&1
