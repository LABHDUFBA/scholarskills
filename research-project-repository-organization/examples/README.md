# Synthetic scaffold example

This example is entirely fictional. It contains no source data, human-subject information, or institutional material.

Run from the package directory, using a destination that does not exist:

```bash
python3 scripts/scaffold_project.py /tmp/example-research-project \
  --title "Synthetic Example Project"
```

The script creates only this starter tree:

```text
example-research-project/
├── .gitignore
├── README.md
├── task_plan.md
├── findings.md
├── progress.md
└── docs/
    ├── protocol.md
    └── vision-and-scope.md
```

It does not create a Git repository, data directory, remote, or commit. Inspect and adapt each file before adding project material. A real project may need a different structure and must follow its own data-access and storage rules.
