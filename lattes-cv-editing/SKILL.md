---
name: lattes-cv-editing
description: "Prepare, check and record items before typing them into a Lattes CV: required fields per record type, duplicate detection by normalised title and year, the rule that preprint and published article are separate records, and a plain summary for the holder to approve. Use when adding or correcting productions, projects, supervisions or committees in a Lattes curriculum."
license: MIT
compatibility: "Requires Python 3.10+ for the checker and a browser session under the CV holder's own login for the editor. No credential is stored in this package: the holder authenticates, and the skill never receives the password."
metadata:
  scholarskills.id: SS-0013
  scholarskills.version: "1.0.0"
  scholarskills.maturity: tested
  scholarskills.method: "Primary-source metadata validation, duplicate detection by normalised title plus year, and a written approval gate before submission"
  scholarskills.spec-version: "agentskills.io specification, accessed 2026-11-24"
---

# Lattes CV Editing

Prepare the item correctly *before* the form is opened. The editor has no API and no transaction log:
a wrong year or a duplicated entry is not caught by anything and becomes part of a public academic
record that other people cite.

## When to use

- Add, correct or complete an item in the CV of the person who owns the profile.
- Check for duplicates before creating a new record.
- Decide whether two similar entries are one record or two.

## When not to use

- Collecting other people's CVs — that is a different operation with different ethics.
- Storing an article, a press clipping or a bibliography that is not the holder's own production.
- Describing an institution or a work by generated text: only what the primary source or the holder
  provides goes in.

## The five-step protocol

**1. Authorisation and scope.** Permission to edit is not permission to submit. Submission publishes
a new version and requires accepting a legal declaration — ask for that separately, in writing, and
never press Send on the strength of a general "go ahead".

**2. Metadata from a primary source.** Confirm DOI/Crossref, the journal or publisher page, the
catalogue record or the official PDF *before* opening the form. A search result, someone else's
summary or an approximate match proves nothing. Persist the verified data locally first: the session
expires and takes the research with it.

**3. Check the item, then fill one per call.** Run `validate` and `find_duplicates` first; the
editor loses unsaved modals between browser calls, so one item per call, with read-back in the same
movement.

**4. Approval gate.** Present type, section, every field, the source used for validation and a
screenshot. Wait for explicit approval. Do not proceed on silence.

**5. Submission is a separate authorisation.** See step 1.

## Rules that decide the hard cases

| Situation | Rule |
|---|---|
| Preprint and the published article | **Two records.** Never merge. |
| Conference paper and journal article | **Two records.** Same work, two vehicles. |
| Book chapter and book | **Two records.** |
| Confirmed duplicate | **Edit the existing one**, keeping the more complete version as the base; it holds links, students and counts. |
| Similar but different title | **Not a duplicate.** "Sociologia digital" and "Sociologia digital: um balanço" are different works. |
| Sensitive field (race/colour, disability) | **Ask the holder.** Never infer. |
| Author name format | Use the holder's preferred form; if a validator demands a linked variant, show the conflict and return the decision — do not switch silently. |

## Usage

```python
from lattes_item import Item, validate, find_duplicates, summary

item = Item("artigo_periodico", {
    "titulo": "Sociologia digital e métodos computacionais",
    "ano": "2026",
    "periodico": "Revista Brasileira de Sociologia",
    "autores": "Nascimento, Leonardo Fernandes",
    "doi": "10.1590/12345",
    "palavras_chave": ["sociologia digital", "metodos", "plataformas"],
})
print(summary(item))            # what will be typed, plus pending issues
print(validate(item))           # [] means ready
print(find_duplicates(item, existing_items))
```

## Requirements

| What | Why |
|---|---|
| Python 3.10+ | the checker |
| Access to the CV holder's own profile | the editor requires the holder's login |
| The primary source of the item | DOI, publisher page, catalogue record or PDF |

No credential is stored. The holder authenticates; the package never receives the password, and no
password should ever be typed into a chat, a file or a commit.

## Limits and compliance

- **No scraping of third-party CVs.** This skill operates the holder's own record only.
- **No automated submission.** Submission is a legal act by the holder.
- **No invention.** A field without a primary source stays empty; an empty field is honest, a guessed
  one is not.
- **Personal data.** The CV is public and personal at the same time: publish only what the holder
  approved, field by field.
- The checker validates structure and consistency, not truth. It cannot tell whether an article was
  actually published in that journal.

## Evidence

`tests/RESULTS.md` records the 33 offline tests shipped here: validation per type, keyword rules,
duplicate detection, distinct-record rules and the approval summary.
