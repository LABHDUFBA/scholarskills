---
name: dou-federal-gazette
description: Collect publications from the Brazilian official gazette (DOU) and federal covenants from the Portal da Transparência API, using the official open-data routes, with explicit guards against silently-ignored filters. Use when an agent must find what an agency published, extract covenant extracts for an institution, or build a citation-ready record of federal acts for a research project.
license: MIT
compatibility: Requires Python 3.10+ and, for the covenants API, a free key from portaldatransparencia.gov.br in PORTAL_TRANSPARENCIA_KEY. The search page parser needs no credential and no network.
metadata:
  scholarskills.id: SS-0010
  scholarskills.version: "1.0.0"
  scholarskills.maturity: tested
  scholarskills.method: Official open-data routes (Portal da Transparência REST API; DOU structured search) with pagination and filter verification
  scholarskills.spec-version: "agentskills.io specification, accessed 2026-11-24"
---

# DOU and Federal Covenants

Collect what the Brazilian federal government published and what it transferred, using the routes the
state itself publishes for machine access — not a workaround around one.

## When to use

- Find the DOU editions in which a ministry, university or foundation published an act.
- Build a time series of federal covenants (convênios) for one grantee.
- Produce a citable record of federal acts for a research corpus, with edition, section and date.
- Check whether a specific term appeared in the official gazette in a given window.

## When not to use

- Bulk collection of the entire gazette. Use the **open-data base** (monthly XML + ZIP) instead;
  scraping thousands of search pages is slower, fragile and impolite.
- Anything requiring a login, a CAPTCHA or an identity that is not yours. This package raises and
  reports instead of circumventing.
- Personal data mining. The gazette publishes acts of public servants (appointments, salaries);
  collecting those at scale is a data-protection question, not a scraping question. See "Limits".

## The two routes, in order of preference

| # | Route | What it gives | Credential |
|---|---|---|---|
| 1 | Portal da Transparência API (`/api-de-dados/convenios`) | structured covenants, paginated | free key |
| 2 | DOU search page (`/consulta/-/buscar/dou`) | discovered acts, HTML | none |
| 3 | DOU open-data base (monthly XML + ZIP) | the whole gazette, complete | none |

Route 1 is structured and stable — start there. Route 2 is for discovery: it answers "what exists",
not "give me everything". Route 3 is the only honest answer to "collect the whole period".

## How it works

1. **Ask for the narrowest thing.** A grantee name, a date window, a section. A broad query on the
   gazette returns thousands of pages and takes hours; the API answers the same question in seconds.
2. **Read the total before paging.** `parse_total()` reads the announced count, so a client knows
   whether it is looking at 3 results or 3 000.
3. **Page until an empty answer, not until a guessed limit.** `max_pages` is a ceiling, never a
   target. Stopping at the ceiling is a truncation and must be reported, not hidden.
4. **Verify the filter on the first rows.** The API silently ignores unknown parameters: a wrong
   field name returns records for *any* grantee. `verify_first_records()` refuses the batch when the
   first three records do not belong to the requested institution.
5. **Respect the pause.** One request per second by default, and back off on 429 rather than
   accelerate. Politeness is part of correctness on a public service.
6. **Write down what the route gave you.** Every row carries edition, section, date and the canonical
   URL so the record can be re-checked by a human.

## Requirements

| What | Why | How |
|---|---|---|
| `PORTAL_TRANSPARENCIA_KEY` | authorises the covenants API | free signup at portaldatransparencia.gov.br → "API de Dados" → generate key |
| Python 3.10+ | runtime | `python3 --version` |
| `requests` | HTTP client | `pip install -r requirements.txt` |

No credential is required for the search-page parser: it works on a saved HTML file, offline.

## Install

```bash
git clone https://github.com/LABHDUFBA/scholarskills.git
cd scholarskills/dou-federal-gazette
pip install -r requirements.txt
export PORTAL_TRANSPARENCIA_KEY="sua_chave"
```

## Usage

```bash
# covenants for one grantee (use the name as the API spells it, not the acronym)
python3 scripts/dou_collect.py convenios \
  --convenente "UNIVERSIDADE FEDERAL DA BAHIA" --out convenios.csv

# extract publications from a search page you saved in the browser
python3 scripts/dou_collect.py parse --html page.html --out publicacoes.csv --format json
```

## Limits and compliance

- **Legal basis.** The DOU is published by the Imprensa Nacional under the access-to-information law
  (Lei 12.527/2011) and its decree (Decreto 7.724/2012); the Portal da Transparência publishes
  transfers under the same regime. Both offer machine access by design.
- **No circumvention.** The client does not rotate identities, solve challenges or tunnel through
  third-party proxies to defeat a block. When a route is blocked, it raises `DouUnavailable`.
- **Personal data.** Acts naming individuals are public, but building a database of people from them
  is processing personal data under the LGPD. Define purpose and legal basis before collecting; this
  package collects acts about institutions, and does not extract personal identifiers.
- **Rate.** One request per second; ceiling of 40 pages per run by default. Do not raise either
  without a written reason.
- **Not authoritative.** The record proves what the route returned on the day it was queried. For
  legal effect, the gazette's own certified copy prevails.

## What this does not do

- It does not download the monthly ZIP base or parse its XML — that is a separate, larger job.
- It does not resolve a grantee name to a CNPJ; pass the name as the API spells it.
- It does not deduplicate across routes. A covenant may appear both as a structured record and as a
  DOU extract; decide upstream which one is your unit of analysis.

## Evidence

`tests/RESULTS.md` records the environment and the result of the suite that ships here. Validation is
structural: it proves the parser and the pagination logic behave as specified, not that the provider's
layout is unchanged today. Run the suite after any provider change.
