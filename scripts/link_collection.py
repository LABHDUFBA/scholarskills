#!/usr/bin/env python3
"""Complete the two-way link between the collection record and the skill records.

Two gaps need a new version, because a published Zenodo record is immutable:

1. a skill published *before* the collection exists has no ``isPartOf``;
2. the collection does not list its parts (``hasPart``).

A third trap, learned the hard way: **creating a new version clears ``metadata.version``**. If the
script does not set it, the record is published with an empty version and the citation loses the
exact snapshot. Every new version here sets the field explicitly.

    python3 scripts/link_collection.py --check     # report only, touches nothing
    python3 scripts/link_collection.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOIS = ROOT / "registry" / "dois.json"
BASE = "https://zenodo.org/api"


def bump(version: str, part: str = "patch") -> str:
    """1.0.0 -> 1.0.1 (patch) or 1.0.0 -> 1.1.0 (minor)."""
    try:
        major, minor, patch = (int(x) for x in (version or "1.0.0").split(".")[:3])
    except ValueError:
        return "1.0.1"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def session():
    import requests
    token = os.environ.get("ZENODO_TOKEN", "")
    if not token:
        raise SystemExit("error: ZENODO_TOKEN not set")
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    return s


def get(s, rec_id: int) -> dict:
    r = s.get(f"{BASE}/records/{rec_id}", timeout=40)
    r.raise_for_status()
    return r.json()


def new_version(s, rec_id: int, mutate, label: str, version: str):
    """Create a new version, apply `mutate` to its metadata, set the version, publish."""
    r = s.post(f"{BASE}/deposit/depositions/{rec_id}/actions/newversion", timeout=40)
    if r.status_code >= 400:
        print(f"  {label}: newversion HTTP {r.status_code} {r.text[:160]}", file=sys.stderr)
        return None
    draft = s.get(r.json()["links"]["latest_draft"], timeout=40).json()
    meta = draft["metadata"]
    mutate(meta)
    meta["version"] = version          # the field the API silently drops
    u = s.put(f"{BASE}/deposit/depositions/{draft['id']}", json={"metadata": meta}, timeout=40)
    if u.status_code >= 400:
        print(f"  {label}: update HTTP {u.status_code} {u.text[:200]}", file=sys.stderr)
        return None
    p = s.post(f"{BASE}/deposit/depositions/{draft['id']}/actions/publish", timeout=60)
    if p.status_code >= 400:
        print(f"  {label}: publish HTTP {p.status_code} {p.text[:200]}", file=sys.stderr)
        return None
    return p.json()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    if not (args.check or args.apply):
        ap.error("choose --check or --apply")

    s = session()
    st = json.loads(DOIS.read_text(encoding="utf-8"))["deposits"]
    coll = st["__collection__"]
    coll_concept = coll["concept_doi"]
    skills = {k: v for k, v in st.items() if k != "__collection__"}

    print(f"collection: {coll_concept} (record {coll['record_id']})")
    coll_j = get(s, coll["record_id"])
    haspart = [x["identifier"] for x in coll_j.get("metadata", {}).get("related_identifiers", [])
               if x.get("relation") == "hasPart"]
    print(f"  hasPart: {len(haspart)} de {len(skills)} skills")

    missing_part, needs_version = [], []
    for slug, d in skills.items():
        j = get(s, d["record_id"])
        md = j.get("metadata", {})
        rel = md.get("related_identifiers", [])
        ok = any(x.get("relation") == "isPartOf" and x["identifier"] == coll_concept for x in rel)
        ver = md.get("version")
        print(f"  {d.get('skill_id') or slug:11} isPartOf={ok}  version={ver!r}  record={d['record_id']}")
        if not ok:
            missing_part.append((slug, d))
        if not ver:
            needs_version.append((slug, d))
        # a published version with an empty field must be superseded to carry it
        if ver:
            d["version"] = ver

    missing_has = [d["concept_doi"] for d in skills.values() if d["concept_doi"] not in haspart]

    if args.check:
        print()
        print(f"missing isPartOf: {len(missing_part)} | empty version: {len(needs_version)} "
              f"| missing in hasPart: {len(missing_has)}")
        return 0

    changed = False

    def apply_skill(slug, d, add_part: bool):
        nonlocal changed
        target = bump(d.get("version") or "1.0.0")

        def mutate(meta):
            rel = meta.setdefault("related_identifiers", [])
            if add_part and not any(x.get("relation") == "isPartOf" for x in rel):
                rel.append({"identifier": coll_concept, "relation": "isPartOf", "scheme": "doi"})

        j = new_version(s, d["record_id"], mutate, slug, target)
        if j:
            d["version_doi"] = j["doi"]
            d["record_id"] = j["id"]
            d["version"] = target
            changed = True
            print(f"  {slug}: v{target} -> {j['doi']}")

    for slug, d in missing_part:
        apply_skill(slug, d, add_part=True)
    for slug, d in needs_version:
        if not any(slug == m[0] for m in missing_part):
            apply_skill(slug, d, add_part=False)

    if missing_has:
        def add_has(meta):
            rel = meta.setdefault("related_identifiers", [])
            rel[:] = [x for x in rel if x.get("relation") != "hasPart"]
            for dd in skills.values():
                rel.append({"identifier": dd["concept_doi"], "relation": "hasPart", "scheme": "doi"})
        target = bump(coll.get("version") or "1.0.0", "minor")
        j = new_version(s, coll["record_id"], add_has, "collection", target)
        if j:
            coll["version_doi"] = j["doi"]
            coll["record_id"] = j["id"]
            coll["version"] = target
            changed = True
            print(f"  collection: v{target} -> {j['doi']}")

    if changed:
        DOIS.write_text(json.dumps({"deposits": st}, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print("state updated")
    else:
        print("nothing to do")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
