---
name: scientific-agent-skill-development
description: Turn a research method into a documented, tested, citable agent skill. Use when an agent must create or review a scientific skill package, define its scope and stop criteria, write positive and negative tests, audit it for privacy and copyright, and prepare it for archival deposit without publishing autonomously.
license: MIT
compatibility: Requires Python 3.10+ and PyYAML. Validation and packaging run offline; no network access is needed.
metadata:
  scholarskills.id: SS-0000
  scholarskills.version: "1.0.0"
  scholarskills.maturity: tested
  scholarskills.method: Agent Skills specification (agentskills.io) + research-software packaging practice
  scholarskills.spec-version: "agentskills.io specification, accessed 2026-11-24"
---

# Scientific Agent Skill Development and Validation Protocol

A meta-skill: it produces other skills, as reviewable scientific artefacts rather than as prompts
that happen to work once.

## When to use

- A researcher wants to turn a method (a coding scheme, a corpus procedure, an estimation step) into
  something an agent can execute and a reader can cite.
- A skill already exists and must be reviewed before deposit, release or publication.
- A catalogue needs a new entry with defensible metadata.

**Do not use** to wrap a proprietary pipeline you cannot describe, to launder an undocumented
heuristic into a "method", or to produce a maturity claim without the evidence that supports it.

## Core rule

A skill is a **methodological claim in executable form**. Everything in the protocol follows from
that: if a claim cannot be tested, it is labelled a hypothesis; if a decision could have gone
another way, it is recorded; if a level of maturity has no artefact behind it, it is not claimed.

## Inputs

| Input | Required | Meaning |
|---|---|---|
| `objective` | yes | The scientific goal: what question the method answers |
| `method` | yes | The method name, its tradition and its literature |
| `inputs` | yes | Data types, schema, provenance and personal-data status |
| `outputs` | yes | Artefacts produced, their format and their consumer |
| `constraints` | yes | Compute, data protection, licensing, institutional limits |
| `author` | yes | Name, affiliation, ORCID if the author supplies one |

## Procedure

### Step 1 — Scope the claim

Write one sentence of the form: *"Given ⟨input⟩, this skill produces ⟨output⟩ by applying ⟨method⟩,
and it is valid only when ⟨assumption⟩."* If any slot cannot be filled, stop and ask — an unfillable
slot is the finding, not an obstacle to route around.

Record explicitly:
- what the output **establishes**;
- what remains **interpretation**;
- what is a **hypothesis** the skill does not test;
- what is **normative**.

### Step 2 — Ground the method

For each methodological decision, record the source. A citation is written only if it can be
verified; otherwise write "unverified — to be confirmed by the author". Do not paraphrase a method
from memory into a specification: the paraphrase becomes the specification, and its errors become
the skill's errors.

See `references/methodology.md` for the section template.

### Step 3 — Generate the package

```bash
python3 scripts/build_package.py --slug <skill-name> --title "<Title>" --out <dir> \
    --author "<Name>" --affiliation "<Affiliation>"
```

Produces the canonical layout (SKILL.md, README.md, CITATION.cff, LICENSE, CHANGELOG.md,
.zenodo.json, references/, scripts/, examples/, tests/, benchmarks/) with placeholder markers (the word TODO followed by the
SS tag) where human content is required. The script refuses a slug that violates the Agent Skills naming rules.

### Step 4 — Write tests that can fail

Minimum set, all of which must exist:

| Type | Example |
|---|---|
| Positive | Canonical input produces the documented output |
| Negative | Input violating an assumption produces an explicit refusal, not a silent coercion |
| Edge | Empty file, single row, missing optional column, duplicated keys |
| Tool failure | Network or dependency unavailable: the run stops and preserves the error |
| Reference absence | No verifiable source available: the output is labelled unverified |

Structural tests validate the *package*, not the *science*. State that distinction in the README so
a reader does not mistake green tests for a validated method.

### Step 5 — Record the environment

Python version, package versions, model name and revision, hardware, date, and the exact command
used. A result without its environment is not reproducible, only reported.

### Step 6 — Audit ethics and rights

Run the checklist in `references/ethics-and-rights.md`. At minimum: personal data, consent,
copyright of source content, dual use, and the aggregation threshold below which a group must not
be identified. Failures here block the package regardless of technical quality.

### Step 7 — Validate

```bash
python3 scripts/validate_skill.py <skill-dir>
python3 scripts/run_checks.py <skill-dir> --json
python3 -m unittest discover -s tests -v
```

`validate_skill.py` enforces the Agent Skills frontmatter rules (name, description length,
name-directory matching), required files, placeholder detection, local link resolution and secret
patterns. `run_checks.py` aggregates the result into a machine-readable report.

### Step 8 — Prepare (not perform) the deposit

```bash
python3 scripts/generate_metadata.py <skill-dir> --out deposit/
```

Produces `.zenodo.json`-based metadata, a ZIP of the version, and its SHA-256, plus a checklist of
what only a human can authorise: authorship, affiliation, licence, institutional clearance,
creation of the community, publication of the release.

**The skill never publishes, never reserves a DOI and never creates a public repository on its own
initiative.** Those are operator decisions, recorded in the deployment log.

## Stop criteria

Stop and report, without working around, when:

- the method cannot be stated in one falsifiable sentence;
- a required input contains personal data whose legal basis is not established;
- a test cannot be written because the behaviour is undefined — that is a specification defect;
- the package would need a claimed maturity level with no evidence artefact;
- publication, DOI reservation or a public release would be the next step.

## Error handling

| Situation | Action |
|---|---|
| Slug violates naming rules | Rename; do not "fix" it after the fact in the frontmatter only |
| Placeholder markers remain | Validation fails by design — the package is incomplete |
| Local link broken | Fix the path; do not delete the link to silence the check |
| Secret pattern detected | Remove and rotate the credential; the test is not a false positive to suppress |
| PyYAML absent | Install it; do not fall back to regex parsing of YAML |

## Limits

- **A passing validation is not a validated method.** It proves structure, not truth.
- Peer review and replication are social processes. This skill can *prepare* evidence for them; it
  cannot confer either status.
- The ethics checklist is a floor, not a substitute for an ethics committee where one is required.
- Metadata schemas change: the script records the spec version it validated against, and that
  version may become obsolete.

## Tools and dependencies

- `scripts/validate_skill.py` — frontmatter, structure, links, placeholders, secret patterns.
- `scripts/build_package.py` — scaffolds the canonical layout.
- `scripts/generate_metadata.py` — deposit metadata, ZIP, SHA-256, human-authorisation checklist.
- `scripts/run_checks.py` — aggregates validation into JSON for CI.
- PyYAML for frontmatter; everything else is the standard library.

## Validation

`tests/` exercises the validator and the builder, including the failure modes above.
Environment and results: `tests/RESULTS.md`.

## References

- `references/methodology.md` — how to write the methodological section.
- `references/validation-protocol.md` — the full validation procedure and its rationale.
- `references/ethics-and-rights.md` — ethics, privacy and copyright checklist.
- `references/metadata-fields.md` — registry and deposit field semantics.
