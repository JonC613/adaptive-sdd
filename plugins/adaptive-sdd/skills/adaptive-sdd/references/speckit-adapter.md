# Official Spec Kit adapter

Use GitHub Spec Kit as an upstream tool; do not vendor its templates or generated skills.

## Prerequisites

- Python 3.11 or newer
- `uv` recommended
- Git when project Git workflows are desired
- A clean commit before initializing into a non-empty repository

## Pinned installation

The repository documents a tested version. Verify the current pin before changing it.

```text
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.16.4
specify version
```

Initialize Codex skills in the current project:

```text
specify init --here --force --integration codex --script ps
```

Use `--script sh` on Linux or macOS. After initialization, use the official `$speckit-*` skills. Spec Kit owns `.specify/`, its installed `speckit-*` skills, and its generated `specs/` workflow.

## Safety

- Confirm the target repository and clean Git state.
- Show the exact pinned version and command before installation.
- Never claim Spec Kit is installed until `specify version` and the expected project files succeed.
- Use `specify integration upgrade codex` for routine integration updates; reserve forced reinitialization for recovery.
