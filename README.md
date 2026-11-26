# ScholarSkills — Skills Métodos Digitais

ScholarSkills is a public catalogue of agent skills for research, maintained by the [Digital Humanities Laboratory at the Federal University of Bahia (LABHDUFBA)](https://labhd.ufba.br). Each available skill has its own directory, documentation, tests, version and citation metadata. The project aims to make research procedures inspectable and reproducible; an agent's output does not replace a researcher's judgment.

**Explore the catalogue:** https://labhdufba.github.io/scholarskills/ · **Machine-readable registry:** [`registry/registry.json`](registry/registry.json) · **How to contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Available skills

The registry is the source of truth for identifiers, status, maturity and DOI. The entries below reflect the current catalogue; `tested` means automated tests passed in a documented environment, **not** that the underlying scientific claims were peer-reviewed or independently replicated.

| ID | Skill | Package | Maturity |
| --- | --- | --- | --- |
| SS-0000 | Scientific Agent Skill Development and Validation Protocol | [`scientific-agent-skill-development/`](scientific-agent-skill-development/) | tested |
| SS-0001 | Zotero Reference Management | [`zotero-reference-management/`](zotero-reference-management/) | tested |
| SS-0010 | DOU and Federal Covenants | [`dou-federal-gazette/`](dou-federal-gazette/) | tested |
| SS-0011 | Brazilian Fiscal Data (SICONFI) | [`brazilian-fiscal-data/`](brazilian-fiscal-data/) | tested |
| SS-0012 | Hugo Site Maintenance | [`hugo-site-maintenance/`](hugo-site-maintenance/) | tested |
| SS-0013 | Lattes CV Editing | [`lattes-cv-editing/`](lattes-cv-editing/) | tested |
| SS-0014 | Research Repository Setup | [`research-project-repository-organization/`](research-project-repository-organization/) | tested |

SS-0002 through SS-0009 are **planned** entries, not downloadable or validated packages. Read their proposed scope in the [registry](registry/registry.json). Do not cite a planned entry as an implemented method.

## What a skill package contains

A package's `SKILL.md` states when to use it, what it needs, how it works and when to stop. Its `README.md` explains installation and use; `tests/` and `tests/RESULTS.md` record evidence for the claimed maturity level. Packages also carry citation metadata, a changelog and a licence file. Depending on the method, they may contain runnable scripts, examples, methodological references and benchmarks.

ScholarSkills keeps these packages in **one Git repository**, rather than requiring a repository per skill. Available skills may receive their own archival record and version DOI; the collection has a separate record. The distinction between concept DOI and version DOI is documented in [`registry/README.md`](registry/README.md). An archived version may differ from the latest `main` branch; cite the version used when one exists.

## Try a package or validate a contribution

Requires Python 3.10+ and Git. Individual skills may require additional dependencies, network access or operator-provided credentials; consult the package README before running it.

```bash
git clone https://github.com/LABHDUFBA/scholarskills.git
cd scholarskills
python3 -m pip install pyyaml
python3 scientific-agent-skill-development/scripts/validate_skill.py scientific-agent-skill-development
(cd scientific-agent-skill-development && python3 -m unittest discover -s tests -v)
```

To validate another package, pass its directory to `validate_skill.py` and run its own documented test suite. Structural validation catches missing files, malformed frontmatter, unresolved placeholders and some unsafe material; it **does not** establish that a cited source supports a claim or that a method is scientifically valid. The CI workflow is in [`.github/workflows/validate.yml`](.github/workflows/validate.yml).

## Repository map

- [`registry/`](registry/) — catalogue, metadata schema and [editorial policy](registry/EDITORIAL_POLICY.md).
- [`skill-template/`](skill-template/) — starting point for a new package; its placeholders are intentional and it is not an available skill.
- The seven package directories listed above — available skills and their local evidence.
- [`scripts/`](scripts/) — site generation and deposit tooling. Deposit and publication require operator authorization.
- [`site/`](site/) — generated bilingual hub, published through [GitHub Pages](https://labhdufba.github.io/scholarskills/). The registry drives the skill pages.
- [`tests/`](tests/) — tests for repository-level tooling.
- [`DEPLOYMENT_LOG.md`](DEPLOYMENT_LOG.md) — historical implementation and deposit decisions. Earlier entries describe past states; use the current registry for current status.

## Review and maturity

The [editorial policy](registry/EDITORIAL_POLICY.md) requires methodological grounding, executable instructions, declared dependencies, positive and negative tests, documented limits, ethics and rights review. Its maturity levels are `experimental`, `tested`, `peer-reviewed` and `replicated`. The last two require review or independent replication records; they must not be inferred from green CI.

Submit one skill per pull request, starting from [`skill-template/`](skill-template/), and propose an identifier for the maintainers to assign. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the checklist.

## Licence and rights

The root [`LICENSE`](LICENSE) and the available packages' `LICENSE` files use MIT for the project's original code and associated documentation. [`CITATION.cff`](CITATION.cff) and the catalogue use the same licence. Preserve copyright notices when reusing substantial portions. Third-party fonts, logos, trademarks, images and other external material may have separate terms; their presence in this repository does not grant MIT rights to them. Check each asset's source and permission before reuse.

## Citation

Use [`CITATION.cff`](CITATION.cff) for the catalogue. For a specific skill, cite its package's `CITATION.cff` and the **version DOI** listed in [`registry/registry.json`](registry/registry.json) when one exists, rather than citing the catalogue as a substitute. Zenodo records identify archived versions; `main` may contain later changes.
