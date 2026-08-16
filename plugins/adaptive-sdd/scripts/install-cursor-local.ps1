[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE ".cursor/plugins/local/adaptive-sdd"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$manifest = Join-Path $repoRoot "plugin.json"
$skills = Join-Path $repoRoot "skills"

if (-not (Test-Path -LiteralPath $manifest)) {
    throw "Agent Plugin manifest is missing: $manifest"
}
if (-not (Test-Path -LiteralPath (Join-Path $skills "adaptive-sdd/SKILL.md"))) {
    throw "Adaptive SDD skill is missing: $skills"
}
if ((Test-Path -LiteralPath $Destination) -and -not $Force) {
    throw "A Cursor plugin already exists at $Destination. Review it and rerun with -Force to replace it."
}

if ($PSCmdlet.ShouldProcess($Destination, "Install Adaptive SDD Cursor plugin")) {
    if (Test-Path -LiteralPath $Destination) {
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Copy-Item -LiteralPath $manifest -Destination (Join-Path $Destination "plugin.json")
    Copy-Item -LiteralPath $skills -Destination (Join-Path $Destination "skills") -Recurse
    Write-Host "Installed Adaptive SDD Cursor plugin at $Destination"
    Write-Host "Restart Cursor or run Developer: Reload Window, then invoke /adaptive-sdd."
}
