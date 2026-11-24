"""Offline suite for the SICONFI client."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from siconfi_client import (  # noqa: E402
    Conta, Query, SiconfiAuth, SiconfiClient, SiconfiUnavailable,
    coverage, parse_contas, total,
)


class R:
    def __init__(self, status=200, payload=None):
        self.status_code = status
        self._p = payload

    def json(self):
        return self._p


class S:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, **kw):
        self.calls.append((url, kw))
        return self.responses.pop(0) if self.responses else R(200, {"items": []})


ITEMS = [
    {"cod_conta": "1.0.0.0.00", "desc_conta": "RECEITAS", "valor": "1000.50", "coluna": "Receitas Realizadas"},
    {"cod_conta": "1.1.0.0.00", "desc_conta": "Receitas Correntes", "valor": 600.0, "coluna": "Receitas Realizadas"},
    {"cod_conta": "2.0.0.0.00", "desc_conta": "DESPESAS", "valor": "300,25", "coluna": "Despesas Empenhadas"},
]


class TestQuery(unittest.TestCase):
    def test_accepts_uf_code(self):
        self.assertEqual(Query("29", 2024).validate().id_ente, "29")

    def test_accepts_municipality_code(self):
        self.assertEqual(Query("2927408", 2024).validate().id_ente, "2927408")

    def test_rejects_name_as_entity(self):
        with self.assertRaises(ValueError):
            Query("Bahia", 2024).validate()

    def test_rejects_wrong_code_length(self):
        with self.assertRaises(ValueError):
            Query("29274080", 2024).validate()

    def test_rejects_unknown_demonstrativo(self):
        with self.assertRaises(ValueError):
            Query("29", 2024, demonstrativo="XYZ").validate()

    def test_rejects_absurd_year(self):
        with self.assertRaises(ValueError):
            Query("29", 1800).validate()

    def test_params_carry_period_and_type(self):
        p = Query("29", 2024, periodo=3).params()
        self.assertEqual(p["nr_periodo"], 3)
        self.assertEqual(p["co_tipo_demonstrativo"], "RREO")
        self.assertEqual(p["an_exercicio"], 2024)


class TestClient(unittest.TestCase):
    def test_unwraps_items(self):
        s = S(R(200, {"items": ITEMS}))
        self.assertEqual(len(SiconfiClient(s).fetch(Query("29", 2024))), 3)

    def test_accepts_bare_list(self):
        s = S(R(200, ITEMS))
        self.assertEqual(len(SiconfiClient(s).fetch(Query("29", 2024))), 3)

    def test_empty_delivery_is_not_an_error(self):
        s = S(R(200, {"items": []}))
        self.assertEqual(SiconfiClient(s).fetch(Query("29", 2024)), [])

    def test_403_raises_auth(self):
        with self.assertRaises(SiconfiAuth):
            SiconfiClient(S(R(403))).fetch(Query("29", 2024))

    def test_500_raises_unavailable(self):
        with self.assertRaises(SiconfiUnavailable):
            SiconfiClient(S(R(500))).fetch(Query("29", 2024))

    def test_malformed_payload_raises(self):
        with self.assertRaises(SiconfiUnavailable):
            SiconfiClient(S(R(200, {"erro": "x"}))).fetch(Query("29", 2024))

    def test_path_uses_demonstrativo(self):
        s = S(R(200, {"items": []}))
        SiconfiClient(s).fetch(Query("29", 2024, demonstrativo="RGF"))
        self.assertTrue(s.calls[0][0].endswith("/rgf"))


class TestParsing(unittest.TestCase):
    def test_parses_brazilian_and_plain_numbers(self):
        c = parse_contas(ITEMS)
        self.assertEqual(len(c), 3)
        self.assertEqual(c[0].valor, 1000.50)
        self.assertEqual(c[2].valor, 300.25)

    def test_skips_row_without_value(self):
        c = parse_contas([{"cod_conta": "1.0", "desc_conta": "X"}])
        self.assertEqual(c, [])

    def test_skips_non_dict_rows(self):
        self.assertEqual(parse_contas(["lixo", 3, None]), [])

    def test_total_by_prefix(self):
        c = parse_contas(ITEMS)
        self.assertAlmostEqual(total(c, "1."), 1600.50)

    def test_total_rejects_empty_prefix(self):
        with self.assertRaises(ValueError):
            total(parse_contas(ITEMS), "  ")

    def test_coverage_reports_columns(self):
        cov = coverage(parse_contas(ITEMS))
        self.assertEqual(cov["contas"], 3)
        self.assertIn("Despesas Empenhadas", cov["colunas"])

    def test_conta_roundtrip(self):
        self.assertEqual(Conta("1", "X", 2.5).as_dict()["valor"], 2.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
