# Changelog

## [1.0.0] — 2026-11-24

### Added
- `scripts/lattes_item.py`: required fields per record type, year and DOI sanity checks, keyword rules
  (3–5, lowercase, no final period), keyword suggestion from the item's own text, duplicate detection
  by normalised title and year, and the distinct-record rules for preprint/anais/capítulo.
- Offline suite of 33 tests.
- Bilingual documentation with the four required sections and the hard-case table.

### Known limitations
- Does not automate the browser: login, navigation and submission stay with the holder.
- Validates structure and consistency, not truth.
