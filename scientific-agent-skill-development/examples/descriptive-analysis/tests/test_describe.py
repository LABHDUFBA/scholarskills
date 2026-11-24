#!/usr/bin/env python3
"""Tests for the descriptive-analysis reference example."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "describe.py"
SAMPLE = HERE.parent / "examples" / "sample.csv"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


class Positive(unittest.TestCase):
    def test_summarises_numeric_columns(self) -> None:
        proc = run(str(SAMPLE), "--json")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        data = json.loads(proc.stdout)
        cols = {c["column"] for c in data["columns"]}
        self.assertEqual(cols, {"id", "idade", "renda_mensal", "anos_estudo"})
        renda = next(c for c in data["columns"] if c["column"] == "renda_mensal")
        self.assertEqual(renda["missing"], 2)
        self.assertGreater(renda["mean"], renda["median"])  # right-skewed by construction

    def test_non_numeric_column_is_skipped(self) -> None:
        data = json.loads(run(str(SAMPLE), "--json").stdout)
        self.assertIn("municipio", data["skipped"])


class Negative(unittest.TestCase):
    def test_missing_file_exits_2(self) -> None:
        proc = run("does-not-exist.csv")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("not found", proc.stderr)

    def test_no_numeric_column_exits_2(self) -> None:
        proc = run(str(HERE.parent / "examples" / "no_numeric.csv"))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("no numeric column", proc.stderr)

    def test_does_not_coerce_text_to_number(self) -> None:
        data = json.loads(run(str(SAMPLE), "--json").stdout)
        self.assertNotIn("municipio", {c["column"] for c in data["columns"]})


class Edge(unittest.TestCase):
    def test_empty_file_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty.csv"
            empty.write_text("", encoding="utf-8")
            proc = run(str(empty))
            self.assertEqual(proc.returncode, 2)
            self.assertIn("empty", proc.stderr)

    def test_single_value_column_warns_and_reports_zero_sd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "single.csv"
            # column x has exactly one value (the other rows are empty), which is the
            # condition that must produce the warning and stdev 0.0
            f.write_text("x,y\n5,1\n,2\n,3\n", encoding="utf-8")
            proc = run(str(f), "--json")
            self.assertEqual(proc.returncode, 0)
            self.assertIn("single value", proc.stderr)
            data = json.loads(proc.stdout)
            x = next(c for c in data["columns"] if c["column"] == "x")
            self.assertEqual(x["stdev"], 0.0)
            self.assertEqual(x["n"], 1)

    def test_header_only_file_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "header.csv"
            f.write_text("a,b\n", encoding="utf-8")
            proc = run(str(f))
            self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
