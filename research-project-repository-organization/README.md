# Research Repository Setup

**ScholarSkills identifier:** SS-0014 proposed; pending maintainer assignment · **Version:** 0.1.0 draft ·
**Maturity:** experimental · **Licence:** MIT (original code and documentation)

## What it does

This draft turns published research-computing guidance into a cautious workflow for setting up or reviewing a research repository. It helps an agent inspect the project brief and existing files, define the repository boundary, plan documentation and provenance, flag sensitive or third-party material, and verify changes without assuming authority to migrate or publish data.

The workflow is adapted from Noble (2009), Wilson et al. (2017), and repository and sensitive-data guidance in *The Turing Way*. It does not prescribe one universal project tree and is not evidence that a particular layout improves research quality.

## Installation and use

The skill itself is a set of agent instructions in `SKILL.md`. The optional scaffold script uses Python 3.10+ and the standard library; it needs no network access or third-party package.

From this package directory:

```bash
python3 scripts/scaffold_project.py /tmp/example-research-project \
  --title "Example Research Project"
```

The script refuses any destination that already exists. It creates a blank documentation scaffold only. It does not initialize Git, create data directories, move existing files, or contact a remote service.

## Example

The example project is fictional and contains no research data or personal information. See `examples/README.md` for the command and generated file list.

## Compatibility actually tested

| Component | Version | Result |
|---|---|---|
| Python | 3.14.9 | Scaffold script and six unit tests passed locally |
| ScholarSkills validator | Candidate worktree based on `b4704aa`; run with `--allow-placeholders` | PASS, no draft warnings |
| GitHub Actions (Python 3.10 / 3.12) | Not yet run for this candidate | Pending |
| Agent host | Not yet exercised | Not tested |

## Limitations

- The repository structure must be adapted to the project's methods, materials, collaborators, and institutional requirements.
- The workflow does not determine whether data may legally or ethically be collected, stored, or shared.
- A `.gitignore` rule does not secure data already tracked by Git.
- The scaffold is a starting point, not a complete research plan or data-management plan.
- Author: Eric Brasil (UNILAB); contribution and identity metadata are recorded in the package files.
- The proposed identifier remains subject to maintainer assignment; no DOI or release has been issued.

## Data and ethics

The runnable example uses only a fictional project title. The script creates no dataset and makes no network request. Never place restricted or personal data in the example package. Public availability alone does not establish consent, permission to redistribute, or approval for a new use. Confirm the relevant institutional requirements before moving or sharing source materials.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The latest test environment and results are recorded in `tests/RESULTS.md`.

## Citation

No DOI has been assigned to this draft. If accepted and deposited, cite the versioned record listed in the ScholarSkills registry.

## Authors and contributions

| Author | Affiliation | Contribution |
|---|---|---|
| Eric Brasil | Institute of Humanities and Languages, University of International Integration of Afro-Brazilian Lusophony (UNILAB) | Source skill, conceptual scope, and review of the generalization |

ORCID: [0000-0001-5067-8475](https://orcid.org/0000-0001-5067-8475).
