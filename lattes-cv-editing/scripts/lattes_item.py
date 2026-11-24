"""Prepare and check items before they are typed into a Lattes CV.

Why this module exists: the Lattes editor has no API and no transaction log. A record typed with a
wrong year, a duplicated entry or a preprint filed as a journal article is not caught by any
validator — it becomes part of a public academic record that other people cite. The only place to
prevent that is before the form is filled.

What is verifiable offline, and therefore automated here:

1. required fields per record type;
2. duplicate detection by normalised title plus year;
3. the rule that the same work in two vehicles is two records, not one;
4. keyword derivation (3-5, lowercase, no final period);
5. a plain summary of what will be typed, for the operator to approve.

What is not automated: the login, the navigation and the submission. Those stay with the holder of
the CV, by design.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable, Optional

# Required fields per record type. Names follow the Lattes sections an editor sees.
REQUIRED = {
    "artigo_periodico": ("titulo", "ano", "periodico", "autores"),
    "artigo_anais": ("titulo", "ano", "evento", "autores"),
    "capitulo_livro": ("titulo", "ano", "livro", "autores"),
    "livro": ("titulo", "ano", "autores"),
    "preprint": ("titulo", "ano", "repositorio", "autores"),
    "projeto": ("titulo", "ano_inicio", "situacao"),
    "orientacao": ("titulo", "ano", "orientando_nivel"),
    "banca": ("titulo", "ano", "instituicao"),
    "evento": ("titulo", "ano"),
}

# Two records that look alike but must never be merged.
DISTINCT_PAIRS = {
    ("preprint", "artigo_periodico"): "preprint and published article are distinct records",
    ("artigo_anais", "artigo_periodico"): "conference paper and journal article are distinct records",
    ("capitulo_livro", "livro"): "book chapter and book are distinct records",
}

STOPWORDS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "na", "no", "nas", "nos",
    "para", "por", "com", "um", "uma", "uns", "umas", "que", "se", "ao", "aos", "à", "às",
    "sobre", "entre", "como", "mais", "menos", "não", "ser", "são", "foi", "sua", "seu",
    "este", "esta", "esse", "essa", "isso", "aquilo", "the", "of", "and", "in", "on", "for",
}


@dataclass
class Item:
    tipo: str
    campos: dict = field(default_factory=dict)

    def get(self, key: str, default: str = "") -> str:
        v = self.campos.get(key, default)
        return "" if v is None else str(v).strip()


def normalize(text: str) -> str:
    """Lowercase, strip accents and punctuation — the form a duplicate comparison needs."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(text))
    no_acc = "".join(c for c in nfkd if not unicodedata.combining(c))
    no_punct = re.sub(r"[^a-z0-9\s]", " ", no_acc.lower())
    return re.sub(r"\s+", " ", no_punct).strip()


def validate(item: Item) -> list[str]:
    """Return a list of problems. Empty list means the item is ready to be typed."""
    problems: list[str] = []
    if item.tipo not in REQUIRED:
        return [f"unknown record type: {item.tipo!r} (known: {', '.join(sorted(REQUIRED))})"]

    for key in REQUIRED[item.tipo]:
        if not item.get(key):
            problems.append(f"missing required field: {key}")

    ano = item.get("ano")
    if ano:
        if not ano.isdigit() or not (1900 <= int(ano) <= 2100):
            problems.append(f"year is not a four-digit number: {ano!r}")
        elif int(ano) > 2027:
            problems.append(f"year is in the future: {ano}")

    autores = item.get("autores")
    if autores and "," not in autores and ";" not in autores and " e " not in autores:
        problems.append("authors field does not look like a list")

    doi = item.get("doi")
    if doi and not re.match(r"^10\.\d{4,9}/\S+$", doi):
        problems.append(f"DOI does not match the 10.NNNN/suffix pattern: {doi!r}")

    kw = item.campos.get("palavras_chave")
    if kw:
        ok, why = check_keywords(kw)
        if not ok:
            problems.append(why)

    return problems


def check_keywords(value) -> tuple[bool, str]:
    """Keywords: 3 to 5, lowercase, no final period."""
    if isinstance(value, str):
        kws = [k.strip() for k in re.split(r"[;,]", value) if k.strip()]
    else:
        kws = [str(k).strip() for k in (value or []) if str(k).strip()]
    if not 3 <= len(kws) <= 5:
        return False, f"expected 3 to 5 keywords, found {len(kws)}"
    if any(k.endswith(".") for k in kws):
        return False, "keywords must not end with a period"
    if any(k != k.lower() for k in kws):
        return False, "keywords must be lowercase"
    return True, ""


def suggest_keywords(text: str, limit: int = 5) -> list[str]:
    """Derive candidate keywords from the item's own text — never from an external thesaurus."""
    words = [w for w in normalize(text).split() if len(w) > 3 and w not in STOPWORDS]
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    out = [w for w, _ in ranked][:limit]
    return out or []


def same_record(a: Item, b: Item) -> bool:
    """True when two items are the same record, by title and year.

    Titles are compared after normalisation but not fuzzily: 'Sociologia digital' and 'Sociologia
    digital: um balanço' are different works, and a fuzzy match would merge a paper with its
    review. The operator decides the doubtful cases; this function only flags the identical ones.
    """
    if normalize(a.get("titulo")) != normalize(b.get("titulo")):
        return False
    ya, yb = a.get("ano"), b.get("ano")
    if ya and yb and ya != yb:
        return False
    return True


def find_duplicates(item: Item, existing: Iterable[Item]) -> list[Item]:
    return [e for e in existing if same_record(item, e)]


def distinct_pair(a: Item, b: Item) -> Optional[str]:
    """Return the reason two similar items must stay separate, or None."""
    return DISTINCT_PAIRS.get((a.tipo, b.tipo)) or DISTINCT_PAIRS.get((b.tipo, a.tipo))


def summary(item: Item) -> str:
    """Plain text the operator can approve before anything is typed."""
    lines = [f"tipo: {item.tipo}"]
    for k, v in item.campos.items():
        if v in (None, "", []):
            continue
        if isinstance(v, (list, tuple)):
            v = "; ".join(str(x) for x in v)
        lines.append(f"{k}: {v}")
    problems = validate(item)
    lines.append("situação: " + ("pronto para digitação" if not problems
                                  else f"{len(problems)} pendência(s)"))
    for p in problems:
        lines.append(f"  - {p}")
    return "\n".join(lines)
