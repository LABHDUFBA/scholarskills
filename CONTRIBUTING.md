# Contributing to ScholarSkills

## Before you open a pull request

1. Read `registry/EDITORIAL_POLICY.md`. It defines what a skill must contain and how maturity is
   granted. Reviewers reject packages that skip a required item rather than negotiating it case by
   case.
2. Start from `skill-template/`. Do not invent a new layout: the layout is what makes the catalogue
   machine-readable.
3. Run the checks locally. A submission that fails validation is not reviewed.

```
python3 scientific-agent-skill-development/scripts/validate_skill.py path/to/your-skill
python3 -m unittest discover -s scientific-agent-skill-development/tests -v
```

## Evidence dimensions

The portal reports six independent dimensions: structural conformance, functional tests, methodological assessment, peer review, independent re-execution and scientific replication. A green test suite supports the second dimension only; it does not grant the others. See `registry/EDITORIAL_POLICY.md`.

## Without Git

If you do not use Git, write to the laboratory address on the portal and describe the skill you want to propose. The team will advise on the format and a submission route. There is no promise of email submission or automatic acceptance.

## Submitting

- One skill per pull request, plus **one** new entry in `registry/registry.json`.
- The identifier `SS-NNNN` is requested, not assigned: propose it in the PR description and let the
  maintainers set the final one.
- New entries must validate against `registry/metadata-schema.json`.
- Fields you do not know stay `null`. Do not write `TBD`, `pending` or a fake DOI — validation
  rejects placeholders on purpose.

## What gets a submission returned without review

- A `description` that does not say **when** to use the skill.
- Tests that only exercise the happy path.
- A limitations section that says "none known".
- A claimed maturity level without the artefact that justifies it.
- Personal data, credentials or scraped private content committed to the repository.
- A DOI invented, reserved but unpublished, or copied from another skill.

## Review

Two reviewers apply the five criteria in the editorial policy and record verdicts in the skill
repository under `reviews/`. Authors respond in the pull request; history is not rewritten.
