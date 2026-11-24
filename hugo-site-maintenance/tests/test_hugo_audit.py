"""Offline suite for the Hugo audit. Builds a temporary site with known defects."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from hugo_audit import (  # noqa: E402
    ERROR, WARNING, audit, parse_front_matter, summarize,
)


class Site:
    """Small helper: build a throwaway content tree."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "content").mkdir()

    def page(self, name: str, body: str = "texto") -> Path:
        p = self.root / "content" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        return p

    def close(self):
        self.tmp.cleanup()


GOOD = """---
title: "Publicações"
date: 2026-01-10
---
Texto com um [link](https://example.org).
"""


class TestFrontMatter(unittest.TestCase):
    def test_parses_yaml_block(self):
        fm, body = parse_front_matter(GOOD)
        self.assertEqual(fm["title"], "Publicações")
        self.assertIn("Texto", body)

    def test_no_front_matter_returns_empty(self):
        fm, body = parse_front_matter("só corpo")
        self.assertEqual(fm, {})
        self.assertEqual(body, "só corpo")

    def test_malformed_yaml_does_not_raise(self):
        fm, _ = parse_front_matter("---\ntitle: [unclosed\n---\ncorpo")
        self.assertIsInstance(fm, dict)


class TestAuditContent(unittest.TestCase):
    def setUp(self):
        self.s = Site()

    def tearDown(self):
        self.s.close()

    def test_clean_page_has_no_errors(self):
        self.s.page("a.md", GOOD)
        res = audit(self.s.root / "content")
        self.assertTrue(res.ok())
        self.assertEqual(res.files, 1)

    def test_missing_title_is_error(self):
        self.s.page("a.md", "---\ndate: 2026-01-01\n---\ncorpo")
        res = audit(self.s.root / "content")
        self.assertIn("missing title", " ".join(str(e) for e in res.errors))

    def test_missing_front_matter_is_warning(self):
        self.s.page("a.md", "só corpo")
        res = audit(self.s.root / "content")
        self.assertTrue(any("no front matter" in str(w) for w in res.warnings))

    def test_empty_body_is_warning(self):
        self.s.page("a.md", '---\ntitle: "X"\n---\n')
        res = audit(self.s.root / "content")
        self.assertTrue(any("empty body" in str(w) for w in res.warnings))

    def test_draft_is_warning(self):
        self.s.page("a.md", '---\ntitle: "X"\ndraft: true\n---\ncorpo')
        res = audit(self.s.root / "content")
        self.assertTrue(any("draft" in str(w) for w in res.warnings))

    def test_bad_date_is_warning(self):
        self.s.page("a.md", '---\ntitle: "X"\ndate: "10 de janeiro"\n---\ncorpo')
        res = audit(self.s.root / "content")
        self.assertTrue(any("unparseable date" in str(w) for w in res.warnings))

    def test_markdown_image_without_alt_is_error(self):
        self.s.page("a.md", '---\ntitle: "X"\n---\n![](foto.jpg)')
        res = audit(self.s.root / "content")
        self.assertTrue(any("without alt" in str(e) for e in res.errors))

    def test_markdown_image_with_alt_is_fine(self):
        self.s.page("a.md", '---\ntitle: "X"\n---\n![fachada do prédio](foto.jpg)')
        res = audit(self.s.root / "content")
        self.assertTrue(res.ok())

    def test_html_img_without_alt_is_error(self):
        self.s.page("a.md", '---\ntitle: "X"\n---\n<img src="a.png">')
        res = audit(self.s.root / "content")
        self.assertTrue(any("alt attribute" in str(e) for e in res.errors))

    def test_duplicate_titles_are_reported(self):
        self.s.page("a.md", '---\ntitle: "Sobre"\n---\nx')
        self.s.page("b.md", '---\ntitle: "sobre"\n---\ny')
        res = audit(self.s.root / "content")
        self.assertTrue(any("duplicate title" in str(w) for w in res.warnings))

    def test_missing_content_dir_is_error(self):
        res = audit(self.s.root / "nao-existe")
        self.assertFalse(res.ok())

    def test_nested_pages_are_counted(self):
        self.s.page("blog/2026/a.md", GOOD)
        self.s.page("blog/2026/b.md", GOOD)
        self.assertEqual(audit(self.s.root / "content").files, 2)


class TestInternalLinks(unittest.TestCase):
    def setUp(self):
        self.s = Site()
        (self.s.root / "public").mkdir()

    def tearDown(self):
        self.s.close()

    def test_broken_internal_link_is_error(self):
        (self.s.root / "public" / "index.html").write_text(
            '<a href="/nao-existe/">x</a>', encoding="utf-8")
        res = audit(self.s.root / "content", self.s.root / "public")
        self.assertTrue(any("broken internal link" in str(e) for e in res.errors))

    def test_existing_target_passes(self):
        pub = self.s.root / "public"
        (pub / "sobre").mkdir()
        (pub / "sobre" / "index.html").write_text("ok", encoding="utf-8")
        (pub / "index.html").write_text('<a href="/sobre/">x</a>', encoding="utf-8")
        res = audit(self.s.root / "content", pub)
        self.assertFalse(any("broken internal link" in str(e) for e in res.errors))

    def test_external_links_are_ignored(self):
        (self.s.root / "public" / "index.html").write_text(
            '<a href="https://example.org/x">x</a>', encoding="utf-8")
        res = audit(self.s.root / "content", self.s.root / "public")
        self.assertTrue(res.ok())


class TestSummary(unittest.TestCase):
    def test_summary_counts(self):
        s = Site()
        s.page("a.md", '---\ndate: 2026-01-01\n---\nx')
        res = audit(s.root / "content")
        self.assertIn("1 files", summarize(res))
        self.assertIn("error(s)", summarize(res))
        s.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
