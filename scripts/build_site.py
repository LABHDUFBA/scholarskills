#!/usr/bin/env python3
"""Generate the ScholarSkills hub from registry/registry.json.

The registry is the single source of truth. The site is a build artefact: if a skill is
not in the registry, it is not on the site, and there is no second place to edit.

    python3 scripts/build_site.py [--out site] [--check]

--check exits 1 if the generated output differs from what is on disk (CI guard).
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "registry.json"

MATURITY_LABEL = {
    "experimental": ("Experimental", "warn"),
    "tested": ("Tested", "ok"),
    "peer-reviewed": ("Peer-reviewed", "accent"),
    "replicated": ("Replicated", "accent"),
}
STATUS_LABEL = {"available": ("Available", "ok"), "planned": ("Planned", "muted"),
                "deprecated": ("Deprecated", "bad")}


def esc(value) -> str:
    return html.escape(str(value)) if value is not None else ""


def css() -> str:
    return """/* ScholarSkills hub — no framework, no tracking, no build step */
:root{
  --bg:#fbfbfc; --surface:#fff; --ink:#16181d; --muted:#5d6470; --line:#e3e6ec;
  --accent:#557EB5; --accent-soft:#eaf0f8; --ok:#1f7a4d; --ok-soft:#e6f4ec;
  --warn:#8a5b00; --warn-soft:#fdf3e0; --bad:#a33; --bad-soft:#fbeaea;
  --radius:14px; --maxw:1120px;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html,body{overflow-x:hidden}
.grid{min-width:0}
.card{min-width:0;overflow-wrap:anywhere}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}

header.site{position:sticky;top:0;z-index:20;background:rgba(251,251,252,.88);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;gap:16px;height:64px}
.brand{display:flex;align-items:center;gap:10px;font-weight:650;letter-spacing:-.01em;color:var(--ink)}
.brand .mark{width:26px;height:26px;border-radius:8px;background:var(--accent);color:#fff;
  display:grid;place-items:center;font-size:14px;font-weight:700}
.brand small{font-weight:400;color:var(--muted);font-size:13px}
nav.site{margin-left:auto;display:flex;gap:26px;font-size:14px}
nav.site a{color:var(--muted)}
nav.site a:hover{color:var(--ink)}

.hero{padding:64px 0 40px;border-bottom:1px solid var(--line)}
.hero h1{margin:0 0 12px;font-size:clamp(30px,4vw,46px);line-height:1.12;letter-spacing:-.025em}
.hero p.lede{margin:0;max-width:62ch;color:var(--muted);font-size:18px;line-height:1.55}
.hero .inst{margin-top:18px;font-size:14px;color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 18px;
  flex:1 1 0;min-width:140px}
.stat b{display:block;font-size:22px;letter-spacing:-.02em}
.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}

.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:28px 0 8px}
.toolbar input,.toolbar select{font:inherit;font-size:14px;padding:9px 12px;border:1px solid var(--line);
  border-radius:10px;background:var(--surface);color:var(--ink);min-width:180px}
.toolbar input{min-width:300px;flex:1 1 300px;max-width:420px}
.toolbar input:focus,.toolbar select:focus{outline:2px solid var(--accent-soft);border-color:var(--accent)}
.count{margin-left:auto;font-size:13px;color:var(--muted)}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px;padding:8px 0 56px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:22px;display:flex;flex-direction:column;gap:12px;transition:.16s ease;position:relative}
.card:hover{border-color:var(--accent);transform:translateY(-2px);
  box-shadow:0 10px 28px rgba(85,126,181,.10)}
.card .top{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.code{font-family:var(--mono);font-size:12px;color:var(--muted);background:#f2f4f8;
  border:1px solid var(--line);border-radius:6px;padding:2px 7px}
.card h3{margin:0;font-size:18px;line-height:1.3;letter-spacing:-.01em}
.card h3 a{color:var(--ink)}
.card p{margin:0;color:var(--muted);font-size:14.5px}
.card .meta{display:flex;flex-wrap:wrap;gap:8px;font-size:12px;color:var(--muted);margin-top:auto;padding-top:6px}
.card .authors{font-size:12.5px;color:var(--muted)}
.card .cta{display:flex;gap:10px;align-items:center;margin-top:4px;font-size:13.5px;font-weight:550}

.badge{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:999px;letter-spacing:.02em;
  border:1px solid transparent;white-space:nowrap}
.badge.ok{background:var(--ok-soft);color:var(--ok)}
.badge.warn{background:var(--warn-soft);color:var(--warn)}
.badge.accent{background:var(--accent-soft);color:var(--accent)}
.badge.muted{background:#f2f4f8;color:var(--muted)}
.badge.bad{background:var(--bad-soft);color:var(--bad)}

/* detail page */
.skill-head{padding:48px 0 28px;border-bottom:1px solid var(--line)}
.crumbs{font-size:13px;color:var(--muted);margin-bottom:14px}
.crumbs .current{color:var(--ink);font-weight:550}
.skill-head h1{margin:0 0 12px;font-size:clamp(26px,3.4vw,40px);letter-spacing:-.02em;line-height:1.15}
.skill-head .meta-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:14px;font-size:13px;color:var(--muted)}
.cols{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:40px;padding:40px 0 72px}
@media(max-width:880px){.cols{grid-template-columns:1fr;gap:28px}}
h2.sec{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);
  margin:34px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
h2.sec:first-child{margin-top:0}
.steps{margin:0;padding-left:22px}
.steps li{margin-bottom:10px}
pre{background:#0f1216;color:#e8ecf2;padding:16px 18px;border-radius:12px;overflow:auto;
  font-family:var(--mono);font-size:13px;line-height:1.55}
blockquote{margin:0;padding:16px 20px;background:var(--accent-soft);border-left:3px solid var(--accent);
  border-radius:0 10px 10px 0;font-size:14.5px;color:#25303f}
aside .panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;margin-bottom:16px}
aside .panel h4{margin:0 0 12px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
dl.facts{margin:0;display:grid;grid-template-columns:auto 1fr;gap:8px 14px;font-size:13.5px}
dl.facts dt{color:var(--muted)}
dl.facts dd{margin:0;text-align:right;overflow-wrap:anywhere;text-wrap:balance}
.btn{display:inline-block;padding:9px 14px;border-radius:10px;font-size:13.5px;font-weight:600;
  border:1px solid var(--line);color:var(--ink);background:var(--surface)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{filter:brightness(1.06);text-decoration:none}
.note{font-size:12.5px;color:var(--muted);margin-top:10px}

footer.site{border-top:1px solid var(--line);padding:32px 0 48px;font-size:13px;color:var(--muted)}
footer.site .wrap{display:flex;flex-wrap:wrap;gap:16px;align-items:center}
footer.site .right{margin-left:auto}
.empty{padding:40px 0;color:var(--muted)}
@media(prefers-color-scheme:dark){
  :root{--bg:#0e1013;--surface:#15181d;--ink:#e9edf3;--muted:#9aa3b0;--line:#252a32;
        --accent:#7fa3d4;--accent-soft:#1b2634;--ok:#6fcf9b;--ok-soft:#14251c;
        --warn:#e0b062;--warn-soft:#2a2113;--bad:#e08c8c;--bad-soft:#2a1717}
  .code{background:#1a1e25}
  header.site{background:rgba(14,16,19,.86)}
  blockquote{color:#cfd8e4}
}
"""


def js() -> str:
    return """// Filtering is client-side and progressive: with JS off, all cards remain visible.
(function(){
  const q = document.getElementById('q');
  const status = document.getElementById('f-status');
  const maturity = document.getElementById('f-maturity');
  const cards = Array.from(document.querySelectorAll('[data-skill]'));
  const count = document.getElementById('count');
  if(!cards.length) return;

  function apply(){
    const term = (q?.value || '').toLowerCase().trim();
    const st = status?.value || '';
    const mt = maturity?.value || '';
    let shown = 0;
    cards.forEach(card => {
      const hay = card.dataset.search || '';
      const okTerm = !term || hay.includes(term);
      const okStatus = !st || card.dataset.status === st;
      const okMaturity = !mt || card.dataset.maturity === mt;
      const show = okTerm && okStatus && okMaturity;
      card.style.display = show ? '' : 'none';
      if(show) shown++;
    });
    if(count) count.textContent = shown + (shown === 1 ? ' skill' : ' skills');
    const empty = document.getElementById('empty');
    if(empty) empty.hidden = shown !== 0;
  }
  q?.addEventListener('input', apply);
  status?.addEventListener('change', apply);
  maturity?.addEventListener('change', apply);
  apply();

  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const target = document.getElementById(btn.dataset.copy);
      if(!target) return;
      try{
        await navigator.clipboard.writeText(target.innerText);
        const old = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(() => btn.textContent = old, 1600);
      }catch(e){ /* clipboard blocked: the text is still selectable */ }
    });
  });
})();
"""


def head(title: str, description: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{{root}}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%23557EB5'/><text x='16' y='22' font-size='16' text-anchor='middle' fill='white' font-family='sans-serif'>S</text></svg>">
</head>
<body>"""


def header(root: str, hub: dict) -> str:
    return f"""<header class="site"><div class="wrap">
  <a class="brand" href="{root}index.html"><span class="mark">S</span>
    ScholarSkills <small>LABHDUFBA</small></a>
  <nav class="site">
    <a href="{root}index.html#skills">Skills</a>
    <a href="{root}index.html#levels">Maturity</a>
    <a href="{hub.get('submission_url') or '#'}">Submit</a>
    <a href="{hub.get('repo_url') or '#'}">GitHub</a>
  </nav>
</div></header>"""


def footer(hub: dict) -> str:
    return f"""<footer class="site"><div class="wrap">
  <span>{esc(hub.get('institution',''))}</span>
  <span class="right">Code MIT · Documentation CC BY 4.0 · no tracking, no cookies</span>
</div></footer>
<script src="{{root}}assets/app.js"></script>
</body></html>"""


def badge(value: str | None, table: dict) -> str:
    if not value:
        return '<span class="badge muted">—</span>'
    label, klass = table.get(value, (value, "muted"))
    return f'<span class="badge {klass}">{esc(label)}</span>'


def card(s: dict) -> str:
    authors = s.get("authors") or []
    names = ", ".join(a.get("name", "") for a in authors) if authors else "—"
    search = " ".join(filter(None, [
        s.get("id"), s.get("slug"), s.get("title"), s.get("summary"),
        " ".join(s.get("keywords") or []), names,
    ])).lower()
    summary = s.get("summary") or "Planned skill — not available yet."
    version = s.get("version") or "—"
    return f"""<article class="card" data-skill data-status="{esc(s.get('status'))}"
  data-maturity="{esc(s.get('maturity') or '')}" data-search="{esc(search)}">
  <div class="top">
    <span class="code">{esc(s.get('id'))}</span>
    {badge(s.get('maturity'), MATURITY_LABEL)}
    {badge(s.get('status'), STATUS_LABEL)}
  </div>
  <h3><a href="skills/{esc(s.get('slug'))}.html">{esc(s.get('title'))}</a></h3>
  <p>{esc(summary)}</p>
  <div class="authors">{esc(names)}</div>
  <div class="meta">
    <span>v{esc(version)}</span>
    <span>·</span>
    <span>{esc(s.get('license') or 'licence pending')}</span>
    {('<span>·</span><span>DOI: ' + esc(s.get('doi_version')) + '</span>') if s.get('doi_version') else ''}
  </div>
  <div class="cta"><a href="skills/{esc(s.get('slug'))}.html">View details →</a></div>
</article>"""


def render_index(reg: dict) -> str:
    hub = reg.get("hub", {})
    skills = reg["skills"]
    available = [s for s in skills if s.get("status") == "available"]
    with_doi = [s for s in skills if s.get("doi_version") or s.get("doi_concept")]
    planned = [s for s in skills if s.get("status") == "planned"]
    ordered = sorted(skills, key=lambda s: (0 if s.get("status") == "available" else 1,
                                            0 if s.get("highlight") else 1, s.get("id") or ""))

    body = head(hub.get("title", "ScholarSkills"),
                hub.get("description", "An academic hub of executable research methodologies."))
    body += header("", hub)
    body += f"""<section class="hero"><div class="wrap">
  <h1>{esc(hub.get('title','ScholarSkills'))}</h1>
  <p class="lede">{esc(hub.get('tagline',''))}</p>
  <p class="inst">{esc(hub.get('description',''))}</p>
  <div class="stats">
    <div class="stat"><b>{len(available)}</b><span>available</span></div>
    <div class="stat"><b>{len(planned)}</b><span>planned</span></div>
    <div class="stat"><b>{len(with_doi)}</b><span>with DOI</span></div>
    <div class="stat"><b>3</b><span>authors</span></div>
  </div>
</div></section>

<main class="wrap">
  <div class="toolbar">
    <input id="q" type="search" placeholder="Search skills, keywords, authors…" aria-label="Search skills">
    <select id="f-status" aria-label="Filter by status">
      <option value="">All statuses</option>
      <option value="available">Available</option>
      <option value="planned">Planned</option>
    </select>
    <select id="f-maturity" aria-label="Filter by maturity">
      <option value="">All maturity levels</option>
      <option value="experimental">Experimental</option>
      <option value="tested">Tested</option>
      <option value="peer-reviewed">Peer-reviewed</option>
      <option value="replicated">Replicated</option>
    </select>
    <span class="count" id="count">{len(skills)} skills</span>
  </div>

  <div class="grid" id="skills">
"""
    body += "\n".join(card(s) for s in ordered)
    body += """
  </div>
  <p class="empty" id="empty" hidden>No skill matches these filters.</p>

  <section id="levels" style="padding:8px 0 64px">
    <h2 class="sec">Maturity levels — evidence, not aspiration</h2>
    <p style="max-width:70ch;color:var(--muted)">A level is granted only with the artefact that
    justifies it, stored in the skill repository. Green tests prove structure; they do not prove a
    method. Peer review and replication are social processes with their own records.</p>
    <div class="grid" style="padding-top:18px">
      <article class="card"><div class="top"><span class="badge muted">Experimental</span></div>
        <p>Works on the author's machine. No independent evidence.</p></article>
      <article class="card"><div class="top"><span class="badge ok">Tested</span></div>
        <p>Automated tests pass in a recorded environment (<code>tests/RESULTS.md</code>).</p></article>
      <article class="card"><div class="top"><span class="badge accent">Peer-reviewed</span></div>
        <p>Two named reviewers applied the editorial policy; verdicts in <code>reviews/</code>.</p></article>
      <article class="card"><div class="top"><span class="badge accent">Replicated</span></div>
        <p>Re-executed by a non-author with a published report.</p></article>
    </div>
  </section>
</main>
"""
    body += footer(hub)
    return body.replace("{root}", "")


def render_skill(s: dict, hub: dict, total_available: int) -> str:
    root = "../"
    body = head(f"{s.get('title')} — ScholarSkills",
                s.get("summary") or "ScholarSkills skill")
    body += header(root, hub)
    authors = s.get("authors") or []
    author_rows = "".join(
        f"<tr><td>{esc(a.get('name'))}</td><td>{esc(a.get('affiliation') or '—')}</td>"
        f"<td>{esc(a.get('orcid') or '—')}</td></tr>" for a in authors
    ) or '<tr><td colspan="3">—</td></tr>'
    steps = s.get("how_it_works") or []
    steps_html = ("<ol class=\"steps\">" + "".join(f"<li>{esc(x)}</li>" for x in steps) + "</ol>"
                  ) if steps else '<p style="color:var(--muted)">Not documented yet.</p>'
    links = s.get("links") or {}
    link_html = "".join(
        f'<a class="btn" style="margin:0 8px 8px 0" href="{esc(url)}">{esc(name.title())}</a>'
        for name, url in links.items()) or ""
    doi = s.get("doi_version")
    cite = s.get("cite") or f"{esc(s.get('title'))} (2026). ScholarSkills {esc(s.get('id'))}."

    body += f"""<section class="skill-head"><div class="wrap">
  <div class="crumbs"><a href="{root}index.html">Hub</a> / <span class="current">{esc(s.get('id'))}</span></div>
  <h1>{esc(s.get('title'))}</h1>
  <p class="lede" style="max-width:70ch;color:var(--muted)">{esc(s.get('summary') or '')}</p>
  <div class="meta-row">
    <span class="code">{esc(s.get('id'))}</span>
    {badge(s.get('maturity'), MATURITY_LABEL)}
    {badge(s.get('status'), STATUS_LABEL)}
    <span>v{esc(s.get('version') or '—')}</span>
    <span>·</span><span>{esc(s.get('license') or 'licence pending')}</span>
  </div>
</div></section>

<main class="wrap"><div class="cols">
  <div>
    <h2 class="sec">Objective</h2>
    <p>{esc(s.get('objective') or s.get('summary') or 'Not documented yet.')}</p>

    <h2 class="sec">How it works</h2>
    {steps_html}

    <h2 class="sec">Authors</h2>
    <table style="width:100%;border-collapse:collapse;font-size:14px">
      <thead><tr style="text-align:left;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em">
        <th style="padding:8px 0;border-bottom:1px solid var(--line)">Name</th>
        <th style="padding:8px 0;border-bottom:1px solid var(--line)">Affiliation</th>
        <th style="padding:8px 0;border-bottom:1px solid var(--line)">ORCID</th>
      </tr></thead>
      <tbody>{author_rows}</tbody>
    </table>

    <h2 class="sec">How to cite</h2>
    <blockquote id="cite-text">{esc(cite)}</blockquote>
    <button class="btn" data-copy="cite-text" style="margin-top:10px">Copy citation</button>
    <p class="note">{'DOI: ' + esc(doi) if doi else 'No DOI registered yet. The field stays empty rather than carrying a placeholder.'}</p>

    {f'<h2 class="sec">Installation</h2><pre id="install-text">{esc(s.get("install"))}</pre>' if s.get('install') else ''}

    <h2 class="sec">Validation</h2>
    <p style="color:var(--muted);max-width:70ch">Structural validation proves conformance to the
    Agent Skills specification and the completeness of the package. It does not prove that the
    method is correct. Evidence for this skill's maturity level:
    {esc(s.get('evidence') or 'not recorded')}.</p>
  </div>

  <aside>
    <div class="panel">
      <h4>Factsheet</h4>
      <dl class="facts">
        <dt>Identifier</dt><dd>{esc(s.get('id'))}</dd>
        <dt>Version</dt><dd>{esc(s.get('version') or '—')}</dd>
        <dt>Maturity</dt><dd>{esc(s.get('maturity') or '—')}</dd>
        <dt>Status</dt><dd>{esc(s.get('status'))}</dd>
        <dt>Licence</dt><dd>{esc(s.get('license') or 'pending')}</dd>
        <dt>DOI (version)</dt><dd>{esc(doi or '—')}</dd>
        <dt>DOI (concept)</dt><dd>{esc(s.get('doi_concept') or '—')}</dd>
        <dt>Added</dt><dd>{esc(s.get('added') or '—')}</dd>
      </dl>
    </div>
    <div class="panel">
      <h4>Links</h4>
      {link_html or '<p class="note">No public repository yet.</p>'}
    </div>
    <div class="panel">
      <h4>Keywords</h4>
      <p class="note">{esc(', '.join(s.get('keywords') or []) or '—')}</p>
    </div>
  </aside>
</div></main>
"""
    body += footer(hub)
    return body.replace("{root}", root)


def build(out: Path) -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    hub = reg.get("hub", {})
    (out / "assets").mkdir(parents=True, exist_ok=True)
    (out / "skills").mkdir(parents=True, exist_ok=True)
    (out / "api").mkdir(parents=True, exist_ok=True)

    (out / "assets" / "style.css").write_text(css(), encoding="utf-8")
    (out / "assets" / "app.js").write_text(js(), encoding="utf-8")
    (out / "index.html").write_text(render_index(reg), encoding="utf-8")

    for s in reg["skills"]:
        (out / "skills" / f"{s['slug']}.html").write_text(
            render_skill(s, hub, len(reg["skills"])), encoding="utf-8")

    public = {k: v for k, v in reg.items()}
    (out / "api" / "registry.json").write_text(
        json.dumps(public, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    files = sorted(p for p in out.rglob("*") if p.is_file())
    digest = hashlib.sha256(b"".join(p.read_bytes() for p in files)).hexdigest()[:16]
    return {"files": len(files), "hash": digest, "skills": len(reg["skills"])}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the ScholarSkills hub.")
    ap.add_argument("--out", type=Path, default=ROOT / "site")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the output on disk differs from a fresh build")
    args = ap.parse_args(argv)

    out: Path = args.out
    if args.check:
        tmp = out.parent / ".site-check"
        if tmp.exists():
            shutil.rmtree(tmp)
        info = build(tmp)
        same = all((tmp / p.relative_to(tmp)).read_bytes() == p.read_bytes()
                   for p in tmp.rglob("*") if p.is_file()) and \
            sorted(str(p.relative_to(tmp)) for p in tmp.rglob("*") if p.is_file()) == \
            sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())
        shutil.rmtree(tmp)
        print("site is up to date" if same else "site is STALE — run scripts/build_site.py")
        return 0 if same else 1

    info = build(out)
    print(f"built {info['files']} files for {info['skills']} skills into {out}")
    print(f"content hash: {info['hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
