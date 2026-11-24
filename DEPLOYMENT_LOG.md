# DEPLOYMENT_LOG

Persistent record of the ScholarSkills implementation. Every entry states what was done, with what
evidence, and what remains blocked. No entry claims a step that was only planned.

---

## Entry 001 — 2026-11-24 — Environment inspection

**Status:** done

| Item | Value |
|---|---|
| Host | `labhd-hermes`, Linux 6.8, Ubuntu |
| Python | 3.14.9 (Hermes venv) |
| PyYAML | 6.0.3 |
| git | 2.43.0 |
| gh CLI | 2.97.0, authenticated as `leofn` |
| Working copy | `/home/hermes/projects/scholarskills` |

**Findings**

- `GH_TOKEN` / `ZENODO_TOKEN` are **not** in the environment. GitHub authentication exists only
  through the `gh` CLI session (`~/.config/gh/hosts.yml`). Zenodo has **no credential available**
  in this environment — sandbox deposits are therefore blocked until the operator provides one.
- GitHub Actions for the `leofn` account are reported blocked by a billing issue (previous session
  note). The workflow file is written and valid, but **CI cannot be assumed to run**. This is
  recorded as a limitation, not worked around.

---

## Entry 002 — 2026-11-24 — Official documentation consulted

**Status:** done

| Source | What was extracted |
|---|---|
| `https://agentskills.io/specification` | Required frontmatter (`name`, `description`), constraints (name 1–64 chars, `[a-z0-9-]`, no edge/double hyphen, must equal directory name; description 1–1024), optional fields (`license`, `compatibility` ≤500, `metadata` string→string, `allowed-tools`), directory conventions, progressive disclosure, relative paths |
| `https://developers.zenodo.org/` | REST API for deposits and records; communities API in testing; publication happens through deposit actions |
| `https://citation-file-format.github.io/` | CFF 1.2.0 structure and example |
| `https://zenodo.org/api/communities/scholarskills` | HTTP 404 — no community with that identifier exists (checked 2026-11-24) |
| `https://sandbox.zenodo.org/api/records` | HTTP 200 — sandbox reachable |

**Availability checks**

- GitHub user/org `scholarskills`: HTTP 404 — the name is free at the time of writing.
- Existing orgs of `leofn`: `dadoscope`, `learning-crawlers`, `LABHDUFBA`, `DadosGovPE`,
  `LABHDUFRJ`, `colmeiabrasil`.

---

## Entry 003 — 2026-11-24 — Local repository produced

**Status:** done

Created at `/home/hermes/projects/scholarskills`:

```
README.md  LICENSE  CITATION.cff  CONTRIBUTING.md  CODE_OF_CONDUCT.md  DEPLOYMENT_LOG.md
registry/     README.md  EDITORIAL_POLICY.md  metadata-schema.json  registry.json
skill-template/
scientific-agent-skill-development/   (SS-0000)
.github/workflows/validate.yml
```

**Evidence:** `scientific-agent-skill-development/tests/RESULTS.md` (generated from real runs).

---

## Entry 004 — 2026-11-24 — SS-0000 implemented and tested

**Status:** done

| Check | Result |
|---|---|
| `validate_skill.py` on the package | PASS, 0 warnings |
| `validate_skill.py` on the reference example | PASS, 0 warnings |
| Protocol test suite | 21 tests, OK |
| Reference example suite | 8 tests, OK |
| `run_checks.py` structural report | OK (see `tests/RESULTS.md`) |

**Implemented scripts:** `validate_skill.py`, `build_package.py`, `generate_metadata.py`,
`run_checks.py`.

**Defect found and fixed during testing (recorded because it documents the value of the tests):**
`descriptive-analysis` had a test asserting a warning for a single-value column that never fired,
because the fixture gave the column three values. The test was wrong, not the code; both the
fixture and the assertion were corrected.

**Second fix:** the validator's placeholder rule matched the literal marker inside its own
documentation and inside the builder's substitution table. Rule narrowed (markers must be followed
by `:` or be the SS/SKILL forms) and the builder now composes the marker at runtime.

---

## Entry 005 — 2026-11-24 — Authorship and collaboration

**Status:** partially blocked

| Person | GitHub account | Status |
|---|---|---|
| Leonardo Fernandes Nascimento | `leofn` | confirmed by session |
| Eric Brasil | `ericbrasiln` | **confirmed** — profile states UNILAB professor and LABHDUFBA researcher |
| Ricardo Sodré | — | **not identified** — no GitHub account found with sufficient confidence; awaiting the operator |

The near-match `RiqSodre` was **rejected** as evidence: the profile describes a student in Sorocaba,
which conflicts with the expected co-author. Adding the wrong account to a repository is worse than
leaving the field empty.

---

## Entry 006 — 2026-11-24 — Decisions awaiting human authorisation

**Status:** blocked by design (the protocol forbids autonomy here)

| # | Decision | Why it cannot be automated |
|---|---|---|
| 1 | Create the public GitHub organisation/repository | Public resource; institutional identity |
| 2 | Add external collaborators | External side effect on third parties |
| 3 | Final licence (MIT for code, CC BY 4.0 for docs) | Institutional rights review |
| 4 | ORCIDs and affiliation wording | Identity claims must be confirmed by the person |
| 5 | Zenodo community creation | No API for creating communities; UI action by the operator |
| 6 | Sandbox deposit | No `ZENODO_SANDBOX_TOKEN` in this environment |
| 7 | Production deposit and DOI | Irreversible; requires authorship and rights clearance |

---

---

## Entry 007 — 2026-11-24 — Repository created (private) and CI verified

**Status:** done

| Item | Value |
|---|---|
| Repository | `https://github.com/LABHDUFBA/scholarskills` |
| Visibility | **private** — public requires operator authorisation |
| Default branch | `main` |
| Commit | `dbd5369` |
| CI run | https://github.com/LABHDUFBA/scholarskills/actions/runs/45357118018 — **success** |
| Jobs | `validate (3.10)` ✓ 16 s · `validate (3.12)` ✓ 10 s |

**Collaborators**

| Account | Permission | State |
|---|---|---|
| `leofn` | admin | active |
| `ericbrasiln` | write | invitation pending acceptance |
| Ricardo Sodré | — | not invited: GitHub account not identified |

**Note on Actions availability:** the previously recorded billing block on `leofn` did **not** affect
this repository. The workflow ran and passed on two Python versions, so CI is real evidence here,
not a claim.

**Decision recorded:** the repository was created **private**. The mission requires human
authorisation before creating public resources, and the final home (personal account vs. a
`ScholarSkills` organisation vs. `LABHDUFBA`) is an institutional decision that has not been taken.
Making it private keeps the work reversible and avoids publishing under a name that may change.

---

## Entry 008 — 2026-11-24 — Deposit artefacts prepared (not uploaded)

**Status:** done locally, blocked at the upload boundary

```
zip       scientific-agent-skill-development-1.0.0.zip   42 122 bytes
sha256    84957b5b5966b4de1a4a3caa557d96355ac7846f4fe8d042bc96a97fcc1c73c8
metadata  zenodo-metadata.json      (upload_type: software, no DOI field)
checklist AUTHORISATION-CHECKLIST.md
```

Generated by `scripts/generate_metadata.py`, which performs **no network calls**. Nothing was
created, reserved or published on Zenodo. The ZIP is deliberately excluded from version control
(`.gitignore`) because deposit artefacts are regenerated, not committed.

**Blocked:** the sandbox deposit requires `ZENODO_SANDBOX_TOKEN`, which is absent from this
environment. The production deposit additionally requires authorship and rights clearance.

---

## Entry 009 — 2026-11-24 — Repository moved to the LABHDUFBA organisation

**Status:** done

| Item | Before | After |
|---|---|---|
| Owner | `leofn` | **`LABHDUFBA`** |
| URL | https://github.com/leofn/scholarskills | **https://github.com/LABHDUFBA/scholarskills** |
| Visibility | private | private (unchanged) |

All URLs inside the repository (`CITATION.cff`, `registry.json`, README, this log) were rewritten and
the local remote updated. The old URL redirects, so no external reference breaks.

**Collaborators:** `leofn` (admin), `rsandrade` (admin), `ericbrasiln` (admin).

**Identification of the coauthor:** the operator indicated that the third author is already an
administrator of the organisation. Listing `orgs/LABHDUFBA/members?role=admin` returns three
accounts — `ericbrasiln`, `leofn`, `rsandrade` — and `rsandrade` is the only remaining candidate. It
was granted admin on the repository. **Caveat recorded:** the public profile of `rsandrade` reads
"Ricardo Andrade", not "Sodré"; the operator asserted the identity, and the profile is not treated as
evidence either way. If the account is wrong, the invitation can be revoked without data loss.

---

## Entry 010 — 2026-11-24 — SS-0001 implemented: Zotero Reference Management

**Status:** done

| Item | Value |
|---|---|
| Repository | https://github.com/LABHDUFBA/zotero-reference-management (private) |
| Identifier | SS-0001, reassigned from the roadmap; previous items shifted to SS-0002…SS-0009 |
| Tests | 20 unittest cases, offline (mock HTTP layer) — OK |
| Structural validation | PASS, 0 warnings |
| CI | `.github/workflows/validate.yml`, Python 3.10 and 3.12 |

**Design decision recorded:** the API key is treated as the boundary of access. A 403 is reported as
a scope limit, never worked around. This is a normative choice and it is stated in
`references/methodology.md`, not hidden in code.

**Numbering change:** SS-0001 was `systematic-literature-review` in the first roadmap. It is now the
Zotero skill, because a skill already implemented, tested and in daily use is a better first deposit
than a planned one. The roadmap was renumbered (SS-0002…SS-0009) and `registry.json` carries a
`renumbering_note`.

---

## Entry 011 — 2026-11-24 — Hub site generated from the registry

**Status:** done locally; hosting blocked

`scripts/build_site.py` generates a static hub into `site/`:

```
site/index.html                 hero, live stats, search + filters, skill grid, maturity table
site/skills/<slug>.html         objective / how it works / authors / how to cite / install / validation
site/api/registry.json          the catalogue as JSON, for other hubs and integrations
site/assets/style.css|app.js    no framework, no tracking, no cookies
```

Verified in a real browser: 10 cards, filters working, no horizontal overflow, two-column detail page
with factsheet at 1425 px and single column below 880 px. `python3 scripts/build_site.py --check`
guards against a stale site in CI.

**Blocked:** GitHub Pages is not available for a **private** repository on the free plan. Publishing
the hub therefore requires one of: (a) making `LABHDUFBA/scholarskills` public, (b) creating a public
repository that hosts only `site/`, or (c) serving the generated static files from another host. All
three are operator decisions, since all three make the content public.

---

## Entry 012 — 2026-11-24 — Zenodo: what exists and what does not

**Status:** investigated

| Question | Finding |
|---|---|
| Is there a Zenodo MCP server or connector available here? | **No.** The connector catalogue has no Zenodo entry, and no Zenodo MCP server is configured. `tool_search` for zenodo returns no matches. |
| Can we still deposit programmatically? | **Yes** — Zenodo's REST API is reachable and documented; a token in an environment variable is the only requirement. |
| Is there an MCP alternative worth building? | A small local MCP wrapping `depositions` (create, upload, metadata, publish) is feasible with the `fastmcp` skill. It would add convenience, not capability: the API already does the work. |
| GitHub–Zenodo integration | The recommended route for this project: it mints a version DOI per release and a concept DOI for the record, with no file juggling. Requires the repository to be **public** and the integration enabled in Zenodo settings (UI action). |

---

## Entry 013 — 2026-11-24 — Repository public, hub live, single-repository policy

**Status:** done

| Item | Value |
|---|---|
| Visibility | **public** (operator authorisation, recorded) |
| Hub | **https://labhdufba.github.io/scholarskills/** — HTTP 200 verified |
| Pages | source = GitHub Actions (`build_type: workflow`), HTTPS enforced |
| Workflows | `validate` ✓ and `hub` ✓ on the same commit |

**Policy change (operator decision):** the project uses **one repository for all skills**. The
standalone repository `LABHDUFBA/zotero-reference-management` was therefore folded into
`zotero-reference-management/` in this repository — content verified present on the remote
(`SKILL.md` 4 925 bytes, test file 7 212 bytes) **before** the standalone repository was archived
(archived, not deleted: reversible, and the history is preserved).

**Consequence for DOIs, stated explicitly:** the Zenodo GitHub integration mints **one DOI per
release of the repository**, not one per skill. With a single repository, every available skill cites
the same concept DOI and points to its own directory. Per-skill DOIs would require one repository per
skill, which the operator has ruled out. This is recorded in `registry.json` under `hub.doi_policy`
and is a deliberate trade-off, not an oversight.

**New script:** `scripts/set_doi.py` registers or clears a DOI idempotently, validates the format
before writing, requires the concept DOI whenever a version DOI is given, and regenerates the hub.
Tested: `--clear` and an invalid identifier (refused with the expected message).

---

## Entry 014 — 2026-11-24 — Release v1.0.0 published; DOI pending an operator toggle

**Status:** partially blocked

| Item | Value |
|---|---|
| Release | https://github.com/LABHDUFBA/scholarskills/releases/tag/v1.0.0 |
| Published | 2026-11-24T08:56:35Z, not a draft |
| DOI | **none** |

**Evidence that the integration is not active for this repository:**

1. `gh api repos/LABHDUFBA/scholarskills/hooks` returns **no webhook**. The Zenodo GitHub integration
   installs a webhook on the repository when its switch is enabled; the absence of the hook means the
   release never reached Zenodo.
2. The Zenodo API is **unreachable from this host**: `https://zenodo.org/api/records` returns
   HTTP 403 with an HTML block page, for both plain and browser-like user agents. Earlier in the
   session the sandbox endpoint answered 200, so the block is recent or path-specific.
3. No `ZENODO_TOKEN` / `ZENODO_SANDBOX_TOKEN` exists in this environment, so a direct API deposit is
   not possible either.

**Action required (operator, in the browser — not automatable):**

1. Open https://zenodo.org/account/settings/github/ and enable the switch for
   **`LABHDUFBA/scholarskills`**. The repository became public only today, which is why it was
   probably absent from the list when the integration was connected.
2. Publish a **new release** (e.g. `v1.0.1`); Zenodo only acts on releases published *after* the
   switch is on. The v1.0.0 release will not be retroactively archived.
3. Send back the two identifiers Zenodo shows: the **concept DOI** and the **version DOI**. Register
   them with `python3 scripts/set_doi.py --concept ... --version ... --release v1.0.1`;

Do not paste a token in the chat: the integration makes one unnecessary.

---

## Entry 015 — 2026-11-24 — Hub bilingual, colour-coded by research stage

**Status:** done

| Change | Detail |
|---|---|
| Languages | Portuguese at the site root (`/`), English under `/en/`. Two static trees, both generated from one registry; the toggle is a plain link, so it works without JavaScript and each URL is stable. |
| Stage taxonomy | `registry.stages` maps eight methodological stages to a colour pair. Every card carries `data-stage`, a coloured top bar and the stage name in text — colour is never the only signal. |
| Card content | `features` (only for available skills) and `integrations` rendered as chips with icons: Zotero, Hermes Agent, Python, GitHub. Planned skills show their expected stack at 62% opacity. |
| Accessibility | Categorical palette (Okabe–Ito, colour-vision safe). Every stage ink was darkened and **measured**: all pairs are 6.19:1 or better on their soft background, above the 4.5:1 WCAG AA threshold for body text. Status "available" moved from green to blue so it no longer shares a colour with maturity "tested". |
| Icons | `assets/img/`: Zotero "Z" (official path, #db2c3a) and the Hermes Agent mascot (48 px official favicon, the largest asset published). Attribution in the footer. |

**Verification:** rendered in a real browser — 10 cards in both languages, stage colours distinct, tool chips legible, filters and language toggle working, no horizontal overflow.

---

## Entry 016 — 2026-11-24 — LABHD visual identity adopted

**Status:** done

| Item | Source | Value |
|---|---|---|
| Brand green | labhdufba.github.io CSS | `#16a34a` (green-600), hover `#15803d`, deep `#0a1f0c` |
| Support greens | idem | `#4ade80`, `#bbf7d0`, `#f0fdf4` |
| Neutrals | idem | `#111827` (text), `#6b7280` (muted), `#e5e7eb` (lines) |
| Type | idem | **Signika** (headings), **Heebo** (body) — the institute's own pairing |
| Logo | `/images/labhd_hu_f740b91ea7236ce2.webp` | official circular badge, used at 38 px in the header, 20 px in the footer, as favicon |

**Colour discipline:** green is now reserved for the brand and for the "available/tested" status. The
"literature review" stage moved from teal-green to cyan `#0891B2` so a stage colour never competes
with the institutional green. Measured again after the change: every stage ink is 6.39:1 or better on
its background; brand text `#15803d` on white is 5.02:1 (AA).

**Prepared to become a tab of the institutional site:** all links are relative, so the hub works at
any path (`/`, `/skills/`, a subdirectory of the Hugo site) without rebuilding. The header carries the
LABHD badge linking to the institutional site, and the language switch is a plain link.

**Note on the logo asset:** the published file is 64×64 px (the largest the site exposes). At 38 px the
badge reads as a seal and its inner micro-text is not legible — mitigated by the "LABHD · UFBA" wordmark
beside it. If the vector original becomes available, swapping the file is the only change needed.

---

## Entry 017 — 2026-11-24 — Fonts self-hosted (performance fix)

**Symptom reported by the operator:** the site felt slow.

**Diagnosis, measured rather than guessed:**

| Check | Before |
|---|---|
| GitHub Pages TTFB (3 runs) | 0.20 s – 0.36 s — healthy, not the cause |
| HTML | 19.7 kB |
| CSS / JS | 10.9 kB / 1.6 kB |
| `fonts.googleapis.com` | **third-party, render-blocking**, plus a second origin `fonts.gstatic.com` for the files |

Two external origins in the critical path, both `render-blocking`, are the classic cause of a slow
first paint on networks with high latency to Google — and the hub has no reason to depend on them.

**Fix:** both families are variable fonts, so each is a single `woff2`. Downloaded the `latin` subset
and self-hosted them under `assets/fonts/` (Heebo 30 kB, Signika 42 kB), declared `@font-face` with
`font-weight` ranges and `font-display: swap`, and added `<link rel="preload">` for both. The Google
stylesheets were removed entirely.

**After, measured in a real browser:**

```
ttfb 28 ms · DOMContentLoaded 246 ms · load 368 ms
10 requests · 0 external requests
```

**General rule recorded:** a static academic site must not put a third-party font CDN in the critical
path. Self-hosting a variable font costs ~70 kB once and removes two DNS lookups, two TLS handshakes
and a blocking round-trip.

---

## Entry 018 — 2026-11-24 — Zenodo integration: still not active

Re-checked after the operator said the connection was made: `gh api repos/LABHDUFBA/scholarskills/hooks`
still returns **0 hooks**, and the only release is `v1.0.0`, published before the repository became
public. The switch per repository was therefore not enabled. Exact steps are in Entry 014.

---

## Entry 019 — 2026-11-24 — Skill pages keep the site's identity (bug fix)

**Symptom:** opening a card led to a white, unstyled page ("o site fica branco e todo feio").

**Root cause, verified in the browser:** `render_skill()` computed the asset prefix as `""` for
Portuguese while the page is written to `site/skills/`. The stylesheet was therefore requested as
`site/skills/assets/style.css` → **HTTP 404**. `document.styleSheets[0].cssRules` was empty and the
body fell back to the browser default: Times, black on white, broken logo. Home page was fine, which
is why the problem only appeared after clicking a card.

**Fix:** prefix is now `../` (PT, depth 1) and `../../` (EN, depth 2) for pages under `<base>/skills/`.
Confirmed by requesting the URL: `assets/style.css` → 200, body font resolves to Heebo.

**Design work on the detail page, so it reads as the same object as the card:**

| Element | Card | Detail page |
|---|---|---|
| Stage colour | 4 px bar on top | 4 px top border **plus** gradient wash in `--stage-soft` |
| Badges | id, maturity, status | same three, plus stage badge |
| Tools | chips with icons | same chips in the hero |
| Accent | stage ink | stage ink on the factsheet, step markers and citation block |

**Translation completed:** `objective_pt`, `how_it_works_pt`, `evidence_pt`, `install_pt` and
`links_pt` added for SS-0000 and SS-0001. The detail page previously mixed Portuguese headings with
English body text; maturity and status values are now shown translated in the factsheet.

---

## Entry 020 — 2026-11-24 — Header: logo only, compact on mobile

The operator reported the header as too busy, especially on a phone.

- Removed the "ScholarSkills / LABHD · UFBA" wordmark from the header; **only the circular badge
  remains**, linking to the institutional site. The site name still appears in the `<title>`, the
  hero `<h1>` and the footer.
- Mobile: the nav goes on one non-wrapping, horizontally scrollable line, and the language switch
  shows a short label (**EN** / **PT**) below 900 px.
- Measured on a 390 px viewport: header height **151 px → 89 px**, no horizontal overflow
  (`scrollWidth == clientWidth == 358`), language button fully inside the viewport.

**Note on the logo:** the badge contains micro-text ("LABHD UFBA") that is illegible at 34 px. Without
the wordmark beside it, the mark reads as a seal — acceptable, but a logo with a larger symbol and no
inner text would read better at this size. Escalated to the operator, since only the 64×64 raster is
published.

---

## Entry 021 — 2026-11-24 — "Requirements" section: what the user must provide

**Operator's point:** a skill page must state up front what the user has to supply for the skill to
work. For Zotero that is an API key, and a bare "403 — scope limit" reads as an implementation detail
rather than as an instruction.

**Implementation:** `requirements[]` in the registry. Each entry carries `name`, `required`, `type`
(`secret` | `id` | `software` | `choice`), the `env` variable the code reads, `what` (in plain
language), `how` (the exact UI path to obtain it), `url` + `doc_url` (verified, opened in a new tab),
`example` (a copyable `export` line) and `note` (the security warning).

Rendered as a card list, above the objective, in both languages:

- **SS-0001 (Zotero)** — API key (`ZOTERO_API_KEY`, secret), library ID (`ZOTERO_LIBRARY_ID`),
  library type (`ZOTERO_LIBRARY_TYPE`, user | group).
- **SS-0000** — Python 3.10+, PyYAML.

The 403 is now framed where it belongs: the key's *scope* is the limit of access, and the requirements
block says which scope to grant instead of telling the reader to work around a 403.

**Links verified before publishing** (not guessed): `zotero.org/settings/keys/new` → 200,
`zotero.org/support/dev/web_api/v3/basics` → 200. The key-creation path, the `Total-Results` header
and `itemType=-attachment` were confirmed against the official Web API v3 documentation.

**Accessibility correction found while testing the block:** white text on the brand green `#16a34a`
measures **3.30:1** — below AA. Solid buttons now use `#15803d` (**5.02:1**), keeping `#16a34a` for
surfaces and non-text accents.

---

## Entry 022 — 2026-11-24 — "Skills Métodos Digitais", research paths and discipline filter

**Benchmark studied:** `scholarskill.com` (opened in a real browser, not from description). It is an
**aggregator**: ~26 k indexed skills whose cards link straight to third-party GitHub repositories.
Measured on its HTML: DOI 0, licence 0, version 0, citation 0, peer-reviewed 0. Quality signal there is
GitHub stars; verification is delegated to the reader ("verify source, freshness and install links").

**Decision:** adopt its *usability* patterns, keep our *epistemic* model. Nothing about DOI, maturity
evidence or licensing changes.

| Item | Change |
|---|---|
| Display name | **Skills Métodos Digitais** (PT) / Digital Methods Skills (EN), always with LABHDUFBA. Resolves the near-collision with `scholarskill.com` (singular, .com, Chinese-first). |
| Technical identity | Unchanged on purpose: repository `labhdufba/scholarskills`, skill prefix `SS-`, GitHub Pages URL. Changing them would break URLs, the release and any citation already pointing here. |
| Research paths | New `collections[]` in the registry: four work sequences (systematic review, corpus→argument, digital data, publish-a-skill). Each card shows **numbered steps** with the skill id, name and a "planejada" tag when the artefact does not exist yet. |
| Disciplines | New `disciplines{}` map (sociology, digital humanities, public health, education, public finance, methodology) with a filter in the toolbar and the value shown in each skill's factsheet. |
| Layout | Paths sit between the hero and the catalogue, mirroring the "popular paths" entry point; a legend of disciplines closes the section and sets the filter on click. |

**Verified in the browser:** 4 path cards, 3 numbered steps each, 8 "planejada" tags, discipline filter
returns 7 of 10 for "Sociologia" and 10 when cleared, grid 2×2 at 1400 px and 1 column at 390 px,
`scrollWidth == innerWidth` at 1400 / 390 / 360 / 320 px. Header on mobile: 89 px at 390 px (logo + EN
on row 1, menu on row 2), 118 px below 360 px where the menu wraps instead of overflowing — nothing is
clipped at any width.

---

## Entry 023 — 2026-11-24 — Manual light/dark toggle and a larger type scale

**Type scale.** Every `font-size` in the stylesheet was converted from px to rem (64 declarations) and
the root was raised from 16 px to **18 px** (`html{font-size:112.5%}`), the body shorthand from
`16px/1.62` to `1rem/1.65`, and the two `clamp()` headings from px to rem. Scaling the root keeps the
whole system proportional: one number changes, nothing is nudged by hand. Measured after:
root 18 px, body 18 px, card paragraph 15.75 px.

**Theme toggle.** Until now dark mode was only `@media (prefers-color-scheme: dark)`, which a visitor
cannot override. The block is now generated twice from one source — once under the media query with
`html:not([data-theme=light])`, once as `html[data-theme=dark]` — so the system preference remains the
default and a click overrides it. The choice persists in `localStorage` (`smd-theme`) and an inline
script in `<head>` applies it before first paint, so there is no white flash on a dark page.

Button lives in the header: 36×32 px, sun/moon swapped by CSS, `aria-pressed` maintained by JS, title
changes between "Mudar para tema claro" and "Mudar para tema escuro". Positioned outside `<nav>`, next
to the language switch.

**Dark-mode defects found and fixed along the way** (the media-query block had never been exercised
with the new components):

| Element | Symptom | Fix |
|---|---|---|
| Path chips, feature tags, `code.env` | inherited the light `--stage-soft`, white blocks on black | `color-mix()` of the stage colour with the surface, 16 % |
| `.stack .chip` | hardcoded `#f7f8fb` background, unreadable | uses `var(--bg-soft)`, with a dark override |
| Skill hero gradient | `--stage-soft` at 100 % produced a pale band on a dark page | `color-mix(... 18%, var(--bg))` |
| Stage badge | ink too close to the background | 22 % stage on surface, ink lifted 55 % toward white |
| "planejada" tag | dark on dark | explicit `#1f2822` / `#c9d3cc` |
| Requirements warning | amber surface kept its light values | `var(--warn-soft)` / `var(--warn)` |

Verified in the browser in both themes on the index and on a skill page: body background flips
`#fff ↔ #0b0f0c`, text `#111827 ↔ #e9efe9`, chips resolve to `color(srgb …)` values from `color-mix`,
and `scrollWidth == innerWidth` at 1400 and 390 px. Header on mobile is 128 px at 390 px (logo, theme
and EN on row one; menu on row two; Submeter centred on row three) — taller than the 89 px of the
previous entry, which is the cost of the larger base type.

---

## Entry 024 — 2026-11-24 — Research paths become a filter; vendor icons replaced

**Decision on the paths section.** The four path cards repeated every skill name that the grid
repeats three hundred pixels below. What they added was *order* — and order is worth keeping, just
not worth four large cards before the catalogue. The section is now a compact bar above the toolbar:
one pill per path, each showing its name and the chain of ids (`SS-0001 → SS-0002 → SS-0003`).
Clicking filters the grid to exactly those skills; clicking again clears it. Zero repeated names,
the grid stays in the first fold, and the sequence is displayed where it is used.

**Vendor icons.** The chips used hand-written SVG paths for Python and GitHub and a 48 px favicon for
Hermes. Replaced with assets taken from the vendors' own sites:

| Chip | Asset | Source |
|---|---|---|
| Python | `python.png`, symbol cropped from the official master PNG, 213×203, transparency preserved | python.org/static/community_logos |
| Zotero | `zotero.svg`, official mark path, `#CC2936` | zotero.org (brand mark) |
| GitHub | `github.png`, 256 px from the official 560 px mark | github.githubassets.com |
| Zenodo | `zenodo.svg` | zenodo.org |
| Hermes | `hermes.png`, 48 px | hermes-agent.nousresearch.com |

`ICON_ASSET` in `build_site.py` is now the single map from integration key to file, so a chip cannot
point at a file that does not exist: an unknown key is skipped instead of rendering a broken image.

**Verified:** 4 path pills, clicking the first reduces the grid from 12 to 3 skills (`count` agrees),
second click restores 12; bar is 54 px tall and 1071/356 px scrollable at 390 px with no page
overflow; dark mode resolves the bar to `--bg-soft` and the active pill to `--brand-soft`.

---

## Entry 025 — 2026-11-24 — Per-skill DOIs on Zenodo, ORCIDs in the hub

**Architecture.** Six skills and one collection record, each with its own concept and version DOI.
The repository stays single; the identity does not. Skills carry `isPartOf` → collection, the
collection carries `hasPart` → six skills.

| Record | Version DOI | Concept DOI |
|---|---|---|
| SS-0000 | 10.5281/zenodo.24505398 | 10.5281/zenodo.24505397 |
| SS-0001 | 10.5281/zenodo.24505402 | 10.5281/zenodo.24505400 |
| SS-0010 | 10.5281/zenodo.24507969 | 10.5281/zenodo.24504881 |
| SS-0011 | 10.5281/zenodo.24505404 | 10.5281/zenodo.24505403 |
| SS-0012 | 10.5281/zenodo.24505406 | 10.5281/zenodo.24505405 |
| SS-0013 | 10.5281/zenodo.24505408 | 10.5281/zenodo.24505407 |
| Collection | 10.5281/zenodo.24507970 | 10.5281/zenodo.24505393 |

**Correction to an earlier claim.** I had written that a per-skill DOI requires a repository per
skill. That is true only of the GitHub integration, which mints one DOI per repository release. The
REST API has no such limit, and the project never needed to fragment. The lesson is recorded in the
skill: distinguish the two deposit routes before telling the operator that one thing implies the other.

**ORCIDs, verified at the source, not by name similarity.** `0000-0003-2929-1115` (Nascimento, UFBA
Professor Adjunto, keywords "digital sociology; CAQDAS"), `0000-0001-5067-8475` (Eric Brasil
Nepomuceno, UNILAB), `0000-0003-3107-3686` (Ricardo Sodré Andrade — filed under "Ricardo Andrade",
found through `other-names`; UFBA and Arquivo Nacional). The third one illustrates the rule: a search
by the name used in the project returns nothing when the record is filed under another surname.

**Two defects found and fixed in the dark theme.** The citation block fell back to `#f8faf9` because
`--stage-soft` is set on `.skill-head` and not inherited by `<main>`; the icon plates kept a fixed
`#eef4ef`. Both were visible as white patches on a dark page. A third defect was mine: the dark
overrides were appended without a selector, so `.badge.kind` turned dark in the light theme. All
three were caught by enumerating every element whose computed background luminance exceeds 200.

**CSS caching.** The stylesheet had no version in its URL, so a rebuilt file was masked by the
browser cache — the fix looked broken when it was already correct. The link now carries
`?v=<sha256[:10]>` of the exact CSS text written in that build.

**A bug worth naming.** `actions/newversion` clears `metadata.version`. The first new version of
SS-0010 was published with an empty version, forcing a second one; the sequence reads 1.0.0 →
(empty) → 1.0.2 because `link_collection.py` bumped a string it had already bumped. Cosmetic, but a
citation that says "v1.0.2" with no 1.0.1 in between needs an explanation, and this is it.

---

## Entry 026 — 2026-11-24 — Contribution page, brief template, and the accessibility pass

**Contribution, not just a link to CONTRIBUTING.md.** The nav CTA now opens `/contribuir.html`: three
steps (download the brief → fill it with your agent → open a proposal), the five things review checks,
and the contact address. The brief lives in `templates/skill-brief.md` and is copied to
`assets/downloads/skill-brief.md` at build time, so the file a reader downloads is the file in the repo.

The brief is addressed to the agent, not to the contributor: it ends with explicit instructions
(follow SS-0000, ask instead of inventing, credentials by environment variable, official route before
any workaround, record the real environment in `tests/RESULTS.md`). An empty field is a question to
ask — stated in the template, because a template that invites guessing produces invented methods.

**Audit against two design references.** Ran the `impeccable` context loader (no PRODUCT.md; incumbent
implementation is authority for refinement) and used `ui-ux-pro-max`'s ten priority categories as the
rubric. Measured in a real browser rather than eyeballed:

| Check | Before | After |
|---|---|---|
| Text below contrast minimum | 12 elements (CTA 3.30:1, `.code` 4.43:1) | 0 |
| Targets under 44 px | 40 | 0 in the header and cards |
| Heading order | H1 → H3 (no H2) | H1 → H2 → H3 |
| Images without `loading` | 33 | 5 (logo and above-the-fold only) |
| Header height at 390 px | 167 px | 109 px |

**Two false alarms worth recording.** The page title appeared to carry a horse emoji; `curl` and the
file on disk showed it clean, and no file in the repository contains it — it is injected into the DOM
by the test browser, not by the site. Chasing it would have meant "fixing" something that was never
broken. Similarly, the CSS fix looked inert until the stylesheet URL got a content hash — the browser
was serving the previous file, so a correct change read as a failed one.

**What the audit actually changed.** The CTA moved to `--brand-ink` (5.02:1); `.code` and `.badge.muted`
went to `#5b6472` (5.3:1); every interactive element gained a 44 px minimum, which forced the mobile
nav into a single scrollable row with a mask fade instead of three stacked rows; and the catalogue got
the missing H2 that the card grid needed.

**Pending.** `hub.contact_email` is empty: the laboratory address is not published anywhere verifiable,
and an invented contact address on a public page is worse than a missing one. The contact block renders
only when the field is filled.

---

## Entry 027 — 2026-11-24 — Accessibility sweep over all fourteen skill pages

**Scope.** The earlier pass measured only the home and the contribution page. This one ran the same
audit across every skill page — fourteen pages × two themes × four widths — plus a link resolver that
walks the built HTML and resolves every `href` and `src` against the published tree.

| Check | Before | After |
|---|---|---|
| Contrast failures (14 pages × 2 themes) | 14 | **0** |
| Targets under 24×24 | 14 | **0** |
| Broken href/src in skill pages | 4 | **0** (269 verified) |
| Anchors with no target | 1 (`#paths`) | **0** |
| Header height at 390 px | 109 px | 109 px |
| Page overflow at 320 px | 0 | 0 |

**The one that mattered most was a theme bug, not a layout bug.** Every dark-mode override lives inside
`@media(prefers-color-scheme:dark)`. The toggle writes `data-theme="dark"` without changing the system
preference, so a reader who *chose* dark got the dark palette but not the dark overrides — the CTA
measured **1.4:1** white-on-light-green. The fix needed the rule in both emitted blocks: the media query
(for the automatic case) and `html[data-theme=dark]` (for the chosen one). This is the pitfall already
recorded in the project skill; it was still live because the earlier pass only ever tested dark by
system, never by click.

**Seven defects, none visible by eye:**

1. **The logo sat at the right edge on desktop.** The flex `order` written for mobile leaked upward:
   `nav` carried `order:0` and pushed the brand to the end of the bar. Brand now renders at x=164.
2. **`href="Repositório"`** — in SS-0012 and SS-0013 the registry stored the *label* where the URL
   belongs, so two panel links pointed nowhere. Fixed, and `metadata-schema.json` now requires
   `^https?://` on `links`, so the CI rejects the shape instead of the browser discovering it.
3. **`../../en/index.html`** on every skill page — the language link climbed two levels out of the
   site from `/skills/`. Now `../en/`.
4. **`#paths` had no target** — the menu pointed at a section that never carried the id.
5. **DOIs broke mid-number**, leaving an orphan digit (`…2450796` + `9`). They are now links to
   `doi.org` that break only after the slash, via `<wbr>`. Measured: 21 px, one line.
6. **Panel values were right-aligned**, so every wrap produced a ragged edge — `(docs)` orphaned, a
   comma dangling after "Disciplina". Left-aligned now.
7. **Python, GitHub and Hermes Agent rendered as three full-width bars** with 1000 px of empty space:
   `.stack` had no `display:flex` outside cards, so each chip became a block. Now 84, 83 and 126 px.

**Verification.** Structural validator PASS on six skills (warnings unchanged); seven suites OK; build
`--check` clean; `node --check` on the generated JS; 269 links and images resolved with zero failures;
three widths with zero page overflow. The two `pre` blocks wider than a 320 px viewport scroll inside
their own `overflow-x:auto` container — correct behaviour, and a false positive worth naming so the
next audit does not chase it.

**Deliberately not changed.** On a skill page the active menu item is still "Início" rather than
"Skills", and requirement cards place their chips slightly differently from one another. Both are
design choices, not defects, and neither was decided unilaterally here.

---

## Entry 028 — 2026-11-24 — Consistency pass: active menu item, requirement cards, mobile header

Two inconsistencies the audit had flagged but left to a decision. Both were fixed here.

**1. The active menu item followed the page, not the assumption that every page is the home.**
`site_header` carried `class="on"` hard-coded on "Início", so a skill page highlighted the wrong
section. It now takes an `active` argument (`home` / `skills` / `contribute`), set per page, and marks
the item with `class="on"` plus `aria-current="page"` — the latter being what a screen reader actually
announces. Verified by reading the rendered anchor on all fourteen pages, in both languages.

**2. Requirement cards placed their badges differently depending on the title length.**
`.req-top` used `justify-content:space-between` on a wrapping row: a short title put the badges on the
right edge, a long title dropped them to a second line, so two cards side by side disagreed about
where the badges live. The row is now a column — title, then badges, always left-aligned, always 28 px
apart. Measured on both cards of SS-0010.

**Two regressions found while doing it, both mine.**

- Reordering the header for desktop (`brand → nav → controls`) changed the flex `order` in the base
  selector, and the mobile rule could no longer win: it used `nav.site` against the new
  `header.site nav.site`, so the menu landed on its own row *between* the controls and the header grew
  from 109 to 161 px. Fixed by declaring the mobile order with matching specificity.
- Squeezing the six menu items into one line at 390 px exposed that the primary action ("Contribuir")
  was being clipped at the right edge. The project rule is explicit — *quebrar é honesto, cortar é
  defeito* — so the menu was tightened (gap 12 → 8 px, font 0.75 → 0.7188 rem) down to 360 px, and at
  320 px it wraps to two lines instead of scrolling. Measured at 1440/390/375/360/320 px: the CTA is
  inside the viewport at every width and page overflow is zero.

**Verification.** Contrast and touch targets on 14 pages × 2 themes: **0 / 0**, and all fourteen report
"Skills" as the active item. Build `--check` clean; `node --check` clean; validator PASS on six skills;
CSS braces balanced 317/317 with no `%SEL%` left; deposit suite OK.

## Next steps (ordered)

1. ~~Operator authorises repository creation (private first)~~ — done, private repository exists.
2. Operator confirms Ricardo Sodré's GitHub account, then invitation is sent.
3. Operator authorises making the repository public, and decides the long-term home
   (`LABHDUFBA/scholarskills` vs. a `ScholarSkills` organisation vs. `LABHDUFBA`).
4. ~~Operator decides the hub hosting route~~ — public repository, Pages via Actions, site live.
5. ~~Deposit route chosen~~ — GitHub–Zenodo integration. Pending: enable the repository switch, then a new release.
5. Sandbox deposit executed with a sandbox token; DOI never presented as scientific.
6. Production release authorised; version DOI and concept DOI recorded separately in
   `registry/registry.json`.
