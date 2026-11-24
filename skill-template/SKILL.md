---
name: your-skill-name
description: One paragraph (max 1024 characters) stating what the skill does AND when an agent should use it. Name the artefact, the method and the trigger words a user would actually say.
license: MIT
compatibility: Requires Python 3.10+ and no network access. Replace with the real environment requirements, or delete this field if the skill has none.
metadata:
  scholarskills.id: SS-XXXX
  scholarskills.version: "0.1.0"
  scholarskills.maturity: experimental
  scholarskills.method: Replace with the method implemented
---

# Your Skill Name

One sentence: what this skill produces from what input, for whom.

## When to use

- Concrete trigger 1 (the situation, in the user's words).
- Concrete trigger 2.
- **Do not use** when the input is X, when the data is Y, or when the claim cannot be checked —
  state the boundary, because a skill used outside its validity domain produces confident nonsense.

## Inputs

| Input | Required | Format | Notes |
|---|---|---|---|
| `data` | yes | CSV with header | One row per observation |
| `method` | no | one of `a`, `b` | Defaults to `a` |

## Outputs

- A result artefact (format, where it is written, how it is named).
- A provenance record: inputs used, versions, parameters, timestamp.

## Procedure

1. **Validate the input.** Check shape, types and coverage. Stop with an explicit message when the
   input cannot satisfy the method's assumptions.
2. **Apply the method.** Point to `references/methodology.md` for the definition and to
   `scripts/` for the implementation. Do not paraphrase the method from memory.
3. **Produce the output**, preserving provenance.
4. **Report limitations** that follow from this specific run, not from the method in general.

## Stop criteria

- Stop when the input violates an assumption — do not "adjust" the data silently.
- Stop when a required external service is unavailable after the retry policy; never substitute a
  different source without recording the substitution.
- Stop when the output would identify an individual or a small group in a way the consent does not
  cover.

## Error handling

| Failure | Response |
|---|---|
| Missing column | Report the column and the expected schema; do not infer it |
| Empty or malformed rows | Report the count and skip them **only** if the method tolerates it; record the count |
| Tool/network failure | Retry per `scripts/`, then stop with the error preserved in the log |

## Limits

- State where the method is known **not** to hold.
- State what the output cannot support (e.g. "association, not causation").

## Tools and dependencies

- Python packages with pinned versions in `README.md`.
- External services, if any, with the failure mode they introduce.

## Validation

- `tests/` contains positive, negative and edge cases. Structural tests do not validate the
  scientific claim — say so explicitly.
- `benchmarks/` records measured cost and accuracy where applicable.

## References

See `references/methodology.md`.
