# Test results — experimental draft

**Date:** 2026-11-25

**Environment:** Python 3.14.9; Linux; standard library only.

**Command:** `python3 -m unittest discover -s tests -v`

```text
Ran 6 tests in 0.004s
OK
```

The suite exercises successful scaffold creation, refusal of existing empty and non-empty directories, blank-title rejection, and refusal to write to the current working directory or filesystem root. It confirms the script does not initialize Git or create a data directory.

**Runnable example:** ran `python3 scripts/scaffold_project.py <temporary-destination> --title 'Synthetic Example Project'`. It created seven documented files, initialized no Git repository, and refused a second run against the existing destination without overwriting it.

**Structural validation:** `python3 scientific-agent-skill-development/scripts/validate_skill.py research-project-repository-organization` returned PASS with 0 warnings. SS-0014 is proposed and awaits maintainer assignment. The package has no DOI or release.

**Not tested:** Python 3.10/3.12 CI, compatibility with any agent host, the procedure against an independent real research project, and the scientific or ethical adequacy of a researcher's project decisions.
