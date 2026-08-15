# Cursor support

Adaptive SDD uses the open Agent Plugins and Agent Skills formats supported by Cursor. The root `plugin.json` identifies the repository as an Agent Plugin, while `skills/adaptive-sdd/SKILL.md` contains the shared workflow used by both Cursor and Codex.

## Project installation

Run:

```powershell
./scripts/install-project.ps1 -Target C:\path\to\project
```

The installed `.agents/skills/adaptive-sdd/` path is discovered by both Cursor and Codex.

## Local plugin installation

Run:

```powershell
./scripts/install-cursor-local.ps1
```

The script installs to `~/.cursor/plugins/local/adaptive-sdd` by default. Restart Cursor or run `Developer: Reload Window`, open Customize, and verify the skill appears in Agent Decides. Invoke it with `/adaptive-sdd`.

Use `-Force` only after reviewing the installed copy:

```powershell
./scripts/install-cursor-local.ps1 -Force
```

## Full Spec Kit for Cursor

To install official Spec Kit with its Cursor integration:

```powershell
./scripts/install-project.ps1 -Target C:\path\to\project -InstallSpecKit -Integration cursor-agent
```

Adaptive SDD remains the tier-selection orchestrator. When full Spec Kit is selected, its official generated commands and project files become authoritative for that feature.

## Marketplace status

This private repository can be loaded locally. Cursor Marketplace submission requires a public repository and manual Cursor review, so no public marketplace listing is claimed by this package.
