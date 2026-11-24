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

## Next steps (ordered)

1. Operator confirms Ricardo Sodré's GitHub account.
2. Operator authorises repository creation (private first) and collaborator invitations.
3. Deposit route chosen: GitHub–Zenodo integration **or** manual/API (not both).
4. Sandbox deposit executed with a sandbox token; DOI never presented as scientific.
5. Production release authorised; version DOI and concept DOI recorded separately in
   `registry/registry.json`.
