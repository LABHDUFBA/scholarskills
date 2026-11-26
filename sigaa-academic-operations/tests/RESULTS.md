# Test results — SS-0015 (sigaa-academic-operations)

Recorded from a real offline execution. These tests validate the request protocol and approval gates; they do not log in to a SIGAA deployment.

## Environment

```
Python 3.14.9
network: not used
date: 2026-11-26
```

## Command

```bash
python3 -m unittest discover -s tests -v
```

## Result

```
Ran 7 tests in 0.001s
OK
```

## Coverage

| Case | Covered |
|---|---|
| Positive | valid teaching operation; formal proposal with named call and approval |
| Negative | missing target; missing call; missing approval; invalid boolean |
| Edge | notification e-mail as explicit side effect; synthetic example loading |
| Not covered | live login, browser navigation, file upload, institutional permissions, real proposal submission |
