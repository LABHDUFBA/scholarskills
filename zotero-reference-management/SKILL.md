---
name: zotero-reference-management
description: Read, search, export and create Zotero references through the Zotero Web API v3, with pagination, collection traversal and BibTeX/CSL export. Use when an agent must query a Zotero library, build a bibliography from a collection, check whether a reference already exists, or add items to a library as part of a research pipeline.
license: MIT
compatibility: Requires Python 3.10+ and network access to api.zotero.org. Credentials come from environment variables (ZOTERO_API_KEY, ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE); no credential is stored in this package.
metadata:
  scholarskills.id: SS-0001
  scholarskills.version: "1.0.0"
  scholarskills.maturity: tested
  scholarskills.method: Zotero Web API v3 (REST) with paginated collection traversal
  scholarskills.spec-version: "agentskills.io specification, accessed 2026-11-24"
---

# Zotero Reference Management

Operates a Zotero library as a data source and a data sink: enumerate, filter, export and write
references without a browser and without storing personal identifiers in the package.

## When to use

- A bibliography must be produced from a Zotero collection for an article, report or thesis.
- A pipeline must check whether a reference is already in the library before adding it.
- A systematic review needs tagged subsets exported for screening or PRISMA counting.
- **Do not use** to scrape a library that is not yours or whose access was not granted: the API key
  defines the boundary of what may be read, and that boundary is not an invitation to widen it.

## Inputs

| Input | Required | Meaning |
|---|---|---|
| `ZOTERO_API_KEY` | yes | Environment variable; never a file in this repository |
| `ZOTERO_LIBRARY_ID` | yes | Numeric library id (not the username) |
| `ZOTERO_LIBRARY_TYPE` | no | `user` (default) or `group` |

## Outputs

- JSON records (one per item) or a rendered bibliography (BibTeX, RIS, CSL JSON).
- A provenance record: library type, library id, number of items, pagination used, timestamp.

## Procedure

1. **Resolve the library.** Call `GET /keys/{key}` when the numeric id is unknown. The response
   carries `userID` and the permission scope; read the scope before attempting a write.
2. **Count before fetching.** `limit` maxes at 100; read `Total-Results` from the response headers
   instead of inferring the total from the length of the returned array.
3. **Paginate with `start`.** The client paginates until an empty page, not for a fixed number of
   iterations.
4. **Exclude attachments when counting references.** Attachments are items; use
   `itemType=-attachment` so that 500 references with 300 PDFs are not reported as 800.
5. **Export.** `format=bibtex|ris|csljson` on the items endpoint. `format=bibtex` ignores `limit` and
   returns the whole set: for large libraries, export per collection.
6. **Write** (only if the key allows it): `POST /users/{id}/items` with a **JSON array**, even for a
   single item.

## Stop criteria

- Stop when `GET /keys/{key}` returns 403: the key is invalid or expired.
- Stop when the scope lacks `write` and the task requires writing; report the missing scope rather
  than attempting a workaround.
- Stop when a group library is required but the key has `groups.all` with write disabled.
- Stop when the record contains personal data the caller is not entitled to export.

## Error handling

| Situation | Response |
|---|---|
| HTTP 403 | Report the scope mismatch; the key defines the limit |
| HTTP 429 | Back off and retry with a smaller page size |
| `Total-Results` absent | Paginate until an empty page; state that the total is unknown |
| 404 on an item file | The attachment is not in Zotero Storage; it exists only locally |
| Creator with `name` instead of first/last | Institutional creator: read `name` |

## Limits

- The Web API serves metadata. It does not deliver PDF blobs that are not synchronised to Zotero
  Storage; a 404 on `/items/{key}/file` is expected there and is **not** a permissions bug.
- `format=bibtex` on the items endpoint ignores pagination.
- Tag filters take one tag per request parameter; multi-tag logic is composed client-side.
- Write access to group libraries depends on a key whose scope grants it and cannot be upgraded
  from the client side.

## Tools and dependencies

- `scripts/zotero_client.py` — resolve, count, paginate, export, create.
- `scripts/zotero_bibliography.py` — CLI to dump a collection to BibTeX or CSL JSON.
- `requests` for HTTP; the standard library otherwise.

## Validation

`tests/` runs against a mock HTTP layer, so the suite is deterministic and offline. It exercises
pagination boundaries, the attachment exclusion rule, a 403 scope failure and a 429 retry.
Results: `tests/RESULTS.md`.

## References

- `references/methodology.md` — why the API is treated as the boundary of access, and how
  bibliographic extraction is documented.
