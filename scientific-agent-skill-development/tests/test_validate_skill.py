#!/usr/bin/env python3
"""Tests for the ScholarSkills validator and builder.

Structure of the suite follows the protocol's own requirement: positive, negative,
edge and tool-failure cases. A suite that only proves the happy path would be the
first thing a reviewer rejects.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
SCRIPTS = SKILL_ROOT / "scripts"
VALIDATOR = SCRIPTS / "validate_skill.py"
BUILDER = SCRIPTS / "build_package.py"
METADATA = SCRIPTS / "generate_metadata.py"
REPO_ROOT = SKILL_ROOT.parent
TEMPLATE = REPO_ROOT / "skill-template"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=cwd)


def make_package(root: Path, name: str, *, description: str | None = None,
                 body: str | None = None, files: dict[str, str] | None = None) -> Path:
    """Create a minimal package that should validate, then let tests break it."""
    pkg = root / name
    (pkg / "references").mkdir(parents=True)
    (pkg / "scripts").mkdir()
    (pkg / "examples").mkdir()
    (pkg / "tests").mkdir()
    (pkg / "benchmarks").mkdir()
    desc = description or (
        "Summarise numeric columns of a CSV file with n, mean, median and stdev. "
        "Use when an agent must characterise a tabular dataset before modelling."
    )
    (pkg / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {desc}\nlicense: MIT\n---\n\n"
        + (body or "# Purpose\n\n" + "Operational instructions. " * 20 + "\n"),
        encoding="utf-8")
    (pkg / "README.md").write_text("# readme\n", encoding="utf-8")
    (pkg / "CITATION.cff").write_text(
        "cff-version: 1.2.0\ntitle: x\nversion: 0.1.0\nauthors:\n  - family-names: Test\n",
        encoding="utf-8")
    (pkg / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (pkg / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    (pkg / ".zenodo.json").write_text(json.dumps({
        "title": "x", "description": "y", "upload_type": "software",
        "creators": [{"name": "Test, A"}]}), encoding="utf-8")
    (pkg / "references" / "methodology.md").write_text("# method\n", encoding="utf-8")
    (pkg / "tests" / "RESULTS.md").write_text("# results\n", encoding="utf-8")
    for rel, content in (files or {}).items():
        target = pkg / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return pkg


class ValidatorPositive(unittest.TestCase):
    def test_valid_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "good-skill")
            proc = run([str(VALIDATOR), str(pkg), "--json"])
            data = json.loads(proc.stdout)
            self.assertTrue(data["ok"], msg=data["errors"])
            self.assertEqual(proc.returncode, 0)

    def test_real_package_in_repo_passes(self) -> None:
        proc = run([str(VALIDATOR), str(SKILL_ROOT), "--json"])
        data = json.loads(proc.stdout)
        self.assertTrue(data["ok"], msg=data["errors"])


class ValidatorNegative(unittest.TestCase):
    def test_uppercase_name_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "bad-skill")
            text = (pkg / "SKILL.md").read_text(encoding="utf-8")
            (pkg / "SKILL.md").write_text(text.replace("name: bad-skill", "name: Bad-Skill"),
                                          encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertFalse(data["ok"])
            self.assertTrue(any("lowercase" in e for e in data["errors"]))

    def test_double_hyphen_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "bad--skill")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertFalse(data["ok"])

    def test_name_directory_mismatch_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "real-dir")
            text = (pkg / "SKILL.md").read_text(encoding="utf-8")
            (pkg / "SKILL.md").write_text(text.replace("name: real-dir", "name: other-name"),
                                          encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("must equal the skill directory" in e for e in data["errors"]))

    def test_missing_description_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "no-desc")
            (pkg / "SKILL.md").write_text("---\nname: no-desc\n---\n\n# body " + "x" * 250,
                                          encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertFalse(data["ok"])

    def test_placeholder_is_hard_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "ph-skill",
                               files={"references/notes.md": "TODO" + "(SS): write the method\n"})
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertFalse(data["ok"])
            self.assertTrue(any("placeholder" in e for e in data["errors"]))

    def test_broken_local_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "link-skill",
                               files={"README.md": "See [method](references/missing.md)\n"})
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("broken local link" in e for e in data["errors"]))

    def test_credential_pattern_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "leak-skill",
                               files={"scripts/run.sh": "export GH=ghp_" + "a" * 30 + "\n"})
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("credential" in e for e in data["errors"]))

    def test_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "incomplete")
            (pkg / "CHANGELOG.md").unlink()
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertIn("required file missing: CHANGELOG.md", data["errors"])


class ValidatorEdge(unittest.TestCase):
    def test_description_over_1024_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "long-desc", description="Use when " + "x" * 1100)
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("1024" in e for e in data["errors"]))

    def test_compatibility_over_500_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "comp-skill")
            text = (pkg / "SKILL.md").read_text(encoding="utf-8")
            (pkg / "SKILL.md").write_text(
                text.replace("license: MIT", f"license: MIT\ncompatibility: {'x' * 501}"),
                encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("compatibility" in e for e in data["errors"]))

    def test_metadata_non_string_value_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "meta-skill")
            text = (pkg / "SKILL.md").read_text(encoding="utf-8")
            (pkg / "SKILL.md").write_text(
                text.replace("license: MIT", "license: MIT\nmetadata:\n  version: 1.0"),
                encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("string" in e for e in data["errors"]))

    def test_short_body_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "thin-skill", body="# x\n")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("too short" in e for e in data["errors"]))


class ValidatorToolFailure(unittest.TestCase):
    def test_nonexistent_path_is_an_error_not_a_crash(self) -> None:
        proc = run([str(VALIDATOR), "/nonexistent/path/xyz", "--json"])
        self.assertEqual(proc.returncode, 1)
        data = json.loads(proc.stdout)
        self.assertFalse(data["ok"])

    def test_missing_frontmatter_reports_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "nofm")
            (pkg / "SKILL.md").write_text("# no frontmatter here\n", encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("frontmatter" in e for e in data["errors"]))

    def test_invalid_yaml_reports_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_package(Path(tmp), "badyaml")
            (pkg / "SKILL.md").write_text("---\nname: [unclosed\n---\n\nbody\n", encoding="utf-8")
            data = json.loads(run([str(VALIDATOR), str(pkg), "--json"]).stdout)
            self.assertTrue(any("YAML" in e for e in data["errors"]))


class Builder(unittest.TestCase):
    def test_rejects_invalid_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = run([str(BUILDER), "--slug", "Bad Slug", "--title", "T",
                        "--out", str(Path(tmp) / "x"), "--template", str(TEMPLATE)])
            self.assertEqual(proc.returncode, 1)
            self.assertIn("REFUSED", proc.stderr)

    def test_refuses_existing_non_empty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "exists"
            dest.mkdir()
            (dest / "keep.txt").write_text("x", encoding="utf-8")
            proc = run([str(BUILDER), "--slug", "ok-slug", "--title", "T",
                        "--out", str(dest), "--template", str(TEMPLATE)])
            self.assertEqual(proc.returncode, 1)

    def test_scaffold_then_validate_fails_on_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "new-skill"
            proc = run([str(BUILDER), "--slug", "new-skill", "--title", "New Skill",
                        "--out", str(dest), "--template", str(TEMPLATE),
                        "--author", "Silva, Ana", "--affiliation", "UFBA"])
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertTrue((dest / "SKILL.md").exists())
            data = json.loads(run([str(VALIDATOR), str(dest), "--json"]).stdout)
            self.assertFalse(data["ok"], "a scaffold must not pass validation untouched")
            self.assertTrue(any("placeholder" in e for e in data["errors"]))


class MetadataGeneration(unittest.TestCase):
    def test_produces_zip_and_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "deposit"
            proc = run([str(METADATA), str(SKILL_ROOT), "--out", str(out)])
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            zips = list(out.glob("*.zip"))
            self.assertEqual(len(zips), 1)
            self.assertTrue((out / (zips[0].name + ".sha256")).exists())
            self.assertTrue((out / "zenodo-metadata.json").exists())
            self.assertTrue((out / "AUTHORISATION-CHECKLIST.md").exists())
            payload = json.loads((out / "zenodo-metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["upload_type"], "software")
            self.assertNotIn("doi", payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
