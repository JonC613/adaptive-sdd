[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE ".cursor/plugins/local/adaptive-sdd"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot 'install-common.ps1')
$repoRoot = Split-Path -Parent $PSScriptRoot
$manifest = Join-Path $repoRoot "plugin.json"
$skills = Join-Path $repoRoot "skills"
$Destination = Assert-InstallPath -Destination $Destination -Source $repoRoot -Marker 'plugin.json'

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
    Publish-Install -Destination $Destination -Populate {
        param($stage)
        Copy-Item -LiteralPath $manifest -Destination (Join-Path $stage "plugin.json")
        Copy-Item -LiteralPath $skills -Destination (Join-Path $stage "skills") -Recurse
    }
    Write-Host "Installed Adaptive SDD Cursor plugin at $Destination"
    Write-Host "Restart Cursor or run Developer: Reload Window, then invoke /adaptive-sdd."
}
