# Methodological grounding

## 1. Method

Bibliographic data extraction through the Zotero **Web API v3**, the documented REST interface of the
reference manager. The skill wraps three operations that a research pipeline actually needs:
counting a set, traversing it completely, and rendering it in a citation format.

Reference: Zotero Developers, *Web API v3 documentation* (https://www.zotero.org/support/dev/web_api/v3/),
accessed 2026-11-24.

## 2. Operationalisation

| Concept | Operation | Decision | Alternative rejected | Reason |
|---|---|---|---|---|
| "the library" | `/{type}s/{id}/items` | numeric id from `/keys/{key}` | username in the path | username is not a valid path parameter; using it fails confusingly |
| "how many references" | `Total-Results` header with `itemType=-attachment` | header | length of the returned page | page length maxes at 100 and silently truncates any count |
| "everything in the collection" | `start` pagination until an empty page | empty page | fixed iteration count | a fixed count breaks when items are added mid-traversal |
| "a bibliography" | `format=bibtex\|ris\|csljson` | per collection | whole library in one call | BibTeX export ignores `limit`; whole-library export is unbounded |
| "access" | the API key scope | report and stop | attempt a workaround | the scope is the boundary; bypassing it is not a technical choice but a consent violation |

## 3. Epistemic status

- **Established**: the records the API returns, with the scope of the key used.
- **Interpretation**: what those records mean for a bibliography is a selection decision.
- **Hypothesis**: nothing about the completeness of someone's library is claimed.
- **Normative**: the skill refuses to bypass scope limits — that refusal is a position, and it is
  stated rather than hidden.

## 4. Assumptions and validity domain

- The library is the key holder's, or access was granted. Valid domain: personal library, or group
  library with a key whose scope covers it.
- Counts exclude attachments. A "500 references" figure is not a file count.
- Validity ends where the API ends: PDFs outside Zotero Storage are not available, and no amount of
  retrying changes that.

## 5. Known alternatives

Browser automation (Selenium) can scrape the web interface, and the desktop local API (port 23119)
offers richer file access. Both were rejected here: the first violates the platform's terms for
automated access and is fragile; the second requires the desktop application running on the same
machine, which defeats the purpose of a portable skill. The Web API is the only interface that is
simultaneously documented, authorised and remote.

## 6. Bibliography

- Zotero. *Web API v3*. https://www.zotero.org/support/dev/web_api/v3/ (accessed 2026-11-24).
- Zotero. *API keys and permissions*. https://www.zotero.org/settings/keys (accessed 2026-11-24).
