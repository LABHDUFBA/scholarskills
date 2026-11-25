# SS-0000 — Scientific Agent Skill Development and Validation Protocol

**ScholarSkills identifier:** SS-0000 · **Version:** 1.0.0 · **Maturity:** `tested`
· **Licence:** MIT (original code and documentation)

A meta-skill. It takes a research method and produces a skill package that can be reviewed, tested,
cited and archived — or it refuses, and says why.

## The claim it makes, and the claim it does not

It *does* enforce a structure: frontmatter that satisfies the Agent Skills specification, required
documentation, tests that include failure modes, placeholder and secret detection, local link
integrity, and metadata prepared for deposit.

It *does not* validate the science. A package that passes every check here can still implement the
wrong method. Peer review and replication are social processes; the skill prepares their evidence
and never confers their status.

## Installation

```bash
git clone https://github.com/LABHDUFBA/scholarskills.git
cd scholarskills/scientific-agent-skill-development
python3 -m venv .venv && . .venv/bin/activate
pip install pyyaml
```

| Component | Version tested |
|---|---|
| Python | 3.14.9 (also exercised on 3.10+) |
| PyYAML | 6.0.3 |
| OS | Linux 6.8 (Ubuntu) |
| Network | not required |

## Minimal example

```bash
python3 scripts/build_package.py     --slug my-descriptive-stats --title "Descriptive Statistics for Tabular Data"     --out /tmp/my-descriptive-stats --author "Surname, Given" --affiliation "Institution"

python3 scripts/validate_skill.py /tmp/my-descriptive-stats
python3 scripts/run_checks.py /tmp/my-descriptive-stats --json
```

Expected on a fresh scaffold: validation **fails by design**, listing the placeholders a human must
replace. That refusal is the feature — the generator will not invent a method.

## Running the reference example

`examples/descriptive-analysis/` is a complete, small skill built with this protocol. It is
deliberately modest (descriptive statistics on tabular data) so that its correctness can be checked
by reading it.

```bash
python3 examples/descriptive-analysis/scripts/describe.py examples/descriptive-analysis/examples/sample.csv
python3 -m unittest discover -s tests -v
```

## Compatibility actually tested

| Agent / host | Version | Result |
|---|---|---|
| Hermes Agent (LABHDUFBA) | 2026-11 build | Skill loaded and executed by the agent runtime |
| Standalone CLI (no agent) | — | Scripts run directly with Python |

Other agents that implement the Agent Skills specification are **not tested**. The package follows
the published format, but format compliance is not the same as a verified integration.

## Limitations

- Validation is structural. It cannot detect a method implemented faithfully but wrongly chosen.
- The secret patterns are narrow by design; a false negative is possible. Never treat a green run as
  a security audit.
- The ethics checklist is a floor, not an ethics committee.
- Metadata schemas evolve. `generate_metadata.py` records the field set it used; that set may age.
- No network calls are made, so the skill cannot verify that a cited DOI resolves.

## Data and ethics

Examples are synthetic. The skill is intended for **publishing methodological artefacts**, and must
not be used to wrap a pipeline whose data provenance cannot be disclosed, nor to produce maturity
claims without evidence.

## Citation

See `CITATION.cff`. No DOI yet: the identifier fields stay empty rather than receiving a placeholder.

## Authors and contributions

| Author | Affiliation | Contribution |
|---|---|---|
| Leonardo Fernandes Nascimento | LABHDUFBA / UFBA | Conception, protocol, implementation |
| Eric Brasil | UNILAB | Editorial policy and review criteria |
| Ricardo Sodré | UFBA | Methodological review |

## Repository layout

```
scientific-agent-skill-development/
  SKILL.md                 operational instructions for an agent
  scripts/                 validator, builder, metadata generator, aggregator
  references/              methodology, validation protocol, ethics, metadata fields
  examples/descriptive-analysis/   complete reference skill
  tests/                   unit tests + recorded results
  benchmarks/              measured behaviour of the validator
```
