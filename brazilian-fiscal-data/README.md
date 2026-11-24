# Brazilian Fiscal Data (SICONFI)

**Digital Methods Skills SS-0011** · version 1.0.0 · maturity `tested` · MIT (code) / CC BY 4.0 (docs)

## Objective

Retrieve the fiscal accounts that Brazilian states and municipalities declare to the National
Treasury, in a form whose arithmetic a reader can audit.

## Description / how it works

**Principle: identifier, not name; explicit period; a total you can re-check.**

1. Identify the entity by **IBGE code**, never by name.
2. State **period and demonstrative** — a fiscal number without them is an anecdote.
3. Sum from the **declared account tree**, not from a pre-computed column.
4. An **empty delivery is a finding**, not a network failure.
5. Rows without a value are **skipped**, never recorded as zero.

## Authors

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## How to cite

> NASCIMENTO, Leonardo Fernandes; BRASIL, Eric; SODRÉ, Ricardo. **Brazilian Fiscal Data**
> (Digital Methods Skills SS-0011), version 1.0.0, 2026. Digital Humanities Laboratory,
> Federal University of Bahia.

## Limits

Public by design (SICONFI open data, no credential). Declared ≠ executed. Not a ranking: comparing
entities without adjusting for population, revenue base and reporting quality is not analysis.
