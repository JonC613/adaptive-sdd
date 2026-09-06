# Contributing

Keep the shared workflow provider-neutral and dependency-light. Add a deterministic
regression for every safety or validation change. Do not describe structural checks,
mocks, or unrun CI as delivery evidence. Preserve compatibility fixtures unless an
approved migration documents their replacement.

Before proposing a change, run:

```text
python -m unittest discover -s plugins/adaptive-sdd/tests -v
python plugins/adaptive-sdd/evals/evaluate.py --plugin plugins/adaptive-sdd
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/doctor.py --plugin plugins/adaptive-sdd
```

The repository owner must choose a license before public distribution rights are
claimed. Contributions do not imply a license grant while that decision is absent.
