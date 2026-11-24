#!/usr/bin/env python3
"""Validate an Agent Skills package for ScholarSkills submission.

Checks the *structure* of a skill package, not its scientific validity.
A green result means "reviewable", never "correct method".

Usage:
    python3 validate_skill.py <skill-dir> [--json] [--allow-template] [--strict]

Exit codes:
    0  all checks passed (warnings may exist)
    1  at least one error
    2  usage or environment error (missing PyYAML, unreadable path)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml). "
          "Refusing to parse YAML with regex: a false pass is worse than a failure.",
          file=sys.stderr)
    raise SystemExit(2)

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_FILES = ("SKILL.md", "README.md", "CITATION.cff", "LICENSE", "CHANGELOG.md")
OPTIONAL_RECOMMENDED = (".zenodo.json",)
PLACEHOLDER_RE = re.compile(r"TODO\(SS\)|TODO\(SKILL\)|\bTBD:|\bFIXME:|\bTODO:")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Deliberately narrow patterns: false positives on prose are expensive and train
# authors to suppress the check. These are credential shapes, not words.
SECRET_PATTERNS = [
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("zenodo_token", re.compile(r"\b[A-Za-z0-9]{40,}\b(?=.{0,40}zenodo)", re.I)),
    ("aws_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("generic_bearer", re.compile(r"\bBearer\s+[A-Za-z0-9\-._~+/]{20,}=*")),
    ("openai_like", re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
]

TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".cff", ".txt", ".py", ".sh", ".toml"}


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: dict = {}

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
        }


def parse_frontmatter(text: str) -> tuple[dict, str, str | None]:
    """Return (frontmatter, body, error)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text, "SKILL.md must start with YAML frontmatter delimited by '---'"
    raw = m.group(1)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return {}, text[m.end():], f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return {}, text[m.end():], "frontmatter must be a mapping of keys to values"
    return data, text[m.end():], None


def check_name(fm: dict, skill_dir: Path, res: Result, allow_template: bool) -> None:
    name = fm.get("name")
    if not isinstance(name, str) or not name:
        res.error("frontmatter.name is required and must be a string")
        return
    res.info["name"] = name
    if len(name) > 64:
        res.error(f"name exceeds 64 characters ({len(name)})")
    if not NAME_RE.match(name):
        res.error(
            f"name '{name}' violates the specification: lowercase a-z, 0-9 and single hyphens "
            "between segments, no leading/trailing hyphen, no consecutive hyphens"
        )
    if not allow_template and name != skill_dir.name:
        res.error(
            f"name '{name}' must equal the skill directory name '{skill_dir.name}' "
            "(use --allow-template only for the template itself)"
        )


def check_description(fm: dict, res: Result) -> None:
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        res.error("frontmatter.description is required and must be a non-empty string")
        return
    res.info["description_length"] = len(desc)
    if len(desc) > 1024:
        res.error(f"description exceeds 1024 characters ({len(desc)})")
    if len(desc.strip()) < 40:
        res.warn("description is very short; it must say what the skill does AND when to use it")
    lowered = desc.lower()
    if not any(k in lowered for k in ("use when", "use para", "when the user", "when an agent",
                                      "use ao", "activate")):
        res.warn("description does not appear to state when the skill should be used")


def check_optional_fields(fm: dict, res: Result) -> None:
    if "license" in fm and not isinstance(fm["license"], str):
        res.error("license, when present, must be a string")
    if "compatibility" in fm:
        comp = fm["compatibility"]
        if not isinstance(comp, str):
            res.error("compatibility, when present, must be a string")
        elif len(comp) > 500:
            res.error(f"compatibility exceeds 500 characters ({len(comp)})")
    if "metadata" in fm:
        md = fm["metadata"]
        if not isinstance(md, dict):
            res.error("metadata, when present, must be a mapping")
        else:
            for k, v in md.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    res.error(f"metadata.{k} must map a string key to a string value")
    if "allowed-tools" in fm and not isinstance(fm["allowed-tools"], str):
        res.error("allowed-tools, when present, must be a space-separated string")


def check_files(skill_dir: Path, res: Result) -> None:
    for fname in REQUIRED_FILES:
        if not (skill_dir / fname).exists():
            res.error(f"required file missing: {fname}")
    for fname in OPTIONAL_RECOMMENDED:
        if not (skill_dir / fname).exists():
            res.warn(f"recommended file missing: {fname} (needed for deposit)")
    for sub in ("references", "scripts", "examples", "tests", "benchmarks"):
        p = skill_dir / sub
        if not p.is_dir():
            res.warn(f"conventional directory missing: {sub}/")
        else:
            entries = [x for x in p.iterdir() if x.name != ".gitkeep"]
            if not entries:
                res.warn(f"{sub}/ exists but is empty — a reviewer will ask what belongs there")


def check_body(body: str, res: Result) -> None:
    if len(body.strip()) < 200:
        res.error("SKILL.md body is too short to be operational (< 200 characters)")
    lines = body.count("\n") + 1
    res.info["body_lines"] = lines
    if lines > 500:
        res.warn(f"SKILL.md body has {lines} lines; move detail to references/ (guideline: <500)")


def check_links(skill_dir: Path, res: Result) -> None:
    for md in sorted(skill_dir.rglob("*.md")):
        rel = md.relative_to(skill_dir)
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            res.warn(f"could not read {rel}: {exc}")
            continue
        for target in MD_LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0].strip()
            if not clean:
                continue
            if not (md.parent / clean).exists():
                res.error(f"{rel}: broken local link -> {target}")


def check_placeholders(skill_dir: Path, res: Result, allow: bool = False) -> None:
    hits = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name == Path(__file__).name:  # the checker documents the marker it looks for
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                hits.append(f"{path.relative_to(skill_dir)}:{lineno}")
    if hits:
        res.info["placeholders"] = len(hits)
        if allow:
            res.warn(f"{len(hits)} placeholder(s) allowed because this is the template")
            return
        res.error(
            "unresolved placeholders (a package with a placeholder is not reviewable): "
            + ", ".join(hits[:12]) + (" ..." if len(hits) > 12 else "")
        )


def check_secrets(skill_dir: Path, res: Result) -> None:
    found = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        # A validator that scans itself would always fail; skip this file.
        if path.name == Path(__file__).name:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                found.append(f"{path.relative_to(skill_dir)} [{label}]")
    if found:
        res.error("possible credential material: " + ", ".join(found) + " — remove and rotate")


def check_citation(skill_dir: Path, res: Result) -> None:
    cff = skill_dir / "CITATION.cff"
    if not cff.exists():
        return
    text = cff.read_text(encoding="utf-8", errors="replace")
    if "cff-version" not in text:
        res.error("CITATION.cff must declare cff-version")
    if "doi" in text.lower():
        for line in text.splitlines():
            if "doi" in line.lower() and not line.strip().startswith("#"):
                if re.search(r"10\.5281/zenodo\.(0|1234)", line):
                    res.error("CITATION.cff contains a placeholder DOI; use a real one or omit it")


def check_registry_entry(skill_dir: Path, res: Result) -> None:
    reg = skill_dir / ".zenodo.json"
    if not reg.exists():
        return
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        res.error(f".zenodo.json is not valid JSON: {exc}")
        return
    for key in ("title", "description", "upload_type", "creators"):
        if key not in data:
            res.error(f".zenodo.json missing required key: {key}")
    if data.get("upload_type") not in (None, "software", "other", "publication"):
        res.warn(f"unexpected upload_type: {data.get('upload_type')}")


def validate(skill_dir: Path, allow_template: bool = False,
             allow_placeholders: bool = False) -> Result:
    res = Result()
    if not skill_dir.exists() or not skill_dir.is_dir():
        res.error(f"not a directory: {skill_dir}")
        return res

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        res.error("SKILL.md is required")
        return res

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, body, err = parse_frontmatter(text)
    if err:
        res.error(err)
        return res

    check_name(fm, skill_dir, res, allow_template)
    check_description(fm, res)
    check_optional_fields(fm, res)
    check_body(body, res)
    check_files(skill_dir, res)
    check_links(skill_dir, res)
    check_placeholders(skill_dir, res, allow=allow_placeholders)
    check_secrets(skill_dir, res)
    check_citation(skill_dir, res)
    check_registry_entry(skill_dir, res)
    res.info["path"] = str(skill_dir)
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate a ScholarSkills / Agent Skills package.")
    ap.add_argument("skill_dir", type=Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--allow-template", action="store_true",
                    help="skip the name==directory check (only for skill-template/)")
    ap.add_argument("--allow-placeholders", action="store_true",
                    help="do not fail on placeholder markers (only for skill-template/)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    args.skill_dir = args.skill_dir.resolve()
    res = validate(args.skill_dir, allow_template=args.allow_template,
                   allow_placeholders=args.allow_placeholders)
    if args.strict and res.warnings:
        res.errors.extend(f"[strict] {w}" for w in res.warnings)

    if args.json:
        print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
    else:
        label = res.info.get("name", args.skill_dir.name)
        print(f"validating: {args.skill_dir}  (name: {label})")
        for e in res.errors:
            print(f"  ERROR   {e}")
        for w in res.warnings:
            print(f"  WARN    {w}")
        if res.ok:
            print(f"  PASS    {len(res.warnings)} warning(s)")
        else:
            print(f"  FAIL    {len(res.errors)} error(s), {len(res.warnings)} warning(s)")
    return 0 if res.ok else 1


if __name__ == "__main__":
    sys.exit(main())
