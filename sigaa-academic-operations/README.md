# SIGAA Academic Operations

**ScholarSkills identifier:** SS-0015 (requested) · **Version:** 0.1.0 · **Maturity:** `tested` · **Licence:** MIT (original code and documentation)

## Objective

Prepare and safely execute teaching and research operations in SIGAA-like academic portals. The skill validates scope, prepares a human-readable approval summary, separates navigation from persistent actions, and requires read-back verification after saving, publishing, approving or submitting. It is designed for the account holder's own institutional profile and does not store credentials.

## What it covers

- Classes, course context and teaching topics.
- Course plans, lessons, notices, materials and activities.
- Attendance and grades.
- Research projects, calls, work plans and frequencies awaiting approval.
- Formal submissions such as PIBIC, PIBITI and equivalent institutional programmes.

## Installation

No package installation is required for the documented procedure. The optional offline protocol checker requires Python 3.10+ from the standard library:

```bash
python3 -m unittest discover -s tests -v
```

The live operation requires a browser session and an account-holder credential manager. Credentials and one-time codes are never inputs to this package.

## Minimal example

```bash
python3 scripts/protocol.py examples/sample_operation.json
```

Expected output is a JSON approval summary. The example is synthetic and does not contact a portal:

```json
{
  "ready": true,
  "target": "HIST-0001 / T01 / 2027.1",
  "action": "update_topic",
  "persistent_action": true,
  "approval_required": true,
  "side_effects": []
}
```

## Compatibility actually tested

| Component | Version | Result |
|---|---|---|
| Python | 3.14.9 | tested offline |
| Network | none | not used |
| Live SIGAA deployment | none in package tests | not tested |
| Browser automation | none in package tests | not tested |

## Limitations

- The package does not claim compatibility with every SIGAA installation.
- Version, labels, permissions, enabled modules and local workflows vary by institution.
- The protocol checker validates request shape and approval gates, not the truth of grades, attendance, eligibility or scientific content.
- It does not replace the official call, institutional regulations or the researcher's judgment.
- No live login, upload, publication, approval or formal submission is performed by the tests.

## Data and ethics

Examples contain synthetic identifiers and text only. Do not commit passwords, tokens, session cookies, student rosters, grades, attendance exports, private proposals or restricted attachments. Operate only records for which the account holder is authorized. Treat publication, grade changes, approvals and formal submissions as separate actions requiring explicit human confirmation.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Results are recorded in `tests/RESULTS.md`.

## Citation

See `CITATION.cff`. No DOI has been assigned.

## Authors and contributions

| Author | Affiliation | Contribution |
|---|---|---|
| Eric Brasil | UNILAB | Author, workflow design and offline tests |
| Leonardo Fernandes Nascimento | LABHDUFBA/UFBA | ScholarSkills project maintenance and review requested |
