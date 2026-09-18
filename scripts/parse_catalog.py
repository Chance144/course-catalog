#!/usr/bin/env python3
"""Parse the WSU Carson College catalog Word export into courses.json.

Preserves course wording. Only normalizes whitespace and strips known
export artifacts (non-breaking spaces and a mojibake Â from a few lines).
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

COURSE_RE = re.compile(
    r"^(?P<number>\d{3,4})\s+"
    r"(?:\(Effective through\s+(?P<effective>[^)]+)\)\s+)?"
    r"(?:\[M\]\s+)?"
    r"(?P<title>.+?)\s+"
    r"(?P<credits>V\s+\d+\s*-\s*\d+|\d+)\s+"
    r"(?P<body>.*)$",
    re.DOTALL,
)

REPEAT_RE = re.compile(
    r"^May be repeated for credit(?:; cumulative maximum\s+\d+\s+credits?)?\.\s*"
)
PREREQ_RE = re.compile(r"^Course Prerequisite:\s*")
RECOMMENDED_RE = re.compile(
    r"\s*Recommended preparation:\s*(?P<text>.+?)\.\s*$"
)
TYPICALLY_RE = re.compile(
    r"\s*Typically offered\s+(?P<text>.+?)\.\s*$"
)
GRADING_RE = re.compile(r"\s*(?P<text>S,\s*[FU]\s+grading)\.\s*$")
CROSSLIST_RE = re.compile(
    r"\s*\(Crosslisted course offered as\s+(?P<text>[^)]+?)\)\.?\s*$"
)


def paragraph_text(paragraph: ET.Element) -> str:
    parts: list[str] = []
    for node in paragraph.iter():
        tag = node.tag.split("}")[-1]
        if tag == "t" and node.text:
            parts.append(node.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag == "br":
            parts.append("\n")
    return "".join(parts)


def clean_text(value: str) -> str:
    # Word uses NBSP between catalog fields. A couple of lines also contain
    # a stray U+00C2 (Â) left from a mangled non-breaking space.
    value = value.replace("\u00c2", "")
    value = value.replace("\xa0", " ").replace("\u202f", " ")
    value = value.replace("\r", " ").replace("\n", " ")
    value = re.sub(r"[ \t]+", " ", value)
    return value.strip()


def extract_docx_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs: list[str] = []
    for paragraph in root.iter(f"{W_NS}p"):
        text = clean_text(paragraph_text(paragraph))
        if text:
            paragraphs.append(text)
    return paragraphs


def peel_trailing(pattern: re.Pattern[str], text: str) -> tuple[str | None, str]:
    match = pattern.search(text)
    if not match:
        return None, text
    captured = match.groupdict().get("text") or match.group(0).strip()
    return captured.strip(), text[: match.start()].rstrip()


def split_body(body: str) -> dict[str, str | None]:
    repeatable = None
    match = REPEAT_RE.match(body)
    if match:
        repeatable = match.group(0).strip()
        body = body[match.end() :]

    prerequisite = None
    prereq_match = PREREQ_RE.match(body)
    if prereq_match:
        after = body[prereq_match.end() :]
        # WSU prints the prerequisite as a single sentence.
        split_at = after.find(". ")
        if split_at == -1:
            prerequisite = after.rstrip(".")
            body = ""
        else:
            prerequisite = after[:split_at].strip()
            body = after[split_at + 2 :].strip()

    grading, body = peel_trailing(GRADING_RE, body)
    typically, body = peel_trailing(TYPICALLY_RE, body)
    recommended, body = peel_trailing(RECOMMENDED_RE, body)
    crosslisted, body = peel_trailing(CROSSLIST_RE, body)
    if crosslisted:
        crosslisted = crosslisted.rstrip(".")

    return {
        "repeatable": repeatable,
        "prerequisite": prerequisite,
        "description": body.strip() or None,
        "recommended": recommended,
        "typicallyOffered": typically,
        "grading": grading,
        "crosslisted": crosslisted,
    }


def level_for(number: int) -> str:
    return "undergraduate" if number < 500 else "graduate"


def slug(dept: str, number: str, effective: str | None) -> str:
    prefix = dept.lower().replace("_", "")
    ident = f"{prefix}-{number}"
    if effective:
        ident += "-" + re.sub(r"[^a-z0-9]+", "-", effective.lower()).strip("-")
    return ident


def parse_courses(paragraphs: list[str]) -> dict:
    policy = (
        "No letter-graded course offered by the Carson College of Business "
        "may be taken for a Pass, Fail (P, F) grade."
    )
    terms = ["Spring 2026", "Summer 2026", "Fall 2026"]
    departments = {
        "I_BUS": {
            "code": "I_BUS",
            "name": "International Business",
            "path": "/ibus/",
        },
        "MKTG": {
            "code": "MKTG",
            "name": "Marketing",
            "path": "/mktg/",
        },
    }

    current_dept = None
    courses: list[dict] = []

    for paragraph in paragraphs:
        if paragraph.startswith("International Business"):
            current_dept = "I_BUS"
            continue
        if paragraph.startswith("Marketing"):
            current_dept = "MKTG"
            continue
        if paragraph.startswith("Spring ") or paragraph == policy:
            continue
        if current_dept is None:
            raise SystemExit(f"Course text before a department heading: {paragraph!r}")

        writing = "[M]" in paragraph[:80]
        match = COURSE_RE.match(paragraph)
        if not match:
            raise SystemExit(f"Unparsed course paragraph: {paragraph!r}")

        number = match.group("number")
        title = match.group("title").strip()
        credits = re.sub(r"\s+", " ", match.group("credits").strip())
        effective = match.group("effective")
        if effective:
            effective = re.sub(r"\s+", " ", effective).strip()
        fields = split_body(match.group("body").strip())

        search_bits = [
            current_dept,
            current_dept.replace("_", " "),
            current_dept.replace("_", ""),
            paragraph,
            "[M]" if writing else "",
        ]

        course = {
            "id": slug(current_dept, number, effective),
            "dept": current_dept,
            "deptName": departments[current_dept]["name"],
            "number": int(number),
            "numberDisplay": number,
            "title": title,
            "credits": credits,
            "writingM": writing,
            "level": level_for(int(number)),
            "effectiveThrough": effective,
            "searchText": re.sub(r"\s+", " ", " ".join(search_bits)).strip().lower(),
            **fields,
            "source": paragraph,
        }
        courses.append(course)

    return {
        "meta": {
            "college": "Carson College of Business",
            "university": "Washington State University",
            "advisor": "Andrew Perkins",
            "terms": terms,
            "policy": policy,
            "source": "WSU catalog export for International Business (I_BUS) and Marketing (MKTG), Spring/Summer/Fall 2026.",
        },
        "departments": list(departments.values()),
        "courses": courses,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    docx_path = root / "source" / "catalog-2026.docx"
    if not docx_path.exists():
        raise SystemExit(f"Missing catalog source: {docx_path}")
    catalog = parse_courses(extract_docx_paragraphs(docx_path))
    out_path = root / "site" / "assets" / "courses.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts: dict[str, int] = {}
    for course in catalog["courses"]:
        counts[course["dept"]] = counts.get(course["dept"], 0) + 1
    print(f"Wrote {len(catalog['courses'])} courses to {out_path.relative_to(root)}")
    for dept, count in counts.items():
        print(f"  {dept}: {count}")


if __name__ == "__main__":
    main()
