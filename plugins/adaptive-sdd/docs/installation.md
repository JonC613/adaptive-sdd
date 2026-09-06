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

Replacement requires a recognized installation in a dedicated `adaptive-sdd`
directory. Linked paths, source overlap, and unexpected top-level content are
rejected. Copies are staged before replacement; the previous installation is
retained in a sibling `.adaptive-sdd-backup-*` directory. Review and remove backups
manually when no longer needed. Failed staging is retained for inspection.
`-WhatIf` performs checks without installing.

The installer copies only the shared skill. It does not create TinySpec, LiteSpec, or Project Memory artifacts in the target. Initialize `.sdd/memory/` later through an explicit, review-gated request.

## Activate the skill

Codex and Cursor discover project skills when a task or agent session starts. After installation, start a new task in the target repository or reopen the existing one; an already-running task may not see a newly copied skill.

Confirm the installed file exists:

```text
.agents/skills/adaptive-sdd/SKILL.md
```

Then send one of these prompts in the fresh task:

```text
$adaptive-sdd Help me define this feature.   # Codex
/adaptive-sdd Help me define this feature.   # Cursor
```

If neither command is available after reopening, verify the task's working directory is the target project and reinstall with `-Force` only after reviewing the installed copy.

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

The shared skill is published only after successful Spec Kit initialization.
External tooling installation and upstream initialization are not transactional:
if upstream fails, inspect its reported changes before retrying. The old Adaptive
SDD copy is not replaced on that failure. Regression tests mock upstream commands;
they do not establish live upstream compatibility.

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

Start or reopen the task in the target repository, then invoke `$adaptive-sdd` in Codex or `/adaptive-sdd` in Cursor.

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
