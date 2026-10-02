# Start PyMOL in the folder containing inputs/3htb.pdb and outputs/.
# All coordinates are from the public PDB entry 3HTB, not course images.
reinitialize
load inputs/3htb.pdb, model_3htb
hide everything, all
select protein_a, model_3htb and polymer.protein and chain A and not alt B
select ligand_jz4, model_3htb and resn JZ4
select pocket_5a, byres (protein_a within 5 of ligand_jz4)
show cartoon, protein_a
show sticks, ligand_jz4 or pocket_5a
color gray80, protein_a
color marine, pocket_5a
color orange, ligand_jz4
color red, elem O
bg_color white
set cartoon_transparency, 0.55, protein_a
set label_size, 16
orient ligand_jz4 or pocket_5a
zoom ligand_jz4 or pocket_5a, 4
save outputs/3htb_pocket.pse
save outputs/3htb_pocket_residues.pdb, pocket_5a
png outputs/3htb_pocket.png, width=1400, height=1000, dpi=200, ray=1
