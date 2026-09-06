# Shared install mechanics. Never recursively delete an existing destination.
function Assert-InstallPath {
    param([string]$Destination, [string]$Source, [string]$Marker)
    $target = [IO.Path]::GetFullPath($Destination)
    $sourcePath = [IO.Path]::GetFullPath($Source)
    $separator = [IO.Path]::DirectorySeparatorChar
    $comparison = if ($IsWindows) { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
    if ((Split-Path -Leaf $target) -ne 'adaptive-sdd' -or
        $target.Equals($sourcePath, $comparison) -or
        $sourcePath.StartsWith($target.TrimEnd($separator) + $separator, $comparison) -or
        $target.StartsWith($sourcePath.TrimEnd($separator) + $separator, $comparison)) {
        throw 'Unsafe install destination: use a dedicated adaptive-sdd directory outside the source.'
    }
    $cursor = $target
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item = Get-Item -LiteralPath $cursor -Force
            if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                throw "Unsafe install path (file or link): $cursor"
            }
        }
        $parent = Split-Path -Parent $cursor
        if ($parent -eq $cursor) { break }
        $cursor = $parent
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
