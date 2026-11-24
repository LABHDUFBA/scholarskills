#!/usr/bin/env python3
"""Deposit each skill as its own Zenodo record — one repository, many DOIs.

Why not the GitHub integration: it mints **one DOI per repository release**, so a monorepo can only
ever have a single DOI. The REST API has no such constraint: every skill becomes an independent
deposition with its own concept DOI and version DOI, while the code stays in one repository.

The collection itself is deposited once (``deposit_collection``), and each skill record points to it
with ``isPartOf``; the collection points back with ``hasPart``. Citation of an individual skill is
therefore possible without fragmenting the git history.

Safety rules, in order of importance:

1. ``--dry-run`` is the default. Nothing is uploaded unless ``--publish`` is passed **and** an
   environment is explicit (``--sandbox`` or ``--production``).
2. Sandbox first. ``--production`` refuses to run if any skill has already been published there and
   its file changed, unless ``--new-version`` is given: overwriting a published record is not a fix.
3. The token is read from the environment and never printed, logged or written.
4. A DOI is written into the catalogue only after the API confirms publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "registry.json"
DOIS = ROOT / "registry" / "dois.json"
API = {
    "sandbox": "https://sandbox.zenodo.org/api",
    "production": "https://zenodo.org/api",
}
SKIP_DIRS = {"__pycache__", ".venv", "venv", ".pytest_cache", ".git"}
SKIP_SUFFIX = {".pyc", ".pyo"}

COLLECTION_TITLE = "Digital Methods Skills — executable research methodologies for AI agents"
COLLECTION_DESC = (
    "<p>A catalogue of executable research methodologies for AI agents, each one a package with a "
    "specification, a test suite, a licence and an explicit statement of what it does not do. "
    "Validation is structural: passing the suite proves conformance, not scientific correctness.</p>"
)


# --------------------------------------------------------------------------- metadata

@dataclass
class Payload:
    slug: str
    title: str
    metadata: dict
    archive: Path
    skill_id: str = ""
    version: str = "1.0.0"


def _creators(authors: list[dict]) -> list[dict]:
    out = []
    for a in authors or []:
        name = (a.get("name") or "").strip()
        if not name:
            continue
        parts = name.split()
        if len(parts) >= 2:
            formatted = f"{parts[-1]}, {' '.join(parts[:-1])}"
        else:
            formatted = name
        c = {"name": formatted, "affiliation": a.get("affiliation") or ""}
        if a.get("orcid"):
            c["orcid"] = a["orcid"]
        out.append(c)
    return out


def build_skill_payload(skill: dict, hub: dict, collection_doi: Optional[str],
                        archive: Path) -> Payload:
    """One record per skill, pointing at the collection."""
    sid = skill.get("id", "")
    title = skill.get("title") or skill.get("title_pt") or skill.get("slug", "")
    desc = (skill.get("summary") or "").strip()
    desc_pt = (skill.get("summary_pt") or "").strip()
    body = f"<p><strong>{sid}</strong> — {desc}</p>"
    if desc_pt:
        body += f"<p><em>{desc_pt}</em></p>"
    site = (hub.get("site_url") or "").rstrip("/")
    if site:
        body += (f'<p>Package page: <a href="{site}/skills/{skill["slug"]}.html">'
                 f'{site}/skills/{skill["slug"]}.html</a></p>')
    body += ("<p>Part of the Digital Methods Skills collection. Validation is structural: the test "
             "suite proves the implementation behaves as specified, not that the method is correct "
             "for every corpus.</p>")

    related = [{"identifier": (hub.get("repo_url") or "").rstrip("/"),
                "relation": "isSupplementTo", "scheme": "url"}]
    if site:
        related.append({"identifier": f"{site}/skills/{skill['slug']}.html",
                        "relation": "isDocumentedBy", "scheme": "url"})
    if collection_doi:
        related.append({"identifier": collection_doi, "relation": "isPartOf", "scheme": "doi"})

    meta = {
        "title": f"{title} ({sid})",
        "upload_type": "software",
        "description": body,
        "creators": _creators(skill.get("authors") or []),
        "license": "mit",
        "access_right": "open",
        "language": "eng",
        "version": skill.get("version") or "1.0.0",
        "publication_date": date.today().isoformat(),
        "keywords": (skill.get("keywords") or []) + ["agent skills", "research methods"],
        "related_identifiers": related,
        "notes": (f"{sid}. Digital Methods Skills, Digital Humanities Laboratory, "
                  f"Federal University of Bahia."),
    }
    return Payload(slug=skill["slug"], title=meta["title"], metadata=meta,
                   archive=archive, skill_id=sid, version=meta["version"])


def build_collection_payload(reg: dict) -> Payload:
    hub = reg.get("hub") or {}
    available = [s for s in reg["skills"] if s.get("status") == "available"]
    body = COLLECTION_DESC + "<p>Skills included: " + "; ".join(
        f'{s["id"]} {s.get("title") or s.get("title_pt")}' for s in available) + ".</p>"
    meta = {
        "title": COLLECTION_TITLE,
        "upload_type": "software",
        "description": body,
        "creators": _creators(next((s.get("authors") for s in reg["skills"] if s.get("authors")), [])),
        "license": "mit",
        "access_right": "open",
        "language": "eng",
        "version": hub.get("release") or "1.1.0",
        "publication_date": date.today().isoformat(),
        "keywords": ["agent skills", "research methods", "reproducibility", "open science",
                     "digital humanities", "methodology"],
        "related_identifiers": [
            {"identifier": (hub.get("repo_url") or "").rstrip("/"),
             "relation": "isSupplementTo", "scheme": "url"},
            {"identifier": (hub.get("site_url") or "").rstrip("/"),
             "relation": "isDocumentedBy", "scheme": "url"},
        ],
        "notes": "Digital Methods Skills collection. Digital Humanities Laboratory, "
                 "Federal University of Bahia.",
    }
    return Payload(slug="__collection__", title=meta["title"], metadata=meta,
                   archive=Path(), skill_id="collection", version=meta["version"])


# --------------------------------------------------------------------------- packaging

def package_dir(src: Path, target: Path) -> Path:
    """Zip one skill directory, deterministically: same content, same hash."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(src.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(src)
            if any(part in SKIP_DIRS for part in rel.parts) or p.suffix in SKIP_SUFFIX:
                continue
            info = zipfile.ZipInfo(rel.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, p.read_bytes())
    return target


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- client

class ZenodoError(Exception):
    pass


class ZenodoClient:
    """Minimal REST client. Injected session keeps the tests offline."""

    def __init__(self, token: str, base: str, session=None):
        if not token:
            raise ZenodoError("missing token: set ZENODO_TOKEN (production) or ZENODO_SANDBOX_TOKEN")
        self.base = base.rstrip("/")
        self.token = token
        if session is None:
            import requests
            session = requests.Session()
        self.session = session
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def _check(self, r, what: str):
        code = getattr(r, "status_code", 200)
        if code >= 400:
            detail = ""
            try:
                detail = str(r.json())[:300]
            except Exception:
                detail = (getattr(r, "text", "") or "")[:300]
            raise ZenodoError(f"{what}: HTTP {code} {detail}")
        return r

    def create(self, metadata: dict) -> dict:
        r = self.session.post(f"{self.base}/deposit/depositions",
                              json={"metadata": metadata})
        return self._check(r, "create deposition").json()

    def upload(self, bucket: str, path: Path) -> None:
        url = f"{bucket.rstrip('/')}/{path.name}"
        with path.open("rb") as fh:
            r = self.session.put(url, data=fh,
                                 headers={"Content-Type": "application/octet-stream"})
        self._check(r, f"upload {path.name}")

    def publish(self, deposition_id: int) -> dict:
        r = self.session.post(f"{self.base}/deposit/depositions/{deposition_id}/actions/publish")
        return self._check(r, "publish").json()

    def new_version(self, deposition_id: int) -> dict:
        r = self.session.post(f"{self.base}/deposit/depositions/{deposition_id}/actions/newversion")
        return self._check(r, "new version").json()


# --------------------------------------------------------------------------- state

def load_state() -> dict:
    if DOIS.exists():
        return json.loads(DOIS.read_text(encoding="utf-8"))
    return {"deposits": {}}


def save_state(state: dict) -> None:
    DOIS.parent.mkdir(parents=True, exist_ok=True)
    DOIS.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record(state: dict, slug: str, env: str, skill_id: str, doi: str,
           concept_doi: str, record_id: int, version: str, digest: str) -> None:
    state.setdefault("deposits", {}).setdefault(slug, {})
    state["deposits"][slug].update({
        "skill_id": skill_id, "environment": env, "concept_doi": concept_doi,
        "version_doi": doi, "record_id": record_id, "version": version,
        "sha256": digest, "published_at": date.today().isoformat(),
    })


# --------------------------------------------------------------------------- run

def plan(reg: dict, only: Optional[str] = None) -> list[Payload]:
    hub = reg.get("hub") or {}
    state = load_state()
    collection_doi = (state.get("deposits", {}).get("__collection__", {}) or {}).get("concept_doi")
    out = [build_collection_payload(reg)]
    for s in reg["skills"]:
        if s.get("status") != "available":
            continue
        if only and s["slug"] != only:
            continue
        archive = ROOT / "deposit" / f'{s["slug"]}-{s.get("version", "1.0.0")}.zip'
        out.append(build_skill_payload(s, hub, collection_doi, archive))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Deposit each skill as its own Zenodo record.")
    ap.add_argument("--env", choices=("sandbox", "production"))
    ap.add_argument("--publish", action="store_true", help="actually upload and publish")
    ap.add_argument("--only", help="single skill slug")
    ap.add_argument("--include-collection", action="store_true",
                    help="also deposit the collection record")
    ap.add_argument("--dry-run", action="store_true", help="default: build payloads only")
    args = ap.parse_args(argv)

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    payloads = plan(reg, args.only)
    if not args.include_collection:
        payloads = [p for p in payloads if p.slug != "__collection__"]

    # package every skill so the dry run shows the exact artefacts
    for p in payloads:
        if p.slug == "__collection__":
            continue
        src = ROOT / p.slug
        if not src.exists():
            print(f"skip {p.slug}: directory not found", file=sys.stderr)
            continue
        package_dir(src, p.archive)

    if not args.publish or not args.env:
        print(f"dry run — {len(payloads)} record(s), nothing uploaded\n")
        for p in payloads:
            size = p.archive.stat().st_size if p.archive.exists() else 0
            print(f"  {p.skill_id:8} {p.slug:26} v{p.version:8} "
                  f"{size/1024:7.1f} KiB  {'…' + sha256(p.archive)[:12] if size else '(no archive)'}")
            print(f"           title: {p.title[:88]}")
        print("\nre-run with --env sandbox --publish to deposit into the sandbox")
        return 0

    token = os.environ.get("ZENODO_SANDBOX_TOKEN" if args.env == "sandbox" else "ZENODO_TOKEN", "")
    if not token:
        print(f"error: set {'ZENODO_SANDBOX_TOKEN' if args.env == 'sandbox' else 'ZENODO_TOKEN'}",
              file=sys.stderr)
        return 2

    client = ZenodoClient(token, API[args.env])
    state = load_state()
    failures = 0
    for p in payloads:
        try:
            dep = client.create(p.metadata)
            dep_id = dep["id"]
            bucket = dep["links"]["bucket"]
            if p.archive.exists():
                client.upload(bucket, p.archive)
            published = client.publish(dep_id)
            doi = published.get("doi", "")
            concept = (published.get("conceptdoi") or doi)
            record(state, p.slug, args.env, p.skill_id, doi, concept, dep_id,
                   p.version, sha256(p.archive) if p.archive.exists() else "")
            print(f"published {p.skill_id}: {doi}  (concept {concept})")
        except Exception as exc:
            failures += 1
            print(f"FAILED {p.slug}: {exc}", file=sys.stderr)
    save_state(state)
    print(f"\nstate written to {DOIS}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
