#!/usr/bin/env python3
"""Export a Zotero collection (or a search) to BibTeX, CSL JSON or RIS.

Credentials are read from the environment. The tool prints provenance to stderr so that
stdout stays a clean, pipeable bibliography.

    python3 zotero_bibliography.py --collection ABC123 --format bibtex --out refs.bib
    python3 zotero_bibliography.py --query "foucault" --format csljson
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zotero_client import ZoteroClient, ZoteroError, ScopeError, provenance  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Export Zotero references.")
    ap.add_argument("--collection", default=None, help="Collection key")
    ap.add_argument("--query", default=None, help="Full-text query")
    ap.add_argument("--format", default="bibtex", choices=("bibtex", "ris", "csljson"))
    ap.add_argument("--out", type=Path, default=None, help="Output file (default: stdout)")
    ap.add_argument("--count-only", action="store_true")
    args = ap.parse_args(argv)

    try:
        client = ZoteroClient.from_env()
    except ZoteroError as exc:
        print(f"error: {exc}. Export ZOTERO_API_KEY and ZOTERO_LIBRARY_ID.", file=sys.stderr)
        return 2

    try:
        count = client.count_references(args.collection)
        if args.count_only:
            print(provenance(client, count, args.collection or "library"))
            return 0

        if args.query:
            # A query cannot be rendered by the export endpoint; collect records instead.
            records = [i["data"] for i in client.iter_items(query=args.query)]
            payload = json_dump(records) if args.format == "csljson" else json_dump(records)
        else:
            payload = client.export(args.collection, args.format)

        if args.out:
            args.out.write_text(payload, encoding="utf-8")
            print(provenance(client, count, args.collection or "library"), file=sys.stderr)
            print(f"wrote {args.out} ({len(payload)} bytes)", file=sys.stderr)
        else:
            print(payload)
            print(provenance(client, count, args.collection or "library"), file=sys.stderr)
        return 0
    except ScopeError as exc:
        print(f"scope error: {exc}", file=sys.stderr)
        return 3
    except ZoteroError as exc:
        print(f"api error: {exc}", file=sys.stderr)
        return 1


def json_dump(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(main())
