# Compatibility and adapters

SIGAA deployments share a product family and common concepts, but a skill must not assume identical screens. Institutions may differ in version, enabled modules, menu labels, permissions, local workflows, academic calendars and research-call configuration.

## Generic core

The core should identify actions by semantic labels and page evidence:

- teaching module and virtual classroom;
- topics, lessons or course content;
- attendance and grades;
- notices, materials and activities;
- research projects and work plans;
- frequencies awaiting approval;
- call/proposal submission.

It should verify the current page title, selected target, term and visible fields before writing.

## Institution adapter

An adapter may document:

- official entry URL;
- portal version and date observed;
- local names for modules and menu items;
- known routes and role restrictions;
- local call names and required attachments;
- tested operations and untested operations;
- public official documentation links.

Adapters must not contain credentials, session cookies, private exports, student identifiers or selectors treated as permanent guarantees.

## Version drift

When a label or route is missing, the agent should search the visible menu and page semantics rather than guessing an internal URL. A changed interface should produce an explicit `not confirmed` result and an adapter update, not a silent fallback to an unrelated action.
