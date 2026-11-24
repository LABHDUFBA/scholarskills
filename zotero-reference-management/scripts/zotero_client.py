#!/usr/bin/env python3
"""Minimal Zotero Web API v3 client.

Design rules, in order of importance:

1. The API key defines the boundary of access. The client never widens it and never
   falls back to another credential source.
2. Credentials come from the environment. The client refuses to run without them and
   never logs them.
3. Totals come from the `Total-Results` header, not from the length of a page. Counting
   by page length is how libraries get silently truncated.

No network call happens at import time, which is what makes the test suite offline.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Iterator

import requests

API_BASE = "https://api.zotero.org"
API_VERSION = "3"
MAX_LIMIT = 100
RETRY_STATUSES = {429, 503}


class ZoteroError(RuntimeError):
    """Raised for API failures that the caller must handle, not swallow."""


class ScopeError(ZoteroError):
    """Raised when the key does not grant the operation the caller needs."""


@dataclass
class ZoteroClient:
    api_key: str
    library_id: str
    library_type: str = "user"
    base_url: str = API_BASE
    session: requests.Session | None = None
    timeout: int = 30
    max_retries: int = 3
    stats: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ZoteroError("ZOTERO_API_KEY is empty")
        if not self.library_id:
            raise ZoteroError("ZOTERO_LIBRARY_ID is empty")
        if self.library_type not in ("user", "group"):
            raise ZoteroError("ZOTERO_LIBRARY_TYPE must be 'user' or 'group'")
        if self.session is None:
            self.session = requests.Session()
        self.session.headers.update({
            "Zotero-API-Key": self.api_key,
            "Zotero-API-Version": API_VERSION,
            "Accept": "application/json",
        })

    # ---------------------------------------------------------------- plumbing

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        attempt = 0
        while True:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            if resp.status_code in RETRY_STATUSES and attempt < self.max_retries:
                attempt += 1
                time.sleep(min(2 ** attempt, 8))
                continue
            if resp.status_code == 403:
                raise ScopeError(
                    "HTTP 403 from Zotero: the API key does not grant this operation. "
                    f"path={path}"
                )
            if resp.status_code >= 400:
                raise ZoteroError(f"HTTP {resp.status_code} for {path}: {resp.text[:200]}")
            self.stats["requests"] = self.stats.get("requests", 0) + 1
            return resp

    @classmethod
    def from_env(cls, **kwargs: Any) -> "ZoteroClient":
        return cls(
            api_key=os.environ.get("ZOTERO_API_KEY", ""),
            library_id=os.environ.get("ZOTERO_LIBRARY_ID", ""),
            library_type=os.environ.get("ZOTERO_LIBRARY_TYPE", "user"),
            **kwargs,
        )

    # ----------------------------------------------------------------- library

    def whoami(self, key: str | None = None) -> dict:
        """GET /keys/{key} — userID and permission scope. The only safe way to learn the id."""
        key = key or self.api_key
        resp = self._request("GET", f"/keys/{key}")
        return resp.json()

    @property
    def _lib_path(self) -> str:
        return f"/{self.library_type}s/{self.library_id}"

    def total_results(self, path: str, params: dict | None = None) -> int | None:
        """Read Total-Results without downloading the page. None when the header is absent."""
        resp = self._request("GET", path, params={**(params or {}), "limit": 1})
        header = resp.headers.get("Total-Results")
        return int(header) if header is not None else None

    def iter_items(self, collection: str | None = None, query: str | None = None,
                   tags: list[str] | None = None, item_type: str = "-attachment",
                   page_size: int = MAX_LIMIT) -> Iterator[dict]:
        """Yield items page by page. Stops on an empty page, never on a counter."""
        if not 1 <= page_size <= MAX_LIMIT:
            raise ValueError(f"page_size must be 1..{MAX_LIMIT}")
        path = f"{self._lib_path}/collections/{collection}/items" if collection \
            else f"{self._lib_path}/items"
        params: dict[str, Any] = {"limit": page_size, "format": "json"}
        if item_type:
            params["itemType"] = item_type
        if query:
            params["q"] = query
            params["qmode"] = "everything"
        if tags:
            params["tag"] = tags[0]          # the API takes one tag per parameter
        start = 0
        while True:
            resp = self._request("GET", path, params={**params, "start": start})
            batch = resp.json()
            if not batch:
                return
            for item in batch:
                yield item
            start += len(batch)
            if len(batch) < page_size:
                return

    def count_references(self, collection: str | None = None) -> int | None:
        """Reference count (attachments excluded)."""
        path = f"{self._lib_path}/collections/{collection}/items" if collection \
            else f"{self._lib_path}/items"
        return self.total_results(path, {"itemType": "-attachment"})

    def collections(self, top: bool = False) -> list[dict]:
        path = f"{self._lib_path}/collections" + ("/top" if top else "")
        return self._request("GET", path, params={"limit": MAX_LIMIT, "format": "json"}).json()

    def export(self, collection: str | None = None, fmt: str = "bibtex") -> str:
        """Rendered bibliography. Note: bibtex ignores `limit` on the items endpoint."""
        if fmt not in ("bibtex", "ris", "csljson"):
            raise ValueError("fmt must be bibtex, ris or csljson")
        path = f"{self._lib_path}/collections/{collection}/items" if collection \
            else f"{self._lib_path}/items"
        params = {"format": fmt, "itemType": "-attachment"}
        return self._request("GET", path, params=params).text

    def create_items(self, items: list[dict]) -> dict:
        """POST a JSON array — a bare object is rejected by the API."""
        if not items:
            raise ValueError("create_items needs at least one item")
        resp = self._request("POST", f"{self._lib_path}/items", json=items)
        return resp.json()


def provenance(client: ZoteroClient, count: int | None, source: str) -> str:
    return json.dumps({
        "source": source,
        "library_type": client.library_type,
        "library_id": client.library_id,
        "references": count,
        "api_requests": client.stats.get("requests", 0),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }, ensure_ascii=False)
