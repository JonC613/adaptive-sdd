# Adaptive SDD

Adaptive SDD packages TinySpec, LiteSpec, an adapter to official GitHub Spec Kit, and portable Project Memory behind one shared skill.

Version 0.4 adds resumable feature state, fingerprint-bound approvals, attributable
evidence, an optional recorded-evidence gate, interaction modes, and optional project profiles.
Markdown validation remains explicitly structural; it never claims implementation
or tests passed.

- Codex: `$adaptive-sdd`
- Cursor: `/adaptive-sdd`
- GitHub Copilot: ask naturally, for example “Use Adaptive SDD to help me define this feature.”

The goal is simple: use the least ceremony that still makes scope, behavior, implementation risk, and verification clear.

Project Memory complements those point-in-time specifications with an optional, OKF-compatible living description of what the repository has become. It uses the same shared skill in Codex, Cursor, and GitHub Copilot and remains readable as ordinary Markdown without an agent.

| Tier | Artifacts | Use |
|---|---:|---|
| TinySpec | 1 | Small, reversible, well-understood work |
| LiteSpec | 3 | Multiple stories, decisions, phases, or test traceability |
| Spec Kit | Full upstream workflow | High-risk, architectural, regulated, or multi-team work |

## Project Memory

Project Memory is not a fourth specification tier. TinySpec, LiteSpec, Spec Kit, and ordinary Git changes can all contribute provenance to the same current-state bundle:

```text
.sdd/
├── memory/
│   ├── index.md
│   ├── project.md
│   ├── architecture.md
│   └── log.md
└── memory-state.json
```

Invoke it through the existing skill:

```text
$adaptive-sdd initialize memory   # Codex
/adaptive-sdd initialize memory   # Cursor
```

The shared operations are `initialize memory`, `status memory`, `update memory`, `refresh memory`, and `verify memory`. Generated knowledge is proposed before it is written. Installation never creates `.sdd/` automatically.

## Install into a project

Clone this repository, then run the root bootstrap script:

```powershell
./install-project.ps1 -Target C:\path\to\your-project
```

The project installer publishes the shared skill to `.agents/skills/` for Codex and Cursor and `.github/skills/` for GitHub Copilot. Both destinations are validated before installation writes occur. Skills are loaded when a task starts, so start a new task or reopen the existing task in the target repository after installation. Then invoke the matching form:

```text
$adaptive-sdd Help me define this feature.   # Codex
/adaptive-sdd Help me define this feature.   # Cursor
```

In Copilot, ask naturally in the fresh task; do not use a slash command. If the skill is unavailable, confirm the matching `SKILL.md` exists, then open a fresh task in that repository. Installing a skill does not retrofit it into an already-running task.

## Repository examples and QA tooling

Examples and their test tooling are maintained with this source repository. They are not copied by the Codex or Cursor installers, which intentionally distribute only the shared `adaptive-sdd` skill. This keeps installed project guidance focused while preserving runnable reference applications and QA evidence for maintainers.

The installer adds only the shared skill at its supported agent discovery locations. Use `-InstallSpecKit` when the target also needs the official full workflow:

```powershell
./install-project.ps1 -Target C:\path\to\your-project -InstallSpecKit
```

Read [installation](docs/installation.md), [tier usage](docs/using-adaptive-sdd.md), and [migration](docs/migration.md) before team rollout.

## Proof-of-concept presentation

Open [the browser presentation](presentation/index.html) for a 16-slide walkthrough of the problem, three-tier model, Kanban evidence, limitations, work-shaped pilot, success measures, and demo plan. It runs without a build step or network connection and includes keyboard navigation, speaker notes, fullscreen, overview, and print-to-PDF support.

## Install as a local Cursor plugin

Adaptive SDD includes a root `plugin.json` conforming to the open Agent Plugins standard supported by Cursor. Install a local development copy with:

```powershell
./install-cursor-local.ps1
```

Reload Cursor, open Customize, and verify Adaptive SDD appears under Skills. See [Cursor support](docs/cursor.md).

## Principles

- One public orchestrator, not a menu of overlapping skills.
- One portable Project Memory format and implementation across Codex, Cursor, and GitHub Copilot.
- One focused discovery question at a time.
- Reuse authorization for routine planning, implementation, checks, and affected documentation; ask only for consequential choices or work outside scope.
- Native artifact conventions for each tier.
- Official Spec Kit remains upstream-managed and version-pinned.
- Promotion preserves source artifacts and provenance.

## Repository contents

- `skills/adaptive-sdd/` — shared agent skill and all tier resources
- `../../install-project.ps1` — root bootstrap installer for new repositories
- `scripts/install-project.ps1` — guarded plugin implementation
- `plugin.json` — portable Agent Plugin manifest used by Cursor
- `.codex-plugin/plugin.json` — Codex plugin manifest
- `examples/simple-kanban/` — TinySpec and LiteSpec versions of one feature
- `examples/simple-kanban/.sdd/memory/` — portable living-memory example
- `presentation/` — self-contained POC presentation and presenter instructions
- `tests/` — deterministic scaffold and validation tests
- `.codex-plugin/plugin.json` — Codex plugin manifest

## Pinned Spec Kit version

The current pin is GitHub Spec Kit `v0.16.4`. Local mocked installer checks do not establish live upstream compatibility. See the [release checklist](../../docs/release-readiness.md) before changing or distributing the pin.
