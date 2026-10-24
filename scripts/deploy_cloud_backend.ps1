$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$backendRoot = Join-Path $projectRoot 'cloud/backend'
$localUv = Join-Path $backendRoot '.venv/Scripts/uv.exe'
if (-not (Test-Path -LiteralPath $localUv)) {
    throw 'Run uv sync --directory cloud/backend first; the cloud tools require uv >= 0.13.4.'
}
Push-Location -LiteralPath $backendRoot
try {
    $env:PATH = "$(Join-Path $backendRoot '.venv/Scripts');$env:PATH"
    & $localUv run --no-sync pywrangler deploy @args
    if ($LASTEXITCODE -ne 0) { throw "Python Worker deploy failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
