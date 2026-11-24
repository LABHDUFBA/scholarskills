"""Offline test suite for the DOU / covenants client.

Every case runs without network: the search page is a recorded fragment of the documented layout
and the HTTP layer is a stub. A green suite proves the parser and the pagination logic, not that a
given day's DOU page still has this markup — that is what the health probe is for.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from dou_client import (  # noqa: E402
    ConveniosClient, DouError, DouPermissionError, DouUnavailable, RateLimited,
    parse_search_results, parse_total, verify_first_records,
)

FIXTURE_TWO = """
<div class="resultados">
  <p>2 resultados para "convenio"</p>
  <div class="resultado">
    <span>Seção 3</span>
    <span class="orgao">MINISTÉRIO DA EDUCAÇÃO</span>
    <span>Edição Nº 220 de 19/11/2026</span>
    <a class="title" href="/web/dou/-/extrato-de-convenio-123">EXTRATO DE CONVÊNIO Nº 12/2026</a>
  </div>
  <div class="resultado">
    <span>Seção 3</span>
    <span class="orgao">FUNDAÇÃO UNIVERSIDADE FEDERAL DA BAHIA</span>
    <span>Edição Nº 220 de 19/11/2026</span>
    <a class="title" href="/web/dou/-/extrato-de-convenio-456">EXTRATO DE CONVÊNIO Nº 34/2026</a>
  </div>
</div>
"""

FIXTURE_EMPTY = '<div class="resultados"><p>0 resultados para "xyz"</p></div>'

FIXTURE_BROKEN = '<html><body><div class="layout-novo">nada aqui</div></body></html>'


class FakeResponse:
    def __init__(self, status=200, payload=None, text=""):
        self.status_code = status
        self._payload = payload if payload is not None else []
        self.text = text

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if not self.responses:
            return FakeResponse(200, [])
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


class TestSearchParsing(unittest.TestCase):
    def test_parses_two_publications(self):
        rows = parse_search_results(FIXTURE_TWO)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].section, "3")
        self.assertEqual(rows[0].published, "19/11/2026")
        self.assertIn("MINISTÉRIO DA EDUCAÇÃO", rows[0].organ)
        self.assertTrue(rows[0].url.startswith("https://www.in.gov.br/web/dou/-/"))
        self.assertIn("CONVÊNIO", rows[0].title.upper())

    def test_total_from_page(self):
        self.assertEqual(parse_total(FIXTURE_TWO), 2)

    def test_total_absent(self):
        self.assertIsNone(parse_total("<p>sem numero</p>"))

    def test_empty_result_is_not_an_error(self):
        self.assertEqual(parse_search_results(FIXTURE_EMPTY), [])

    def test_unknown_layout_raises(self):
        with self.assertRaises(DouUnavailable):
            parse_search_results(FIXTURE_BROKEN)

    def test_blank_page_raises(self):
        with self.assertRaises(DouUnavailable):
            parse_search_results("   ")

    def test_html_entities_are_unescaped(self):
        rows = parse_search_results(
            '<div class="resultado"><span>Seção 1</span>'
            '<span class="orgao">MEC &amp; CAPES</span>'
            '<a href="/web/dou/-/x">Portaria &quot;X&quot;</a></div>'
        )
        self.assertIn("MEC & CAPES", rows[0].organ)


def rows(n, convenente="UNIVERSIDADE FEDERAL DA BAHIA"):
    return [
        {"numero": f"{i}/2026", "convenente": convenente, "objeto": "pesquisa",
         "valor": "1000.50", "situacao": "VIGENTE"}
        for i in range(n)
    ]


class TestConveniosClient(unittest.TestCase):
    def test_requires_key(self):
        with self.assertRaises(DouPermissionError):
            ConveniosClient(FakeSession([]), "")

    def test_single_page_shorter_than_page_size(self):
        s = FakeSession([FakeResponse(200, rows(3))])
        out = ConveniosClient(s, "k").collect("UFBA")
        self.assertEqual(len(out), 3)
        self.assertEqual(len(s.calls), 1)
        self.assertEqual(out[0].valor, 1000.5)

    def test_paginates_until_empty_page(self):
        s = FakeSession([FakeResponse(200, rows(15)), FakeResponse(200, rows(15)),
                         FakeResponse(200, [])])
        out = ConveniosClient(s, "k").collect("UFBA", delay_s=0)
        self.assertEqual(len(out), 30)
        self.assertEqual(len(s.calls), 3)
        self.assertEqual(s.calls[1][1]["params"]["pagina"], 2)

    def test_respects_page_ceiling(self):
        s = FakeSession([FakeResponse(200, rows(15)) for _ in range(3)])
        out = ConveniosClient(s, "k").collect("UFBA", max_pages=3, delay_s=0)
        self.assertEqual(len(s.calls), 3)
        self.assertEqual(len(out), 45)

    def test_403_raises_permission_error(self):
        s = FakeSession([FakeResponse(403)])
        with self.assertRaises(DouPermissionError):
            ConveniosClient(s, "k").collect("UFBA")

    def test_429_raises_rate_limited(self):
        s = FakeSession([FakeResponse(429)])
        with self.assertRaises(RateLimited):
            ConveniosClient(s, "k").collect("UFBA")

    def test_503_raises_unavailable(self):
        s = FakeSession([FakeResponse(503)])
        with self.assertRaises(DouUnavailable):
            ConveniosClient(s, "k").collect("UFBA")

    def test_non_list_payload_raises(self):
        s = FakeSession([FakeResponse(200, {"erro": "x"})])
        with self.assertRaises(DouUnavailable):
            ConveniosClient(s, "k").collect("UFBA")

    def test_empty_convenente_rejected(self):
        with self.assertRaises(ValueError):
            ConveniosClient(FakeSession([]), "k").collect("  ")

    def test_key_goes_in_header_not_params(self):
        s = FakeSession([FakeResponse(200, [])])
        ConveniosClient(s, "SEGREDO123").collect("UFBA")
        _, kwargs = s.calls[0]
        self.assertEqual(kwargs["headers"]["chave-api-dados"], "SEGREDO123")
        self.assertNotIn("SEGREDO123", str(kwargs["params"]))

    def test_wrong_grantee_detected(self):
        s = FakeSession([FakeResponse(200, rows(3, convenente="OUTRA ENTIDADE"))])
        out = ConveniosClient(s, "k").collect("UNIVERSIDADE FEDERAL DA BAHIA")
        self.assertFalse(verify_first_records(out, "UNIVERSIDADE FEDERAL DA BAHIA"))

    def test_matching_grantee_accepted(self):
        s = FakeSession([FakeResponse(200, rows(3))])
        out = ConveniosClient(s, "k").collect("UNIVERSIDADE FEDERAL DA BAHIA")
        self.assertTrue(verify_first_records(out, "universidade federal da bahia"))

    def test_acronym_does_not_match_the_full_name(self):
        """The guard compares names, not acronyms: pass the grantee as the API spells it."""
        s = FakeSession([FakeResponse(200, rows(2))])
        out = ConveniosClient(s, "k").collect("UFBA")
        self.assertFalse(verify_first_records(out, "UFBA"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
