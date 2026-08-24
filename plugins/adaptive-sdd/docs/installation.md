# Installation

## Prerequisites

- Git
- Python 3.11 or newer for validators
- Codex or Cursor for the bundled skill
- PowerShell 7 for the provided installer
- `uv` only when installing full Spec Kit

## Install Adaptive SDD only

Clone Adaptive SDD and run its root bootstrap script to copy the skill into a target project:

```powershell
git clone https://github.com/JonC613/adaptive-sdd.git
cd adaptive-sdd
./install-project.ps1 -Target C:\path\to\project
```

The script refuses to replace an existing Adaptive SDD installation unless `-Force` is supplied.

The installer copies only the shared skill. It does not create TinySpec, LiteSpec, or Project Memory artifacts in the target. Initialize `.sdd/memory/` later through an explicit, review-gated request.

## Install Adaptive SDD and full Spec Kit

Commit or stash target-project changes first. Then run:

```powershell
./install-project.ps1 -Target C:\path\to\project -InstallSpecKit
```

The installer:

1. Verifies the target exists.
2. Refuses a dirty Git worktree before Spec Kit initialization.
3. Installs official `specify-cli` from `github/spec-kit` at the tested pin.
4. Verifies the CLI.
5. Initializes the selected Spec Kit agent integration with PowerShell scripts.

Equivalent manual commands:

```powershell
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.16.4
specify version
specify init --here --force --integration codex --script ps
```

Use `--script sh` on Linux or macOS.

For Cursor and full Spec Kit:

```powershell
./install-project.ps1 -Target C:\path\to\project -InstallSpecKit -Integration cursor-agent
```

## Verify

Confirm these paths:

```text
.agents/skills/adaptive-sdd/SKILL.md       # Codex and Cursor
.agents/skills/speckit-*/SKILL.md   # only with full Spec Kit
.specify/                           # only with full Spec Kit
```

Then invoke `$adaptive-sdd` in Codex or `/adaptive-sdd` in Cursor.

## Local Cursor plugin installation

To test the repository as a user-level Cursor plugin:

```powershell
./install-cursor-local.ps1
```

This copies only `plugin.json` and `skills/` to `~/.cursor/plugins/local/adaptive-sdd`. Restart Cursor or run `Developer: Reload Window`, then verify the skill in Customize.

## Update

Update Adaptive SDD by pulling this repository and rerunning the installer with `-Force`. Review the diff before committing.

For official Spec Kit integration updates, use:

```text
specify integration upgrade codex
```

Do not rerun forced initialization as the routine upgrade path.
