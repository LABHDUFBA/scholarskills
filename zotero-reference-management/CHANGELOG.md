# Changelog

## [1.0.0] — 2026-11-24

### Added
- `scripts/zotero_client.py`: library resolution, `Total-Results` counting, pagination to an empty
  page, collection traversal, BibTeX/RIS/CSL export, item creation, provenance record.
- `scripts/zotero_bibliography.py`: CLI export with clean stdout and provenance on stderr.
- Offline test suite with a mock HTTP layer covering pagination boundaries, attachment exclusion,
  a 403 scope failure and a 429 retry.
- Bilingual documentation (EN / pt-BR) with the four required sections: objective, how it works,
  authors, how to cite.

### Known limitations
- Metadata only: PDFs outside Zotero Storage return 404 by design.
- `format=bibtex` on the items endpoint ignores pagination.
- Group write depends on a key scope that cannot be upgraded client-side.
