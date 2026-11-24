# Test results — SS-0001 (zotero-reference-management)

Recorded from a real execution.

## Environment

```
Python 3.14.9
requests 2.34.2
date: 2026-11-24T09:41:01
network: not used by the test suite (mock HTTP layer)
```

## Command

```bash
python3 -m unittest discover -s tests -v
```

## Result

```
----------------------------------------------------------------------
Ran 20 tests in 2.028s

OK
```

## Coverage of the protocol requirement

| Case type | Tests |
|---|---|
| Positive | 3-page traversal, exact-multiple traversal, header counting, BibTeX export |
| Negative | invalid library type, unknown export format, empty item list, empty credentials |
| Edge | page size above the 100 limit, absent `Total-Results` header, empty-page stop |
| Tool failure | HTTP 403 → `ScopeError`; HTTP 429 → retry then success; other 4xx → `ZoteroError` |
| Privacy | provenance record contains library id but never the API key |

## What is not covered

- No live API call: the suite proves the client's logic, not that a specific key works. A key test
  must be run by the operator with their own credential.
- No test of group libraries beyond the `library_type` path, because that requires a group credential.
