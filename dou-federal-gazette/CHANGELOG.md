# Changelog

## [1.0.0] — 2026-11-24

### Added
- `scripts/dou_client.py`: DOU search-page parser (section, organ, edition, date, canonical URL),
  announced-total reader, and a covenants client with pagination to an empty answer, a page ceiling,
  and `verify_first_records()` as a guard against silently ignored filters.
- `scripts/dou_collect.py`: CLI for covenants (CSV/JSON) and for parsing a saved search page offline.
- Offline suite of 20 tests covering parsing, empty results, unknown layouts, pagination boundaries,
  401/403/429/503 handling, key placement (header, never query string) and filter verification.
- Bilingual documentation with the four required sections and an explicit compliance section
  (legal basis, no circumvention, personal data under the LGPD, rate limits).

### Known limitations
- Does not download or parse the monthly open-data ZIP base.
- Does not resolve institution names to CNPJ: pass the name as the API spells it.
- Does not deduplicate across routes.
