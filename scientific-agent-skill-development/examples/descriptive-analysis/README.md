# descriptive-analysis — reference example

A deliberately small skill built with the SS-0000 protocol, included so that the protocol has a
worked example whose correctness can be checked by reading it.

## Run

```bash
python3 scripts/describe.py examples/sample.csv
python3 scripts/describe.py examples/sample.csv --json
```

## What to expect

- `idade`, `renda_mensal` and `anos_estudo` are summarised; `municipio` is skipped as non-numeric.
- `renda_mensal` shows a high mean with a visible spread — the case where mean and median diverge.
- Row 6 has empty numeric cells: they are counted as `missing`, not as zero.

## Failure behaviour (by design)

```bash
python3 scripts/describe.py does-not-exist.csv     # exit 2, names the path
python3 scripts/describe.py examples/no_numeric.csv  # exit 2, lists the columns
```

## Data

`examples/sample.csv` is **synthetic**. It does not correspond to real people and must not be
presented as data from any survey.
