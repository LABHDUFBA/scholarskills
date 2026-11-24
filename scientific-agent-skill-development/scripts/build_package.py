#!/usr/bin/env python3
"""Scaffold a new ScholarSkills package from the canonical template.

Copies skill-template/ into a new directory, substituting slug, title, author and
affiliation. It does NOT fill in the method, the tests or the limitations: those
require a human decision, and a generator that invents them would produce the
exact artefact this project exists to avoid.

Usage:
    python3 build_package.py --slug my-skill --title "My Skill" --out ../my-skill \
        --author "Name" --affiliation "Institution" [--template ../../skill-template]

Exit codes: 0 created, 1 refused (invalid slug / destination exists), 2 usage error.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKIP_NAMES = {".git", "__pycache__", ".venv", "node_modules"}


def default_template() -> Path:
    # scripts/ -> skill root -> repo root -> skill-template/
    here = Path(__file__).resolve()
    return here.parents[2] / "skill-template"


def copy_tree(src: Path, dst: Path) -> list[str]:
    copied = []
    for item in sorted(src.rglob("*")):
        if any(part in SKIP_NAMES for part in item.parts):
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied.append(str(rel))
    return copied


def substitute(path: Path, mapping: dict[str, str]) -> None:
    if path.suffix.lower() not in {".md", ".yml", ".yaml", ".json", ".cff", ".txt", ".py"}:
        return
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    original = text
    for key, value in mapping.items():
        text = text.replace(key, value)
    if text != original:
        path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Create a ScholarSkills package from the template.")
    ap.add_argument("--slug", required=True, help="Agent Skills name (lowercase, hyphens)")
    ap.add_argument("--title", required=True, help="Human-readable title")
    ap.add_argument("--out", required=True, type=Path, help="Destination directory")
    ap.add_argument("--author", default="", help="Primary author, 'Family, Given'")
    ap.add_argument("--affiliation", default="", help="Author affiliation")
    ap.add_argument("--template", type=Path, default=None)
    ap.add_argument("--skill-id", default="", help="Requested identifier, e.g. SS-0001")
    args = ap.parse_args(argv)

    if not SLUG_RE.match(args.slug) or len(args.slug) > 64:
        print(f"REFUSED: slug '{args.slug}' violates the Agent Skills naming rules "
              "(1-64 chars, lowercase a-z/0-9, single hyphens, no edge hyphen).", file=sys.stderr)
        return 1

    template = args.template or default_template()
    if not (template / "SKILL.md").exists():
        print(f"REFUSED: template not found at {template}", file=sys.stderr)
        return 2

    out: Path = args.out.resolve()
    if out.exists() and any(out.iterdir()):
        print(f"REFUSED: destination {out} exists and is not empty.", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)

    copied = copy_tree(template, out)

    # The template's placeholder markers are built at runtime so that this source file
    # does not itself contain an unresolved placeholder (the validator scans every file).
    mark = "TODO" + "(SS)"
    mapping = {
        "your-skill-name": args.slug,
        f"{mark}: skill title": args.title,
        f"{mark}, {mark}": args.author or f"{mark}, {mark}",
    }
    if args.skill_id:
        mapping["SS-XXXX"] = args.skill_id

    for rel in copied:
        substitute(out / rel, mapping)

    print(f"created: {out}")
    print(f"  files: {len(copied)}")
    print("  next: fill the method and tests, then run")
    print(f"        python3 {Path(__file__).name} --help")
    print(f"        python3 validate_skill.py {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
