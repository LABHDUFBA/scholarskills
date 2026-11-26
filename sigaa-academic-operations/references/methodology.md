# Methodological grounding

## Method implemented

This package implements a human-in-the-loop protocol for operating institutional academic portals. The protocol has five commitments:

1. establish the identity and scope of the target record;
2. validate user-provided or primary-source content before entry;
3. prepare a reversible draft before any persistent action;
4. require explicit approval for publication, record changes, approval and formal submission;
5. read back the target after the action and report the observed result.

The method is procedural rather than a scientific analysis method. It is intended to reduce wrong-target edits, duplicate submissions, accidental notifications and false claims of success in stateful web portals.

## Decisions encoded

- Navigation permission is not submission permission.
- A saved draft is not a formal submission.
- A portal success message is evidence of a server response, not by itself proof that the intended record is correct; the target must be re-read.
- A notification e-mail is an additional side effect and must be disclosed.
- Missing scientific, academic or eligibility data remains missing; the agent must not invent it.
- Portal selectors and routes are session-discovered because SIGAA deployments differ.

## Grounding sources

The institutional and technical details must be checked against the current portal and the applicable official documents. This package does not reproduce an institution's private interface or regulations. For a deployment adapter, cite:

- the institution's official SIGAA documentation or help pages;
- the official call text and research regulations for PIBIC, PIBITI or equivalent programmes;
- the institution's privacy, records and academic regulations;
- the Agent Skills specification used by the host agent.

## What this does not establish

The procedure does not establish that a grade, attendance record, eligibility claim or proposal statement is true. It only structures safe interaction with the portal and makes the human approval and verification points explicit.
