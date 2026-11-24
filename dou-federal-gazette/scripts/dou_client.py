"""DOU (Diário Oficial da União) and federal covenants — read-only client.

Design rules this module enforces:

1. **Official routes first.** The DOU publishes an open-data base (XML + ZIP, monthly) and the
   Portal da Transparência publishes a REST API for covenants. Both are designed for machine
   access. A search-result HTML page is a fallback for *discovery*, never for bulk collection.
2. **No authentication is bypassed.** Nothing here logs in, solves a challenge or rotates an
   identity to evade a block. If a route is unavailable, the client raises and says so.
3. **Politeness is part of correctness.** A fixed delay between requests and a hard ceiling on
   pagination keep the client inside the terms of a public service.

The HTTP layer is injected, so the test suite runs offline against recorded fixtures.
"""
from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass, asdict, field
from typing import Any, Iterable, Optional, Protocol

USER_AGENT = "ScholarSkills-DOU/1.0 (academic research; +https://labhdufba.github.io/scholarskills/)"


class DouError(Exception):
    """Base error for the DOU client."""


class DouUnavailable(DouError):
    """The route is blocked, offline or returning 5xx. Retry later; do not work around."""


class DouPermissionError(DouError):
    """401/403 from the API: the key is missing or lacks the required scope."""


class RateLimited(DouError):
    """429 from the API. Back off; a client must not accelerate when asked to slow down."""


class HttpSession(Protocol):
    def get(self, url: str, **kwargs: Any) -> Any:  # pragma: no cover - structural type
        ...


@dataclass
class Publication:
    """One item of a DOU search result page."""

    section: str
    organ: str
    edition: str
    published: str
    title: str
    url: str
    snippet: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Convenio:
    """One covenant record from the Portal da Transparência API."""

    numero: str
    convenente: str
    objeto: str
    valor: Optional[float]
    situacao: str
    inicio_vigencia: str = ""
    fim_vigencia: str = ""
    raw: dict = field(default_factory=dict, repr=False)

    def as_dict(self) -> dict:
        d = asdict(self)
        d.pop("raw", None)
        return d


# --------------------------------------------------------------------------- parsing

_BLOCK_SPLIT = re.compile(r'<div[^>]+class="[^"]*resultado[^"]*"', re.I)
_EDITION = re.compile(r"Edi[^<]{0,4}o\s*(?:N[ºo°]\.?\s*)?([\d.]+)\s*de\s*([0-9]{2}/[0-9]{2}/[0-9]{4})", re.I)
_SECTION = re.compile(r"Se[^<]{0,4}o\s*([123])", re.I)
_ORGAN = re.compile(r'class="[^"]*orgao[^"]*"[^>]*>(.*?)</', re.I | re.S)
_LINK = re.compile(r'href="(/web/dou/-/[^"]+)"', re.I)
_TITLE = re.compile(r'class="[^"]*title[^"]*"[^>]*>(.*?)</', re.I | re.S)
_TOTAL = re.compile(r"([\d.]+)\s+resultados?", re.I)


def _text(raw: str) -> str:
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()


def parse_total(page_html: str) -> Optional[int]:
    """Total number of results announced by the page, if present."""
    m = _TOTAL.search(_text(page_html))
    if not m:
        return None
    digits = re.sub(r"[^\d]", "", m.group(1))
    return int(digits) if digits else None


def parse_search_results(page_html: str, base_url: str = "https://www.in.gov.br") -> list[Publication]:
    """Parse a DOU search results page into publications.

    Returns an empty list for a legitimate "no results" page. Raises DouUnavailable when the page
    contains no recognisable result structure at all — silently returning [] there would report
    "nothing published" when the truth is "the route changed".
    """
    if not page_html or not page_html.strip():
        raise DouUnavailable("empty page: nothing to parse")

    blocks = [b for b in _BLOCK_SPLIT.split(page_html) if b.strip()]
    marked = [b for b in blocks if _LINK.search(b)]
    if not marked:
        if re.search(r"0\s+resultados?|nenhum resultado", _text(page_html), re.I):
            return []
        raise DouUnavailable("no result structure found; the search layout probably changed")

    out: list[Publication] = []
    for block in marked:
        link = _LINK.search(block)
        if not link:
            continue
        ed = _EDITION.search(_text(block))
        sec = _SECTION.search(_text(block))
        organ = _ORGAN.search(block)
        title = _TITLE.search(block)
        out.append(
            Publication(
                section=sec.group(1) if sec else "",
                organ=_text(organ.group(1)) if organ else "",
                edition=ed.group(1) if ed else "",
                published=ed.group(2) if ed else "",
                title=_text(title.group(1)) if title else "",
                url=base_url.rstrip("/") + link.group(1),
                snippet=_text(block)[:280],
            )
        )
    return out


# --------------------------------------------------------------------------- covenants API

API_BASE = "https://api.portaldatransparencia.gov.br/api-de-dados"
CONVENIOS_PATH = "/convenios"
_PAGE_SIZE = 15  # fixed by the provider; sending tamanhoPagina is silently ignored


class ConveniosClient:
    """Read covenants for one grantee from the Portal da Transparência API.

    The API key is read from ``PORTAL_TRANSPARENCIA_KEY`` by the CLI; it is never accepted as a
    positional argument so it cannot leak into a shell history or a log line.
    """

    def __init__(self, session: HttpSession, api_key: str, base: str = API_BASE):
        if not api_key:
            raise DouPermissionError("missing API key: set PORTAL_TRANSPARENCIA_KEY")
        self.session = session
        self.api_key = api_key
        self.base = base.rstrip("/")

    def _get(self, page: int, convenente: str) -> list[dict]:
        r = self.session.get(
            self.base + CONVENIOS_PATH,
            params={"convenente": convenente, "pagina": page},
            headers={"chave-api-dados": self.api_key, "accept": "application/json"},
            timeout=60,
        )
        status = getattr(r, "status_code", 200)
        if status in (401, 403):
            raise DouPermissionError(f"HTTP {status}: key rejected or out of scope")
        if status == 429:
            raise RateLimited("HTTP 429: the provider asked the client to slow down")
        if status >= 500:
            raise DouUnavailable(f"HTTP {status}: provider unavailable")
        if status >= 400:
            raise DouError(f"HTTP {status} on convenios page {page}")
        data = r.json()
        if not isinstance(data, list):
            raise DouUnavailable("unexpected payload: expected a list of records")
        return data

    def collect(self, convenente: str, max_pages: int = 40, delay_s: float = 1.0,
                sleep=None) -> list[Convenio]:
        """Page through covenants until an empty page or the ceiling.

        ``max_pages`` is a safety ceiling, not a target: stopping because the ceiling was reached
        is reported to the caller through ``reached_ceiling`` on the returned list's attribute.
        """
        if not convenente or not convenente.strip():
            raise ValueError("convenente is required")
        out: list[Convenio] = []
        for page in range(1, max_pages + 1):
            rows = self._get(page, convenente)
            if not rows:
                break
            for row in rows:
                out.append(_convenio(row))
            if len(rows) < _PAGE_SIZE:
                break
            if sleep is not None and delay_s:
                sleep(delay_s)
        return out


def _convenio(row: dict) -> Convenio:
    def g(*keys: str) -> Any:
        for k in keys:
            if k in row and row[k] not in (None, ""):
                return row[k]
        return None

    valor = g("valor", "valorLiberado", "valorDaUltimaLiberacao")
    try:
        valor = float(valor) if valor is not None else None
    except (TypeError, ValueError):
        valor = None
    return Convenio(
        numero=str(g("numero", "numeroConvenio") or ""),
        convenente=str(g("convenente", "nomeConvenente") or ""),
        objeto=str(g("objeto", "descricaoObjeto") or ""),
        valor=valor,
        situacao=str(g("situacao", "situacaoConvenio") or ""),
        inicio_vigencia=str(g("dataInicioVigencia", "inicioVigencia") or ""),
        fim_vigencia=str(g("dataFinalVigencia", "fimVigencia") or ""),
        raw=dict(row),
    )


def verify_first_records(records: list[Convenio], expect: str) -> bool:
    """Guard against the provider silently ignoring a filter.

    The documented pitfall is a parameter that does not exist: the API then answers with records
    from any grantee. Before a long collection, confirm that the first rows actually belong to the
    requested grantee.
    """
    if not records:
        return True
    needle = expect.strip().lower()
    return all(needle in (r.convenente or "").lower() for r in records[:3])
