# Changelog

## [1.0.0] — 2026-11-24

### Added
- Initial public-ready version of the protocol: scoping, methodological grounding, package
  generation, test design, environment recording, ethics audit, structural validation and deposit
  preparation.
- `scripts/validate_skill.py` — Agent Skills frontmatter validation, required-file checks,
  placeholder and credential detection, local link integrity, CITATION/.zenodo consistency.
- `scripts/build_package.py` — scaffolds the canonical layout and refuses invalid slugs.
- `scripts/generate_metadata.py` — ZIP + SHA-256 + deposit metadata + human authorisation checklist;
  performs no network calls.
- `scripts/run_checks.py` — aggregates validation, registry consistency and test presence into JSON.
- Reference example: `examples/descriptive-analysis/`.
- Unit tests covering positive, negative, edge and tool-failure behaviour.

### Known limitations
- Structural validation only; the scientific claim is not checked.
- Secret patterns are intentionally narrow and can miss obfuscated material.
- No verification that cited DOIs resolve (no network access by design).
