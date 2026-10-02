# Start PyMOL from chapter-08/assets, then run this file.
load results/3htb-jz4-single/3htb_jz4_single_model_0.cif, prediction
load ../../chapter-03/assets/data/3htb/3htb.pdb, crystal
hide everything
align prediction and chain A and name CA, crystal and chain A and name CA
show cartoon, prediction and chain A
show cartoon, crystal and chain A and polymer.protein
color cyan, prediction and chain A
color gray70, crystal and chain A
show sticks, prediction and chain LIG
show sticks, crystal and resn JZ4
color orange, prediction and chain LIG
color green, crystal and resn JZ4
zoom crystal and resn JZ4, 8
set cartoon_transparency, 0.35
