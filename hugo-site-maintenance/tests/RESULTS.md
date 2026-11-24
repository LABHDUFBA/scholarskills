# Test results — SS-0012 (hugo-site-maintenance)

Recorded from a real execution.

## Environment

```
Python 3.14.9
network: not used by the test suite (temporary site built in a tmpdir)
date: 2026-11-24T15:32:53
```

## Command

```bash
python3 -m unittest discover -s tests -v
```

## Result

```
Ran 19 tests in 0.018s

OK
```

## Coverage

| Case type | Tests |
|---|---|
| Positive | clean page passes, image with alt passes, existing internal target passes, external links ignored |
| Negative | missing title, image without alt (Markdown and HTML), broken internal link, missing content dir |
| Edge | no front matter, empty body, `draft: true`, unparseable date, duplicate titles, nested pages |
| Robustness | malformed YAML does not raise; site-root and relative hrefs both resolved |

## What is not covered

- `hugo` is not executed: the suite audits the content tree, not the rendered build.
- Shortcode arguments and theme internals are out of scope.
