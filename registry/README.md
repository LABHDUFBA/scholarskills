# ScholarSkills Registry

The registry is the **catalogue** of the project. It does not host skill code: each skill lives in
its own repository, with its own releases and DOIs. The registry records what exists, at which
maturity level, and how to cite it.

## Files

| File | Purpose |
|---|---|
| `registry.json` | Machine-readable catalogue (one entry per skill) |
| `metadata-schema.json` | JSON Schema that every entry must validate against |
| `EDITORIAL_POLICY.md` | What a skill must contain to be accepted, per maturity level |
| `../CONTRIBUTING.md` | How to submit |
| `../CODE_OF_CONDUCT.md` | Expected conduct in reviews and issues |

## Rules

1. **One entry per skill.** Identifier `SS-NNNN` is assigned on acceptance, not on submission.
2. **Unknown is `null`, never invented.** A missing DOI is `null`; it is not a placeholder string.
3. **Concept DOI ≠ version DOI.** `doi_concept` identifies the always-latest record;
   `doi_version` identifies one archived snapshot. They are different fields for a reason.
4. **`planned` entries carry no DOI and no URL.** They document the roadmap and must never look
   like available artefacts.
5. **Maturity is evidence-bound.** See `EDITORIAL_POLICY.md`. Promotion requires a linked artefact.
