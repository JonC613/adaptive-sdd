# Cursor Marketplace submission

This repository is a Cursor multi-plugin repository. The marketplace manifest at
`.cursor-plugin/marketplace.json` identifies `plugins/adaptive-sdd` as the source;
the per-plugin Cursor manifest specifies that `skills/` is the discoverable
component directory. The plugin also retains its root `plugin.json` Agent Plugins
manifest for portable Codex/Cursor use.

## Submission sequence

1. Choose and commit a repository license. Cursor’s public Marketplace reviews
   open-source plugins; do not submit this repository until the license decision
   is recorded.
2. Create a release candidate: synchronize manifest versions, changelog, README,
   package lockfile, and marketplace version. Keep unreleased work out of the
   candidate.
3. Run the [release-readiness checklist](release-readiness.md), including fresh
   Codex and Cursor installation checks. Record the actual commands, versions,
   test results, and any skipped work.
4. On a machine with Cursor, test the repository locally:

   ```text
   ~/.cursor/plugins/local/adaptive-sdd/
   └── [a copy or symlink of plugins/adaptive-sdd]
   ```

   Reload Cursor, open Customize, and confirm that `adaptive-sdd` appears under
   Skills. Open a fresh agent session and invoke `/adaptive-sdd`. If local plugin
   imports are blocked, request that the Cursor administrator enable them; do not
   treat a failed local import as a successful marketplace test.
5. Push the reviewed release candidate to the public Git repository. Commit a
   logo and reference it in the Cursor manifest if one is available; it is
   recommended, not required.
6. Submit the repository URL at
   [Cursor Marketplace publish](https://cursor.com/marketplace/publish). Include
   concise installation steps, the supported environments, and the project’s
   evidence limits. Cursor manually reviews public marketplace plugins and their
   updates.

## Pre-submission checks

```text
python scripts/check_repository.py
python -m unittest discover -s plugins/adaptive-sdd/tests -v
npm ci
npm test
npm run test:e2e
```

The repository checker confirms the Cursor marketplace source, manifest metadata,
and version agreement. The test suites do not replace the fresh Cursor import
check or Cursor’s marketplace review.

## Scope of this preparation

This adds Cursor marketplace metadata only. It does not create a release, submit
the repository, install a plugin in Cursor, choose a license, or claim approval.
