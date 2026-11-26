#!/usr/bin/env python3
"""Create a blank, non-destructive research-project documentation scaffold."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def scaffold_files(title: str) -> dict[str, str]:
    """Return relative file paths and contents for the minimal starter scaffold."""
    title = title.strip()
    if not title:
        raise ValueError("project title must not be empty")
    return {
        ".gitignore": """# Local secrets and common generated files; review for this project's data policy.
.env
.env.*
!.env.example
.venv/
__pycache__/
*.py[cod]
.DS_Store
Thumbs.db
""",
        "README.md": f"""# {title}

## Purpose

[What is this project about, and who is it for?]

## Research question and objective

[State the question and the intended output.]

## Scope and non-goals

- In scope: [describe]
- Out of scope: [describe]

## Repository map

- `docs/`: project vision and working protocol
- `task_plan.md`: planned work, dependencies, and blockers
- `findings.md`: source-backed findings and documented decisions
- `progress.md`: completed actions and verification

## Current state

[Record the stage, responsible roles, and next milestone.]

## Sources and citation

[Link to the governing brief, protocol, public sources, or citation record. Do not put restricted source contents here.]

## Data and access

[State where data are authorized to live, who may access them, and what must not be committed.]
""",
        "task_plan.md": """# Task plan

## Objective and completion criteria

- Objective: [state the deliverable]
- Completion criteria: [state observable checks]

## Work stages

| Stage | Status | Dependency | Owner | Acceptance check |
|---|---|---|---|---|
| Scope and source inventory | pending | — | [role/name] | [check] |
| Data and ethics review | pending | Scope | [role/name] | [check] |
| Method and implementation | pending | Source inventory | [role/name] | [check] |
| Verification and handoff | pending | Implementation | [role/name] | [check] |

## Blockers and open decisions

- [decision or blocker; responsible person; next review point]
""",
        "findings.md": """# Findings and decisions

Use this file for source-backed findings and durable project decisions, not as a task list.

## Findings from sources

| Claim or observation | Source / locator | Verification status | Relevance |
|---|---|---|---|
| [finding] | [citation, URL, page or section] | [verified / pending] | [why it matters] |

## Decisions

| Date | Decision | Reason and evidence | Revisit when |
|---|---|---|---|
| [date] | [decision] | [basis] | [condition] |

## Unresolved questions

- [question, owner, next step]
""",
        "progress.md": """# Progress record

Add dated entries for work that was actually completed. Separate actions performed from planned work.

## Entries

| Date | Action completed | Evidence or artifact | Result / limitation |
|---|---|---|---|
| [YYYY-MM-DD] | [action] | [path, command, or source] | [verified result] |
""",
        "docs/vision-and-scope.md": """# Project vision and scope

## Research problem

[Describe the problem and the context needed to understand it.]

## Question and objectives

[State the research question and bounded objectives.]

## Intended users and products

[Name the audience and expected research products.]

## Scope and non-goals

[State what the project will and will not answer or produce.]

## People, roles, and decisions

[Record responsibilities and who can authorize changes to data, methods, and publication.]

## Constraints and assumptions

[Record institutional, ethical, legal, technical, and resource constraints; identify assumptions.]
""",
        "docs/protocol.md": """# Working protocol

## Sources and inputs

[Record source identifiers, access conditions, collection or snapshot dates, and the version used.]

## Method and transformations

[Describe procedures, software and parameters. Link to methodological sources.]

## Provenance

[For each output, identify its input, transformation, unit of analysis, denominator, and destination.]

## Verification

[Describe checks, tests, responsible reviewer, and the evidence they produce.]

## Limitations and change history

[State what the procedure cannot establish and how methodological changes will be recorded.]
""",
    }


def create_scaffold(destination: str | Path, title: str) -> Path:
    """Create files at a new path; refuse all existing destinations."""
    files = scaffold_files(title)
    target = Path(destination).expanduser().resolve()
    protected = {Path(target.anchor), Path.home().resolve(), Path.cwd().resolve()}
    if target in protected:
        raise ValueError(f"refusing unsafe destination: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)
    created_directories: list[Path] = []
    created_files: list[Path] = []
    try:
        # mkdir without exist_ok is the atomic no-overwrite boundary.
        target.mkdir()
        created_directories.append(target)
        for relative, contents in files.items():
            output = target / relative
            missing = []
            parent = output.parent
            while parent != target and not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                created_directories.append(directory)
            with output.open("x", encoding="utf-8") as stream:
                created_files.append(output)
                stream.write(contents)
    except Exception:
        # Remove only files and empty directories this invocation created. If
        # another process added content, rmdir fails safely and preserves it.
        for output in reversed(created_files):
            output.unlink(missing_ok=True)
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", help="new project directory; it must not already exist")
    parser.add_argument("--title", required=True, help="human-readable project title")
    args = parser.parse_args(argv)
    try:
        target = create_scaffold(args.destination, args.title)
    except (OSError, ValueError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"created scaffold: {target}")
    print("files: .gitignore, README.md, task_plan.md, findings.md, progress.md, docs/vision-and-scope.md, docs/protocol.md")
    print("note: no Git repository initialized; inspect and adapt before adding project material")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
