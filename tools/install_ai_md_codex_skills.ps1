param(
    [string]$SourceRepo = "K-Dense-AI/scientific-agent-skills",
    [string]$SourceCommit = "93124850ef08487e423165554c54f0b333d5631d",
    [string]$CodexSkillsRoot = "C:\Users\xsui\.codex\skills"
)

$ErrorActionPreference = "Stop"

$installer = Join-Path $CodexSkillsRoot ".system\skill-installer\scripts\install-skill-from-github.py"
if (-not (Test-Path $installer)) {
    throw "Codex skill installer not found: $installer"
}

$selectedSkills = @(
    "scientific-writing",
    "literature-review",
    "citation-management",
    "peer-review",
    "scientific-critical-thinking",
    "hypothesis-generation",
    "research-grants",
    "markdown-mermaid-writing",
    "scientific-schematics",
    "scientific-slides",
    "venue-templates",
    "markitdown",
    "exploratory-data-analysis",
    "statistical-analysis",
    "scientific-visualization",
    "networkx",
    "datamol",
    "rdkit",
    "medchem",
    "molecular-dynamics",
    "diffdock"
)

$missingPaths = @()
foreach ($skill in $selectedSkills) {
    $dest = Join-Path $CodexSkillsRoot $skill
    if (Test-Path $dest) {
        Write-Host "already installed: $skill"
    } else {
        $missingPaths += "skills/$skill"
    }
}

if ($missingPaths.Count -eq 0) {
    Write-Host "All AI_MD selected Codex skills are already installed."
    exit 0
}

$arguments = @(
    $installer,
    "--repo", $SourceRepo,
    "--ref", $SourceCommit,
    "--path"
) + $missingPaths

python @arguments

Write-Host "Restart Codex to pick up newly installed skills."
