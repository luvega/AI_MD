# Execute from chapter-10/assets after running analyze_refold.py.
# Both views use one common target orientation, zoom and image dimensions.
python
from pathlib import Path
import csv
import pymol
from pymol import cmd

cmd.reinitialize()
cmd.load("data/pdl1_test_0_model_0.pdb", "design")
cmd.load("results/boltz-refold/analysis/pdl1_mpnn_1_target_aligned.pdb", "refold_1")
cmd.load("results/boltz-refold/analysis/pdl1_mpnn_2_target_aligned.pdb", "refold_2")
cmd.create("target", "design and chain B")
cmd.create("designed_A", "design and chain A")
cmd.delete("design")
cmd.remove("(refold_1 or refold_2) and chain B")
cmd.hide("everything", "all")
cmd.show("cartoon", "target or designed_A or refold_1 or refold_2")
cmd.color("gray70", "target")
cmd.color("marine", "designed_A")
cmd.color("orange", "refold_1 or refold_2")
cmd.bg_color("white")
cmd.set("orthoscopic", 1)
cmd.set("ray_shadows", 0)
cmd.set("antialias", 2)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_transparency", 0.25, "target")
cmd.orient("target")
cmd.zoom("target or designed_A or refold_1 or refold_2", buffer=6)
common_view = cmd.get_view()
cmd.set("label_color", "black")
cmd.set("label_size", 20)
cmd.set("label_font_id", 7)
cmd.set("label_outline_color", "white")
cmd.viewport(1500, 1000)
Path("figures").mkdir(exist_ok=True)
with open("results/boltz-refold/analysis/refold_summary.tsv", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

for row in rows:
    number = int(row["candidate_id"].rsplit("_", 1)[1])
    placement = float(row["binder_placement_backbone_rmsd_angstrom"])
    cmd.disable("refold_1 or refold_2")
    cmd.enable(f"refold_{number}")
    cmd.set_view(common_view)
    cmd.pseudoatom("annotation", pos=cmd.get_position(), label=f"Candidate {number}: B-fit A RMSD = {placement:.2f} Angstrom")
    cmd.set("label_relative_mode", 2, "annotation")
    cmd.set("label_screen_point", [750, 930, 0], "annotation")
    cmd.hide("nonbonded", "annotation")
    cmd.png(f"figures/pdl1_refold_{number}.png", width=1500, height=1000, dpi=150, ray=1)
    cmd.delete("annotation")
if pymol.invocation.options.no_gui:
    cmd.quit()
python end
