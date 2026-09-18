#!/usr/bin/env python3
"""Write static HTML pages from a shared catalog template."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#f6f6f4">
  <link rel="icon" href="{asset_prefix}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{asset_prefix}styles.css">
</head>
<body data-page="{page}"{dept_attr}>
  <a class="skip-link" href="#catalog">Skip to courses</a>
  <header class="site-header">
    <div class="header-inner">
      <div class="brand">
        <p class="brand-kicker">Andrew Perkins · Carson College of Business</p>
        <a class="brand-title" href="{home_href}">Course catalog</a>
        <p class="brand-terms">Spring · Summer · Fall 2026</p>
      </div>
      <nav class="primary-nav" aria-label="Departments">
        <a href="{home_href}" {home_current}>All courses</a>
        <a href="{ibus_href}" {ibus_current}>I_BUS</a>
        <a href="{mktg_href}" {mktg_current}>MKTG</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="intro">
      <div class="intro-inner">
        <h1>{heading}</h1>
        <p class="lede">{lede}</p>
        {hero_extra}
      </div>
    </section>

    <section class="toolbar" aria-label="Search and filters">
      <div class="toolbar-inner">
        <label class="search-field">
          <span class="visually-hidden">Search courses</span>
          <input id="search" type="search" name="q" placeholder="Search number, title, description, or prerequisite" autocomplete="off" spellcheck="false">
        </label>
        <div class="filters">
          <fieldset class="filter-group" data-filter="dept" {dept_hidden}>
            <legend>Department</legend>
            <label class="chip"><input type="radio" name="dept" value="all" checked> All</label>
            <label class="chip"><input type="radio" name="dept" value="I_BUS"> I_BUS</label>
            <label class="chip"><input type="radio" name="dept" value="MKTG"> MKTG</label>
          </fieldset>
          <fieldset class="filter-group" data-filter="level">
            <legend>Level</legend>
            <label class="chip"><input type="radio" name="level" value="all" checked> All</label>
            <label class="chip"><input type="radio" name="level" value="undergraduate"> Undergrad</label>
            <label class="chip"><input type="radio" name="level" value="graduate"> Graduate</label>
          </fieldset>
          <fieldset class="filter-group" data-filter="writing">
            <legend>Writing</legend>
            <label class="chip"><input type="radio" name="writing" value="all" checked> All</label>
            <label class="chip"><input type="radio" name="writing" value="m"> [M] only</label>
          </fieldset>
        </div>
      </div>
    </section>

    <section id="catalog" class="catalog" aria-live="polite">
      <div class="catalog-inner">
        <div class="catalog-head">
          <h2 class="catalog-title">{catalog_title}</h2>
          <p id="result-count" class="result-count">Loading courses…</p>
        </div>
        <p class="policy">{policy}</p>
        <div id="course-list" class="course-list"></div>
        <div id="empty-state" class="empty-state" hidden>
          <p id="empty-copy">No courses match those filters.</p>
          <button type="button" id="clear-filters">Clear search and filters</button>
        </div>
        <noscript><p class="empty-state">This catalog search needs JavaScript. Enable it to browse I_BUS and MKTG courses.</p></noscript>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <p>Unofficial catalog mirror maintained for advising by Andrew Perkins. Course listings, prerequisites, writing [M] designations, credits, and descriptions are copied from the WSU catalog export for <strong>Spring, Summer, and Fall 2026</strong>. Verify every requirement against the official Washington State University catalog before registering.</p>
      <p class="footer-meta">Carson College of Business · International Business (I_BUS) and Marketing (MKTG) · Not an official WSU publication.</p>
    </div>
  </footer>
  <script src="{asset_prefix}app.js" defer></script>
</body>
</html>
"""

POLICY = (
    "No letter-graded course offered by the Carson College of Business "
    "may be taken for a Pass, Fail (P, F) grade."
)

HOME_PATHS = {
    "asset_prefix": "assets/",
    "home_href": "./",
    "ibus_href": "ibus/",
    "mktg_href": "mktg/",
}

DEPT_PATHS = {
    "asset_prefix": "../assets/",
    "home_href": "../",
    "ibus_href": "../ibus/",
    "mktg_href": "../mktg/",
}

PAGES = [
    {
        "out": SITE / "index.html",
        "page": "home",
        "dept": "",
        "title": "WSU Carson College Course Catalog · I_BUS & MKTG",
        "description": "Searchable unofficial mirror of Washington State University Carson College International Business and Marketing courses for Spring, Summer, and Fall 2026.",
        "heading": "I_BUS and MKTG",
        "lede": "Unofficial advising copy of the Carson College catalog for Spring, Summer, and Fall 2026.",
        "hero_extra": "",
        "catalog_title": "All courses",
        "home_current": 'aria-current="page"',
        "ibus_current": "",
        "mktg_current": "",
        "dept_hidden": "",
        **HOME_PATHS,
    },
    {
        "out": SITE / "ibus" / "index.html",
        "page": "ibus",
        "dept": "I_BUS",
        "title": "International Business (I_BUS) · WSU Course Catalog",
        "description": "International Business (I_BUS) courses at Washington State University Carson College of Business for Spring, Summer, and Fall 2026.",
        "heading": "International Business",
        "lede": "I_BUS undergraduate and graduate listings, including writing [M] courses, internships, and MBA seminars.",
        "hero_extra": '<p class="prefix-note">Subject prefix I_BUS</p>',
        "catalog_title": "I_BUS courses",
        "home_current": "",
        "ibus_current": 'aria-current="page"',
        "mktg_current": "",
        "dept_hidden": "hidden",
        **DEPT_PATHS,
    },
    {
        "out": SITE / "mktg" / "index.html",
        "page": "mktg",
        "dept": "MKTG",
        "title": "Marketing (MKTG) · WSU Course Catalog",
        "description": "Marketing (MKTG) courses at Washington State University Carson College of Business for Spring, Summer, and Fall 2026.",
        "heading": "Marketing",
        "lede": "MKTG undergraduate and graduate listings, including professional sales, research, the [M] capstone, and doctoral seminars.",
        "hero_extra": '<p class="prefix-note">Subject prefix MKTG</p>',
        "catalog_title": "MKTG courses",
        "home_current": "",
        "ibus_current": "",
        "mktg_current": 'aria-current="page"',
        "dept_hidden": "hidden",
        **DEPT_PATHS,
    },
]


def render(page: dict) -> str:
    dept_attr = f' data-dept="{page["dept"]}"' if page["dept"] else ""
    return TEMPLATE.format(
        policy=POLICY,
        dept_attr=dept_attr,
        **page,
    )


NOT_FOUND = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found · Course Catalog</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <main class="intro">
    <div class="intro-inner">
      <p class="brand-kicker">Andrew Perkins · Carson College of Business</p>
      <h1>Page not found</h1>
      <p class="lede">That address is not part of this catalog mirror.</p>
      <p><a class="text-link" href="./">Return to the catalog</a></p>
    </div>
  </main>
</body>
</html>
"""


def main() -> None:
    for page in PAGES:
        page["out"].parent.mkdir(parents=True, exist_ok=True)
        page["out"].write_text(render(page), encoding="utf-8")
        print(f"Wrote {page['out'].relative_to(ROOT)}")
    (SITE / "404.html").write_text(NOT_FOUND, encoding="utf-8")
    print("Wrote site/404.html")


if __name__ == "__main__":
    main()
