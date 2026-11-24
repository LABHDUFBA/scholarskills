# Test results — SS-0011 (brazilian-fiscal-data)

Recorded from a real execution.

## Environment

```
Python 3.14.9
network: not used by the test suite (recorded payloads + stub HTTP layer)
date: 2026-11-24T14:33:21
```

## Command

```bash
python3 -m unittest discover -s tests -v
```

## Result

```
Ran 21 tests in 0.001s

OK
```

## Coverage

| Case type | Tests |
|---|---|
| Positive | items unwrapping, bare-list payload, Brazilian and plain numbers, prefix totals |
| Negative | name instead of IBGE code, wrong code length, unknown demonstrative, absurd year |
| Edge | empty delivery treated as a finding, row without value skipped, empty prefix rejected |
| Tool failure | 403 → `SiconfiAuth`, 500 → `SiconfiUnavailable`, malformed payload → `SiconfiUnavailable` |
| Traceability | `coverage()` reports accounts and columns; `total()` only sums an explicit prefix |

## What is not covered

- No live call: the suite proves the client, not that a given exercise/period exists for an entity.
- No deflation, interpolation or cross-entity adjustment — out of scope by design.
