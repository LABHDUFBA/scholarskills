# Validation protocol — what is checked, and what it proves

## Two different questions

1. **Is the package structurally reviewable?** — automated, deterministic, cheap.
2. **Is the method correct?** — requires domain judgement, cannot be automated here.

`validate_skill.py` answers only the first. Every artefact that reports on validation must say so,
or readers will read green checks as scientific endorsement.

## Checks performed

| Check | Rule | Failure mode prevented |
|---|---|---|
| Frontmatter present | `---` YAML block at the top of `SKILL.md` | Skill not loadable by any client |
| `name` syntax | 1–64 chars, `[a-z0-9-]`, no edge or doubled hyphen | Client rejects the skill silently |
| `name` = directory | Exact match | Ambiguous identity, broken relative paths |
| `description` length | 1–1024 chars | Truncation in client listings |
| `description` content | States what *and* when (warning) | Skill never activated |
| `compatibility` length | ≤500 chars | Spec violation |
| `metadata` types | string → string | Client crash on non-string values |
| Required files | SKILL.md, README, CITATION.cff, LICENSE, CHANGELOG | Unreviewable, uncitable package |
| Placeholders | No unfinished-marker text remains | Shipping an incomplete method |
| Local links | Every relative markdown link resolves | Broken instructions for the next agent |
| Credentials | Narrow patterns for tokens and keys | Leaked secret in a public archive |
| CITATION/.zenodo | `cff-version` present, no placeholder DOI | Fabricated identifier |

## Why placeholders are a hard error

A package with a placeholder is not a draft to be merged and fixed later: it is a method with an
undecided step. In a citable artefact, an undecided step is a wrong answer waiting to be executed.

## What the protocol cannot see

- A method implemented faithfully but wrongly chosen.
- A test that asserts the wrong behaviour, consistently.
- A citation that exists but does not support the claim.
- A licence incompatible with the data the skill touches.
- A dataset that is legal but unethical to use.

Those require a human reviewer applying `EDITORIAL_POLICY.md`, and, where relevant, an ethics
committee.

## Maturity and evidence

| Level | Evidence artefact |
|---|---|
| `tested` | `tests/RESULTS.md` with environment, command and output |
| `peer-reviewed` | `reviews/` with two named assessments |
| `replicated` | `reviews/` with a third-party re-execution report |

Absence of the artefact means the lower level. There is no "in review, so effectively reviewed".
