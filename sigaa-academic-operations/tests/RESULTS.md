# Test results — SS-0015 (sigaa-academic-operations)

Recorded from real offline and live smoke-test executions. The live test used the account holder's authenticated UNILAB SIGAA session; no credential, token, roster or private export was stored in the package.

## Offline environment

```
Python 3.14.9
network: not used
date: 2026-11-26
```

## Offline command and result

```bash
python3 -m unittest discover -s tests -v
```

```
Ran 7 tests in 0.001s
OK
```

## Live smoke test — UNILAB

| Check | Result |
|---|---|
| Login through the account holder's credential manager | passed |
| Portal profile and current term displayed | passed; term `2026.2` |
| Teacher portal listed classes | passed |
| `Pesquisa` menu discovered | passed |
| `Planos de Trabalho` submenu discovered | passed |
| `Frequencias para Homologar` route opened | passed |
| Empty homologation table handled | passed; portal reported no results |
| Persistent action during this smoke test | none |

The browser session expired during setup and the browser harness timed out once. Re-authentication through the credential manager recovered the session; the route was then opened and read back successfully. This is evidence for the documented session-expiry path, not a claim that every browser backend will behave identically.

## Prior controlled live operations in the same SIGAA account

The broader conversation also verified, with explicit approval and post-action read-back:

- publication of a class notice;
- correction of a notice's grade value;
- editing a lesson topic and verifying the new rendered content.

These are contextual live checks, not automated tests and not a substitute for independent replication.

## Coverage and limits

| Case | Covered |
|---|---|
| Positive | valid teaching operation; formal proposal with named call and approval |
| Negative | missing target; missing call; missing approval; invalid boolean |
| Edge | notification e-mail as explicit side effect; synthetic example loading; expired live session |
| Live not covered | grade/attendance mutation in this smoke test; file upload; PIBIC/PIBITI formal submission; institutional permissions beyond the current profile; another SIGAA deployment |
