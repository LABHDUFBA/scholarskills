---
name: hugo-site-maintenance
description: "Maintain a Hugo site on GitHub Pages: inspect before creating, verify published state against the clone, audit front matter and broken links, and read the deploy run when the site does not update. Use when a Hugo page must be edited, a menu item added, a deploy diagnosed, or a site audited before publishing."
license: MIT
compatibility: "Requires Hugo extended 0.110+ and git. No credential in the package: deploy runs from GitHub Actions with the repository token."
metadata:
  scholarskills.id: SS-0012
  scholarskills.version: "1.0.0"
  scholarskills.maturity: tested
  scholarskills.method: "Live-versus-clone verification, structural audit of front matter and links, and deploy-run diagnosis"
  scholarskills.spec-version: "agentskills.io specification, accessed 2026-11-24"
---

# Hugo Site Maintenance

Keep a Hugo site correct while it is being edited: check what exists before creating, check what is
published before believing the clone, and read the deploy log before touching the build.

## When to use

- Edit or add a page, menu entry, shortcode or layout.
- Diagnose "I pushed and the site did not change".
- Audit a site before publishing: front matter, alt text, broken internal links.
- Move a site between hosts (root, subpath, or a folder inside another site).

## When not to use

- Authoring the article itself. This skill maintains the site, not the prose.
- A non-Hugo generator. The audit half works on any rendered HTML; the rest is Hugo-specific.

## The three rules that prevent most damage

**1. Inspect before creating.** Before writing any new page, shortcode, layout or data file, grep the
content tree, list `layouts/` and `data/`, and open the page the person says already has the feature.
Duplicate infrastructure — a second news listing, a second shortcode for the same embed — is the
most common self-inflicted defect, and it is invisible until someone edits the wrong one.

**2. The clone is not the site.** The published site can be ahead of your working copy (a commit
pushed from another machine, a page published straight to the branch, a deploy that never ran).
Before editing, compare:

```bash
curl -sI https://<site>/<path>/ | grep -i last-modified
curl -s https://<site>/<path>/ | md5sum
git fetch origin && git log --oneline origin/main -5
gh api /repos/<owner>/<repo>/pages
```

A page whose `last-modified` is months older than the homepage is frozen on a stale deploy, not
missing. Deleting its source file does not remove it from the live site.

**3. Read the run, not the code.** When the deploy fails, the annotation names the cause — and it is
often not the build: a locked account, an exhausted quota, a workflow permission. `gh run view <id>`
before changing a single line of configuration.

## Setup

```bash
git clone <repo> && cd <repo>
git submodule update --init --recursive    # a theme kept as a submodule renders blank without this
```

Hugo must be **extended** if the theme uses SCSS or Hugo Pipes:

```bash
HUGO_VERSION="0.124.1"   # match the CI version, do not invent one
wget -q "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" -O /tmp/hugo.tar.gz
tar xzf /tmp/hugo.tar.gz -C /tmp hugo && mkdir -p ~/.local/bin && mv /tmp/hugo ~/.local/bin/
export PATH="$HOME/.local/bin:$PATH" && hugo version
```

## Audit before publishing

```bash
python3 scripts/hugo_audit.py content            # front matter, alt text, duplicates
python3 scripts/hugo_audit.py content --public   # adds broken internal links
hugo --gc --minify --baseURL "https://example.org/"   # the only proof the build works
```

The audit separates **errors** (missing title, image without alt, broken internal link) from
**warnings** (no front matter, empty body, `draft: true`, duplicate title, unparseable date). Mixing
them is how an audit becomes noise.

## Deploy checklist

1. `hugo --gc --minify` passes locally with the production `baseURL`.
2. `git status` shows no stray `public/` (it is built by CI, not committed).
3. The deploy workflow runs on the branch that Pages serves (`build_type: workflow` vs `branch`).
4. After the run: `curl -sI` the changed URL and confirm the new `last-modified`.
5. If nothing changed, `gh run view` — read the annotation before touching code.

## Limits and compliance

- No credential in the package. Deploys use the repository's own token in Actions.
- The audit is structural, not editorial: it cannot tell whether a sentence is true.
- A green build does not mean a correct site: a page can build and still link to a 404.

## Evidence

`tests/RESULTS.md` records the suite shipped here: 19 offline tests over a temporary site with known
defects.
