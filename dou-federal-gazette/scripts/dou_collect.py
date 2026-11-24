#!/usr/bin/env python3
"""CLI: collect DOU search results or federal covenants as CSV/JSON.

Credentials come from the environment only:

    export PORTAL_TRANSPARENCIA_KEY="..."   # free key, portaldatransparencia.gov.br

Examples

    # covenants for one grantee (structured API, preferred)
    python3 scripts/dou_collect.py convenios --convenente "UNIVERSIDADE FEDERAL DA BAHIA" --out convenios.csv

    # discovered publications from a saved search page (no network)
    python3 scripts/dou_collect.py parse --html page.html --out publicacoes.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dou_client import (  # noqa: E402
    ConveniosClient, DouError, DouPermissionError, DouUnavailable, RateLimited,
    parse_search_results, parse_total, verify_first_records,
)


def _write(rows: list[dict], out: str, fmt: str) -> None:
    path = Path(out)
    if fmt == "json":
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        return
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def cmd_convenios(args) -> int:
    import requests

    key = os.environ.get("PORTAL_TRANSPARENCIA_KEY", "").strip()
    if not key:
        print("erro: defina PORTAL_TRANSPARENCIA_KEY no ambiente", file=sys.stderr)
        return 2
    client = ConveniosClient(requests.Session(), key)
    try:
        rows = client.collect(args.convenente, max_pages=args.max_pages, sleep=time.sleep)
    except (DouPermissionError, RateLimited, DouUnavailable, DouError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    if not verify_first_records(rows, args.convenente):
        print("aviso: os primeiros registros não pertencem ao convenente pedido — "
              "o filtro pode ter sido ignorado; coleta abortada", file=sys.stderr)
        return 4
    _write([r.as_dict() for r in rows], args.out, args.format)
    print(f"{len(rows)} convênios escritos em {args.out}", file=sys.stderr)
    return 0


def cmd_parse(args) -> int:
    html = Path(args.html).read_text(encoding="utf-8", errors="replace")
    try:
        rows = parse_search_results(html)
    except DouUnavailable as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    total = parse_total(html)
    _write([r.as_dict() for r in rows], args.out, args.format)
    print(f"{len(rows)} publicações (total anunciado: {total}) em {args.out}", file=sys.stderr)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="DOU and federal covenants collector (read-only).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("convenios", help="coletar convênios federais por convenente")
    a.add_argument("--convenente", required=True)
    a.add_argument("--out", default="convenios.csv")
    a.add_argument("--format", choices=("csv", "json"), default="csv")
    a.add_argument("--max-pages", type=int, default=40)
    a.set_defaults(func=cmd_convenios)

    b = sub.add_parser("parse", help="extrair publicações de uma página de busca salva")
    b.add_argument("--html", required=True)
    b.add_argument("--out", default="publicacoes.csv")
    b.add_argument("--format", choices=("csv", "json"), default="csv")
    b.set_defaults(func=cmd_parse)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
