#!/usr/bin/env python3
"""Extract facts from The Sustainable Development Goals Report 2026 (PDF).

Writes data/sdg-report-2026.json with:

* goal key messages (the bullet list on the first page of each goal chapter),
  quoted verbatim with the printed page number;
* the "SDG progress by target" chart (printed pages 44-45): each target's
  short title and its progress status.

The status is read from the chart symbols (filled or hollow circles in green,
yellow, red or grey) by sampling the rendered page, then mapped with the
chart legend. This is the only tool in the repo that needs a third-party
package (PyMuPDF), so it lives in tools/extras/. You only need to run it if
the report changes.

Usage:
    pip install pymupdf
    python tools/extras/extract_sdg_report_2026.py path/to/report.pdf
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

REPORT_URL = (
    "https://unstats.un.org/sdgs/report/2026/"
    "The-Sustainable-Development-Goals-Report-2026.pdf"
)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "sdg-report-2026.json"

# Printed page number of the first page of each goal chapter.
GOAL_FIRST_PAGE = {
    1: 8, 2: 10, 3: 12, 4: 16, 5: 18, 6: 20, 7: 22, 8: 24, 9: 26,
    10: 28, 11: 30, 12: 32, 13: 34, 14: 36, 15: 38, 16: 40, 17: 42,
}
PAGE_OFFSET = 2  # PDF page index (1-based) = printed page + 2
CHART_PAGES = (44, 45)  # printed page numbers

# Chart legend (printed p.45): colour + fill -> status
LEGEND = {
    ("green", "filled"): "on-track",
    ("yellow", "filled"): "moderate",
    ("yellow", "hollow"): "marginal",
    ("red", "hollow"): "stagnation",
    ("red", "filled"): "regression",
    ("grey", "filled"): "insufficient-data",
}
LEGEND_TEXT = {
    "on-track": "On track or target met",
    "moderate": "Moderate progress, but acceleration needed",
    "marginal": "Marginal progress, and significant acceleration needed",
    "stagnation": "Stagnation",
    "regression": "Regression",
    "insufficient-data": "Insufficient data",
}
CODE_RE = re.compile(r"^\d{1,2}\.(\d{1,2}|[a-d])$")


def colour_name(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    if r > 240 and g > 240 and b > 240:
        return "white"
    if g > 150 and r < 60:
        return "green"
    if r > 200 and g > 150 and b < 80:
        return "yellow"
    if r > 200 and g < 60:
        return "red"
    if abs(r - g) < 15 and abs(g - b) < 15 and 150 < r < 230:
        return "grey"
    raise ValueError(f"unknown chart colour {rgb}")


def chart_statuses(doc: fitz.Document) -> dict[str, str]:
    result: dict[str, str] = {}
    zoom = 6
    for printed in CHART_PAGES:
        page = doc[printed + PAGE_OFFSET - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        circles = [
            d["rect"] for d in page.get_drawings()
            if 4 < d["rect"].width < 12
            and abs(d["rect"].width - d["rect"].height) < 1
        ]
        for x0, y0, _x1, y1, word, *_ in page.get_text("words"):
            if not CODE_RE.match(word):
                continue
            cy = (y0 + y1) / 2
            near = [
                r for r in circles
                if 0 < r.x0 - x0 < 160 and abs((r.y0 + r.y1) / 2 - cy) < 5
            ]
            if not near:
                raise ValueError(f"no status symbol found for {word}")
            r = max(near, key=lambda r: r.width)
            mid_y = int((r.y0 + r.y1) / 2 * zoom)
            centre = pix.pixel(int((r.x0 + r.x1) / 2 * zoom), mid_y)
            edge = pix.pixel(int((r.x0 + 0.6) * zoom), mid_y)
            fill = "hollow" if colour_name(centre) == "white" else "filled"
            result[word] = LEGEND[(colour_name(edge), fill)]
    return result


def chart_titles(doc: fitz.Document) -> dict[str, str]:
    text = ""
    for printed in CHART_PAGES:
        text += " " + doc[printed + PAGE_OFFSET - 1].get_text()
    text = text.split("Legend")[0]
    flat = re.sub(r"\s+", " ", text)
    code = r"\d{1,2}\.(?:\d{1,2}|[a-d])"
    titles = {}
    for m in re.finditer(rf"(?<!\S)({code}) (.*?)(?= {code} |$)", flat):
        title = m.group(2)
        title = title.replace("SDG progress by target", "").strip()
        title = re.sub(r"(\s\d{1,2})+$", "", title)  # page numbers, goal labels
        titles[m.group(1)] = title
    return titles


def key_messages(doc: fitz.Document) -> dict[str, dict]:
    """Key messages are the text blocks starting with a bullet on the first
    page of each goal chapter."""
    goals = {}
    for goal, printed in GOAL_FIRST_PAGE.items():
        page = doc[printed + PAGE_OFFSET - 1]
        bullets = []
        for block in page.get_text("blocks"):
            text = block[4].strip()
            if not text.startswith("\u2022"):
                # a bullet can continue in the next block (column break)
                if bullets and not bullets[-1].endswith((".", ".\u201d")):
                    bullets[-1] += " " + re.sub(r"\s+", " ", text)
                continue
            text = text.lstrip("\u2022").strip()
            text = re.sub(r"-\s*\n", "-", text)
            text = re.sub(r"\s+", " ", text).strip()
            bullets.append(text)
        goals[str(goal)] = {"page": printed, "key_messages": bullets}
    return goals


def main() -> int:
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not pdf or not pdf.exists():
        print(__doc__)
        return 2
    doc = fitz.open(pdf)
    statuses = chart_statuses(doc)
    titles = chart_titles(doc)
    if set(statuses) != set(titles):
        raise SystemExit(f"mismatch: {set(statuses) ^ set(titles)}")
    data = {
        "source": REPORT_URL,
        "title": "The Sustainable Development Goals Report 2026",
        "publisher": "United Nations, Department of Economic and Social Affairs",
        "note": (
            "Page numbers are the printed page numbers. Key messages are "
            "quoted verbatim. Target statuses come from the 'SDG progress by "
            "target' chart (pp.44-45); see the report's Progress Chart 2026 "
            "technical note for the method."
        ),
        "progress_chart_pages": list(CHART_PAGES),
        "progress_legend": LEGEND_TEXT,
        "goals": key_messages(doc),
        "targets": {
            code: {"short_title": titles[code], "progress": statuses[code]}
            for code in sorted(
                titles, key=lambda c: [int(p) if p.isdigit() else ord(p)
                                       for p in c.split(".")]
            )
        },
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({len(data['targets'])} targets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
