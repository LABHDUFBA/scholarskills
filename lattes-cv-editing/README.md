# Lattes CV Editing

**Digital Methods Skills SS-0013** · version 1.0.0 · maturity `tested` · MIT (original code and documentation)

## Objective

Prepare the item correctly **before** the form is opened. The Lattes editor has no API and no
transaction log: a wrong year or a duplicated entry is caught by nothing and becomes part of a public
academic record that others cite.

## Description / how it works

Five-step protocol: authorisation and scope → metadata from a primary source → check the item and
fill one per call → explicit approval gate → submission as a separate authorisation.

Hard cases: preprint ≠ published article, conference paper ≠ journal article, chapter ≠ book.
A confirmed duplicate is edited, not re-created. A sensitive field is asked, never inferred.

## Authors

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## Limits

No scraping of third-party CVs. No automated submission. No invention: a field without a primary
source stays empty. No credential is stored.
