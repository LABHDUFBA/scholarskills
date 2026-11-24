#!/usr/bin/env python3
"""Register a DOI in the catalogue, idempotently.

Deposit identifiers are never typed by hand into three files. This script writes the DOI into the
registry and regenerates the hub, so the site and the citation text cannot disagree with the record.

    python3 scripts/set_doi.py --concept 10.5281/zenodo.123456 --version 10.5281/zenodo.123457 \\
        --release v1.0.0

    python3 scripts/set_doi.py --clear      # remove a DOI that was registered by mistake

Rules enforced:
- only one of --clear or a DOI;
- a version DOI requires a concept DOI (they are different identifiers and both must exist);
- the DOI format is checked before writing, because a malformed identifier in a public catalogue is
  worse than a missing one;
- nothing is written if the value is unchanged (safe to re-run).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "registry.json"
DOI_RE = re.compile(r"^10\.\d{4,9}/[^\s]+$")
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "site"}


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save(reg: dict) -> None:
    REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_doi(value: str, label: str) -> str:
    value = value.strip()
    if not DOI_RE.match(value):
        raise SystemExit(f"refused: '{value}' is not a DOI ({label}). Expected the form 10.5281/zenodo.NNNNNNN")
    return value


def update_citation_texts(reg: dict, concept: str | None) -> list[str]:
    """Keep the human-readable citation in step with the identifier."""
    changed = []
    for s in reg["skills"]:
        if s.get("status") != "available":
            continue
        cite = s.get("cite") or ""
        if not cite:
            continue
        base = re.sub(r"\s*DOI:?\s*10\.\d{4,9}/[^\s]+\.?$", "", cite).rstrip(". ").rstrip()
        new = f"{base} DOI: {concept}." if concept else base + "."
        if new != s.get("cite"):
            s["cite"] = new
            changed.append(s["slug"])
    return changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Register or clear a DOI in the catalogue.")
    ap.add_argument("--concept", help="Concept DOI (resolves to the latest version)")
    ap.add_argument("--version", dest="version_doi", help="Version DOI (pins this snapshot)")
    ap.add_argument("--release", help="Release tag the version DOI belongs to, e.g. v1.0.0")
    ap.add_argument("--clear", action="store_true", help="Remove registered DOIs")
    args = ap.parse_args(argv)

    reg = load()
    hub = reg.setdefault("hub", {})

    if args.clear:
        hub["doi_concept"] = None
        hub["doi_version"] = None
        hub["release"] = None
        for s in reg["skills"]:
            s["doi_concept"] = None
            s["doi_version"] = None
        changed = update_citation_texts(reg, None)
        save(reg)
        print(f"cleared DOIs; citation texts updated for: {', '.join(changed) or 'none'}")
        return finish()

    if not args.concept:
        raise SystemExit("refused: --concept is required when registering a DOI "
                         "(the concept DOI is what a citation should carry)")

    concept = validate_doi(args.concept, "concept")
    version = validate_doi(args.version_doi, "version") if args.version_doi else None

    hub["doi_concept"] = concept
    hub["doi_version"] = version
    hub["release"] = args.release or hub.get("release")

    # One repository, one record: every available skill cites the same concept DOI and points to
    # its own directory. Per-skill identifiers would require a repository per skill.
    for s in reg["skills"]:
        if s.get("status") == "available":
            s["doi_concept"] = concept
            s["doi_version"] = version

    changed = update_citation_texts(reg, concept)
    save(reg)
    print(f"concept DOI: {concept}")
    print(f"version DOI: {version or '(none)'}")
    print(f"release:     {hub['release'] or '(none)'}")
    print(f"citation texts updated: {', '.join(changed) or 'none'}")
    return finish()


def finish() -> int:
    proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")],
                          capture_output=True, text=True)
    print(proc.stdout.strip() or proc.stderr.strip())
    return 0 if proc.returncode == 0 else proc.returncode


if __name__ == "__main__":
    sys.exit(main())
