# Test results — SS-0000

Recorded from a real execution, not from expectation. A results file that was written before
running the tests is a lie with a timestamp.

## Environment

```
Python 3.14.9
PyYAML 6.0.3
Linux 6.8.0-149-generic
date: 2026-11-24T09:32:32
host: LABHDUFBA Hermes (Linux)
```

## Commands

```bash
# 1. protocol test suite (validator, builder, metadata generator)
python3 -m unittest discover -s tests

# 2. reference example suite
cd examples/descriptive-analysis && python3 -m unittest discover -s tests

# 3. structural validation of this package
python3 scripts/validate_skill.py .

# 4. aggregated report
python3 scripts/run_checks.py . --json --registry ../registry/registry.json
```

## Results

### 1. Protocol suite

```
.....................
----------------------------------------------------------------------
Ran 21 tests in 3.746s

OK
```

### 2. Reference example suite

```
----------------------------------------------------------------------
Ran 8 tests in 1.190s

OK
```

### 3. Structural validation

```
validating: /home/hermes/projects/scholarskills/scientific-agent-skill-development  (name: scientific-agent-skill-development)
  PASS    0 warning(s)
```

### 4. Aggregated checks

```json
{
  "package": "scientific-agent-skill-development",
  "structural_ok": true,
  "validation": {
    "ok": true,
    "errors": [],
    "warnings": [],
    "info": {
      "name": "scientific-agent-skill-development",
      "description_length": 314,
      "body_lines": 166,
      "path": "/home/hermes/projects/scholarskills/scientific-agent-skill-development"
    }
  },
  "consistency_problems": [],
  "tests": {
    "test_files": [
      "test_validate_skill.py"
    ],
    "has_results_record": false,
    "note": "structural tests do not validate the scientific claim"
  },
  "disclaimer": "A passing report means the package is reviewable. It does not mean the method is correct, validated, peer-reviewed or reproducible."
}
/home/hermes/projects/scholarskills/scientific-agent-skill-developmen
```

## What these results do and do not prove

They prove that the validator enforces the Agent Skills rules, that the builder refuses invalid
input, that the metadata generator produces a ZIP with a matching checksum, and that the reference
example behaves as documented on its positive, negative and edge cases.

They do **not** prove that any method is correct, that a citation supports its claim, or that the
package is fit for a specific research use. Structural validation is not scientific validation, and
this file says so on purpose.

## Known gaps

- The validator has not been exercised against a package produced by a third party.
- No fuzzing of malformed CSV or YAML beyond the cases listed in `tests/`.
- Compatibility with agent clients other than the one used here is untested (see README).
