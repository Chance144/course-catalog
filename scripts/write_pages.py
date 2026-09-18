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
  <meta name="theme-color" content="#981e32">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body data-page="{page}"{dept_attr}>
  <a class="skip-link" href="#catalog">Skip to courses</a>
  <header class="masthead">
    <div class="masthead-inner">
      <p class="eyebrow">Andrew Perkins · Washington State University</p>
      <div class="brand-row">
        <a class="wordmark" href="/">Course Catalog</a>
        <p class="brand-sub">Carson College of Business</p>
      </div>
      <nav class="primary-nav" aria-label="Departments">
        <a href="/" {home_current}>All courses</a>
        <a href="/ibus/" {ibus_current}>International Business</a>
        <a href="/mktg/" {mktg_current}>Marketing</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="hero-inner">
        <p class="terms">Spring 2026 · Summer 2026 · Fall 2026</p>
        <h1>{heading}</h1>
        <p class="lede">{lede}</p>
        {hero_extra}
      </div>
    </section>

    {dept_cards}

    <section class="toolbar" aria-label="Search and filters">
      <div class="toolbar-inner">
        <label class="search-field">
          <span class="search-label">Search courses</span>
          <input id="search" type="search" name="q" placeholder="Search by number, title, description, or prerequisite" autocomplete="off" spellcheck="false">
          <span class="search-hint">Press <kbd>/</kbd> to search</span>
        </label>
        <div class="filters">
          <fieldset class="filter-group" data-filter="dept" {dept_hidden}>
            <legend>Department</legend>
            <label><input type="radio" name="dept" value="all" checked> All</label>
            <label><input type="radio" name="dept" value="I_BUS"> I_BUS</label>
            <label><input type="radio" name="dept" value="MKTG"> MKTG</label>
          </fieldset>
          <fieldset class="filter-group" data-filter="level">
            <legend>Level</legend>
            <label><input type="radio" name="level" value="all" checked> All</label>
            <label><input type="radio" name="level" value="undergraduate"> Undergraduate</label>
            <label><input type="radio" name="level" value="graduate"> Graduate</label>
          </fieldset>
          <fieldset class="filter-group" data-filter="writing">
            <legend>Writing</legend>
            <label><input type="radio" name="writing" value="all" checked> All</label>
            <label><input type="radio" name="writing" value="m"> [M] Writing in the Major</label>
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
        <p id="empty-state" class="empty-state" hidden>No courses match those filters. Try a different search or clear a filter.</p>
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
  <script src="/assets/app.js" defer></script>
</body>
</html>
"""

POLICY = (
    "No letter-graded course offered by the Carson College of Business "
    "may be taken for a Pass, Fail (P, F) grade."
)

DEPT_CARDS = """
    <section class="dept-cards" aria-label="Departments">
      <div class="dept-cards-inner">
        <a class="dept-card" href="/ibus/">
          <p class="dept-code">I_BUS</p>
          <h2>International Business</h2>
          <p>Undergraduate and graduate I_BUS courses, including writing [M] options, internships, and MBA seminars.</p>
          <p class="dept-stat" data-dept-count="I_BUS">14 courses</p>
        </a>
        <a class="dept-card" href="/mktg/">
          <p class="dept-code">MKTG</p>
          <h2>Marketing</h2>
          <p>Undergraduate and graduate MKTG courses, including sales, research, the [M] capstone, and doctoral seminars.</p>
          <p class="dept-stat" data-dept-count="MKTG">31 courses</p>
        </a>
      </div>
    </section>
"""

PAGES = [
    {
        "out": SITE / "index.html",
        "page": "home",
        "dept": "",
        "title": "WSU Carson College Course Catalog · I_BUS & MKTG",
        "description": "Searchable unofficial mirror of Washington State University Carson College International Business and Marketing courses for Spring, Summer, and Fall 2026.",
        "heading": "International Business & Marketing",
        "lede": "A fast, searchable copy of the Carson College I_BUS and MKTG listings for advising. Undergraduate and graduate courses for Spring, Summer, and Fall 2026.",
        "hero_extra": "",
        "dept_cards": DEPT_CARDS,
        "catalog_title": "All courses",
        "home_current": 'aria-current="page"',
        "ibus_current": "",
        "mktg_current": "",
        "dept_hidden": "",
    },
    {
        "out": SITE / "ibus" / "index.html",
        "page": "ibus",
        "dept": "I_BUS",
        "title": "International Business (I_BUS) · WSU Course Catalog",
        "description": "International Business (I_BUS) courses at Washington State University Carson College of Business for Spring, Summer, and Fall 2026.",
        "heading": "International Business",
        "lede": "I_BUS undergraduate and graduate courses from the Carson College catalog, including global leadership, trade, management, marketing, and MBA seminars.",
        "hero_extra": '<p class="hero-code">Subject prefix I_BUS</p>',
        "dept_cards": "",
        "catalog_title": "I_BUS courses",
        "home_current": "",
        "ibus_current": 'aria-current="page"',
        "mktg_current": "",
        "dept_hidden": "hidden",
    },
    {
        "out": SITE / "mktg" / "index.html",
        "page": "mktg",
        "dept": "MKTG",
        "title": "Marketing (MKTG) · WSU Course Catalog",
        "description": "Marketing (MKTG) courses at Washington State University Carson College of Business for Spring, Summer, and Fall 2026.",
        "heading": "Marketing",
        "lede": "MKTG undergraduate and graduate courses from the Carson College catalog, including professional sales, research, digital marketing, the [M] capstone, and doctoral seminars.",
        "hero_extra": '<p class="hero-code">Subject prefix MKTG</p>',
        "dept_cards": "",
        "catalog_title": "MKTG courses",
        "home_current": "",
        "ibus_current": "",
        "mktg_current": 'aria-current="page"',
        "dept_hidden": "hidden",
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
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
  <main class="hero">
    <div class="hero-inner">
      <p class="eyebrow">Andrew Perkins · Carson College of Business</p>
      <h1>Page not found</h1>
      <p class="lede">That address is not part of this catalog mirror. Open the home page to search I_BUS and MKTG courses.</p>
      <p><a class="text-link" href="/">Return to the catalog</a></p>
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
