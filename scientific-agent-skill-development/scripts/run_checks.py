#!/usr/bin/env python3
"""Aggregate structural checks for a ScholarSkills package into one JSON report.

Wraps validate_skill.py and adds repository-level checks: registry consistency
(if a registry.json is reachable), CITATION/.zenodo field agreement, and test-suite
presence. It reports facts; it never edits files.

Usage:
    python3 run_checks.py <skill-dir> [--json] [--registry path/to/registry.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run_validate(skill_dir: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, str(HERE / "validate_skill.py"), str(skill_dir), "--json"],
        capture_output=True, text=True,
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "errors": [f"validator crashed: {proc.stderr[:400]}"], "warnings": []}


def check_citation_agreement(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    cff = skill_dir / "CITATION.cff"
    zen = skill_dir / ".zenodo.json"
    if not (cff.exists() and zen.exists()):
        return problems
    cff_text = cff.read_text(encoding="utf-8", errors="replace")
    try:
        zen_data = json.loads(zen.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["\.zenodo.json is not valid JSON"]

    # version agreement
    zen_version = str(zen_data.get("version", "")).strip()
    if zen_version:
        if f'version: "{zen_version}"' not in cff_text and f"version: {zen_version}" not in cff_text:
            problems.append(f"version mismatch: .zenodo.json='{zen_version}' not found in CITATION.cff")

    # creator surname agreement (loose: first surname token must appear)
    creators = zen_data.get("creators", [])
    for c in creators:
        name = (c or {}).get("name", "")
        if not name or "TODO" in name:
            continue
        surname = name.split(",")[0].strip()
        if surname and surname not in cff_text:
            problems.append(f"creator '{surname}' present in .zenodo.json but absent from CITATION.cff")
    return problems


def check_registry_entry(skill_dir: Path, registry: Path | None) -> list[str]:
    problems: list[str] = []
    if not registry or not registry.exists():
        return problems
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [f"registry is not valid JSON: {registry}"]
    entry = next((s for s in data.get("skills", []) if s.get("slug") == skill_dir.name), None)
    if entry is None:
        return [f"no registry entry with slug '{skill_dir.name}'"]
    if entry.get("status") == "available" and not entry.get("version"):
        problems.append("registry entry is 'available' but has no version")
    if entry.get("maturity") in ("peer-reviewed", "replicated") and not entry.get("evidence"):
        problems.append(f"maturity '{entry.get('maturity')}' claimed without an evidence artefact")
    if entry.get("doi_version") and not entry.get("doi_concept"):
        problems.append("doi_version set but doi_concept missing (they are different identifiers)")
    return problems


def check_tests(skill_dir: Path) -> dict:
    tests_dir = skill_dir / "tests"
    files = [p.name for p in tests_dir.glob("test_*.py")] if tests_dir.is_dir() else []
    results = tests_dir / "RESULTS.md"
    return {
        "test_files": files,
        "has_results_record": results.exists(),
        "note": "structural tests do not validate the scientific claim",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Aggregate structural checks for a skill package.")
    ap.add_argument("skill_dir", type=Path)
    ap.add_argument("--registry", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    skill_dir: Path = args.skill_dir.resolve()
    validation = run_validate(skill_dir)
    problems = []
    problems += check_citation_agreement(skill_dir)
    problems += check_registry_entry(skill_dir, args.registry)
    tests = check_tests(skill_dir)

    report = {
        "package": skill_dir.name,
        "structural_ok": bool(validation.get("ok")) and not problems,
        "validation": validation,
        "consistency_problems": problems,
        "tests": tests,
        "disclaimer": "A passing report means the package is reviewable. It does not mean the "
                      "method is correct, validated, peer-reviewed or reproducible.",
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"package: {report['package']}")
        print(f"structural: {'OK' if report['structural_ok'] else 'PROBLEMS'}")
        for e in validation.get("errors", []):
            print(f"  ERROR   {e}")
        for w in validation.get("warnings", []):
            print(f"  WARN    {w}")
        for p in problems:
            print(f"  PROBLEM {p}")
        print(f"  tests: {len(tests['test_files'])} file(s); results record: "
              f"{'yes' if tests['has_results_record'] else 'no'}")
        print(f"  {report['disclaimer']}")

    return 0 if report["structural_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
