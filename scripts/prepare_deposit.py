#!/usr/bin/env python3
"""Prepare a Zenodo deposit without performing it.

The generation step makes **no network call**. It produces:

    deposit/scholarskills-<version>.zip   the archive to upload
    deposit/manifest.json                 files, hashes, sizes and metadata
    deposit/CHECKLIST.md                  what a human must confirm before publishing

Publishing, reserving a DOI and choosing a definitive licence are human decisions; this script stops
one step before them on purpose.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "site", "deposit", ".venv", "node_modules", ".pytest_cache"}
SKIP_FILES = {".DS_Store"}
SKIP_SUFFIX = {".pyc", ".pyo"}


def git(*args: str, cwd: Path) -> str:
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:
        return ""


def collect(root: Path) -> list[Path]:
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.name in SKIP_FILES or p.suffix in SKIP_SUFFIX:
            continue
        out.append(p)
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_archive(root: Path, files: list[Path], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.relative_to(root).as_posix())


def metadata(root: Path, version: str) -> dict:
    cff = root / "CITATION.cff"
    title = "Digital Methods Skills — executable research methodologies for AI agents"
    if cff.exists():
        for line in cff.read_text(encoding="utf-8").splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip('"')
                break
    return {
        "title": title,
        "upload_type": "software",
        "version": version,
        "publication_date": datetime.now(timezone.utc).date().isoformat(),
        "description": (
            "<p>A catalogue of executable research methodologies for AI agents, each one a package "
            "with a specification, a test suite, a licence and an explicit statement of what it does "
            "not do. Every entry declares the research stage it serves, the disciplines it was "
            "designed for and the credentials the operator must provide. Validation is structural "
            "and is reported as such: passing the suite proves conformance, not scientific "
            "correctness.</p>"
        ),
        "creators": [
            {"name": "Nascimento, Leonardo Fernandes",
             "affiliation": "Digital Humanities Laboratory (LABHDUFBA), Federal University of Bahia"},
            {"name": "Brasil, Eric",
             "affiliation": "University of International Integration of Afro-Brazilian Lusophony (UNILAB)"},
            {"name": "Sodré, Ricardo", "affiliation": "Federal University of Bahia"},
        ],
        "license": "mit",
        "access_right": "open",
        "language": "eng",
        "keywords": ["agent skills", "research methods", "reproducibility", "open science",
                     "digital humanities", "methodology"],
        "related_identifiers": [
            {"identifier": "https://github.com/LABHDUFBA/scholarskills",
             "relation": "isSupplementTo", "scheme": "url"},
            {"identifier": "https://labhdufba.github.io/scholarskills/",
             "relation": "isDocumentedBy", "scheme": "url"},
        ],
    }


CHECKLIST = """# Deposit checklist — {title}

Generated {when} from `{commit}`. **Nothing has been published.**

## What was built

| Item | Value |
|---|---|
| Archive | `{zipname}` |
| Files | {nfiles} |
| Size | {size:.1f} MiB |
| SHA-256 | `{digest}` |
| Version | {version} |

## Decisions that need a human

- [ ] **Title** — `{title}`
- [ ] **Author order** — the manifest lists Nascimento, Brasil, Sodré. Confirm the order.
- [ ] **Licence** — confirm MIT for original code and associated documentation; review rights
      to third-party assets separately before the deposit.
- [ ] **DOI policy** — one DOI per repository release, not per skill. Confirm that a new release
      should mint a new version DOI.
- [ ] **Community** — a Zenodo community can only be created in the web interface; decide whether
      one is wanted before publishing.

## Steps after approval

1. Activate the repository in <https://zenodo.org/account/settings/github/>.
2. Confirm the webhook exists: `gh api repos/LABHDUFBA/scholarskills/hooks`.
3. Publish the release that matches this archive.
4. Read the concept DOI and the version DOI from Zenodo, then record them:
   `python3 scripts/set_doi.py --concept <DOI> --version <DOI>`.
5. Rebuild the hub and confirm the DOI appears on the site.

## What this archive does not prove

Structural validation only. Each package's `tests/RESULTS.md` records the environment and the result
of its own suite; none of it is peer review.
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Prepare (never publish) a Zenodo deposit.")
    ap.add_argument("--root", default=".", help="repository root")
    ap.add_argument("--version", required=True, help="version to deposit, e.g. 1.1.0")
    ap.add_argument("--out", default="deposit")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    out = root / args.out
    files = collect(root)
    if not files:
        print("nothing to archive", file=sys.stderr)
        return 1

    zipname = f"scholarskills-{args.version}.zip"
    target = out / zipname
    build_archive(root, files, target)

    digest = sha256(target)
    size = target.stat().st_size / (1024 * 1024)
    commit = git("rev-parse", "--short", "HEAD", cwd=root)
    meta = metadata(root, args.version)

    manifest = {
        "metadata": meta,
        "archive": {"name": zipname, "sha256": digest,
                    "size_bytes": target.stat().st_size},
        "source": {"repository": "https://github.com/LABHDUFBA/scholarskills",
                   "commit": commit, "generated": datetime.now(timezone.utc).isoformat()},
        "files": [{"path": f.relative_to(root).as_posix(),
                   "bytes": f.stat().st_size, "sha256": sha256(f)} for f in files],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    (out / "CHECKLIST.md").write_text(
        CHECKLIST.format(title=meta["title"], when=manifest["source"]["generated"],
                         commit=commit or "(no git)", zipname=zipname, nfiles=len(files),
                         size=size, digest=digest, version=args.version),
        encoding="utf-8")

    print(f"archive : {target} ({size:.1f} MiB)")
    print(f"sha256  : {digest}")
    print(f"files   : {len(files)}")
    print(f"manifest: {out / 'manifest.json'}")
    print("nothing was uploaded; see CHECKLIST.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
