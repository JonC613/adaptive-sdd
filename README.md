# Adaptive SDD

Adaptive SDD packages TinySpec, LiteSpec, and an adapter to official GitHub Spec Kit behind one portable skill.

- Codex: `$adaptive-sdd`
- Cursor: `/adaptive-sdd`

The goal is simple: use the least ceremony that still makes scope, behavior, implementation risk, and verification clear.

| Tier | Artifacts | Use |
|---|---:|---|
| TinySpec | 1 | Small, reversible, well-understood work |
| LiteSpec | 3 | Multiple stories, decisions, phases, or test traceability |
| Spec Kit | Full upstream workflow | High-risk, architectural, regulated, or multi-team work |

## Install into a project

Clone this repository, then run from its root:

```powershell
./scripts/install-project.ps1 -Target C:\path\to\your-project
```

The project installer uses `.agents/skills/`, which both Codex and Cursor officially discover. Restart or reopen the agent in the target repository and invoke the matching form:

```text
$adaptive-sdd Help me define this feature.   # Codex
/adaptive-sdd Help me define this feature.   # Cursor
```

The installer adds only `.agents/skills/adaptive-sdd`. Use `-InstallSpecKit` when the target also needs the official full workflow:

```powershell
./scripts/install-project.ps1 -Target C:\path\to\your-project -InstallSpecKit
```

Read [installation](docs/installation.md), [tier usage](docs/using-adaptive-sdd.md), and [migration](docs/migration.md) before team rollout.

## Install as a local Cursor plugin

Adaptive SDD includes a root `plugin.json` conforming to the open Agent Plugins standard supported by Cursor. Install a local development copy with:

```powershell
./scripts/install-cursor-local.ps1
```

Reload Cursor, open Customize, and verify Adaptive SDD appears under Skills. See [Cursor support](docs/cursor.md).

## Principles

- One public orchestrator, not a menu of overlapping skills.
- One focused discovery question at a time.
- Explicit approval before tier changes, artifacts, tooling installation, or implementation.
- Native artifact conventions for each tier.
- Official Spec Kit remains upstream-managed and version-pinned.
- Promotion preserves source artifacts and provenance.

## Repository contents

- `skills/adaptive-sdd/` — installable Codex skill and all tier resources
- `scripts/install-project.ps1` — guarded project installer
- `plugin.json` — portable Agent Plugin manifest used by Cursor
- `.codex-plugin/plugin.json` — Codex plugin manifest
- `examples/simple-kanban/` — TinySpec and LiteSpec versions of one feature
- `tests/` — deterministic scaffold and validation tests
- `.codex-plugin/plugin.json` — Codex plugin manifest

## Tested Spec Kit version

The current pin is GitHub Spec Kit `v0.16.4`. Check the official release notes before changing it.
