# DOU and Federal Covenants

**Digital Methods Skills SS-0010** · version 1.0.0 · maturity `tested` · MIT (code) / CC BY 4.0 (docs)

## Objective

Collect what the Brazilian federal government published in the official gazette (DOU) and what it
transferred through covenants, using the routes the state publishes for machine access — not a
workaround around them.

## Description / how it works

**Principle: official route first, and the filter must be verified.**

1. **Ask for the narrowest thing.** A grantee, a date window, a section. A broad gazette query returns
   thousands of pages; the API answers the same question in seconds.
2. **Read the total before paging**, so the client knows whether it faces 3 results or 3 000.
3. **Page until an empty answer**, not until a guessed limit. `max_pages` is a ceiling, never a
   target: stopping at the ceiling is truncation and must be reported.
4. **Verify the filter on the first rows.** The API silently ignores unknown parameters, so a wrong
   field name returns records for *any* grantee. `verify_first_records()` refuses the batch.
5. **Respect the pause.** One request per second by default, and back off on 429.
6. **Write down what the route gave you**: edition, section, date and canonical URL per row.

## Authors

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## How to cite

Until a DOI exists, cite by the package identifier:

> NASCIMENTO, Leonardo Fernandes; BRASIL, Eric; SODRÉ, Ricardo. **DOU and Federal Covenants**
> (Digital Methods Skills SS-0010), version 1.0.0, 2026. Digital Humanities Laboratory,
> Federal University of Bahia. https://github.com/LABHDUFBA/scholarskills/tree/main/dou-federal-gazette

## Limits

Legal basis: Lei 12.527/2011 (access to information) and Decreto 7.724/2012 for the DOU. No
circumvention, no identity rotation, no third-party proxy. Public acts naming individuals are still
personal data under the LGPD: define purpose and legal basis before building people-level datasets.
