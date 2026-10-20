#!/usr/bin/env python3
"""Validate every goals/*/*/problem.md.

Checks the front matter (required fields, allowed values, codes that match
the folder names) and that the standard sections and UN markers are there.

Usage:
  python tools/check_problems.py            # check all problems
  python tools/check_problems.py FILE ...   # check some files
Exit code 1 if anything is wrong.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdg_common import (  # noqa: E402
    GOALS, GOALS_DIR, PRIORITIES, PROGRESS, ROOT, STATUSES,
    FrontMatterError, goal_slug, split_front_matter,
)

REQUIRED = {
    "goal": int, "goal_title": str, "target": str, "title": str,
    "un_target_text": str, "indicators": list, "status": str,
    "priority": str, "owner": str, "lead": str, "tags": list,
    "source_url": str,
}
SECTIONS = [
    "The problem (UN target)",
    "How progress is measured (UN indicators)",
    "Latest status",
    "What already exists",
    'What "solved" looks like',
    "Data we can use",
    "Open questions",
    "Tasks",
]
TARGET_RE = re.compile(r"^(\d{1,2})\.(\d{1,2}|[a-z])$")
TAG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def check(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data, body = split_front_matter(path.read_text(encoding="utf-8"))
    except (FrontMatterError, ValueError) as exc:
        return [str(exc)]

    for key, kind in REQUIRED.items():
        if key not in data:
            errors.append(f"missing field '{key}'")
        elif not isinstance(data[key], kind):
            errors.append(f"'{key}' should be a {kind.__name__}")
    if errors:
        return errors

    goal, target = data["goal"], data["target"]
    m = TARGET_RE.match(target)
    if goal not in GOALS:
        errors.append(f"goal {goal} is not 1-17")
    elif not m or int(m.group(1)) != goal:
        errors.append(f"target '{target}' does not belong to goal {goal}")
    else:
        if path.parent.parent.name != goal_slug(goal):
            errors.append(f"should live in goals/{goal_slug(goal)}/")
        if not path.parent.name.startswith(f"{target}-"):
            errors.append(f"folder name should start with '{target}-'")
        if data["goal_title"] != GOALS[goal]["short"]:
            errors.append(f"goal_title should be '{GOALS[goal]['short']}'")

    if not data["title"].strip():
        errors.append("title is empty")
    if not data["un_target_text"].strip():
        errors.append("un_target_text is empty")
    if data["status"] not in STATUSES:
        errors.append(f"status '{data['status']}' not in {STATUSES}")
    if data["status"] == "paused" and not str(
            data.get("paused_reason", "")).strip():
        errors.append("status 'paused' needs a 'paused_reason'")
    if data["priority"] not in PRIORITIES:
        errors.append(f"priority '{data['priority']}' not in {PRIORITIES}")
    progress = data.get("un_progress_2026")
    if progress is not None and progress not in PROGRESS:
        errors.append(f"un_progress_2026 '{progress}' is not a UN category")
    if not data["source_url"].startswith("https://"):
        errors.append("source_url must be an https:// link")

    if not data["indicators"]:
        errors.append("indicators list is empty")
    for ind in data["indicators"]:
        if not isinstance(ind, dict) or not {"code", "description",
                                             "tier"} <= set(ind):
            errors.append("each indicator needs code, description, tier")
            continue
        if not str(ind["code"]).startswith(f"{target}."):
            errors.append(f"indicator {ind['code']} is not under {target}")
        if not re.fullmatch(r"[12](/[12])?", str(ind["tier"])):
            errors.append(f"indicator {ind['code']}: tier '{ind['tier']}' "
                          "should be 1, 2 or 1/2")
    for tag in data["tags"]:
        if not isinstance(tag, str) or not TAG_RE.match(tag):
            errors.append(f"tag '{tag}' should be lowercase-with-hyphens")

    headings = re.findall(r"^## (.+?)\s*$", body, re.M)
    for section in SECTIONS:
        if section not in headings:
            errors.append(f"missing section '## {section}'")
    starts = re.findall(r"<!-- UN:START (\S+) -->", body)
    ends = re.findall(r"<!-- UN:END (\S+) -->", body)
    if starts != ends:
        errors.append("UN:START / UN:END markers do not match")
    return errors


def main(argv: list[str]) -> int:
    paths = [Path(p).resolve() for p in argv] or sorted(
        GOALS_DIR.glob("*/*/problem.md"))
    failed = 0
    bad_files = 0
    for path in paths:
        errors = check(path)
        if errors:
            failed += 1
            bad_files += 1
            print(f"✗ {path.relative_to(ROOT)}")
            for err in errors:
                print(f"    - {err}")
    folders = sorted(p.name for p in GOALS_DIR.iterdir() if p.is_dir())
    expected = sorted(goal_slug(n) for n in GOALS)
    if not argv and folders != expected:
        failed += 1
        print(f"✗ goal folders differ from the 17 expected: {folders}")
    print(f"Checked {len(paths)} problem file(s): "
          f"{len(paths) - bad_files} ok, {bad_files} with problems.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
