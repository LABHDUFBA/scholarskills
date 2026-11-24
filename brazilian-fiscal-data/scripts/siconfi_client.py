"""SICONFI / Tesouro Transparente client — read-only fiscal data for Brazilian states and municipalities.

Design rules:

1. **One identifier, one entity.** Fiscal queries are keyed by the IBGE code (``id_ente``), never by a
   name. Names change with each administration; the code does not.
2. **Periods are explicit.** A fiscal indicator without its period and demonstrative type is not a
   number, it is an anecdote. Every record carries exercise, period and type.
3. **Totals are computed from the declared accounts**, not from a pre-computed column that may not
   exist for the entity in that period.
4. **An empty answer is an answer.** SICONFI returns an empty item list for entities that did not
   deliver; that is a finding about the entity, and must not be confused with a network failure.

The HTTP layer is injected so the suite runs offline against recorded payloads.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol

BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
DEMONSTRATIVOS = ("RREO", "RGF", "DCA")


class SiconfiError(Exception):
    """Base error."""


class SiconfiUnavailable(SiconfiError):
    """Provider unavailable or payload unrecognisable."""


class SiconfiAuth(SiconfiError):
    """401/403."""


class HttpSession(Protocol):
    def get(self, url: str, **kwargs: Any) -> Any:  # pragma: no cover
        ...


@dataclass(frozen=True)
class Query:
    """A keyed fiscal query. ``id_ente`` is the IBGE code as a string."""

    id_ente: str
    exercicio: int
    periodo: int = 1                 # 1..6 for RREO bimesters, 1..3 for RGF quadrimesters
    demonstrativo: str = "RREO"
    anexo: Optional[str] = None

    def validate(self) -> "Query":
        if not self.id_ente or not self.id_ente.strip().isdigit():
            raise ValueError("id_ente must be the numeric IBGE code")
        if self.demonstrativo not in DEMONSTRATIVOS:
            raise ValueError(f"demonstrativo must be one of {DEMONSTRATIVOS}")
        if len(self.id_ente) not in (2, 7):
            raise ValueError("id_ente must be a UF (2 digits) or a municipality (7 digits)")
        if not (2000 <= self.exercicio <= 2100):
            raise ValueError("exercicio out of range")
        if self.periodo < 1:
            raise ValueError("periodo starts at 1")
        return self

    def params(self) -> dict:
        p = {
            "an_exercicio": self.exercicio,
            "nr_periodo": self.periodo,
            "co_tipo_demonstrativo": self.demonstrativo,
            "id_ente": self.id_ente,
        }
        if self.anexo:
            p["no_anexo"] = self.anexo
        return p


@dataclass
class Conta:
    codigo: str
    descricao: str
    valor: float
    coluna: str = ""

    def as_dict(self) -> dict:
        return {"codigo": self.codigo, "descricao": self.descricao,
                "valor": self.valor, "coluna": self.coluna}


class SiconfiClient:
    def __init__(self, session: HttpSession, base: str = BASE):
        self.session = session
        self.base = base.rstrip("/")

    def fetch(self, q: Query) -> list[dict]:
        """Return the raw item list for a query. Raises instead of guessing."""
        q.validate()
        r = self.session.get(f"{self.base}/{q.demonstrativo.lower()}", params=q.params(), timeout=90)
        status = getattr(r, "status_code", 200)
        if status in (401, 403):
            raise SiconfiAuth(f"HTTP {status}: SICONFI refused the request")
        if status >= 400:
            raise SiconfiUnavailable(f"HTTP {status} on {q.demonstrativo} {q.exercicio}/{q.periodo}")
        payload = r.json()
        # SICONFI wraps results in {"items": [...]} on the ORDS endpoints
        if isinstance(payload, dict):
            payload = payload.get("items")
        if not isinstance(payload, list):
            raise SiconfiUnavailable("unexpected payload: no items list")
        return payload


def parse_contas(items: list[dict]) -> list[Conta]:
    """Normalise SICONFI rows into (account, value) pairs.

    The provider uses different field spellings across demonstratives (``conta``/``cod_conta``,
    ``valor``/``valor_realizado``). A row without a recognisable value is skipped rather than
    recorded as zero — a fabricated zero in a fiscal table is worse than a gap.
    """
    out: list[Conta] = []
    for row in items:
        if not isinstance(row, dict):
            continue
        codigo = str(row.get("cod_conta") or row.get("conta") or "").strip()
        desc = str(row.get("desc_conta") or row.get("descricao_conta") or row.get("conta") or "").strip()
        raw_valor = row.get("valor") if "valor" in row else row.get("valor_realizado")
        if raw_valor in (None, ""):
            continue
        try:
            valor = float(str(raw_valor).replace(".", "").replace(",", ".")) \
                if isinstance(raw_valor, str) and "," in raw_valor else float(raw_valor)
        except (TypeError, ValueError):
            continue
        if not codigo and not desc:
            continue
        out.append(Conta(codigo=codigo, descricao=desc, valor=valor,
                         coluna=str(row.get("coluna") or "")))
    return out


def total(contas: list[Conta], prefixo: str) -> float:
    """Sum accounts whose code starts with ``prefixo``.

    Fiscal totals are hierarchical: 'ReceitaTotal' is not a column, it is the sum of a subtree of
    account codes. Summing a prefix keeps the operation auditable by a reader who can see the tree.
    """
    p = prefixo.strip()
    if not p:
        raise ValueError("empty prefix would sum the whole tree")
    return sum(c.valor for c in contas if c.codigo.startswith(p))


def coverage(contas: list[Conta]) -> dict:
    """Cheap sanity report: how many accounts, how many distinct columns."""
    cols = sorted({c.coluna for c in contas if c.coluna})
    return {"contas": len(contas), "colunas": cols}
