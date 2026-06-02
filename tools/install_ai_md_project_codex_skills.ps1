param(
    [string]$CodexSkillsRoot = "C:\Users\xsui\.codex\skills"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$sourceRoot = Join-Path $repoRoot ".claude\skills"

if (-not (Test-Path $sourceRoot)) {
    throw "Source project skill directory not found: $sourceRoot"
}

$skills = @(
    @{
        Source = "ai-md-router"
        Name = "ai-md-router"
        Description = "Use for broad AI_MD routing tasks: next-step planning, cross-chapter updates, plugin/Codex skill choice, and deciding whether to ingest, query, lint, write notes, link Zotero literature, or run vault maintenance."
    },
    @{
        Source = "ingest-source"
        Name = "ai-md-ingest-source"
        Description = "Use when new AI_MD sources arrive, including PDFs, webpages, literature, experiment outputs, attachments, maintenance reports, or source-ingest requests. Identifies impact before durable wiki writing."
    },
    @{
        Source = "query-wiki"
        Name = "ai-md-query-wiki"
        Description = "Use when answering questions from the AI_MD LLM Wiki, doing cross-chapter synthesis, comparing methods, or deciding whether an answer should be saved back into the wiki."
    },
    @{
        Source = "takenote"
        Name = "ai-md-takenote"
        Description = "Use when recording durable AI_MD knowledge: course notes, method cards, literature notes, experiment records, attachment notes, project ideas, or user-provided content that should enter the wiki."
    },
    @{
        Source = "update-vault"
        Name = "ai-md-update-vault"
        Description = "Use when maintaining AI_MD indexes, links, attachment coverage, Zotero/BibTeX consistency, raw-source boundaries, validation reports, or update-vault style checks."
    },
    @{
        Source = "wiki-lint"
        Name = "ai-md-wiki-lint"
        Description = "Use when checking AI_MD LLM Wiki health: orphan pages, duplicate concepts, stale claims, contradictory notes, missing sources, weak relations, or high-level graph quality."
    },
    @{
        Source = "zotero-literature-link"
        Name = "ai-md-zotero-literature-link"
        Description = "Use when linking Zotero and BibTeX literature to AI_MD chapters, creating literature candidates, updating references.bib or zotero-map.tsv, or adding literature notes."
    }
)

New-Item -ItemType Directory -Force -Path $CodexSkillsRoot | Out-Null

foreach ($skill in $skills) {
    $sourcePath = Join-Path $sourceRoot (Join-Path $skill.Source "SKILL.md")
    if (-not (Test-Path $sourcePath)) {
        throw "Missing source skill: $sourcePath"
    }

    $destinationDir = Join-Path $CodexSkillsRoot $skill.Name
    New-Item -ItemType Directory -Force -Path $destinationDir | Out-Null

    $sourceText = Get-Content $sourcePath -Raw -Encoding UTF8
    $body = $sourceText -replace "(?s)^---\s*.*?\s*---\s*", ""
    $migrationNote = @"
> Codex migration note: this global Codex skill is generated from AI_MD project rules at `.claude/skills/$($skill.Source)/SKILL.md`.
> Use it only inside the AI_MD workspace. Always read `CLAUDE.md`, `index.md`, and the relevant `_index.md` before writing.
> Do not move or upload `06_原始学习素材/` contents. Third-party skills are installed globally, not under `.claude/skills/`.

"@

    $frontmatter = @"
---
name: $($skill.Name)
description: $($skill.Description)
metadata:
  source_project: AI_MD
  source_skill: .claude/skills/$($skill.Source)
  generated_by: tools/install_ai_md_project_codex_skills.ps1
---

"@

    $content = $frontmatter + $migrationNote + $body.TrimStart()
    Set-Content -LiteralPath (Join-Path $destinationDir "SKILL.md") -Value $content -Encoding UTF8
    Write-Host "installed AI_MD Codex skill: $($skill.Name)"
}

Write-Host "Restart Codex to pick up generated AI_MD project skills."
