[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$installer = Join-Path $PSScriptRoot "plugins/adaptive-sdd/scripts/install-cursor-local.ps1"

if (-not (Test-Path -LiteralPath $installer)) {
    throw "Adaptive SDD Cursor installer is missing: $installer"
}

& $installer @PSBoundParameters
