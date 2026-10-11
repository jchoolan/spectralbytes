$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
Set-Location $project
$log = Join-Path $project 'spectralbytes-setup-log.txt'
Start-Transcript -Path $log -Force | Out-Null
try {
  Write-Host '=== SpectralBytes Remote Setup ===' -ForegroundColor Cyan
  if (-not (Test-Path 'compose.yaml')) { throw 'compose.yaml not found. Copy these setup files into the cloned repository root.' }
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker CLI not installed. Install and start Docker Desktop first.' }
  docker info *> $null
  if ($LASTEXITCODE -ne 0) { throw 'Docker Engine is not running. Open Docker Desktop and retry.' }
  if (-not (Test-Path '.env')) {
    $alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.ToCharArray()
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    function New-Secret([int]$length) {
      $b = New-Object byte[] $length
      $rng.GetBytes($b)
      return -join ($b | ForEach-Object { $alphabet[[int]($_ % $alphabet.Length)] })
    }
    $db = New-Secret 40
    $key = New-Secret 64
    [System.IO.File]::WriteAllText((Join-Path $project '.env'), "CTFD_DB_PASSWORD=$db`nCTFD_SECRET_KEY=$key`n", [System.Text.Encoding]::ASCII)
    Write-Host 'Created private .env with random credentials.' -ForegroundColor Green
  } else { Write-Host 'Using existing .env (not overwriting).' }
  docker compose --env-file .env config --quiet
  if ($LASTEXITCODE -ne 0) { throw 'Compose configuration invalid. Check missing environment variables or compose.yaml.' }
  $compose = Join-Path $project 'compose.yaml'
  $original = [System.IO.File]::ReadAllText($compose)
  $changed = $false
  # Only change the S05 host port mapping, preserving the container port.
  $lines = $original -split "`r?`n"
  $insideS05 = $false
  $s05Indent = -1
  $newPort = 18055
  $probe = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $newPort)
  try { $probe.Start(); $probe.Stop() } catch { $newPort = 28055 }
  for ($i=0; $i -lt $lines.Length; $i++) {
    $line = $lines[$i]
    if ($line -match '^(\s*)s05:\s*(?:#.*)?$') { $insideS05=$true; $s05Indent=$Matches[1].Length; continue }
    if ($insideS05 -and $line -match '^(\s*)([\w-]+):\s*(?:#.*)?$' -and $Matches[1].Length -le $s05Indent) { $insideS05=$false }
    if ($insideS05 -and $line -match '8055' -and $line -match '^\s*-\s*["'']?(?:127\.0\.0\.1:|0\.0\.0\.0:)?8055:') {
      $updated = $line -replace '(^\s*-\s*["'']?(?:127\.0\.0\.1:|0\.0\.0\.0:)?)8055:', "`${1}${newPort}:"
      if ($updated -ne $line) { $lines[$i]=$updated; $changed=$true }
    }
  }
  if ($changed) {
    Copy-Item $compose "$compose.before-remote-setup.bak" -Force
    [System.IO.File]::WriteAllText($compose, ($lines -join "`n"), [System.Text.Encoding]::UTF8)
    Write-Host "S05 host port changed from 8055 to $newPort; backup saved." -ForegroundColor Green
  } else { Write-Host 'No 8055 S05 mapping found to change; using existing Compose ports.' }
  docker compose --env-file .env config --quiet
  if ($LASTEXITCODE -ne 0) { throw 'Compose configuration invalid after port update.' }
  Write-Host 'Building and starting containers. First run may take several minutes...' -ForegroundColor Cyan
  docker compose --env-file .env up -d --build
  if ($LASTEXITCODE -ne 0) { throw 'Docker Compose failed to start. See log; possible port conflict or unavailable custom CTFd image.' }
  docker compose --env-file .env ps
  Write-Host 'CTFd: http://localhost:8090' -ForegroundColor Green
  Write-Host "S05: http://localhost:$newPort (if S05 host port was changed)" -ForegroundColor Green
  Write-Host 'NOTE: CTFd challenge database is NOT in Git. Import the separate CTFd backup if required.' -ForegroundColor Yellow
  Write-Host 'Setup finished. If a service is not running, see the diagnostics file.' -ForegroundColor Green
} catch {
  Write-Host "SETUP ERROR: $($_.Exception.Message)" -ForegroundColor Red
} finally {
  try {
    '=== STATUS ===' | Out-File -FilePath (Join-Path $project 'spectralbytes-diagnostics.txt') -Encoding utf8
    docker compose --env-file .env ps 2>&1 | Out-File -FilePath (Join-Path $project 'spectralbytes-diagnostics.txt') -Append -Encoding utf8
    '=== RECENT LOGS ===' | Out-File -FilePath (Join-Path $project 'spectralbytes-diagnostics.txt') -Append -Encoding utf8
    docker compose --env-file .env logs --tail=35 2>&1 | Out-File -FilePath (Join-Path $project 'spectralbytes-diagnostics.txt') -Append -Encoding utf8
  } catch {}
  Stop-Transcript | Out-Null
  Write-Host "Log: $log"
  Write-Host 'Diagnostics: spectralbytes-diagnostics.txt'
}
