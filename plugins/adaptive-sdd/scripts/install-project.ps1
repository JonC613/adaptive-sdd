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
$targetPath = (Resolve-Path -LiteralPath $Target).Path
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repoRoot "skills/adaptive-sdd"
$targetSkills = Join-Path $targetPath ".agents/skills"
$targetSkill = Join-Path $targetSkills "adaptive-sdd"

if (-not (Test-Path -LiteralPath (Join-Path $sourceSkill "SKILL.md"))) {
    throw "Adaptive SDD source skill is missing: $sourceSkill"
}

if ((Test-Path -LiteralPath $targetSkill) -and -not $Force) {
    throw "Adaptive SDD already exists at $targetSkill. Review it and rerun with -Force to replace it."
}

if ($PSCmdlet.ShouldProcess($targetSkill, "Install Adaptive SDD skill")) {
    New-Item -ItemType Directory -Force -Path $targetSkills | Out-Null
    if (Test-Path -LiteralPath $targetSkill) {
        Remove-Item -LiteralPath $targetSkill -Recurse -Force
    }
    Copy-Item -LiteralPath $sourceSkill -Destination $targetSkill -Recurse
    Write-Host "Installed Adaptive SDD at $targetSkill"
}

if (-not $InstallSpecKit) {
    return
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv is required to install official Spec Kit. Install uv, then rerun this command."
}

if (Test-Path -LiteralPath (Join-Path $targetPath ".git")) {
    $dirty = git -C $targetPath status --porcelain
    if ($LASTEXITCODE -ne 0) { throw "Unable to inspect target Git status." }
    if ($dirty) { throw "Target Git worktree must be clean before Spec Kit initialization." }
}

$source = "git+https://github.com/github/spec-kit.git@$SpecKitVersion"
if ($PSCmdlet.ShouldProcess($targetPath, "Install Spec Kit $SpecKitVersion and initialize Codex integration")) {
    uv tool install specify-cli --from $source
    if ($LASTEXITCODE -ne 0) { throw "Spec Kit installation failed." }
    specify version
    if ($LASTEXITCODE -ne 0) { throw "Spec Kit verification failed." }
    Push-Location $targetPath
    try {
        specify init --here --force --integration $Integration --script ps
        if ($LASTEXITCODE -ne 0) { throw "Spec Kit project initialization failed." }
    }
    finally {
        Pop-Location
    }
}
