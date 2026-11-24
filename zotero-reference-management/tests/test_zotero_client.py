#!/usr/bin/env python3
"""Offline tests for the Zotero client.

The HTTP layer is replaced by a scripted fake, so the suite is deterministic and needs no
credential and no network. That is deliberate: a test suite that requires a live API key
cannot run in CI, and a suite that runs only on the author's machine is a claim, not a check.
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from zotero_client import (  # noqa: E402
    MAX_LIMIT, ScopeError, ZoteroClient, ZoteroError, provenance,
)


class FakeResponse:
    def __init__(self, status: int = 200, payload=None, headers=None, text: str = "") -> None:
        self.status_code = status
        self._payload = payload if payload is not None else []
        self.headers = headers or {}
        self.text = text or "[]"

    def json(self):
        return self._payload


class FakeSession:
    """Scripted HTTP session: returns queued responses and records the requests."""

    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[str, str, dict]] = []
        self.headers: dict = {}

    def request(self, method: str, url: str, **kwargs):
        self.calls.append((method, url, kwargs.get("params") or {}))
        if not self.responses:
            return FakeResponse(200, [], headers={}, text="[]")  # empty page by default
        return self.responses.pop(0)


def client(responses: list[FakeResponse], **kw) -> ZoteroClient:
    return ZoteroClient(api_key="k" * 20, library_id="1234", session=FakeSession(responses), **kw)


class Construction(unittest.TestCase):
    def test_missing_key_refused(self) -> None:
        with self.assertRaises(ZoteroError):
            ZoteroClient(api_key="", library_id="1")

    def test_missing_library_id_refused(self) -> None:
        with self.assertRaises(ZoteroError):
            ZoteroClient(api_key="k", library_id="")

    def test_invalid_library_type_refused(self) -> None:
        with self.assertRaises(ZoteroError):
            ZoteroClient(api_key="k", library_id="1", library_type="nonsense")

    def test_from_env_requires_variables(self) -> None:
        saved = {k: os.environ.pop(k, None) for k in
                 ("ZOTERO_API_KEY", "ZOTERO_LIBRARY_ID", "ZOTERO_LIBRARY_TYPE")}
        try:
            with self.assertRaises(ZoteroError):
                ZoteroClient.from_env()
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_from_env_reads_variables(self) -> None:
        os.environ["ZOTERO_API_KEY"] = "k" * 20
        os.environ["ZOTERO_LIBRARY_ID"] = "999"
        try:
            c = ZoteroClient.from_env()
            self.assertEqual(c.library_id, "999")
            self.assertEqual(c.library_type, "user")
        finally:
            os.environ.pop("ZOTERO_API_KEY", None)
            os.environ.pop("ZOTERO_LIBRARY_ID", None)


class Pagination(unittest.TestCase):
    def _items(self, n: int) -> list[dict]:
        return [{"key": f"K{i:04d}", "data": {"title": f"t{i}"}} for i in range(n)]

    def test_three_pages_stop_at_short_page(self) -> None:
        c = client([
            FakeResponse(200, self._items(100)),
            FakeResponse(200, self._items(100)),
            FakeResponse(200, self._items(30)),
        ])
        got = list(c.iter_items())
        self.assertEqual(len(got), 230)
        self.assertEqual(len(c.session.calls), 3)

    def test_exact_multiple_needs_an_extra_empty_page(self) -> None:
        c = client([
            FakeResponse(200, self._items(100)),
            FakeResponse(200, self._items(100)),
            FakeResponse(200, []),   # empty page: the only reliable stop signal
        ])
        got = list(c.iter_items())
        self.assertEqual(len(got), 200)
        self.assertEqual(len(c.session.calls), 3)

    def test_start_advances_by_page_size(self) -> None:
        c = client([
            FakeResponse(200, self._items(100)),
            FakeResponse(200, self._items(5)),
        ])
        list(c.iter_items())
        starts = [call[2].get("start") for call in c.session.calls]
        self.assertEqual(starts, [0, 100])

    def test_page_size_above_max_refused(self) -> None:
        c = client([])
        with self.assertRaises(ValueError):
            list(c.iter_items(page_size=MAX_LIMIT + 1))

    def test_attachment_exclusion_is_sent(self) -> None:
        c = client([FakeResponse(200, self._items(3))])
        list(c.iter_items())
        self.assertEqual(c.session.calls[0][2]["itemType"], "-attachment")


class Counting(unittest.TestCase):
    def test_total_from_header_not_from_page_length(self) -> None:
        # Header says 8122; the page has 1 item. Counting the page would report 1.
        c = client([FakeResponse(200, [{"key": "X"}], headers={"Total-Results": "8122"})])
        self.assertEqual(c.count_references(), 8122)

    def test_absent_header_returns_none(self) -> None:
        c = client([FakeResponse(200, [])])
        self.assertIsNone(c.count_references())


class Failures(unittest.TestCase):
    def test_403_raises_scope_error(self) -> None:
        c = client([FakeResponse(403, {"error": "forbidden"}, text="forbidden")])
        with self.assertRaises(ScopeError):
            c.count_references()

    def test_429_is_retried_then_succeeds(self) -> None:
        c = client([
            FakeResponse(429, text="slow down"),
            FakeResponse(200, [{"key": "A"}], headers={"Total-Results": "1"}),
        ], max_retries=2)
        self.assertEqual(c.count_references(), 1)
        self.assertEqual(len(c.session.calls), 2)

    def test_other_4xx_raises(self) -> None:
        c = client([FakeResponse(400, text="bad request")])
        with self.assertRaises(ZoteroError):
            c.count_references()


class ExportAndWrite(unittest.TestCase):
    def test_bibtex_returns_text(self) -> None:
        c = client([FakeResponse(200, [], text="@article{a, title={T}}")])
        self.assertIn("@article", c.export("COL1", "bibtex"))

    def test_export_rejects_unknown_format(self) -> None:
        c = client([])
        with self.assertRaises(ValueError):
            c.export(None, "docx")

    def test_create_sends_a_list(self) -> None:
        c = client([FakeResponse(200, {"successful": {"0": {"key": "NEW"}}})])
        c.create_items([{"itemType": "journalArticle", "title": "X"}])
        _, url, _ = c.session.calls[0]
        self.assertTrue(url.endswith("/users/1234/items"))

    def test_create_refuses_empty(self) -> None:
        c = client([])
        with self.assertRaises(ValueError):
            c.create_items([])


class Provenance(unittest.TestCase):
    def test_provenance_has_no_credential(self) -> None:
        c = client([FakeResponse(200, [{"key": "A"}], headers={"Total-Results": "1"})])
        c.count_references()
        record = provenance(c, 1, "COL1")
        self.assertIn("library_id", record)
        self.assertNotIn("k" * 20, record)


if __name__ == "__main__":
    unittest.main(verbosity=2)
