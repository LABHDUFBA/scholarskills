#!/usr/bin/env python3
"""Prepare — never perform — a Zenodo deposit for a ScholarSkills package.

Produces:
  deposit/<slug>-<version>.zip     archive of the package
  deposit/<slug>-<version>.zip.sha256
  deposit/zenodo-metadata.json     metadata to paste or POST
  deposit/AUTHORISATION-CHECKLIST.md  what only a human can approve

It does not create records, does not reserve DOIs, does not contact Zenodo.
Any call to the Zenodo API belongs to the operator, after authorisation, and is
recorded in DEPLOYMENT_LOG.md.

Usage:
    python3 generate_metadata.py <skill-dir> [--out deposit/] [--version 1.0.0]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required.", file=sys.stderr)
    raise SystemExit(2)

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}


def read_frontmatter(skill_dir: Path) -> dict:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        raise SystemExit("SKILL.md has no YAML frontmatter")
    return yaml.safe_load(m.group(1)) or {}


def build_zip(skill_dir: Path, dest: Path) -> Path:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.is_file():
                zf.write(path, path.relative_to(skill_dir.parent))
    return dest


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def metadata_from_package(skill_dir: Path, version: str) -> dict:
    fm = read_frontmatter(skill_dir)
    meta = dict(fm.get("metadata") or {})
    zenodo_path = skill_dir / ".zenodo.json"
    base: dict = {}
    if zenodo_path.exists():
        base = json.loads(zenodo_path.read_text(encoding="utf-8"))
    payload = {
        "title": base.get("title") or meta.get("scholarskills.title") or skill_dir.name,
        "description": base.get("description") or fm.get("description", ""),
        "upload_type": base.get("upload_type", "software"),
        "access_right": base.get("access_right", "open"),
        "license": base.get("license", "mit"),
        "version": version,
        "publication_date": date.today().isoformat(),
        "creators": base.get("creators", []),
        "keywords": base.get("keywords", []),
        "language": base.get("language", "eng"),
        "notes": base.get("notes", ""),
        "related_identifiers": base.get("related_identifiers", []),
    }
    return payload


CHECKLIST = """# Authorisation checklist — {title} v{version}

Only a human operator can close these items. Nothing below has been done automatically.

## 1. Authorship and rights
- [ ] Every creator listed in `zenodo-metadata.json` agreed to be listed, in that order.
- [ ] ORCID values (if present) belong to the right person and are public.
- [ ] Affiliation is stated as the institution itself requires (LABHDUFBA / UFBA wording checked).
- [ ] Intellectual property: the institution has been consulted if the material was produced under
      contract, grant or employment that assigns rights.
- [ ] Licence chosen and approved (code: MIT or Apache-2.0; documentation: CC BY 4.0).

## 2. Content
- [ ] No personal data, no third-party private content, no credential in the package.
- [ ] The example dataset is synthetic or public, and is stated as such.
- [ ] Limitations section describes where the method does not hold.
- [ ] Maturity level matches the evidence present in the repository.

## 3. Deposit route — choose ONE
- [ ] **GitHub integration**: repository authorised in Zenodo settings, release published, record and
      DOI generated, deposit requested for the community.
- [ ] **Manual/API**: draft created, ZIP uploaded, metadata filled, DOI reserved **if** the DOI must
      appear inside the files (never deposit twice by both routes).

## 4. Before publishing
- [ ] SHA-256 of the ZIP matches `{sha256}`.
- [ ] Version number and file list reviewed.
- [ ] Visibility (open/restricted) is deliberate.
- [ ] This deposit is on **production** Zenodo, not sandbox. Sandbox DOIs are never presented as
      scientific identifiers.

## 5. After publishing
- [ ] DOI resolves at https://doi.org/ .
- [ ] Version DOI and concept DOI recorded separately in `registry/registry.json`.
- [ ] `CITATION.cff` updated with the identifier (new version if the archived files must change).
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prepare deposit artefacts (no API calls).")
    ap.add_argument("skill_dir", type=Path)
    ap.add_argument("--out", type=Path, default=Path("deposit"))
    ap.add_argument("--version", default=None)
    args = ap.parse_args(argv)

    skill_dir: Path = args.skill_dir.resolve()
    if not (skill_dir / "SKILL.md").exists():
        print(f"ERROR: {skill_dir} has no SKILL.md", file=sys.stderr)
        return 2

    fm = read_frontmatter(skill_dir)
    meta = dict(fm.get("metadata") or {})
    version = args.version or str(meta.get("scholarskills.version") or "0.1.0")

    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    zip_path = out / f"{skill_dir.name}-{version}.zip"
    build_zip(skill_dir, zip_path)
    digest = sha256(zip_path)
    (out / f"{zip_path.name}.sha256").write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    payload = metadata_from_package(skill_dir, version)
    (out / "zenodo-metadata.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (out / "AUTHORISATION-CHECKLIST.md").write_text(
        CHECKLIST.format(title=payload["title"], version=version, sha256=digest), encoding="utf-8")

    print(f"zip:      {zip_path}  ({zip_path.stat().st_size} bytes)")
    print(f"sha256:   {digest}")
    print(f"metadata: {out / 'zenodo-metadata.json'}")
    print(f"checklist:{out / 'AUTHORISATION-CHECKLIST.md'}")
    print("NOTE: nothing was uploaded, reserved or published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
