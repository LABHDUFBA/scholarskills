# Zotero Reference Management

**ScholarSkills SS-0001** · version 1.0.0 · maturity `tested` · MIT (code) / CC BY 4.0 (documentation)

## Objetivo / Objective

Turn a Zotero library into a **reliable, citable data source for research pipelines**: enumerate,
filter, export and write references through the Web API v3, without a browser, without scraping, and
without storing personal identifiers in the skill package.

The target reader is an agent (or a researcher automating a pipeline) that needs to answer questions
such as: *does this reference already exist in my library?*, *what is in this collection and how many
items are really there?*, *give me a BibTeX file that I can trust*.

## Descrição / How it works

**Principle: the API key is the boundary of access.** The skill never widens what the key allows. If
the scope is read-only, the skill reads and reports that writing is unavailable instead of finding a
workaround.

Flow:

1. **Resolve** — `GET /keys/{key}` returns the numeric `userID` and the permission scope. The user id
   is numeric; the username is not a valid path parameter.
2. **Count** — `Total-Results` is an HTTP header, not a field in the JSON body. The client reads the
   header, because counting from a returned array is how libraries get silently truncated.
3. **Paginate** — `limit` maxes at 100. The client advances `start` and stops on an empty page.
4. **Filter** — `itemType=-attachment` excludes PDFs, notes and snapshots, so a reference count is a
   count of references.
5. **Export** — `format=bibtex|ris|csljson`. BibTeX on the items endpoint ignores `limit`, so large
   libraries are exported per collection.
6. **Write** — `POST /users/{id}/items` with a JSON **array**, even for one item.

### What it does not do

- Does not download PDFs that are not in Zotero Storage (the API returns 404 there, by design).
- Does not bypass the API key scope, and does not accept a key pasted in a chat: it reads
  environment variables.
- Does not decide what a bibliography *should* contain. Selection is a methodological decision, and
  it is documented in `references/methodology.md`, not hard-coded.

## Autores / Authors

| Author | Affiliation | Contribution |
|---|---|---|
| Leonardo Fernandes Nascimento | Digital Humanities Laboratory (LABHDUFBA), Federal University of Bahia | Conception, implementation, tests |
| Eric Brasil | University of International Integration of Afro-Brazilian Lusophony (UNILAB) | Methodological review |
| Ricardo Sodré | Federal University of Bahia | Review of bibliographic criteria |

ORCIDs are included only when each author supplies them; none is invented here.

## Como citar / How to cite

Until the first authorised deposit, cite the repository:

> Nascimento, L. F.; Brasil, E.; Sodré, R. (2026). *Zotero Reference Management* (ScholarSkills
> SS-0001, version 1.0.0) [Software]. Digital Humanities Laboratory, Federal University of Bahia.
> https://github.com/LABHDUFBA/scholarskills/tree/main/zotero-reference-management

`CITATION.cff` carries the same information in machine-readable form. After the deposit, the version
DOI and the concept DOI are added here and in `CITATION.cff` — separately, because they are different
identifiers: the concept DOI resolves to the latest version, the version DOI pins this snapshot.

## Installation

```bash
git clone https://github.com/LABHDUFBA/scholarskills.git
cd zotero-reference-management
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export ZOTERO_API_KEY="..."        # never commit it
export ZOTERO_LIBRARY_ID="123456"
```

## Minimal example

```bash
python3 scripts/zotero_bibliography.py --collection ABC123 --format bibtex --out refs.bib
python3 scripts/zotero_bibliography.py --query "foucault" --format csljson
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The suite uses a mock HTTP layer: it runs offline and deterministically. Recorded results and
environment: `tests/RESULTS.md`.

## Limits

- Metadata only; no PDF extraction.
- BibTeX export ignores pagination on the items endpoint.
- Group write requires a key whose scope grants it.
- Counts are references (`-attachment`), not files.
