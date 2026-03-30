# backup-docker.ps1
# Backs up all Docker volumes and container filesystems to G:\docker_backups\<timestamp>
# Requires: Docker running, G: drive available

$ErrorActionPreference = "Stop"
$backupRoot = "G:\docker_backups"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $backupRoot $timestamp

Write-Host "Docker full backup -> $backupDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$volDir  = Join-Path $backupDir "volumes"
$conDir  = Join-Path $backupDir "containers"
New-Item -ItemType Directory -Path $volDir -Force | Out-Null
New-Item -ItemType Directory -Path $conDir -Force | Out-Null

# 1) Snapshot of what exists (for reference)
Write-Host "Saving container and volume lists..." -ForegroundColor Yellow
docker ps -a > (Join-Path $backupDir "docker_ps_a.txt")
docker volume ls > (Join-Path $backupDir "docker_volume_ls.txt")
docker images > (Join-Path $backupDir "docker_images.txt")

# 2) Backup every volume (tar.gz from volume contents)
$volumes = @(docker volume ls -q)
if ($volumes.Count -gt 0) {
    Write-Host "Backing up $($volumes.Count) volume(s)..." -ForegroundColor Yellow
    foreach ($v in $volumes) {
        $v = $v.Trim()
        if (-not $v) { continue }
        $safe = $v -replace '[^\w\-]', '_'
        $out = Join-Path $volDir "$safe.tar.gz"
        try {
            docker run --rm -v "${v}:/data" -v "${volDir}:/backup" alpine tar czf "/backup/$safe.tar.gz" -C /data . 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { Write-Host "  OK volume: $v" } else { Write-Host "  SKIP volume: $v (exit $LASTEXITCODE)" -ForegroundColor Red }
        } catch {
            Write-Host "  SKIP volume: $v - $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "No volumes to backup." -ForegroundColor Gray
}

# 3) Export every container filesystem (tar per container)
$containers = @(docker ps -a --format "{{.Names}}")
if ($containers.Count -gt 0) {
    Write-Host "Exporting $($containers.Count) container(s)..." -ForegroundColor Yellow
    foreach ($c in $containers) {
        $c = $c.Trim()
        if (-not $c) { continue }
        $safe = $c -replace '[^\w\-]', '_'
        $out = Join-Path $conDir "$safe.tar"
        try {
            docker export $c -o $out 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { Write-Host "  OK container: $c" } else { Write-Host "  SKIP container: $c (exit $LASTEXITCODE)" -ForegroundColor Red }
        } catch {
            Write-Host "  SKIP container: $c - $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "No containers to export." -ForegroundColor Gray
}

# 4) Save all images to a single tar (optional; can be large)
$imgFile = Join-Path $backupDir "all_images.tar"
Write-Host "Saving all images to $imgFile (this may take a while)..." -ForegroundColor Yellow
$ids = docker images -q | Sort-Object -Unique
if ($ids) {
    try {
        docker save $ids -o $imgFile 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { Write-Host "  OK images saved." } else { Write-Host "  SKIP images (exit $LASTEXITCODE)" -ForegroundColor Red }
    } catch {
        Write-Host "  SKIP images - $_" -ForegroundColor Red
    }
}

$size = (Get-ChildItem -Path $backupDir -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host ""
Write-Host "Backup complete: $backupDir" -ForegroundColor Green
Write-Host "Total size: $([math]::Round($size, 2)) MB" -ForegroundColor Green
