# Shared install mechanics. Never recursively delete an existing destination.
function Resolve-CanonicalInstallPath {
    param([string]$Path)
    $fullPath = [IO.Path]::GetFullPath($Path)
    $missingParts = [Collections.Generic.Stack[string]]::new()
    $cursor = $fullPath

    while (-not (Test-Path -LiteralPath $cursor)) {
        $missingParts.Push((Split-Path -Leaf $cursor))
        $parent = Split-Path -Parent $cursor
        if (-not $parent -or $parent -eq $cursor) {
            throw "Unable to resolve install path: $Path"
        }
        $cursor = $parent
    }

    $existing = Get-Item -LiteralPath $cursor -Force
    if (-not $existing.PSIsContainer) {
        throw "Unsafe install path (ancestor is a file): $cursor"
    }
    $resolved = (Resolve-Path -LiteralPath $cursor).Path
    while ($missingParts.Count -gt 0) {
        $resolved = Join-Path $resolved $missingParts.Pop()
    }
    return [IO.Path]::GetFullPath($resolved)
}

function Assert-InstallPath {
    param([string]$Destination, [string]$Source, [string]$Marker)
    $requestedTarget = [IO.Path]::GetFullPath($Destination)
    if ((Split-Path -Leaf $requestedTarget) -ne 'adaptive-sdd') {
        throw 'Unsafe install destination: use a dedicated adaptive-sdd directory outside the source.'
    }
    if (Test-Path -LiteralPath $requestedTarget) {
        $targetItem = Get-Item -LiteralPath $requestedTarget -Force
        if (-not $targetItem.PSIsContainer -or ($targetItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Unsafe install path (file or link): $requestedTarget"
        }
    }

    # Resolve the nearest existing ancestor so normal platform links (for example
    # macOS /var -> /private/var) are accepted without weakening overlap checks.
    $target = Resolve-CanonicalInstallPath $requestedTarget
    $sourcePath = Resolve-CanonicalInstallPath $Source
    $separator = [IO.Path]::DirectorySeparatorChar
    $comparison = if ($IsWindows) { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
    if ($target.Equals($sourcePath, $comparison) -or
        $sourcePath.StartsWith($target.TrimEnd($separator) + $separator, $comparison) -or
        $target.StartsWith($sourcePath.TrimEnd($separator) + $separator, $comparison)) {
        throw 'Unsafe install destination: use a dedicated adaptive-sdd directory outside the source.'
    }
    if (Test-Path -LiteralPath $target) {
        $markerPath = Join-Path $target $Marker
        if (-not (Test-Path -LiteralPath $markerPath -PathType Leaf)) {
            throw 'Refusing to replace an unrecognized installation.'
        }
        if ($Marker -eq 'plugin.json') {
            if ((Get-Content -LiteralPath $markerPath -Raw | ConvertFrom-Json).name -ne 'adaptive-sdd') {
                throw 'Existing plugin identity is not adaptive-sdd.'
            }
            $allowed = @('plugin.json', 'skills')
        } else {
            if ((Get-Content -LiteralPath $markerPath -Raw) -notmatch '(?m)^name:\s*adaptive-sdd\s*$') {
                throw 'Existing skill identity is not adaptive-sdd.'
            }
            $allowed = @('SKILL.md', 'agents', 'assets', 'references', 'scripts')
        }
        foreach ($child in Get-ChildItem -LiteralPath $target -Force) {
            if ($child.Name -notin $allowed) { throw "Unexpected content in installation: $($child.Name)" }
        }
    }
    return $target
}

function Publish-Install {
    param([string]$Destination, [scriptblock]$Populate)
    $parent = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    $stage = Join-Path $parent ('.adaptive-sdd-stage-' + [Guid]::NewGuid().ToString('N'))
    $backup = Join-Path $parent ('.adaptive-sdd-backup-' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $stage | Out-Null
    try {
        & $Populate $stage
        if (Test-Path -LiteralPath $Destination) {
            Move-Item -LiteralPath $Destination -Destination $backup
        }
        try { Move-Item -LiteralPath $stage -Destination $Destination }
        catch {
            if ((Test-Path -LiteralPath $backup) -and -not (Test-Path -LiteralPath $Destination)) {
                Move-Item -LiteralPath $backup -Destination $Destination
            }
            throw
        }
        if (Test-Path -LiteralPath $backup) { Write-Host "Previous installation retained at $backup" }
    } catch {
        Write-Warning "Installation failed. Any staging files remain at $stage for inspection."
        throw
    }
}
