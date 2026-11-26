"""Invariants for the generated ScholarSkills hub.

These tests do not prove that a research method works. They prove that the catalogue
does not present a roadmap record as software, that both language trees stay in
parity, and that every internal link points at a generated file.
"""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site  # noqa: E402

REGISTRY = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
SKILLS = REGISTRY["skills"]
AVAILABLE = [s for s in SKILLS if s.get("status") == "available"]
PLANNED = [s for s in SKILLS if s.get("status") == "planned"]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: list[str] = []
        self.h1 = 0
        self.scripts: list[str] = []
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag in ("img", "script") and values.get("src"):
            self.hrefs.append(values["src"])
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_ld:
            self.scripts.append(data)


def parse(path: Path) -> Links:
    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class HubTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_site.CSS_HASH = build_site._css_hash(build_site.css())
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        build_site.build(cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_registry_entries_validate(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = json.loads((ROOT / "registry" / "metadata-schema.json").read_text(encoding="utf-8"))
        for s in SKILLS:
            jsonschema.validate(s, schema)

    def test_ids_and_slugs_are_unique(self):
        self.assertEqual(len({s["id"] for s in SKILLS}), len(SKILLS))
        self.assertEqual(len({s["slug"] for s in SKILLS}), len(SKILLS))

    def test_pages_exist_in_both_languages(self):
        for page_pt, page_en in build_site.PAGES.values():
            self.assertTrue((self.out / page_pt).is_file(), page_pt)
            self.assertTrue((self.out / "en" / page_en).is_file(), page_en)
        for s in SKILLS:
            self.assertTrue((self.out / "skills" / f"{s['slug']}.html").is_file())
            self.assertTrue((self.out / "en" / "skills" / f"{s['slug']}.html").is_file())

    def test_no_template_placeholders(self):
        for path in self.out.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            for marker in ("{rel}", "{css_hash}", "{dimension_cards}", "{dim_headers}",
                           "{evidence_rows}", "{diagram_wide}", "{diagram_tall}", "{email}"):
                self.assertNotIn(marker, text, f"{marker} in {path}")

    def test_roadmap_pages_are_not_presented_as_software(self):
        for s in PLANNED:
            for path in (self.out / "skills" / f"{s['slug']}.html",
                         self.out / "en" / "skills" / f"{s['slug']}.html"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("doi.org/", text)
                self.assertNotIn('id="cite-text"', text)
                self.assertNotIn('id="install"', text)
                self.assertIn("noindex", text)
                self.assertRegex(text, r"roadmap|Roadmap")
                self.assertNotIn('class="badge ok"', text)

    def test_available_pages_carry_install_evidence_limits(self):
        for s in AVAILABLE:
            for path in (self.out / "skills" / f"{s['slug']}.html",
                         self.out / "en" / "skills" / f"{s['slug']}.html"):
                text = path.read_text(encoding="utf-8")
                self.assertIn('id="install"', text)
                self.assertIn('id="cite"', text)
                self.assertTrue(s.get("limits") or s.get("limits_pt"))
                self.assertIn('class="dims-list"', text)

    def test_counters_are_derived(self):
        text = (self.out / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"<b>{len(AVAILABLE)}</b>", text)
        self.assertIn(f"<b>{len(PLANNED)}</b>", text)
        self.assertNotIn("<b>3</b><span>Autores", text.replace(
            f"<b>{len(build_site.unique_authors(REGISTRY))}</b>", ""))

    def test_language_switch_points_to_equivalent_page(self):
        cases = {
            "index.html": ("en/index.html", "../index.html"),
            "conceitos.html": ("en/concepts.html", "../conceitos.html"),
            "skills/zotero-reference-management.html": (
                "../en/skills/zotero-reference-management.html",
                "../../skills/zotero-reference-management.html"),
        }
        for source, (target, back_target) in cases.items():
            parser = parse(self.out / source)
            self.assertIn(target, parser.hrefs, source)
            back = parse((self.out / source).parent / target)
            self.assertIn(back_target, back.hrefs, target)

    def test_internal_links_resolve(self):
        for path in self.out.rglob("*.html"):
            parser = parse(path)
            for href in parser.hrefs:
                if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                    continue
                target = href.split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if target.endswith("/"):
                    resolved = resolved / "index.html"
                self.assertTrue(resolved.exists(), f"{href} in {path.relative_to(self.out)}")

    def test_jsonld_parses(self):
        for path in self.out.rglob("*.html"):
            for block in parse(path).scripts:
                json.loads(block)

    def test_sitemap_matches_generated_files(self):
        xml = (self.out / "sitemap.xml").read_text(encoding="utf-8")
        prefix = build_site.site_root(REGISTRY["hub"])
        locs = re.findall(r"<loc>([^<]+)</loc>", xml)
        self.assertGreaterEqual(len(locs), 2 * (6 + len(SKILLS)))
        for loc in locs:
            self.assertTrue(loc.startswith(prefix), loc)
            rel = loc[len(prefix):]
            self.assertTrue((self.out / rel).is_file(), rel)

    def test_accessibility_scaffold(self):
        for path in self.out.rglob("*.html"):
            parser = parse(path)
            self.assertEqual(parser.h1, 1, path)
            self.assertEqual(len(parser.ids), len(set(parser.ids)), f"duplicate id in {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn('class="skip-link"', text)
            self.assertIn('id="main"', text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
