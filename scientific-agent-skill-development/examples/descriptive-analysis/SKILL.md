---
name: descriptive-analysis
description: Compute descriptive statistics (n, mean, median, standard deviation, min, max, missing count) for numeric columns of a CSV file, and refuse explicitly when a column cannot be summarised. Use when an agent must characterise a tabular dataset before modelling, or check whether a distribution is skewed or has missing values.
license: MIT
compatibility: Requires Python 3.10+ and only the standard library. No network access.
metadata:
  scholarskills.id: SS-EXAMPLE
  scholarskills.version: "0.2.0"
  scholarskills.maturity: tested
  scholarskills.method: descriptive statistics (measures of central tendency and dispersion)
---

# Descriptive Analysis

Summarises numeric columns so that a later step (modelling, comparison, reporting) starts from what
the data actually looks like.

## When to use

- Before any model or test: to see distribution, spread and missingness.
- To detect that a column is constant, almost empty, or wildly skewed.
- **Do not use** to infer causation, to test hypotheses, or on columns whose meaning is unknown.

## Inputs

| Input | Required | Format |
|---|---|---|
| `path` | yes | CSV with header row, comma separated |

## Outputs

A table with one row per numeric column: `n`, `mean`, `median`, `stdev`, `min`, `max`, `missing`.
With `--json`, the same content as a JSON object.

## Procedure

1. Read the CSV with the standard library `csv` module (no pandas dependency, so the skill runs
   anywhere).
2. Classify columns: numeric if every non-empty value parses as a float.
3. For each numeric column compute the statistics, ignoring empty cells and counting them as
   `missing`.
4. Print the table. With `--json`, print JSON instead.

## Stop criteria

- Stop with an explicit error if the file does not exist, is empty, or has no header.
- Stop if **no** column is numeric: reporting an empty table would look like a valid result.
- Do not coerce non-numeric text into numbers. Refusing is the correct behaviour.

## Error handling

| Situation | Behaviour |
|---|---|
| Missing file | exit 2 with a message naming the path |
| Empty file | exit 2, "file is empty" |
| No numeric column | exit 2, listing the columns found |
| Column with a single value | stdev reported as 0.0, with a warning on stderr |
| Mixed numeric/text | the column is skipped and reported as non-numeric |

## Limits

- Assumes values are on a meaningful numeric scale; the mean of an ordinal scale may be misleading.
- Does not detect bimodality: a mean can hide two clusters.
- Ignores missing data mechanism; `missing` is a count, not an analysis.

## Tools and dependencies

Python standard library only.

## Validation

`python3 -m unittest discover -s tests` in the parent project exercises positive, negative and edge
cases of this script.

## References

See `references/methodology.md`.
