---
name: brazilian-fiscal-data
description: "Query Brazilian state and municipal fiscal data from SICONFI (Tesouro Transparente) by IBGE code, normalise accounts across demonstratives, and compute auditable totals by account prefix. Use when an agent must retrieve RREO/RGF/DCA figures for an entity, compare periods, or build a fiscal series that a reader can re-check."
license: MIT
compatibility: "Requires Python 3.10+. No credential and no API key: SICONFI is a public endpoint. Network is needed only for live queries; the test suite runs offline."
metadata:
  scholarskills.id: SS-0011
  scholarskills.version: "1.0.0"
  scholarskills.maturity: tested
  scholarskills.method: SICONFI/ORD REST queries keyed by IBGE code, with hierarchy-preserving aggregation
  scholarskills.spec-version: "agentskills.io specification, accessed 2026-11-24"
---

# Brazilian Fiscal Data (SICONFI)

Retrieve the fiscal accounts that states and municipalities declare to the National Treasury, in a
form whose arithmetic a reader can audit.

## When to use

- Fetch RREO, RGF or DCA figures for one state or municipality.
- Compare two periods of the same entity, or the same period across entities.
- Build a fiscal series for research where each number must be traceable to a declared account.
- Check whether an entity actually delivered a given period.

## When not to use

- Budget execution at the level of a single contract or payment order — that lives in the state's
  own transparency portal, not in SICONFI.
- Anything requiring a login. SICONFI is public; there is no credential to obtain.

## How it works

1. **Identify the entity by IBGE code, never by name.** `29` is Bahia; `2927408` is Salvador. Names
   change with administrations; codes do not.
2. **State the period and the demonstrative.** Every record carries exercise, period and type — a
   fiscal number without them is an anecdote.
3. **Read the item list, not a pre-computed total.** Totals are summed from the declared account tree
   (`total(contas, "1.")`), so the operation is visible and re-checkable.
4. **Treat an empty delivery as a finding.** SICONFI returns an empty list for entities that did not
   file. That is information about the entity, not a network failure — the two are never conflated.
5. **Skip rows without a value.** A fabricated zero in a fiscal table is worse than a documented gap.

## Requirements

| What | Why |
|---|---|
| Python 3.10+ | runtime |
| `requests` | HTTP client, only for live queries |
| IBGE code of the entity | the query key |

No credential. SICONFI is a public service; do not send keys to it.

## Install

```bash
git clone https://github.com/LABHDUFBA/scholarskills.git
cd scholarskills/brazilian-fiscal-data
pip install -r requirements.txt
```

## Usage

```python
from siconfi_client import Query, SiconfiClient, parse_contas, total
import requests

cli = SiconfiClient(requests.Session())
items = cli.fetch(Query(id_ente="29", exercicio=2024, periodo=3, demonstrativo="RREO"))
contas = parse_contas(items)
print(total(contas, "1."))      # subtree of revenue accounts
```

## Limits and compliance

- **Public by design.** SICONFI is published by the National Treasury as open data. No circumvention,
  no credential, no scraping of HTML.
- **Declared ≠ executed.** These are the figures the entity declared; auditing them is a different
  operation. Do not present a declared total as a payment.
- **Not a ranking.** Comparing entities without adjusting for population, revenue base and reporting
  quality produces a league table, not an analysis.
- **Period coverage varies.** Older exercises and smaller municipalities may have gaps; report them.

## Evidence

`tests/RESULTS.md` records the environment and result of the suite shipped here. Validation is
structural: it proves normalisation and aggregation logic, not the accuracy of any declared figure.
