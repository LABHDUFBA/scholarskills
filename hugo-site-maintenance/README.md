# Hugo Site Maintenance

**Digital Methods Skills SS-0012** · version 1.0.0 · maturity `tested` · MIT (original code and documentation)

## Objective

Keep a Hugo site correct while it is being edited: check what exists before creating, check what is
published before believing the clone, and read the deploy log before touching the build.

## Description / how it works

Three rules prevent most damage:

1. **Inspect before creating** — duplicate infrastructure is the most common self-inflicted defect.
2. **The clone is not the site** — compare `last-modified`, checksums and `origin/main` before editing.
3. **Read the run, not the code** — the failing annotation is often a locked account, not a build error.

## Authors

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## Limits

No credential in the package. Structural audit only. A green build does not prove a correct site.
