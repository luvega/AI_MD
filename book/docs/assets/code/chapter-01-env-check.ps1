$ErrorActionPreference = 'Stop'
$run = '2026-05-31_dry-run'
New-Item -ItemType Directory -Force -Path $run, "$run/inputs", "$run/outputs", "$run/logs", "$run/notes" | Out-Null
python --version | Tee-Object -FilePath "$run/logs/python-version.log"
Get-ChildItem "$run/inputs" -Force | Out-File "$run/logs/input-list.txt"
"status	path	note" | Set-Content "$run/notes/qc.tsv"
"dry-run	$run	created minimal reproducible task folder" | Add-Content "$run/notes/qc.tsv"
