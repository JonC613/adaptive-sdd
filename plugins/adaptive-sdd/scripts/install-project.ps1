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
. (Join-Path $PSScriptRoot 'install-common.ps1')
$targetPath = (Resolve-Path -LiteralPath $Target).Path
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repoRoot "skills/adaptive-sdd"
$targetSkills = Join-Path $targetPath ".agents/skills"
$targetSkill = Join-Path $targetSkills "adaptive-sdd"
$targetSkill = Assert-InstallPath -Destination $targetSkill -Source $sourceSkill -Marker 'SKILL.md'

if (-not (Test-Path -LiteralPath (Join-Path $sourceSkill "SKILL.md"))) {
    throw "Adaptive SDD source skill is missing: $sourceSkill"
}

if ((Test-Path -LiteralPath $targetSkill) -and -not $Force) {
    throw "Adaptive SDD already exists at $targetSkill. Review it and rerun with -Force to replace it."
}

if ($InstallSpecKit) {
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv is required to install official Spec Kit. Install uv, then rerun this command."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required for Spec Kit initialization.' }
if ($SpecKitVersion -notmatch '^v\d+\.\d+\.\d+$') { throw 'SpecKitVersion must be a release tag such as v0.16.4.' }

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
}

if ($PSCmdlet.ShouldProcess($targetSkill, "Install Adaptive SDD skill")) {
    # Recheck after any external tooling initialization and before replacement.
    $targetSkill = Assert-InstallPath -Destination $targetSkill -Source $sourceSkill -Marker 'SKILL.md'
    Publish-Install -Destination $targetSkill -Populate {
        param($stage)
        foreach ($child in Get-ChildItem -LiteralPath $sourceSkill -Force) {
            Copy-Item -LiteralPath $child.FullName -Destination $stage -Recurse
        }
    }
    Write-Host "Installed Adaptive SDD at $targetSkill"
    Write-Host "Activation required: start a new or reopen the Codex/Cursor task in the target repository before invoking the skill. Existing tasks may not discover skills installed after they start."
    Write-Host "Verify with `$adaptive-sdd Help me define this feature. (Codex) or /adaptive-sdd Help me define this feature. (Cursor)."
}
