# Adaptive SDD marketplace

This repository is a Codex marketplace containing the [Adaptive SDD plugin](./plugins/adaptive-sdd/README.md).

Version 0.4 adds resumable evidence-backed delivery, safer installation, explicit
structural diagnostics, interaction modes, and optional project profiles. See the
[changelog](CHANGELOG.md) and [upgrade record](docs/upgrade-roadmap.md).

After cloning this public repository, add it as a marketplace and install the plugin:

```powershell
codex plugin marketplace add JonC613/adaptive-sdd
codex plugin add adaptive-sdd@adaptive-sdd
```

Open a new Codex task after installing the plugin before invoking `$adaptive-sdd`; an already-running task may not load newly installed skills.

The plugin guides TinySpec, LiteSpec, official GitHub Spec Kit, and portable Project Memory through approval gates.

To install the shared skill into one repository for both Codex and Cursor, run the root bootstrap script:

```powershell
./install-project.ps1 -Target C:\path\to\your-project
```

Add `-InstallSpecKit` only when that project also needs the full upstream Spec Kit workflow. The root scripts delegate to the versioned plugin implementation in `plugins/adaptive-sdd/`.
