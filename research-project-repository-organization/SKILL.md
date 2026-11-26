---
name: research-project-repository-organization
description: "Plan or revise a research project's repository structure and working record from a project brief. Use when starting a research repository, onboarding collaborators, or auditing an existing project for scope, provenance, sensitive material, and version-control risks."
license: MIT
compatibility: Requires Python 3.10+ for the optional scaffold script; Git is needed only when auditing a version-controlled project. No network access.
metadata:
  scholarskills.id: SS-0014
  scholarskills.version: "0.1.0"
  scholarskills.maturity: experimental
  scholarskills.method: Research project organization and provenance planning, adapted from reproducible research computing guidance
---

# Research Repository Setup

This skill helps a research team establish or review a repository that makes the project understandable, traceable, and safe to work on. It produces a project-specific structure and working record; it does not prescribe one universal directory tree.

## When to use

- A researcher asks to start a repository for a study, dataset, method, or research software project.
- A team needs to document scope, responsibilities, milestones, or working practices in an existing repository.
- A project repository needs an audit before moving, sharing, or publishing its contents.
- A project includes data, code, documents, figures, or other outputs whose provenance and storage need to be made explicit.

**Do not use** this skill to decide whether sensitive data may legally or ethically be collected, stored, or shared. Follow the responsible institution's data-management, ethics, security, and legal procedures. Do not use it to migrate files automatically or to publish, commit, push, or change remote settings without explicit authorization.

## Inputs

Gather what is available; mark unknowns instead of filling them by inference.

| Input | Required | Examples |
|---|---|---|
| Project brief | yes | Research question, objective, intended output, acceptance criteria |
| Repository state | yes | New or existing; local path or canonical remote; current branch and status if Git is used |
| People and workflow | recommended | Roles, collaborators, review points, communication and deadlines |
| Research materials | recommended | Data, sources, code, instruments, analysis outputs, manuscripts |
| Constraints | required before file movement or sharing | Sensitivity, consent, access restrictions, copyright, funder or institutional rules |

If the question, output, repository identity, or data-handling constraints are unclear, ask before making changes.

## Outputs

Depending on the request, produce:

- A repository inventory and explicit project boundary.
- A fit-for-purpose directory map, with reasons for important inclusions and exclusions.
- A concise `README.md`, a working plan, and a dated progress record; add findings, protocol, source inventory, schemas, or examples only when the project needs them.
- A data and artifact provenance record. For quantitative or corpus projects, include the unit of analysis, source, snapshot or collection interval, filters, transformations, and denominator for reported totals.
- A review of sensitive, private, third-party, generated, or bulky materials before anything is staged.
- A Git state and validation report. The optional script creates only a blank starter scaffold; it does not initialize Git or migrate content.

## Procedure

1. **Inspect before editing.** Determine whether the repository is new or existing. For an existing project, inspect its README, local instructions, plan, current tree, Git status, branch, remotes, recent history, and relevant source artifacts. Treat the canonical remote and the user's stated source of truth as facts to verify, not assumptions. Preserve uncommitted work.
2. **Define the project boundary.** Write the research objective, question, intended products, non-goals, collaborators, dependencies, deadline, and completion criteria from the brief. Decide whether work belongs in this repository by examining shared data, code, methods, contributors, governance, and release needs. Do not split or combine projects by a universal percentage or naming rule.
3. **Classify material before moving or staging it.** Separate public, restricted, personal, confidential, third-party, and generated material. Check permissions and storage rules with the responsible institution. Keep restricted originals in an approved location; version only reviewed, authorized derivatives or a metadata inventory. A private Git remote is not a secure-data approval. Create or update `.gitignore` before staging local secrets or sensitive files, but do not rely on ignore rules as the sole safeguard.
4. **Choose a structure that serves this project.** Separate inputs, methods, outputs, documentation, and publication artefacts when doing so improves navigation and traceability. Avoid empty mandatory folders, duplicate copies of the same source, and unexplained generic directories. Do not restructure an existing project merely to match an example tree.
5. **Create the minimum useful documentation.** Make the README answer what the project is, why it exists, its scope, how to navigate it, current state, and how to cite or contribute when applicable. Maintain a plan for decisions and next steps, a progress record for completed work and verification, and findings for source-backed evidence and design choices. Keep plans distinct from external evidence. Add protocol, architecture, schema, or source inventory documents only when they support actual work.
6. **Record provenance where outputs depend on sources or data.** Preserve source identifiers, acquisition or snapshot date, version, filters, transformations, software environment, and output paths as relevant. Name each metric's unit and denominator. Do not infer missing provenance or silently correct malformed source values.
7. **Audit the change boundary.** Before moving files, compare source and destination trees and list proposed inclusions and exclusions. Use version-control history when it helps preserve provenance. Never overwrite, delete, migrate, commit, push, publish, or change a remote without the user's explicit authorization. Follow the repository's existing branch and review conventions.
8. **Verify and report.** Check links and referenced files, ensure no credentials or unauthorized sensitive content are staged, run documented tests or project checks where available, and inspect `git diff --check` and the final changed-file list. Report what was actually inspected, changed, excluded, and tested; separate verified facts from open decisions.

## Stop criteria

Stop before file changes or sharing when:

- The canonical repository or source-of-truth version cannot be identified.
- The brief lacks enough information to define project scope or an acceptable output.
- Rights, consent, access, storage location, or institutional policy for a sensitive source are unresolved.
- The proposed migration could overwrite, delete, expose, or irreversibly alter material.
- A requested metric lacks a defined unit, time window, or source snapshot and the missing information cannot be recovered.
- The next action would publish, commit, push, change permissions, or move data outside the approved environment without explicit authorization.

## Error handling

| Situation | Response |
|---|---|
| Existing project has uncommitted changes | Preserve them; report the state and avoid staging unrelated files |
| Remote or branch differs from the request | Stop and verify the canonical target before editing |
| Source file is missing or unreadable | Record the gap; do not recreate its contents from memory |
| Sensitive material is already tracked | Do not copy it elsewhere or publish it; report the exposure and ask the owner for a remediation decision |
| Directory contains unknown files | Inventory them and ask before moving or deleting them |
| Script destination already exists | The scaffold script refuses; choose a new path or review the destination manually |
| Git or a test command fails | Preserve the exact error, identify what remains unverified, and do not claim success |

## Limits

- There is no universally correct research repository tree. The structure must fit the project's methods, materials, people, governance, and outputs.
- Documentation and version control improve traceability; they do not by themselves establish scientific validity, reproducibility, legal compliance, ethical approval, or secure storage.
- A README or plan can become stale. Record dates and update it when project decisions change.
- The scaffold script creates a blank starter layout only. It cannot infer a research design, institutional policy, rights, provenance, or correct project structure.
- The workflow is informed by research-computing and project-repository guidance; it is not a validated intervention with a measured effect on research quality.

## Tools and dependencies

- Python 3.10+ standard library for `scripts/scaffold_project.py`.
- Git for repository-state inspection when the project uses Git.
- No network access is needed by the scaffold script or its tests.

## Validation

Run from this package directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/scaffold_project.py /tmp/example-research-project --title "Example Research Project"
```

The tests check scaffold creation and refusal conditions. They do not validate the user's research design, chosen repository layout, data rights, or empirical claims.

## References

See [`references/methodology.md`](references/methodology.md) for the sources and how their recommendations are operationalized here. The repository scaffold example uses synthetic project information only.
