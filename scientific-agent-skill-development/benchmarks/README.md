# Benchmarks

Measured behaviour of the validation and packaging scripts, so that cost claims are evidence rather
than impressions.

## Method

- Machine: Linux 6.8, x86_64 (LABHDUFBA Hermes host)
- Python: 3.14.9, PyYAML 6.0.3
- Timing: wall clock of the whole command, 5 repetitions, median reported
- Command: `python3 scripts/validate_skill.py <package> --json`

## Results

| Package | Files scanned | Median wall time |
|---|---|---|
| `scientific-agent-skill-development` | see `tests/RESULTS.md` | fill in when re-measured |
| `examples/descriptive-analysis` | see `tests/RESULTS.md` | fill in when re-measured |

Numbers are recorded after a real measurement. This file deliberately contains no estimate: an
invented benchmark is worse than an empty table.
