# Changelog

## [1.0.0] — 2026-11-24

### Added
- `scripts/siconfi_client.py`: keyed queries by IBGE code, payload unwrapping (`items` or bare list),
  normalisation across RREO/RGF/DCA field spellings, prefix aggregation and a coverage report.
- Offline suite of 21 tests: identifier validation, period/type params, empty delivery, 403/500,
  malformed payload, Brazilian decimal notation, gap handling, prefix totals.
- Bilingual documentation with the four required sections and a limits section.

### Known limitations
- Does not implement intra-year interpolation or deflation.
- Does not compare entities; adjustment (population, revenue base) is the researcher's job.
