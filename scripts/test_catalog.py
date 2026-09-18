#!/usr/bin/env python3
"""Guardrails for the parsed 2026 I_BUS / MKTG catalog."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from parse_catalog import extract_docx_paragraphs, parse_courses  # noqa: E402

IBUS_NUMBERS = [280, 380, 415, 435, 453, 470, 480, 482, 496, 498, 499, 580, 582, 600]
MKTG_NUMBERS = [
    279, 360, 368, 379, 407, 450, 461, 467, 468, 470, 477, 478, 478, 479, 480,
    487, 495, 496, 498, 499, 506, 561, 565, 577, 590, 591, 592, 593, 600, 702, 800,
]
WRITING = {
    ("I_BUS", 415),
    ("I_BUS", 453),
    ("I_BUS", 482),
    ("MKTG", 461),
    ("MKTG", 495),
}


def main() -> None:
    docx = ROOT / "source" / "catalog-2026.docx"
    catalog = parse_courses(extract_docx_paragraphs(docx))
    json_catalog = json.loads((ROOT / "site" / "assets" / "courses.json").read_text(encoding="utf-8"))
    assert catalog == json_catalog, "courses.json is out of date; run scripts/parse_catalog.py"

    courses = catalog["courses"]
    assert len(courses) == 45, len(courses)

    ibus = [course for course in courses if course["dept"] == "I_BUS"]
    mktg = [course for course in courses if course["dept"] == "MKTG"]
    assert [course["number"] for course in ibus] == IBUS_NUMBERS
    assert [course["number"] for course in mktg] == MKTG_NUMBERS

    for course in courses:
        assert "Â" not in course["source"]
        assert course["title"]
        assert course["credits"]
        assert course["level"] == ("undergraduate" if course["number"] < 500 else "graduate")
        key = (course["dept"], course["number"])
        if course["effectiveThrough"]:
            assert course["id"] == "mktg-478-summer-2026"
            assert course["writingM"] is True
        elif key in WRITING:
            assert course["writingM"] is True, course["id"]
        else:
            assert course["writingM"] is False, course["id"]

    trade = next(course for course in courses if course["id"] == "ibus-470")
    assert trade["crosslisted"] == "ECONS 327, I BUS 470"
    assert "crosslisted" in trade["searchText"]
    capstone = next(course for course in courses if course["id"] == "mktg-495")
    assert capstone["recommended"] == "MKTG 368 and 407"
    assert "Integrative marketing capstone course" in capstone["description"]

    pages = [
        ROOT / "site" / "index.html",
        ROOT / "site" / "ibus" / "index.html",
        ROOT / "site" / "mktg" / "index.html",
    ]
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert "Unofficial catalog mirror" in html
        assert "Spring, Summer, and Fall 2026" in html
        assert "assets/app.js" in html
        assert 'href="/assets/' not in html
        assert 'src="/assets/' not in html
        assert 'href="/ibus/"' not in html
        assert 'href="/mktg/"' not in html

    home = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    ibus = (ROOT / "site" / "ibus" / "index.html").read_text(encoding="utf-8")
    assert 'href="assets/styles.css"' in home
    assert 'src="assets/app.js"' in home
    assert 'href="ibus/"' in home
    assert 'href="../assets/styles.css"' in ibus
    assert 'src="../assets/app.js"' in ibus
    assert 'href="../"' in ibus

    print("Catalog checks passed: 14 I_BUS + 31 MKTG listings.")


if __name__ == "__main__":
    main()
