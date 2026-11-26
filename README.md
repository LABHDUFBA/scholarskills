# Métodos Digitais — skills de pesquisa para agentes de IA

Identificador técnico do repositório: `scholarskills` (prefixo de ID `SS-`). O nome mudou; o
identificador não, para não quebrar URLs, DOIs e citações já emitidos.

An academic repository of **executable research methodologies for AI agents**, maintained by the
[Digital Humanities Laboratory, Federal University of Bahia (LABHDUFBA)](https://labhd.ufba.br).

Métodos Digitais treats an agent skill as a **citable methodological object**: documented, versioned,
tested, licensed and archived with a DOI, in the same way a method section or a piece of research
software is. The goal is methodological transparency and reproducibility for computational social
science and the digital humanities — not tool distribution.

## Skills in this repository

One repository holds every skill. Each skill keeps its own directory, version, CHANGELOG and
evidence, so it can be cited and deposited independently without fragmenting the project into a
dozen small repositories.

| ID | Skill | Directory | Status |
|---|---|---|---|
| SS-0000 | Scientific Agent Skill Development and Validation Protocol | `scientific-agent-skill-development/` | available · tested |
| SS-0001 | Zotero Reference Management | `zotero-reference-management/` | available · tested |
| SS-0002 … SS-0009 | Roadmap | — | planned |

The catalogue is `registry/registry.json`; it is the single source of truth for the hub site
(`site/`, published at https://labhdufba.github.io/scholarskills/), which is generated from it by
`scripts/build_site.py`.

## Why

Agent skills circulate widely and are rarely inspectable. A reader cannot tell what a skill
actually does, which decisions it encodes, where it fails, or how to cite it. Métodos Digitais
addresses that gap by requiring, for every skill: verifiable methodological grounding, executable
instructions, declared dependencies, tests including failure cases, documented limitations, a
license, and ethical considerations.

## Repository layout

```
scholarskills/
  registry/                              # catalogue: policy, schema, registry.json
  skill-template/                        # canonical package for a new skill
  scientific-agent-skill-development/    # SS-0000 — the meta-skill
```

Each skill lives in its **own repository** so that it can carry its own release, version DOI and
concept DOI. This repository holds the catalogue, the template and the meta-skill.

## Maturity levels

| Level | Meaning | Evidence required |
|---|---|---|
| `experimental` | Works on the author's machine; not independently exercised | Author's report |
| `tested` | Automated tests exist and pass in a declared environment | CI log or `tests/RESULTS.md` |
| `peer-reviewed` | Assessed by named reviewers under the editorial policy | Review record |
| `replicated` | Independently re-executed by a third party with reported results | Replication report |

A level is **never** assigned by aspiration. `peer-reviewed` and `replicated` require documentary
evidence stored in the skill repository; absence of evidence means the lower level.

## Status

This repository is in **pre-release**. The catalogue (`registry/registry.json`) lists SS-0000 as
`tested` and SS-0001…SS-0008 as `planned` (no DOI, no deposit, not available).

## Licence

Code: MIT. Documentation: CC BY 4.0. **Pending institutional approval** — see
`DEPLOYMENT_LOG.md` before reusing.

## Citation

See `CITATION.cff`. No DOI is registered yet; the record is intentionally left without an
identifier rather than carrying a placeholder.
