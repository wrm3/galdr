# sanitize-logs.ps1 - Shared log sanitization module
# Replaces real API key values with their variable names before writing to any log.
#
# Usage in a hook:
#   . (Join-Path $PSScriptRoot "sanitize-logs.ps1")
#   $safeText = Invoke-Sanitize $rawText
#
# The sanitizer reads key values from two sources (in priority order):
#   1. ~/.galdr/user_config.json  (mcp_url, any user secrets)
#   2. .env file in the project root (all KEY=value pairs)
# Any value that matches is replaced with [KEY_NAME].
# Short values (<8 chars) and obvious non-secrets (true/false/localhost/numbers) are skipped.

function Get-SanitizationMap {
    $map = [System.Collections.Generic.Dictionary[string,string]]::new()

    # Skip list — values too short or obviously non-secret
    $skipPatterns = @(
        '^(true|false|yes|no|null|none|localhost|127\.0\.0\.1|0\.0\.0\.0)$',
        '^\d+$',                 # pure numbers
        '^https?://',            # URLs
        '^\s*$',                 # empty/whitespace
        '^(knowledge_base|postgres|admin|user|password|default)$'  # generic placeholders
    )

    # Load .env from project root
    $envFile = ".env"
    if (Test-Path $envFile) {
        $lines = Get-Content $envFile -ErrorAction SilentlyContinue
        foreach ($line in $lines) {
            $line = $line.Trim()
            if ($line -match '^\s*#' -or $line -notmatch '=') { continue }
            $parts = $line -split '=', 2
            if ($parts.Count -lt 2) { continue }
            $varName = $parts[0].Trim()
            $value   = $parts[1].Trim()
            if ($value.Length -lt 8) { continue }
            $skip = $false
            foreach ($pat in $skipPatterns) {
                if ($value -match $pat) { $skip = $true; break }
            }
            if (-not $skip) {
                $map[$value] = "[$varName]"
            }
        }
    }

    # Load user_config.json secrets (mcp_url etc.)
    $userCfgPath = Join-Path $env:USERPROFILE ".galdr\user_config.json"
    if (Test-Path $userCfgPath) {
        try {
            $cfg = Get-Content $userCfgPath -Raw | ConvertFrom-Json
            $cfg.PSObject.Properties | ForEach-Object {
                $k = $_.Name; $v = $_.Value
                if ($v -is [string] -and $v.Length -ge 8) {
                    $skip = $false
                    foreach ($pat in $skipPatterns) {
                        if ($v -match $pat) { $skip = $true; break }
                    }
                    if (-not $skip) { $map[$v] = "[user_config.$k]" }
                }
            }
        } catch {}
    }

    return $map
}

function Invoke-Sanitize {
    param([string]$Text)
    if (-not $Text) { return $Text }

    # Build map once per process (cached in script scope)
    if (-not $script:_sanitizeMap) {
        $script:_sanitizeMap = Get-SanitizationMap
    }

    $result = $Text
    foreach ($entry in $script:_sanitizeMap.GetEnumerator()) {
        if ($result.Contains($entry.Key)) {
            $result = $result.Replace($entry.Key, $entry.Value)
        }
    }
    return $result
}

# Reset cache (call this if .env changes during a session)
function Clear-SanitizeCache {
    $script:_sanitizeMap = $null
}
