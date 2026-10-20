#!/usr/bin/env python3
"""Regenerate the target tables in the goal READMEs and the goal table in the
root README from the front matter of every problem.md.

Usage:
  python tools/build_index.py           # rewrite the tables
  python tools/build_index.py --check   # exit 1 if a table is out of date
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdg_common import (  # noqa: E402
    GOALS, GOALS_DIR, PROGRESS, ROOT, code_key, goal_slug, issues_url,
    md_escape, replace_block, split_front_matter,
)

PROGRESS_ORDER = list(PROGRESS)


def load_problems() -> dict[int, list[tuple[Path, dict]]]:
    out: dict[int, list[tuple[Path, dict]]] = {n: [] for n in GOALS}
    for path in sorted(GOALS_DIR.glob("*/*/problem.md")):
        data, _ = split_front_matter(path.read_text(encoding="utf-8"))
        out[int(data["goal"])].append((path, data))
    for n in out:
        out[n].sort(key=lambda item: code_key(str(item[1]["target"])))
    return out


def progress_cell(progress: str) -> str:
    emoji, label = PROGRESS.get(progress, ("", progress))
    short = label.split(",")[0]
    return f"{emoji} {short}".strip()


def tier_summary(indicators: list[dict]) -> str:
    tiers = Counter(str(i.get("tier", "")) for i in indicators)
    parts = [f"T{t}: {c}" for t, c in sorted(tiers.items()) if t]
    return f"{len(indicators)} ({', '.join(parts)})" if parts else str(
        len(indicators))


def goal_table(goal: int, problems: list[tuple[Path, dict]]) -> str:
    rows = [
        "| Target | Problem | UN progress 2026 | Priority | Status "
        "| Indicators |",
        "|---|---|---|---|---|---|",
    ]
    for path, d in problems:
        rel = f"{path.parent.name}/problem.md"
        rows.append(
            f"| [{d['target']}]({rel}) | {md_escape(str(d['title']))} "
            f"| {progress_cell(d.get('un_progress_2026', ''))} "
            f"| {d.get('priority', '')} | `{d.get('status', '')}` "
            f"| {tier_summary(d.get('indicators') or [])} |"
        )
    status = Counter(d.get("status") for _, d in problems)
    active = sum(c for s, c in status.items() if s != "suggested")
    rows += [
        "",
        f"{len(problems)} targets · {active} being worked on · "
        f"[open tasks]({issues_url(goal)}) · "
        "T1/T2 = indicator tier (see any problem.md)",
    ]
    return "\n".join(rows)


def progress_summary(problems: list[tuple[Path, dict]]) -> str:
    counts = Counter(d.get("un_progress_2026") for _, d in problems)
    return " ".join(f"{PROGRESS[p][0]}{counts[p]}"
                    for p in PROGRESS_ORDER if counts.get(p))


def root_table(all_problems: dict[int, list[tuple[Path, dict]]]) -> str:
    rows = [
        "| | Goal | Targets | Indicators | UN progress 2026 "
        "| High priority | Active |",
        "|---|---|---:|---:|---|---:|---:|",
    ]
    total_t = total_high = total_active = 0
    all_ind: set[str] = set()
    for n, problems in all_problems.items():
        meta = GOALS[n]
        ind = {i["code"] for _, d in problems
               for i in d.get("indicators") or []}
        all_ind |= ind
        high = sum(1 for _, d in problems if d.get("priority") == "high")
        active = sum(1 for _, d in problems if d.get("status") != "suggested")
        total_t += len(problems)
        total_high += high
        total_active += active
        badge = (f"![{n}](https://img.shields.io/badge/-{n:02d}-"
                 f"{meta['colour']}?style=flat-square)")
        rows.append(
            f"| {badge} | [{meta['short']}](goals/{goal_slug(n)}/README.md) "
            f"| {len(problems)} | {len(ind)} | {progress_summary(problems)} "
            f"| {high} | {active} |"
        )
    rows.append(f"| | **Total** | **{total_t}** | **{len(all_ind)}** | "
                f"| **{total_high}** | **{total_active}** |")
    legend = " · ".join(f"{e} {label.split(',')[0]}"
                        for e, label in PROGRESS.values())
    rows += [
        "",
        f"UN progress legend: {legend}.  ",
        "Indicators are counted once even when the UN lists them under "
        "more than one target. High priority = targets the UN rates as "
        "*stagnation* or *regression*. Active = status beyond `suggested`.",
    ]
    return "\n".join(rows)


def render() -> dict[Path, str]:
    problems = load_problems()
    out: dict[Path, str] = {}
    for n, items in problems.items():
        readme = GOALS_DIR / goal_slug(n) / "README.md"
        if not readme.exists():
            continue
        out[readme] = replace_block(readme.read_text(encoding="utf-8"),
                                    "targets", goal_table(n, items),
                                    kind="INDEX")
    root = ROOT / "README.md"
    out[root] = replace_block(root.read_text(encoding="utf-8"), "goals",
                              root_table(problems), kind="INDEX")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild README tables.")
    parser.add_argument("--check", action="store_true",
                        help="only check; exit 1 if anything is stale")
    args = parser.parse_args(argv)
    stale = []
    for path, text in render().items():
        if path.read_text(encoding="utf-8") != text:
            stale.append(path)
            if not args.check:
                path.write_text(text, encoding="utf-8")
    rel = [str(p.relative_to(ROOT)) for p in stale]
    if args.check:
        if stale:
            print("Out of date (run python tools/build_index.py):")
            print("\n".join(f"  {p}" for p in rel))
            return 1
        print("All index tables are up to date.")
        return 0
    print(f"Updated {len(stale)} index file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
