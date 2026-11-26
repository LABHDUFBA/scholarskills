---
name: sigaa-academic-operations
description: "Prepare, review and safely execute teaching and research operations in SIGAA-like academic portals. Use when creating classes, editing lessons, recording grades or attendance, publishing notices, managing research projects, work plans or submitting calls such as PIBIC and PIBITI."
license: MIT
compatibility: "Requires a browser session in the account owner's institution portal. No credentials are stored. Offline protocol checks require Python 3.10+ and no network access."
metadata:
  scholarskills.id: SS-0015
  scholarskills.version: "0.1.0"
  scholarskills.maturity: tested
  scholarskills.method: "Human-in-the-loop academic portal operation with pre-action validation, explicit approval gates, and post-action read-back verification"
  scholarskills.spec-version: "Agent Skills specification"
---

# SIGAA Academic Operations

Prepare, review and execute teaching and research operations in SIGAA-like academic portals while keeping the account holder in control of every persistent action.

## When to use

- Create or update a class, teaching topic, course plan or schedule.
- Record or correct attendance, grades or assessment information.
- Publish a class notice, material, activity or assignment.
- Find research projects, work plans or frequencies awaiting approval.
- Prepare a research proposal or submit a call such as PIBIC, PIBITI or an equivalent institutional programme.
- **Do not use** for another person's account, for bypassing permissions or challenges, or for submitting an incomplete proposal merely to test a page.

## Inputs

| Input | Required | Format | Notes |
|---|---|---|---|
| `operation` | yes | structured request | State module, target, action and desired result |
| `institution_portal` | yes | URL or connected portal | The account holder authenticates in the portal |
| `academic_context` | yes | text or structured record | Institution, term, class/project/call and relevant dates |
| `content` | when applicable | text, values or files | Must come from the user or a verified primary document |
| `approval` | before persistence | explicit human confirmation | General permission to navigate is not approval to submit |

## Outputs

- A prepared or completed portal operation.
- A pre-action summary containing target, fields, values, files, dates and side effects.
- A post-action verification containing the portal message, identifier/protocol when available and read-back result.
- A limitation or failure report when the portal, permission or evidence is insufficient.

## Core protocol

1. **Identify scope.** Confirm institution, user profile, module, term, class, project or call.
2. **Discover the current interface.** Locate the semantic equivalent of the requested module and action. Do not rely on permanent CSS selectors, coordinates or JSF IDs.
3. **Read before writing.** Inspect current values, required fields, target checkboxes, visibility, attachments and notification settings.
4. **Validate inputs.** Check dates, scales, required fields, file names, file sizes, call deadlines and target identity. Do not invent missing academic or scientific content.
5. **Prepare without persistence.** Fill a draft or local plan, but do not press `Save`, `Publish`, `Submit`, `Finalize`, `Approve`, `Homologate` or equivalent.
6. **Ask for explicit approval.** Show a concise diff or summary. State whether the action publishes, sends e-mail, changes student records or submits a formal proposal.
7. **Persist once.** Perform the approved action. Do not retry blindly after a timeout.
8. **Read back.** Reopen the list or record and verify the exact target, content, status and message.
9. **Report honestly.** Separate confirmed success, ambiguous result, failure and untested follow-up.

## Teaching operations

### Classes and course context

Before editing, verify component code and name, class/section, academic term, responsible lecturer, dates, schedule, student count and class status. A portal may list classes directly or expose them through a teacher menu and virtual classroom.

### Lessons and topics

For a topic or lesson:

1. locate it by description and date;
2. verify start date, end date, parent topic, visibility and associated class;
3. preserve existing text, formatting, references and attachments;
4. append or change only the requested passage;
5. show the resulting text or diff;
6. save only after approval;
7. reopen the topic and verify the persisted content.

Rich-text editors may keep a hidden form field and a visible editor. Synchronize both before submitting and verify the rendered text after saving.

### Attendance and grades

- Confirm the class, meeting date, unit, assessment and affected students.
- Preserve the portal's accepted scale and precision.
- Prefer point changes over replacing a whole roster.
- Separate saving from publishing/finalizing when the portal distinguishes them.
- Re-read the changed rows after saving.

### Notices, materials and activities

Confirm title, body, recipients, class, attachment, deadline and e-mail notification state. Treat notification as an additional side effect. A notice that refers to an assignment must not be used as evidence that the assignment itself exists; verify the assignment separately.

## Research operations

### Projects and calls

Before a project or call submission, collect from the official call or user-provided documents:

- call title, identifier, programme and deadline;
- eligibility and institutional restrictions;
- title, abstract, keywords, problem, justification, objectives and methodology;
- team, supervisor, student, scholarship/volunteer mode and institutional links;
- schedule, expected results and references;
- required declarations and attachments, formats and size limits.

Save a draft where possible. Reopen it, check every required field and present a submission checklist. The final approval must say that the action will formally submit the proposal to the named call.

### Work plans and frequencies

Verify the parent project, student, supervisor, modality, scholarship quota, objectives, activities, schedule and validity period. For frequencies awaiting approval, report whether the table is empty or list each record before any approval. Never approve a batch without listing its scope and obtaining explicit confirmation.

## Stop criteria

Stop before persistence when:

- the target institution, class, project, student or call is ambiguous;
- a required field or source document is missing;
- the call deadline or version cannot be verified;
- the portal shows an expired session, permission error, challenge or ambiguous result;
- the proposed action would expose credentials, private student data or restricted research material;
- a retry could duplicate a notice, submission, attachment or grade change.

## Error handling

| Failure | Response |
|---|---|
| Timeout or blank response | Wait/reload once, then inspect whether the action persisted before retrying |
| Session expired | Re-authenticate through the credential manager; do not ask for a password in chat |
| Permission denied | Report the required role; do not attempt a workaround |
| Missing call or menu | Record the route searched; do not infer institutional unavailability |
| Upload failure | Check file type/size and portal message; do not repeatedly upload blindly |
| Accepted form without protocol/status | Treat formal submission as unconfirmed and verify the proposal list |
| Conflicting class/project records | Stop and ask the account holder to identify the target |

## Privacy, ethics and rights

- Operate only the account and records for which the user is authorized.
- Never store credentials, one-time codes, session cookies or raw private exports.
- Minimize student personal data in summaries and tests.
- Use synthetic or public fixtures in examples and tests.
- Do not infer grades, attendance, eligibility, authorship, supervision or research results.
- Respect institutional regulations, the call text, privacy law and copyright of uploaded materials.
- Human approval remains necessary for publication, formal submission, grade changes and approvals.

## Limits

SIGAA deployments share a family resemblance but may differ in version, enabled modules, labels, permissions, workflows and local customizations. This skill is workflow-generic; institution-specific URLs and menu paths belong in an adapter or session note. Offline tests validate the protocol and safety gates, not live compatibility with every SIGAA deployment.

## Validation

Run the offline tests from the package root:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover valid requests, missing scope, persistent-action approval, notification side effects, formal submission confirmation and ambiguous outcomes. They do not log in to an institution or submit real data.

## References

- `references/methodology.md` — human-in-the-loop procedure and approval gates.
- `references/compatibility.md` — deployment differences and adapter design.
- `scripts/protocol.py` — offline request validation and approval summary.
