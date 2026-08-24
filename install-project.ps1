[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory = $true)]
    [string]$Target,
    [switch]$Force,
    [switch]$InstallSpecKit,
    [ValidateSet("codex", "cursor-agent")]
    [string]$Integration = "codex",
    [string]$SpecKitVersion = "v0.16.4"
)

$ErrorActionPreference = "Stop"
$installer = Join-Path $PSScriptRoot "plugins/adaptive-sdd/scripts/install-project.ps1"

if (-not (Test-Path -LiteralPath $installer)) {
    throw "Adaptive SDD project installer is missing: $installer"
}

& $installer @PSBoundParameters
