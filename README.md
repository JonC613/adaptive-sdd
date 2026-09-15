# Adaptive-SDD

[![Tests](https://github.com/JonC613/adaptive-sdd/actions/workflows/test.yml/badge.svg)](https://github.com/JonC613/adaptive-sdd/actions/workflows/test.yml)

**Specification depth that matches the change.** AI-assisted development can miss requirements when the brief is vague, while a full planning process can overwhelm a small fix. Adaptive-SDD gives developers and small product teams one shared Codex/Cursor workflow for choosing enough specification to make scope, implementation decisions, and verification reviewable.

The agent inspects the work and explains its recommendation using scope, complexity, uncertainty, and risk. Small, reversible changes stay lightweight; larger or riskier changes get more structure. This is guidance and judgment, not a scored classifier or a guarantee of correct code.

| Tier | Choose it when | Artifacts |
|---|---|---|
| **TinySpec** | A bounded, reversible change has one clear implementation path | One Markdown file with requirements and verification |
| **LiteSpec** | Multiple stories, design decisions, or acceptance-to-test traceability need attention | `spec.md`, `plan.md`, `tests.md` |
| **Official GitHub Spec Kit** | Architecture, irreversible migrations, security, or coordination needs the full workflow | Upstream-managed specification, planning, and task artifacts |

[Selection rules](plugins/adaptive-sdd/skills/adaptive-sdd/references/tier-selection.md) · [Compare one feature at two depths](plugins/adaptive-sdd/examples/simple-kanban/README.md)

## What I built

Adaptive-SDD adds tier selection, TinySpec and LiteSpec conventions, promotion guidance, a shared Codex/Cursor skill, guarded installers, and portable Project Memory around the official Spec Kit workflow. Python tooling checks document structure and tracks optional approval/evidence state. Spec Kit remains an upstream dependency; its templates and implementation are not vendored here.

Strict delivery tracking is **optional**. When enabled, it requires recognized criteria and current recorded evidence. Document validation checks structure; evidence commands record attributed claims; actual tests must run separately. The gate does not execute checks or authenticate the person recording them.

```text
Request + repository context
             |
             v
Agent guidance: choose tier, clarify scope, plan, implement
             |
      TinySpec / LiteSpec / official Spec Kit artifacts
             |
             v
Deterministic tooling: document validation + optional state/evidence gate
             ^
             |
Actual checks: Python / Node / Playwright / human review
             |
             +--> results recorded by the operator or agent

Optional Project Memory: current repository context and change provenance
```

[Shared guidance](plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md) · [Tooling](plugins/adaptive-sdd/skills/adaptive-sdd/scripts/) · [Regression tests](plugins/adaptive-sdd/tests/)

## See it work in five minutes

**Daymark** is a runnable browser-local habit tracker. Its request is: “Create a habit tracker with daily check-ins, calendar history, and local persistence.” Several user journeys and persistence decisions make it a LiteSpec example.

1. Read [requirements](.litespec/habit-tracker-example/spec.md): `AC-01.1` covers adding a habit; `AC-04.1` covers retaining progress after reload.
2. Follow the [implementation plan](.litespec/habit-tracker-example/plan.md) to the [application](plugins/adaptive-sdd/examples/habit-tracker/app.js).
3. Open [Daymark's index.html](plugins/adaptive-sdd/examples/habit-tracker/index.html) from your local clone. Add a habit, check it off, view its calendar, and reload.
4. Run the checks below. [Unit tests](plugins/adaptive-sdd/examples/habit-tracker/app.test.mjs) exercise state and dates; [browser tests](tests/e2e/daymark.spec.mjs) exercise user interactions, persistence, and screenshot comparisons. The [test plan](.litespec/habit-tracker-example/tests.md) also identifies manual checks.

### Quickstart

Prerequisites: Git, Python **3.11+**, and Node **22.14.0** for the documented test environment. The app itself has no runtime dependencies. Browser testing needs an initial npm/browser download; committed visual baselines use **Windows + bundled Chromium**.

From the repository root:

```text
git clone https://github.com/JonC613/adaptive-sdd.git
cd adaptive-sdd
python -m unittest discover -s plugins/adaptive-sdd/tests -v
npm test
npm ci
npx playwright install chromium
npm run test:e2e
```

Expected: Python reports its pass/skip summary, Node runs five state/calendar tests, and Playwright runs five browser scenarios. Missing installer dependencies produce explicit skips in those integration tests. Use Windows for the screenshot suite; other operating systems do not have committed baselines. CI uses `windows-2022`, Node 22.14.0, and locked Playwright 1.63.0. See [browser environment and baseline policy](docs/qa/daymark-e2e.md).

For document validation only:

```text
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/validate_litespec.py .litespec/habit-tracker-example --json
```

Expected: `kind: structural`, `valid: true`. This does **not** mean the application or every requirement has been verified. See the [short demo script](docs/demo.md) for the request-to-check walkthrough and an empty-criteria failure demonstration.

### Use the workflow in another project

The shared project installer requires **PowerShell 7** and copies the skill for both Codex and Cursor:

```powershell
./install-project.ps1 -Target C:\path\to\your-project
```

Start a new task in the target project and invoke `$adaptive-sdd` in Codex or `/adaptive-sdd` in Cursor. Expect a tier recommendation based on the change and repository context. Add `-InstallSpecKit` only when the project needs the full upstream workflow. [Installation and marketplace options](plugins/adaptive-sdd/docs/installation.md)

## Coverage, compatibility, and limits

- **Deterministic coverage:** scaffold and validator behavior, traceability failures, approval/evidence staleness, memory drift, installer safety, evaluation reporting, diagnostics, JavaScript logic, and browser interactions. [CI workflow](.github/workflows/test.yml)
- **Evidence boundaries:** local installer integration tests exercise real PowerShell copies in temporary folders. The Spec Kit command path also has mocked tests; those do not establish a live upstream installation. [Contribution/check guide](CONTRIBUTING.md)
- **Compatibility:** Python 3.11+; PowerShell 7 for installers; one shared skill for Codex/Cursor. Spec Kit is pinned to `v0.16.4`. Strict tracking supports current TinySpec, the numbered legacy TinySpec example, LiteSpec, and the documented Spec Kit artifact subset. [Delivery formats and migration limits](plugins/adaptive-sdd/skills/adaptive-sdd/references/delivery-evidence.md)
- **Experimental:** tier recommendations and clarification quality have no live-agent benchmark results. [Evaluation design](plugins/adaptive-sdd/evals/README.md) separates regression outcomes from proposed measurements.
- **Adoption:** an ongoing departmental SDD pilot, primarily using GitHub Spec Kit and Adaptive-SDD guidance, with three-person teams spanning product ownership, development, and testing. Smoke and Playwright tests are being incorporated. No measured productivity improvement or production-maturity claim is made. [Portfolio case study](docs/case-study.md)
- **Licensing:** no repository license has been selected. An owner decision is pending; dependency licenses do not license this project.

Current manifest version: **0.4.1**. These improvements are recorded under Unreleased in the [changelog](CHANGELOG.md). [Project status](docs/upgrade-roadmap.md) · [Release-readiness checklist](docs/release-readiness.md) · [Full usage guide](plugins/adaptive-sdd/docs/using-adaptive-sdd.md)
