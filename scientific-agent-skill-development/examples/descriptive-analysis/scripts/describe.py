#!/usr/bin/env python3
"""Descriptive statistics for numeric columns of a CSV file.

Refuses explicitly instead of coercing data: a table of numbers computed from
non-numbers is worse than an error message.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path


def classify(values: list[str]) -> tuple[bool, list[float]]:
    """Return (is_numeric, numbers). Empty strings are skipped, not zero."""
    nums: list[float] = []
    for v in values:
        s = (v or "").strip()
        if not s:
            continue
        try:
            nums.append(float(s))
        except ValueError:
            return False, []
    return True, nums


def summarise(path: Path) -> tuple[list[dict], list[str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError("no header row")
        rows = list(reader)
    if not rows:
        raise ValueError("file has no data rows")

    results: list[dict] = []
    skipped: list[str] = []
    for col in reader.fieldnames:
        values = [r.get(col, "") for r in rows]
        is_num, nums = classify(values)
        missing = sum(1 for v in values if not (v or "").strip())
        if not is_num or not nums:
            skipped.append(col)
            continue
        results.append({
            "column": col,
            "n": len(nums),
            "mean": round(statistics.fmean(nums), 6),
            "median": round(statistics.median(nums), 6),
            "stdev": round(statistics.stdev(nums), 6) if len(nums) > 1 else 0.0,
            "min": min(nums),
            "max": max(nums),
            "missing": missing,
        })
    return results, skipped


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Descriptive statistics for numeric CSV columns.")
    ap.add_argument("path", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.path.exists():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2
    if args.path.stat().st_size == 0:
        print("error: file is empty", file=sys.stderr)
        return 2

    try:
        results, skipped = summarise(args.path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not results:
        print("error: no numeric column found. Columns present: "
              + ", ".join(skipped), file=sys.stderr)
        return 2

    for row in results:
        if row["n"] == 1:
            print(f"warning: column '{row['column']}' has a single value; "
                  "standard deviation is reported as 0.0", file=sys.stderr)

    if args.json:
        print(json.dumps({"columns": results, "skipped": skipped}, indent=2, ensure_ascii=False))
    else:
        header = f"{'column':<20}{'n':>6}{'mean':>12}{'median':>12}{'stdev':>12}{'min':>10}{'max':>10}{'miss':>6}"
        print(header)
        print("-" * len(header))
        for r in results:
            print(f"{r['column']:<20}{r['n']:>6}{r['mean']:>12.4f}{r['median']:>12.4f}"
                  f"{r['stdev']:>12.4f}{r['min']:>10.4f}{r['max']:>10.4f}{r['missing']:>6}")
        if skipped:
            print(f"\nnon-numeric columns skipped: {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
