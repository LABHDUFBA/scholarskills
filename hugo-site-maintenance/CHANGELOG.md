# Changelog

## [1.0.0] — 2026-11-24

### Added
- `scripts/hugo_audit.py`: front matter parsing (YAML with a minimal fallback), error/warning split,
  alt-text checks for Markdown and HTML images, duplicate-title detection, and broken-internal-link
  detection over `public/` (Markdown links and `href` attributes, site-root and relative paths).
- Offline suite of 19 tests over a temporary site with known defects.
- Bilingual documentation with the four required sections and a deploy checklist.

### Known limitations
- Does not run `hugo`; the build must be verified by the operator.
- Does not validate shortcode arguments or theme internals.
