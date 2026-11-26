# Editorial Policy — Métodos Digitais

## 1. What a submission must contain

A skill is accepted for review only if the package contains all of the following:

1. **Authorship** — named authors with affiliation; ORCID when the author provides one. No ghost
   or gift authorship; contributions are described in `README.md`.
2. **Methodological grounding** — a `references/methodology.md` stating which method the skill
   implements, which literature it follows, and which decisions it encodes. Claims that are
   hypotheses must be labelled as such.
3. **Executable instructions** — a `SKILL.md` following the Agent Skills specification, with
   triggers, inputs, outputs, steps, stop criteria, error handling, limits, tool requirements and
   validation.
4. **Dependencies** — declared versions of packages, models and external services.
5. **Examples** — at least one runnable example, synthetic or public data only.
6. **Tests** — positive, negative and edge cases. Failure modes of tools and invalid inputs must
   be exercised, not merely mentioned.
7. **Limitations** — explicit, including where the method is *not* valid.
8. **Licence** — code and documentation licences stated in the package.
9. **Ethical considerations** — privacy, consent, copyright, dual use, and any restriction the
   method implies.

## 2. Maturity levels

| Level | Granted when |
|---|---|
| `experimental` | Package is complete and the author has run it at least once. No independent evidence. |
| `tested` | Automated tests exist, pass, and the environment and versions are recorded (`tests/RESULTS.md`). |
| `peer-reviewed` | Two named reviewers applied section 1 and recorded their assessment in `reviews/`. |
| `replicated` | A third party, not an author, re-executed the example and published the outcome in `reviews/`. |

**Never** label a skill `peer-reviewed` or `replicated` without the corresponding record present in
the repository. Reviewing the *code* is not the same as validating the *scientific claim*.

## 3. Review criteria

Reviewers assess five dimensions and record a verdict per dimension:

- **Fidelity** — does the implementation match the method described in the literature?
- **Reproducibility** — can a third party obtain the same output from the same input?
- **Failure honesty** — are limits, error conditions and non-applicability documented?
- **Data ethics** — are privacy, consent and copyright addressed for the data the skill touches?
- **Maintainability** — are dependencies pinned and the scope bounded?

## 4. Corrections and withdrawal

Errors found after archiving are corrected by a **new version** with a CHANGELOG entry. Archived
snapshots are never silently replaced. A skill may be marked `deprecated` in `registry.json` with
the reason and the superseding identifier; its DOI remains resolvable.

## 5. What the registry does not do

The Zenodo community aggregates records; it does not itself mint DOIs. Inclusion in the community
does not imply review by Zenodo. Métodos Digitais review is internal to this project and must not be
presented as evaluation by any external body.
