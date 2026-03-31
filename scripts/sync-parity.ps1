<#
.SYNOPSIS
    Enforces C-007 (8-target propagation) by detecting and fixing parity gaps
    between root IDE directories and template directories.

.DESCRIPTION
    Compares rules and skills across all platform targets:
      Rules:  templates/{.cursor,.claude,.agent} ↔ root/{.cursor,.claude,.agent}
      Skills: templates/{.cursor,.claude,.agent,.codex} ↔ root/{.cursor,.claude,.agent,.codex}

    Handles extension mapping (.mdc for Cursor, .md for others).
    Excludes proprietary skills that should remain root-only.

.PARAMETER Fix
    Actually copy files to resolve gaps. Without this flag, only reports.

.PARAMETER Verbose
    Show detailed per-file comparisons.

.EXAMPLE
    .\scripts\sync-parity.ps1
    # Report-only mode — shows all gaps

.EXAMPLE
    .\scripts\sync-parity.ps1 -Fix
    # Detects and fixes all parity gaps
#>

param(
    [switch]$Fix
)

$ErrorActionPreference = "Stop"

# --- Configuration ---

$RepoRoot = (Get-Item $PSScriptRoot).Parent.FullName

$ProprietarySkills = @(
    "hieroglyphics",
    "silicon-valley-superfan",
    "turboquant-compression"
)

$ProprietaryRules = @(
    "silicon_valley_personality"
)

# Platform definitions: Name, TemplateRulesDir, RootRulesDir, RulesExt, TemplateSkillsDir, RootSkillsDir
$Platforms = @(
    @{ Name = ".cursor"; RulesExt = ".mdc"; HasRules = $true },
    @{ Name = ".claude";  RulesExt = ".md";  HasRules = $true },
    @{ Name = ".agent";   RulesExt = ".md";  HasRules = $true },
    @{ Name = ".codex";   RulesExt = $null;  HasRules = $false }
)

# --- Helper Functions ---

function Get-RuleBaseName {
    param([string]$FileName)
    $FileName -replace '\.(mdc|md)$', ''
}

function Get-SkillNames {
    param([string]$Path)
    if (Test-Path $Path) {
        Get-ChildItem $Path -Directory -Name | Sort-Object
    } else {
        @()
    }
}

function Get-RuleNames {
    param([string]$Path)
    if (Test-Path $Path) {
        Get-ChildItem $Path -File -Name | ForEach-Object { Get-RuleBaseName $_ } | Sort-Object
    } else {
        @()
    }
}

function Copy-RuleFile {
    param(
        [string]$SourceDir,
        [string]$SourceBaseName,
        [string]$SourceExt,
        [string]$DestDir,
        [string]$DestExt
    )
    $src = Join-Path $SourceDir "$SourceBaseName$SourceExt"
    $dst = Join-Path $DestDir "$SourceBaseName$DestExt"
    if (-not (Test-Path $DestDir)) {
        New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    }
    Copy-Item $src $dst -Force
    return $dst
}

function Copy-SkillDir {
    param(
        [string]$SourceDir,
        [string]$SkillName,
        [string]$DestParent
    )
    $src = Join-Path $SourceDir $SkillName
    $dst = Join-Path $DestParent $SkillName
    if (-not (Test-Path $DestParent)) {
        New-Item -ItemType Directory -Path $DestParent -Force | Out-Null
    }
    Copy-Item $src $dst -Recurse -Force
    return $dst
}

# --- Main Logic ---

$totalGaps = 0
$fixedGaps = 0

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  galdr Parity Sync (C-007 Enforcement)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Repo root: $RepoRoot"
Write-Host "Mode: $(if ($Fix) { 'FIX' } else { 'REPORT (use -Fix to resolve)' })`n"

# --- RULES PARITY ---

Write-Host "--- Rules Parity ---" -ForegroundColor Yellow

$templateRulesCanonical = @{}
foreach ($p in ($Platforms | Where-Object { $_.HasRules })) {
    $dir = Join-Path $RepoRoot "templates\$($p.Name)\rules"
    foreach ($name in (Get-RuleNames $dir)) {
        if (-not $templateRulesCanonical.ContainsKey($name)) {
            $templateRulesCanonical[$name] = @{ Dir = $dir; Ext = $p.RulesExt }
        }
    }
}

foreach ($p in ($Platforms | Where-Object { $_.HasRules })) {
    $templateDir = Join-Path $RepoRoot "templates\$($p.Name)\rules"
    $rootDir     = Join-Path $RepoRoot "$($p.Name)\rules"
    $ext         = $p.RulesExt

    $templateNames = Get-RuleNames $templateDir
    $rootNames     = Get-RuleNames $rootDir

    # Templates -> Root
    foreach ($name in $templateNames) {
        if ($name -notin $rootNames) {
            $totalGaps++
            Write-Host "  GAP  template->root  $($p.Name)/rules/$name$ext" -ForegroundColor Red
            if ($Fix) {
                $src = $templateRulesCanonical[$name]
                $result = Copy-RuleFile $src.Dir $name $src.Ext $rootDir $ext
                Write-Host "       FIXED -> $result" -ForegroundColor Green
                $fixedGaps++
            }
        }
    }

    # Root -> Templates (non-proprietary only)
    foreach ($name in $rootNames) {
        if ($name -notin $templateNames -and $name -notin $ProprietaryRules) {
            $totalGaps++
            Write-Host "  GAP  root->template  $($p.Name)/rules/$name (missing from templates)" -ForegroundColor Red
            if ($Fix) {
                foreach ($tp in ($Platforms | Where-Object { $_.HasRules })) {
                    $tDir = Join-Path $RepoRoot "templates\$($tp.Name)\rules"
                    $result = Copy-RuleFile $rootDir $name $ext $tDir $tp.RulesExt
                    Write-Host "       FIXED -> $result" -ForegroundColor Green
                }
                $fixedGaps++
            }
        }
    }
}

# --- SKILLS PARITY ---

Write-Host "`n--- Skills Parity ---" -ForegroundColor Yellow

$cursorTemplateSkills = Join-Path $RepoRoot "templates\.cursor\skills"
$canonicalSkillNames = Get-SkillNames $cursorTemplateSkills

foreach ($p in $Platforms) {
    $templateDir = Join-Path $RepoRoot "templates\$($p.Name)\skills"
    $rootDir     = Join-Path $RepoRoot "$($p.Name)\skills"

    $templateNames = Get-SkillNames $templateDir
    $rootNames     = Get-SkillNames $rootDir

    # Templates -> Root
    foreach ($name in $templateNames) {
        if ($name -notin $rootNames) {
            $totalGaps++
            Write-Host "  GAP  template->root  $($p.Name)/skills/$name/" -ForegroundColor Red
            if ($Fix) {
                $result = Copy-SkillDir $templateDir $name $rootDir
                Write-Host "       FIXED -> $result" -ForegroundColor Green
                $fixedGaps++
            }
        }
    }

    # Root -> Templates (non-proprietary only)
    foreach ($name in $rootNames) {
        if ($name -notin $templateNames -and $name -notin $ProprietarySkills) {
            $totalGaps++
            Write-Host "  GAP  root->template  $($p.Name)/skills/$name/ (missing from templates)" -ForegroundColor Red
            if ($Fix) {
                foreach ($tp in $Platforms) {
                    $tDir = Join-Path $RepoRoot "templates\$($tp.Name)\skills"
                    if (-not (Test-Path (Join-Path $tDir $name))) {
                        $srcDir = $rootDir
                        $result = Copy-SkillDir $srcDir $name $tDir
                        Write-Host "       FIXED -> $result" -ForegroundColor Green
                    }
                }
                $fixedGaps++
            }
        }
    }
}

# --- CROSS-TEMPLATE PARITY (ensure all template platforms have same skills) ---

Write-Host "`n--- Cross-Template Parity ---" -ForegroundColor Yellow

$allTemplateSkillSets = @{}
foreach ($p in $Platforms) {
    $dir = Join-Path $RepoRoot "templates\$($p.Name)\skills"
    $allTemplateSkillSets[$p.Name] = Get-SkillNames $dir
}

$cursorTemplateName = ".cursor"
$reference = $allTemplateSkillSets[$cursorTemplateName]
$referenceDir = Join-Path $RepoRoot "templates\$cursorTemplateName\skills"

foreach ($p in $Platforms) {
    if ($p.Name -eq $cursorTemplateName) { continue }
    $theirs = $allTemplateSkillSets[$p.Name]
    $theirDir = Join-Path $RepoRoot "templates\$($p.Name)\skills"

    foreach ($name in $reference) {
        if ($name -notin $theirs) {
            $totalGaps++
            Write-Host "  GAP  cross-template  templates/$($p.Name)/skills/$name/ (present in .cursor, missing here)" -ForegroundColor Red
            if ($Fix) {
                $result = Copy-SkillDir $referenceDir $name $theirDir
                Write-Host "       FIXED -> $result" -ForegroundColor Green
                $fixedGaps++
            }
        }
    }
}

# --- AGENTS PARITY CHECK ---

Write-Host "`n--- Agents Parity ---" -ForegroundColor Yellow

foreach ($p in $Platforms) {
    $templateAgentsDir = Join-Path $RepoRoot "templates\$($p.Name)\agents"
    $rootAgentsDir     = Join-Path $RepoRoot "$($p.Name)\agents"

    if (-not (Test-Path $templateAgentsDir)) { continue }
    if (-not (Test-Path $rootAgentsDir)) {
        Write-Host "  WARN  $($p.Name)/agents/ dir missing in root" -ForegroundColor DarkYellow
        continue
    }

    $templateAgents = if (Test-Path $templateAgentsDir) { Get-ChildItem $templateAgentsDir -File -Name | Sort-Object } else { @() }
    $rootAgents     = if (Test-Path $rootAgentsDir) { Get-ChildItem $rootAgentsDir -File -Name | Sort-Object } else { @() }

    foreach ($name in $templateAgents) {
        if ($name -notin $rootAgents) {
            $totalGaps++
            Write-Host "  GAP  template->root  $($p.Name)/agents/$name" -ForegroundColor Red
            if ($Fix) {
                Copy-Item (Join-Path $templateAgentsDir $name) (Join-Path $rootAgentsDir $name) -Force
                Write-Host "       FIXED -> $($p.Name)/agents/$name" -ForegroundColor Green
                $fixedGaps++
            }
        }
    }

    foreach ($name in $rootAgents) {
        if ($name -notin $templateAgents) {
            $totalGaps++
            Write-Host "  GAP  root->template  $($p.Name)/agents/$name (missing from templates)" -ForegroundColor Red
            if ($Fix) {
                foreach ($tp in $Platforms) {
                    $tAgentsDir = Join-Path $RepoRoot "templates\$($tp.Name)\agents"
                    if ((Test-Path $tAgentsDir) -and -not (Test-Path (Join-Path $tAgentsDir $name))) {
                        Copy-Item (Join-Path $rootAgentsDir $name) (Join-Path $tAgentsDir $name) -Force
                        Write-Host "       FIXED -> templates/$($tp.Name)/agents/$name" -ForegroundColor Green
                    }
                }
                $fixedGaps++
            }
        }
    }
}

# --- COMMANDS PARITY CHECK ---

Write-Host "`n--- Commands Parity ---" -ForegroundColor Yellow

foreach ($p in $Platforms) {
    $templateCmdsDir = Join-Path $RepoRoot "templates\$($p.Name)\commands"
    $rootCmdsDir     = Join-Path $RepoRoot "$($p.Name)\commands"

    if (-not (Test-Path $templateCmdsDir)) { continue }
    if (-not (Test-Path $rootCmdsDir)) {
        Write-Host "  WARN  $($p.Name)/commands/ dir missing in root" -ForegroundColor DarkYellow
        continue
    }

    $templateCmds = if (Test-Path $templateCmdsDir) { Get-ChildItem $templateCmdsDir -File -Name | Sort-Object } else { @() }
    $rootCmds     = if (Test-Path $rootCmdsDir) { Get-ChildItem $rootCmdsDir -File -Name | Sort-Object } else { @() }

    foreach ($name in $templateCmds) {
        if ($name -notin $rootCmds) {
            $totalGaps++
            Write-Host "  GAP  template->root  $($p.Name)/commands/$name" -ForegroundColor Red
            if ($Fix) {
                Copy-Item (Join-Path $templateCmdsDir $name) (Join-Path $rootCmdsDir $name) -Force
                Write-Host "       FIXED -> $($p.Name)/commands/$name" -ForegroundColor Green
                $fixedGaps++
            }
        }
    }

    foreach ($name in $rootCmds) {
        if ($name -notin $templateCmds) {
            $totalGaps++
            Write-Host "  GAP  root->template  $($p.Name)/commands/$name (missing from templates)" -ForegroundColor Red
            if ($Fix) {
                foreach ($tp in $Platforms) {
                    $tCmdsDir = Join-Path $RepoRoot "templates\$($tp.Name)\commands"
                    if ((Test-Path $tCmdsDir) -and -not (Test-Path (Join-Path $tCmdsDir $name))) {
                        Copy-Item (Join-Path $rootCmdsDir $name) (Join-Path $tCmdsDir $name) -Force
                        Write-Host "       FIXED -> templates/$($tp.Name)/commands/$name" -ForegroundColor Green
                    }
                }
                $fixedGaps++
            }
        }
    }
}

# --- Summary ---

Write-Host "`n========================================" -ForegroundColor Cyan
if ($totalGaps -eq 0) {
    Write-Host "  All targets in parity. No gaps found." -ForegroundColor Green
} elseif ($Fix) {
    Write-Host "  Found $totalGaps gap(s). Fixed $fixedGaps." -ForegroundColor Yellow
} else {
    Write-Host "  Found $totalGaps gap(s). Run with -Fix to resolve." -ForegroundColor Red
}
Write-Host "========================================`n" -ForegroundColor Cyan

exit $(if ($totalGaps -eq 0 -or $Fix) { 0 } else { 1 })
