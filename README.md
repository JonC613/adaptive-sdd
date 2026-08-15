# Adaptive SDD

Adaptive SDD packages TinySpec, LiteSpec, and an adapter to official GitHub Spec Kit behind one Codex skill: `$specflow`.

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

Restart or reopen Codex in the target repository and invoke:

```text
$specflow Help me define this feature.
```

The installer adds only `.agents/skills/specflow`. Use `-InstallSpecKit` when the target also needs the official full workflow:

```powershell
./scripts/install-project.ps1 -Target C:\path\to\your-project -InstallSpecKit
```

Read [installation](docs/installation.md), [tier usage](docs/using-specflow.md), and [migration](docs/migration.md) before team rollout.

## Principles

- One public orchestrator, not a menu of overlapping skills.
- One focused discovery question at a time.
- Explicit approval before tier changes, artifacts, tooling installation, or implementation.
- Native artifact conventions for each tier.
- Official Spec Kit remains upstream-managed and version-pinned.
- Promotion preserves source artifacts and provenance.

## Repository contents

- `skills/specflow/` — installable Codex skill and all tier resources
- `scripts/install-project.ps1` — guarded project installer
- `examples/simple-kanban/` — TinySpec and LiteSpec versions of one feature
- `tests/` — deterministic scaffold and validation tests
- `.codex-plugin/plugin.json` — Codex plugin manifest

## Tested Spec Kit version

The current pin is GitHub Spec Kit `v0.16.4`. Check the official release notes before changing it.
