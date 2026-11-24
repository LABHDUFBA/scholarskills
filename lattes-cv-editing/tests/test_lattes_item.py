"""Offline suite for the Lattes item checker. No network, no browser, no credential."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from lattes_item import (  # noqa: E402
    Item, check_keywords, distinct_pair, find_duplicates, normalize,
    same_record, suggest_keywords, summary, validate,
)


def artigo(**kw):
    base = {"titulo": "Sociologia digital e métodos computacionais",
            "ano": "2026", "periodico": "Revista Brasileira de Sociologia",
            "autores": "Nascimento, Leonardo Fernandes"}
    base.update(kw)
    return Item("artigo_periodico", base)


class TestNormalize(unittest.TestCase):
    def test_strips_accents_and_case(self):
        self.assertEqual(normalize("SOCIOLOGIA Digital"), "sociologia digital")

    def test_removes_punctuation(self):
        self.assertEqual(normalize("Métodos: um balanço."), "metodos um balanco")

    def test_collapses_spaces(self):
        self.assertEqual(normalize("a   b"), "a b")

    def test_empty(self):
        self.assertEqual(normalize(""), "")


class TestValidate(unittest.TestCase):
    def test_complete_item_is_valid(self):
        self.assertEqual(validate(artigo()), [])

    def test_unknown_type(self):
        problems = validate(Item("resenha", {"titulo": "x"}))
        self.assertIn("unknown record type", problems[0])

    def test_missing_title(self):
        self.assertIn("missing required field: titulo", validate(artigo(titulo="")))

    def test_missing_periodico(self):
        self.assertIn("missing required field: periodico", validate(artigo(periodico="")))

    def test_bad_year(self):
        self.assertTrue(any("four-digit" in p for p in validate(artigo(ano="26"))))

    def test_future_year(self):
        self.assertTrue(any("future" in p for p in validate(artigo(ano="2099"))))

    def test_invalid_doi(self):
        self.assertTrue(any("DOI" in p for p in validate(artigo(doi="abc/123"))))

    def test_valid_doi(self):
        self.assertEqual(validate(artigo(doi="10.1590/12345")), [])

    def test_authors_must_look_like_a_list(self):
        self.assertTrue(any("authors" in p for p in validate(artigo(autores="Fulano"))))

    def test_authors_with_semicolon_ok(self):
        self.assertEqual(validate(artigo(autores="A, B; C, D")), [])

    def test_bad_keyword_count(self):
        problems = validate(artigo(palavras_chave=["um", "dois"]))
        self.assertTrue(any("3 to 5 keywords" in p for p in problems))


class TestKeywords(unittest.TestCase):
    def test_correct_keywords_accepted(self):
        ok, why = check_keywords("sociologia digital; métodos; plataformas")
        self.assertTrue(ok, why)

    def test_uppercase_rejected(self):
        ok, _ = check_keywords("Sociologia digital; métodos; plataformas")
        self.assertFalse(ok)

    def test_final_period_rejected(self):
        ok, _ = check_keywords(["sociologia.", "metodos", "plataformas"])
        self.assertFalse(ok)

    def test_suggestions_come_from_the_text(self):
        kws = suggest_keywords("plataformas digitais e sociologia digital: "
                               "plataformas, dados e sociologia")
        self.assertIn("plataformas", kws)
        self.assertIn("sociologia", kws)
        self.assertLessEqual(len(kws), 5)

    def test_suggestions_skip_stopwords(self):
        kws = suggest_keywords("o estudo de plataformas no campo das plataformas")
        self.assertNotIn("das", kws)

    def test_empty_text_gives_no_keywords(self):
        self.assertEqual(suggest_keywords(""), [])


class TestDuplicates(unittest.TestCase):
    def test_identical_title_and_year(self):
        a = artigo()
        b = artigo(periodico="Outra revista")
        self.assertTrue(same_record(a, b))

    def test_accent_difference_still_duplicate(self):
        a = artigo(titulo="Métodos digitais")
        b = artigo(titulo="METODOS DIGITAIS")
        self.assertTrue(same_record(a, b))

    def test_different_year_is_not_duplicate(self):
        self.assertFalse(same_record(artigo(), artigo(ano="2024")))

    def test_similar_title_is_not_duplicate(self):
        a = artigo(titulo="Sociologia digital")
        b = artigo(titulo="Sociologia digital: um balanço")
        self.assertFalse(same_record(a, b))

    def test_find_duplicates_returns_matches(self):
        existing = [artigo(ano="2024"), artigo()]
        self.assertEqual(len(find_duplicates(artigo(), existing)), 1)

    def test_no_duplicates(self):
        self.assertEqual(find_duplicates(artigo(), [artigo(ano="2019")]), [])


class TestDistinctRecords(unittest.TestCase):
    def test_preprint_is_not_a_journal_article(self):
        a = Item("preprint", {"titulo": "X", "ano": "2026", "repositorio": "OSF",
                              "autores": "A, B"})
        b = artigo(titulo="X")
        self.assertIn("preprint", distinct_pair(a, b))

    def test_anais_is_not_periodico(self):
        a = Item("artigo_anais", {"titulo": "X", "ano": "2026", "evento": "SBS",
                                  "autores": "A, B"})
        self.assertIn("conference paper", distinct_pair(a, artigo(titulo="X")))

    def test_unrelated_types_have_no_reason(self):
        a = Item("evento", {"titulo": "X", "ano": "2026"})
        self.assertIsNone(distinct_pair(a, artigo(titulo="Y")))


class TestSummary(unittest.TestCase):
    def test_ready_message(self):
        self.assertIn("pronto para digitação", summary(artigo()))

    def test_pending_count(self):
        s = summary(artigo(titulo="", ano=""))
        self.assertIn("pendência", s)

    def test_lists_are_joined(self):
        s = summary(artigo(palavras_chave=["a", "b", "c"]))
        self.assertIn("a; b; c", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
