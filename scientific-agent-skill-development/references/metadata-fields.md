# Metadata fields — registry and deposit

Two different schemas, easily confused. Keep them distinct.

## Registry entry (`registry/registry.json`)

| Field | Type | Rule |
|---|---|---|
| `id` | `SS-NNNN` | Assigned on acceptance, not on submission |
| `slug` | string | Equals `SKILL.md` `name` and the directory name |
| `title` | string | Human-readable |
| `summary` | string or null | One sentence, no marketing |
| `version` | semver or null | `M.m.p`; null while `planned` |
| `status` | enum | `planned` · `available` · `deprecated` |
| `maturity` | enum | `experimental` · `tested` · `peer-reviewed` · `replicated` |
| `repository` | URL or null | The skill's own repository |
| `doi_version` | DOI or null | Identifier of one archived snapshot |
| `doi_concept` | DOI or null | Identifier of the always-latest record |
| `license` | string or null | Code and documentation stated separately when they differ |
| `authors` | array | `name` required; `affiliation`, `orcid`, `github` optional |
| `keywords` | array of strings | Indexing terms |
| `skill_spec_version` | string or null | Which specification version was validated against |
| `compatibility` | string or null | Mirrors the frontmatter field |
| `evidence` | path/URL or null | Artefact justifying the maturity level |
| `deprecated_reason` | string or null | Required when `status = deprecated` |
| `superseded_by` | `SS-NNNN` or null | Successor identifier |
| `added` | `YYYY-MM-DD` or null | Date of acceptance |

### Concept DOI versus version DOI

Zenodo mints both. The **concept DOI** always resolves to the latest version and is the one to cite
for "this skill" in general. The **version DOI** pins the exact snapshot a paper used. A registry
entry with `doi_version` and no `doi_concept` is a sign that the distinction was missed.

## Deposit metadata (`.zenodo.json` / `zenodo-metadata.json`)

| Field | Note |
|---|---|
| `title` | Version-independent title |
| `description` | HTML allowed; state what it does and its limits |
| `upload_type` | `software` for skills |
| `license` | SPDX-ish identifier accepted by Zenodo (`mit`, `apache-2.0`, `cc-by-4.0`) |
| `version` | Must match `CITATION.cff` and the registry |
| `creators` | `Family, Given`; affiliation as the institution requires |
| `keywords` | Same vocabulary as the registry |
| `related_identifiers` | e.g. `isSupplementedBy`, `isVersionOf` |

## Placeholders

Unknown values are `null` in the registry and *absent* from the deposit payload. Never the strings "TBD" or "pending", never `0`, never a reserved-but-unpublished DOI
presented as published. The validator looks for the TODO marker and fails on it.
