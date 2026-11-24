# Test results — SS-0010 (dou-federal-gazette)

Recorded from a real execution.

## Environment

```
Python 3.14.9
network: not used by the test suite (recorded fixtures + stub HTTP layer)
date: 2026-11-24T14:32:41
```

## Command

```bash
python3 -m unittest discover -s tests -v
```

## Result

```
Ran 20 tests in 0.003s

OK
```

## Coverage

| Case type | Tests |
|---|---|
| Positive | two-publication parse, announced total, single-page covenants, pagination to an empty page |
| Negative | blank page, unknown layout, non-list payload, empty grantee, wrong grantee detected |
| Edge | results page announcing zero, HTML entities, page ceiling respected, acronym vs full name |
| Tool failure | 403 → `DouPermissionError`, 429 → `RateLimited`, 503 → `DouUnavailable` |
| Privacy | the API key travels in the `chave-api-dados` header and never in the query string |

## What is not covered

- No live call to `api.portaldatransparencia.gov.br`: the suite proves the client's logic, not that a
  given key works or that the provider's field names are still the documented ones.
- No live DOU search: the parser is exercised against a recorded fragment of the documented layout.
  If the Imprensa Nacional changes the markup, `parse_search_results` raises `DouUnavailable` instead
  of returning an empty list — that is the signal to re-record the fixture.
- The monthly open-data ZIP base is out of scope for this version.
