#!/usr/bin/env python3
"""Write site/data/problems.json for the GitHub Pages catalogue.

Reads the front matter of every goals/*/*/problem.md plus
data/plain-language.yml and (if present) data/un-series-world-latest.json.
No network. The Pages workflow runs this before publishing site/.

Usage:
  python tools/build_site.py            # writes site/data/problems.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_index import load_problems  # noqa: E402
from import_un_sdgs import load_plain, load_series  # noqa: E402
from sdg_common import (  # noqa: E402
    GOALS, PROGRESS, REPO_URL, ROOT, goal_slug, issues_url,
)

OUT = ROOT / "site" / "data" / "problems.json"


def main() -> int:
    plain = load_plain()
    snapshot = load_series() or {"indicators": {}}
    problems = []
    for n, items in load_problems().items():
        for path, d in items:
            code = str(d["target"])
            rel = path.relative_to(ROOT).as_posix()
            world = sum(
                1 for i in d.get("indicators") or []
                for s in (snapshot["indicators"].get(i["code"]) or {})
                .get("series", []) if s.get("world"))
            problems.append({
                "goal": n,
                "target": code,
                "title": d["title"],
                "un_target_text": d["un_target_text"],
                "plain": (plain.get(code) or {}).get("summary", ""),
                "progress": d.get("un_progress_2026", ""),
                "priority": d.get("priority", ""),
                "status": d.get("status", ""),
                "tags": d.get("tags") or [],
                "indicators": [i["code"] for i in d.get("indicators") or []],
                "world_series": world,
                "url": f"{REPO_URL}/blob/main/{rel}",
                "tasks_url": issues_url(n, code),
            })
    data = {
        "repo": REPO_URL,
        "goals": {
            str(n): {"short": g["short"], "colour": g["colour"],
                     "url": f"{REPO_URL}/blob/main/goals/{goal_slug(n)}/"
                            "README.md",
                     "tasks_url": issues_url(n)}
            for n, g in GOALS.items()
        },
        "progress": {k: {"emoji": e, "label": label}
                     for k, (e, label) in PROGRESS.items()},
        "un_numbers_retrieved": snapshot.get("retrieved", ""),
        "problems": problems,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(problems)} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
