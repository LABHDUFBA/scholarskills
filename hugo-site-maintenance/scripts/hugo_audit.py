"""Audit a Hugo site before publishing: front matter, internal links, alt text, collisions.

The audit is deliberately conservative about what it calls an error. A site that fails to build is
an error; a page whose title is 90 characters is a warning. Mixing the two is how an audit becomes
noise and stops being read.

No network, no Hugo binary required: this reads the content tree and the rendered output, because
the failures that reach production are usually the ones the build does not catch.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

try:  # PyYAML is a dependency of the validator; fall back to a minimal parser if absent
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

ERROR, WARNING = "error", "warning"

_FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_HTML_IMG = re.compile(r"<img\b[^>]*>", re.I)
_MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
_ALT_ATTR = re.compile(r'alt\s*=\s*"([^"]*)"', re.I)
_HTML_LINK = re.compile(r'<a\b[^>]*?href\s*=\s*"([^"]+)"', re.I)


@dataclass
class Issue:
    level: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"[{self.level}] {self.path}: {self.message}"


@dataclass
class AuditResult:
    issues: list = field(default_factory=list)
    files: int = 0

    @property
    def errors(self) -> list:
        return [i for i in self.issues if i.level == ERROR]

    @property
    def warnings(self) -> list:
        return [i for i in self.issues if i.level == WARNING]

    def ok(self) -> bool:
        return not self.errors


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Return (front matter, body). Front matter is TOML/YAML delimited by ---."""
    m = _FRONT.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    if yaml is None:
        # minimal "key: value" reader, enough for the fields audited here
        data = {}
        for line in raw.splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip('"').strip("'")
        return data, body
    try:
        loaded = yaml.safe_load(raw)
        return (loaded if isinstance(loaded, dict) else {}), body
    except Exception:
        return {}, body


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def audit(content_dir: Path, public_dir: Optional[Path] = None) -> AuditResult:
    """Audit a Hugo `content/` tree (and, optionally, the built `public/`)."""
    res = AuditResult()
    content_dir = Path(content_dir)
    if not content_dir.exists():
        res.issues.append(Issue(ERROR, str(content_dir), "content directory not found"))
        return res

    pages: list[tuple[Path, dict, str]] = []
    for f in sorted(content_dir.rglob("*")):
        if f.suffix.lower() not in (".md", ".markdown", ".html"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_front_matter(text)
        pages.append((f, fm, body))
        res.files += 1

        rel = str(f.relative_to(content_dir))
        if not fm:
            res.issues.append(Issue(WARNING, rel, "no front matter: the page cannot be listed or dated"))
        if not fm.get("title"):
            res.issues.append(Issue(ERROR, rel, "missing title"))
        if not body.strip():
            res.issues.append(Issue(WARNING, rel, "empty body"))
        if fm.get("draft") in (True, "true", "True"):
            res.issues.append(Issue(WARNING, rel, "draft: true — will not be published"))
        date = fm.get("date")
        if date and re.match(r"^\d{4}-\d{2}-\d{2}", str(date)) is None:
            res.issues.append(Issue(WARNING, rel, f"unparseable date: {date!r}"))

        for m in _MD_IMG.finditer(body):
            if not m.group(1).strip():
                res.issues.append(Issue(ERROR, rel, f"image without alt text: {m.group(2)}"))
        for tag in _HTML_IMG.finditer(body):
            if not _ALT_ATTR.search(tag.group(0)):
                res.issues.append(Issue(ERROR, rel, "img tag without alt attribute"))

    # duplicate titles are a real navigation problem, not a style preference
    seen: dict[str, str] = {}
    for f, fm, _ in pages:
        t = _norm(str(fm.get("title") or ""))
        if not t:
            continue
        if t in seen:
            res.issues.append(Issue(WARNING, str(f.relative_to(content_dir)),
                                    f"duplicate title with {seen[t]}"))
        else:
            seen[t] = str(f.relative_to(content_dir))

    if public_dir is not None:
        res = _check_internal_links(res, Path(public_dir))

    return res


def _check_internal_links(res: AuditResult, public_dir: Path) -> AuditResult:
    """Broken internal links are invisible in a green build and obvious to a reader."""
    if not public_dir.exists():
        res.issues.append(Issue(WARNING, str(public_dir), "public/ not found: links not checked"))
        return res
    for page in public_dir.rglob("*.html"):
        text = page.read_text(encoding="utf-8", errors="replace")
        hrefs = [m.group(2) for m in _MD_LINK.finditer(text)]
        hrefs += [m.group(1) for m in _HTML_LINK.finditer(text)]
        for href in hrefs:
            if href.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            clean = href.split("#")[0].split("?")[0]
            # a leading "/" is site-root relative, not filesystem-root relative
            target = (public_dir / clean.lstrip("/")) if clean.startswith("/") \
                else (page.parent / clean)
            target = target.resolve()
            if href.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                res.issues.append(Issue(ERROR, str(page.relative_to(public_dir)),
                                        f"broken internal link: {href}"))
    return res


def summarize(res: AuditResult) -> str:
    return (f"{res.files} files, {len(res.errors)} error(s), "
            f"{len(res.warnings)} warning(s)")
