# Benchmarks

What was measured, and what was not.

## Measured

| Metric | Value | How |
|---|---|---|
| Test suite wall time | ~2.0 s for 20 tests | `python3 -m unittest discover -s tests` |
| Pagination logic cost | negligible vs. network | mock session, no I/O |

## Not measured

- **Latency and throughput against api.zotero.org.** Measuring that requires a credential and a real
  library, and publishing a timing that depends on someone's library size would mislead. When the
  operator runs it against their library, the number goes here with the library size and the date.

An empty benchmark table is honest; an invented one is not.
