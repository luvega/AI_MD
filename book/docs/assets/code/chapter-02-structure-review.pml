load inputs/receptor.pdb, receptor
hide everything
show cartoon, receptor
color slate, receptor
select active_site, byres receptor within 5 of resn LIG
show sticks, active_site
png outputs/receptor_active_site.png, dpi=220
