# Adaptive SDD marketplace

This repository is a Codex marketplace containing the [Adaptive SDD plugin](./plugins/adaptive-sdd/README.md).

After cloning this public repository, add it as a marketplace and install the plugin:

```powershell
codex plugin marketplace add JonC613/adaptive-sdd
codex plugin add adaptive-sdd@adaptive-sdd
```

The plugin guides TinySpec, LiteSpec, official GitHub Spec Kit, and portable Project Memory through approval gates.

To install the shared skill into one repository for both Codex and Cursor, run the root bootstrap script:

```powershell
./install-project.ps1 -Target C:\path\to\your-project
```

Add `-InstallSpecKit` only when that project also needs the full upstream Spec Kit workflow. The root scripts delegate to the versioned plugin implementation in `plugins/adaptive-sdd/`.
