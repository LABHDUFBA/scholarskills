# Test results — SS-0013 (lattes-cv-editing)

Recorded from a real execution.

## Environment

```
Python 3.14.9
network: not used
date: 2026-11-24T15:32:53
```

## Command

```bash
python3 -m unittest discover -s tests -v
```

## Result

```
Ran 33 tests in 0.002s

OK
```

## Coverage

| Case type | Tests |
|---|---|
| Positive | complete item valid, DOI in pattern accepted, authors with separators accepted, correct keywords accepted |
| Negative | unknown type, missing title/periodico, invalid year, future year, invalid DOI, authors not a list, wrong keyword count |
| Edge | accent/case difference still duplicate, different year not duplicate, similar-but-longer title not duplicate, empty text yields no keywords |
| Semantics | preprint vs article, anais vs periodico, chapter vs book are reported as distinct records |
| Approval | summary says ready or counts pending issues; lists are joined for reading |

## What is not covered

- No browser automation: login, navigation and submission stay with the CV holder.
- The checker validates structure and consistency, not whether a claim is true.
