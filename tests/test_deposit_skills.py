"""Offline tests for the per-skill deposit client. No network: the HTTP layer is stubbed."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import deposit_skills as ds  # noqa: E402


REG = {
    "hub": {"repo_url": "https://github.com/LABHDUFBA/scholarskills",
            "site_url": "https://labhdufba.github.io/scholarskills",
            "release": "1.1.0"},
    "skills": [
        {"id": "SS-0010", "slug": "dou-federal-gazette", "status": "available",
         "title": "DOU and Federal Covenants", "summary": "Collect gazette publications.",
         "version": "1.0.0", "keywords": ["DOU", "open data"],
         "authors": [{"name": "Leonardo Fernandes Nascimento",
                      "affiliation": "LABHDUFBA/UFBA"}]},
        {"id": "SS-0002", "slug": "systematic-literature-review", "status": "planned",
         "title": "SLR", "summary": "planned"},
    ],
}


class FakeResponse:
    def __init__(self, status=201, payload=None):
        self.status_code = status
        self._p = payload or {}

    def json(self):
        return self._p


class FakeSession:
    def __init__(self, script=None):
        self.headers = {}
        self.calls = []
        self.script = script or []

    def _next(self, default):
        return self.script.pop(0) if self.script else default

    def post(self, url, **kw):
        self.calls.append(("POST", url, kw))
        return self._next(FakeResponse(201, {"id": 1, "doi": "10.5281/zenodo.1",
                                             "links": {"bucket": "https://bucket"}}))

    def put(self, url, **kw):
        self.calls.append(("PUT", url, kw))
        return self._next(FakeResponse(201))

    def update(self, *a, **k):
        pass


class TestMetadata(unittest.TestCase):
    def test_creator_is_formatted_surname_first(self):
        p = ds.build_skill_payload(REG["skills"][0], REG["hub"], None, Path("/tmp/x.zip"))
        self.assertEqual(p.metadata["creators"][0]["name"], "Nascimento, Leonardo Fernandes")

    def test_title_carries_the_identifier(self):
        p = ds.build_skill_payload(REG["skills"][0], REG["hub"], None, Path("/tmp/x.zip"))
        self.assertIn("SS-0010", p.metadata["title"])

    def test_description_mentions_structural_validation(self):
        p = ds.build_skill_payload(REG["skills"][0], REG["hub"], None, Path("/tmp/x.zip"))
        self.assertIn("structural", p.metadata["description"])

    def test_collection_doi_becomes_isPartOf(self):
        p = ds.build_skill_payload(REG["skills"][0], REG["hub"], "10.5281/zenodo.9",
                                   Path("/tmp/x.zip"))
        rel = {(r["relation"], r["identifier"]) for r in p.metadata["related_identifiers"]}
        self.assertIn(("isPartOf", "10.5281/zenodo.9"), rel)

    def test_no_collection_doi_means_no_isPartOf(self):
        p = ds.build_skill_payload(REG["skills"][0], REG["hub"], None, Path("/tmp/x.zip"))
        self.assertFalse(any(r["relation"] == "isPartOf"
                             for r in p.metadata["related_identifiers"]))

    def test_keywords_are_extended_not_replaced(self):
        p = ds.build_skill_payload(REG["skills"][0], REG["hub"], None, Path("/tmp/x.zip"))
        self.assertIn("DOU", p.metadata["keywords"])
        self.assertIn("agent skills", p.metadata["keywords"])

    def test_each_skill_gets_its_own_record(self):
        payloads = ds.plan(REG)
        slugs = [p.slug for p in payloads]
        self.assertIn("__collection__", slugs)
        self.assertIn("dou-federal-gazette", slugs)

    def test_planned_skills_are_not_deposited(self):
        slugs = [p.slug for p in ds.plan(REG)]
        self.assertNotIn("systematic-literature-review", slugs)

    def test_only_filters_to_one_skill(self):
        payloads = ds.plan(REG, only="dou-federal-gazette")
        self.assertEqual([p.slug for p in payloads if p.slug != "__collection__"],
                         ["dou-federal-gazette"])

    def test_collection_payload_lists_available_skills(self):
        p = ds.build_collection_payload(REG)
        self.assertIn("SS-0010", p.metadata["description"])
        self.assertNotIn("SS-0002", p.metadata["description"])


class TestPackaging(unittest.TestCase):
    def test_zip_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "skill"
            src.mkdir()
            (src / "SKILL.md").write_text("conteudo", encoding="utf-8")
            a = ds.package_dir(src, Path(tmp) / "a.zip")
            b = ds.package_dir(src, Path(tmp) / "b.zip")
            self.assertEqual(ds.sha256(a), ds.sha256(b))

    def test_pycache_is_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "skill"
            (src / "__pycache__").mkdir(parents=True)
            (src / "__pycache__" / "x.pyc").write_bytes(b"lixo")
            (src / "SKILL.md").write_text("ok", encoding="utf-8")
            z = ds.package_dir(src, Path(tmp) / "x.zip")
            import zipfile
            names = zipfile.ZipFile(z).namelist()
            self.assertIn("SKILL.md", names)
            self.assertFalse(any("__pycache__" in n for n in names))


class TestClient(unittest.TestCase):
    def test_missing_token_is_refused(self):
        with self.assertRaises(ds.ZenodoError):
            ds.ZenodoClient("", "https://sandbox.zenodo.org/api")

    def test_token_goes_in_header_not_url(self):
        s = FakeSession()
        c = ds.ZenodoClient("SEGREDO", "https://sandbox.zenodo.org/api", session=s)
        self.assertEqual(s.headers["Authorization"], "Bearer SEGREDO")
        self.assertNotIn("SEGREDO", c.base)

    def test_create_returns_deposition(self):
        s = FakeSession()
        c = ds.ZenodoClient("k", "https://api", session=s)
        dep = c.create({"title": "x"})
        self.assertEqual(dep["id"], 1)
        self.assertIn("/deposit/depositions", s.calls[0][1])

    def test_http_error_raises(self):
        s = FakeSession([FakeResponse(403, {"message": "forbidden"})])
        c = ds.ZenodoClient("k", "https://api", session=s)
        with self.assertRaises(ds.ZenodoError):
            c.create({"title": "x"})

    def test_publish_hits_the_action_endpoint(self):
        s = FakeSession([FakeResponse(202, {"doi": "10.5281/zenodo.5"})])
        c = ds.ZenodoClient("k", "https://api", session=s)
        out = c.publish(7)
        self.assertEqual(out["doi"], "10.5281/zenodo.5")
        self.assertIn("/7/actions/publish", s.calls[0][1])

    def test_full_flow_writes_state(self):
        s = FakeSession([
            FakeResponse(201, {"id": 42, "links": {"bucket": "https://b"}}),   # create
            FakeResponse(201),                                                  # upload
            FakeResponse(202, {"doi": "10.5281/zenodo.42",
                               "conceptdoi": "10.5281/zenodo.41"}),             # publish
        ])
        c = ds.ZenodoClient("k", "https://api", session=s)
        dep = c.create({"title": "x"})
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.zip"
            f.write_bytes(b"zip")
            c.upload(dep["links"]["bucket"], f)
        out = c.publish(dep["id"])
        state = {"deposits": {}}
        ds.record(state, "dou-federal-gazette", "sandbox", "SS-0010", out["doi"],
                  out["conceptdoi"], 42, "1.0.0", "abc")
        self.assertEqual(state["deposits"]["dou-federal-gazette"]["version_doi"],
                         "10.5281/zenodo.42")
        self.assertEqual(state["deposits"]["dou-federal-gazette"]["concept_doi"],
                         "10.5281/zenodo.41")


class TestSafety(unittest.TestCase):
    def test_dry_run_is_the_default(self):
        self.assertEqual(ds.main(["--only", "dou-federal-gazette"]), 0)

    def test_publish_without_env_refuses(self):
        # --publish without --env must not reach the network
        self.assertEqual(ds.main(["--publish", "--only", "dou-federal-gazette"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
