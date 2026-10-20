#!/usr/bin/env python3
"""Create or refresh the goal and target folders from UN data.

Safe to run again and again (idempotent):

* creates any missing goal folder, target folder, problem.md,
  research/README.md and solution/README.md;
* in existing files it only rewrites the UN-sourced parts: the UN fields in
  the front matter and the text between <!-- UN:START x --> and
  <!-- UN:END x --> markers. Everything people wrote is kept.

Inputs (committed in data/):
  data/un-sdg-framework.json  goals, targets, indicators (UN SDG API)
  data/sdg-report-2026.json   short titles, progress status, key messages

Usage:
  python tools/import_un_sdgs.py              # regenerate from data/
  python tools/import_un_sdgs.py --fetch      # refresh data/ from the UN API
  python tools/import_un_sdgs.py --from-raw FILE   # trim a saved API dump
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_index  # noqa: E402
from sdg_common import (  # noqa: E402
    DATA_DIR, FRAMEWORK_FILE, GOALS, GOALS_DIR, PRIORITY_FROM_PROGRESS, PROGRESS,
    REPORT_FILE, REPORT_URL, block_re, code_key, dump_front_matter,
    goal_slug, issues_url, load_json, make_block, md_escape, new_issue_url,
    replace_block, split_front_matter, target_metadata_url, target_slug,
    write_if_changed,
)

API_URL = ("https://unstats.un.org/sdgapi/v1/sdg/Goal/List"
           "?includechildren=true")
PLAIN_FILE = DATA_DIR / "plain-language.yml"
SERIES_FILE = DATA_DIR / "un-series-world-latest.json"
DATA_PORTAL = "https://unstats.un.org/sdgs/dataportal/database"
UN_FIELDS = ["goal", "goal_title", "target", "un_target_text", "indicators",
             "un_progress_2026", "source_url"]


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
def trim_api(raw: list, retrieved: str) -> dict:
    goals = []
    for g in raw:
        targets = []
        for t in g["targets"]:
            targets.append({
                "code": t["code"],
                "title": t["title"].strip(),
                "uri": t.get("uri"),
                "indicators": [
                    {"code": i["code"],
                     "description": i["description"].strip(),
                     "tier": str(i.get("tier") or "").strip(),
                     "uri": i.get("uri")}
                    for i in t["indicators"]
                ],
            })
        goals.append({"code": g["code"], "title": g["title"].strip(),
                      "description": g["description"].strip(),
                      "uri": g.get("uri"), "targets": targets})
    return {
        "source": API_URL,
        "publisher": "United Nations Statistics Division, "
                     "SDG Global Database",
        "retrieved": retrieved,
        "note": "Trimmed copy: goals, targets and indicators only "
                "(data series removed). Tier = IAEG-SDGs tier "
                "classification as returned by the API.",
        "goals": goals,
    }


def fetch(raw_path: str | None) -> None:
    if raw_path:
        raw = json.loads(Path(raw_path).read_text(encoding="utf-8"))
        retrieved = dt.date.fromtimestamp(
            Path(raw_path).stat().st_mtime).isoformat()
    else:
        with urllib.request.urlopen(API_URL, timeout=120) as resp:
            raw = json.load(resp)
        retrieved = dt.date.today().isoformat()
    data = trim_api(raw, retrieved)
    FRAMEWORK_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"wrote {FRAMEWORK_FILE.relative_to(GOALS_DIR.parent)}")


# --------------------------------------------------------------------------
# Optional inputs: plain-language summaries and World numbers
# --------------------------------------------------------------------------
def load_plain(path: Path = PLAIN_FILE) -> dict[str, dict[str, str]]:
    """Parse data/plain-language.yml (a tiny YAML subset, no PyYAML)."""
    out: dict[str, dict[str, str]] = {}
    if not path.exists():
        return out
    current = None
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.match(r'^"([0-9]+\.[0-9a-z]+)":\s*$', line)
        sub = re.match(r'^  ([a-z_]+): (".*")\s*$', line)
        if top:
            current = top.group(1)
            out[current] = {}
        elif sub and current:
            out[current][sub.group(1)] = json.loads(sub.group(2))
        else:
            raise ValueError(f"{path.name} line {n}: cannot parse {line!r}")
    return out


def load_series(path: Path = SERIES_FILE) -> dict | None:
    return load_json(path) if path.exists() else None


def plain_block(code: str, entry: dict[str, str] | None) -> str:
    edit = (f"[Edit](../../../data/plain-language.yml) · "
            "community-written, not official UN text. Check it against "
            "the [UN target](#the-problem-un-target) below.")
    if not entry or not entry.get("summary"):
        return ("> **In plain language:** _not written yet._ " + edit)
    lines = [f"> **In plain language:** {entry['summary']}"]
    if entry.get("who"):
        lines += [">", f"> **Who it is about:** {entry['who']}"]
    lines += [">", f"> <sub>{edit}</sub>"]
    return "\n".join(lines)


def fmt_value(raw) -> str:
    text = str(raw).strip()
    try:
        num = float(text)
    except ValueError:
        return md_escape(text)
    if num.is_integer() and abs(num) >= 1000:
        return f"{int(num):,}"
    if num.is_integer():
        return str(int(num))
    return f"{num:,.2f}".rstrip("0").rstrip(".") if abs(num) < 1e15 else text


def data_block(target: dict, snapshot: dict) -> str:
    rows = ["| Indicator | Data series (UN code) | Latest World value | "
            "Earlier World value | Unit |", "|---|---|---|---|---|"]
    with_world = 0
    for ind in target["indicators"]:
        info = snapshot["indicators"].get(ind["code"])
        link = f"[{ind['code']}]({DATA_PORTAL}?indicator={ind['code']})"
        if not info or not info["series"]:
            rows.append(f"| {link} | _No data series in the UN database "
                        "yet_ | – | – | – |")
            continue
        for s in info["series"]:
            desc = md_escape(s["description"])
            w = s.get("world")
            if w:
                with_world += 1
                extra = (f" ({md_escape('; '.join(w['breakdown']))})"
                         if w.get("breakdown") else "")
                latest = f"**{fmt_value(w['latest']['value'])}** ({w['latest']['year']})"
                if w["earliest"]["year"] != w["latest"]["year"]:
                    early = (f"{fmt_value(w['earliest']['value'])} "
                             f"({w['earliest']['year']})")
                else:
                    early = "–"
                rows.append(f"| {link} | {desc}{extra} `{s['code']}` | "
                            f"{latest} | {early} | {md_escape(w['unit'])} |")
            else:
                n_c = s.get("countries_with_data", 0)
                rows.append(f"| {link} | {desc} `{s['code']}` | _No World "
                            f"total_ ({n_c} countries or areas report "
                            "data) | – | – |")
    note = ("World figures (UN area code 1) copied from the "
            f"[UN SDG Global Database]({DATA_PORTAL}), release "
            f"{snapshot['database_release']}, retrieved "
            f"{snapshot['retrieved']} by `tools/fetch_un_data.py`. Up to "
            "three series per indicator. Earlier value = first year with "
            "World data. Click an indicator for country data.")
    if not with_world:
        note = ("The UN publishes no World total for these series yet. "
                + note)
    return "\n".join(["### Latest global numbers", "", *rows, "", note])


def ensure_block(body: str, name: str, content: str, after: str) -> str:
    """Replace block `name`, or insert it right after block `after`."""
    if block_re(name).search(body):
        return replace_block(body, name, content)
    m = block_re(after).search(body)
    if not m:
        raise KeyError(f"block UN:{after} not found")
    return (body[:m.end()] + "\n\n" + make_block(name, content)
            + body[m.end():])


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def tier_text(tier: str) -> str:
    parts = [p for p in tier.replace(" ", "").split("/") if p]
    return " / ".join(f"Tier {p}" for p in parts) if parts else "Not set"


def progress_text(progress: str) -> str:
    emoji, label = PROGRESS[progress]
    return f"{emoji} {label}"


def bold_first_sentence(text: str) -> str:
    head, sep, tail = text.partition(". ")
    if not sep:
        return text
    return f"**{head}.** {tail}"


def goal_blocks(goal: dict, report: dict) -> dict[str, str]:
    n = int(goal["code"])
    meta = GOALS[n]
    n_ind = len({i["code"] for t in goal["targets"]
                 for i in t["indicators"]})
    label = (meta["short"].replace("-", "--").replace(" ", "_")
             .replace(",", "%2C"))
    badge = (f"https://img.shields.io/badge/Goal_{n}-{label}-"
             f"{meta['colour']}?style=for-the-badge")
    header = "\n".join([
        f"# Goal {n} · {meta['short']}",
        "",
        f"![Goal {n}: {meta['short']}]({badge})",
        "",
        f"> **{goal['title']}**",
        ">",
        f"> {goal['description']}",
        "",
        f"{len(goal['targets'])} targets · {n_ind} indicators · "
        "Text from the [UN SDG Global Database](https://unstats.un.org/sdgs/)",
    ])
    rep = report["goals"][str(n)]
    why = [f"Key messages from *The Sustainable Development Goals Report "
           f"2026*, p.{rep['page']} ([PDF]({REPORT_URL})), quoted:", ""]
    why += [f"- {bold_first_sentence(m)}" for m in rep["key_messages"]]
    return {"header": header, "why": "\n".join(why)}


def goal_readme(goal: dict, report: dict) -> str:
    n = int(goal["code"])
    b = goal_blocks(goal, report)
    return "\n".join([
        make_block("header", b["header"]),
        "",
        "## In plain language",
        "",
        "> **Help wanted:** explain this goal in three or four sentences a "
        "14-year-old would understand. What is going wrong, who is "
        "affected, and where could software, data or design help?",
        "",
        "## Why it matters",
        "",
        make_block("why", b["why"]),
        "",
        "## Targets",
        "",
        "Each target is one problem folder. UN progress is the UN's own "
        "2026 assessment; priority and status are ours "
        "(see [problem lifecycle](../../how-we-work/problem-lifecycle.md)).",
        "",
        make_block("targets", "_Run `python tools/build_index.py`._",
                   kind="INDEX"),
        "",
        "## How to help",
        "",
        "1. Pick a target above and read its `problem.md`.",
        f"2. Look at the [open tasks for Goal {n}]({issues_url(n)}) or "
        f"[suggest a problem]({new_issue_url('01-suggest-a-problem.yml')}).",
        "3. Read [CONTRIBUTING](../../CONTRIBUTING.md) and say hi on the "
        "issue before you start.",
        "",
    ])


def problem_blocks(goal: dict, target: dict, rep_t: dict) -> dict[str, str]:
    n = int(goal["code"])
    code = target["code"]
    rows = ["| Indicator | What it measures | Tier |", "|---|---|---|"]
    for ind in target["indicators"]:
        desc = ind["description"].replace("|", "\\|").replace("\n", " ")
        rows.append(f"| {ind['code']} | {desc} | {tier_text(ind['tier'])} |")
    indicators = "\n".join(rows + [
        "",
        "**Tier 1** = the method is agreed and countries regularly produce "
        "data. **Tier 2** = the method is agreed, but data are patchy. "
        "Tiers are set by the UN expert group (IAEG-SDGs). Full metadata: "
        f"[UN SDG indicator metadata]({target_metadata_url(n, code)}).",
    ])
    header = "\n".join([
        f"# {code} · {rep_t['short_title']}",
        "",
        f"**Goal {n}: {GOALS[n]['short']}** · "
        f"UN progress 2026: {progress_text(rep_t['progress'])} · "
        "[All targets in this goal](../README.md)",
    ])
    status = (
        f"**UN progress assessment:** {progress_text(rep_t['progress'])}  \n"
        "Source: \"SDG progress by target\", *The Sustainable Development "
        f"Goals Report 2026*, pp.44-45 ([PDF]({REPORT_URL})). For "
        "goal-level facts see [Why it matters](../README.md#why-it-matters)."
    )
    tasks = "\n".join([
        f"- [Open tasks for {code}]({issues_url(n, code)})",
        f"- [Add a task]({new_issue_url('02-add-a-task.yml', f'[{code} ')})",
        "- Notes and sources go in [research/](research/); "
        "code goes in [solution/](solution/).",
    ])
    return {
        "header": header,
        "target": f"> **Target {code}:** {target['title']}",
        "indicators": indicators,
        "status": status,
        "tasks": tasks,
    }


HELP = {
    "status": "> **Help wanted:** add the latest numbers for this target "
              "(with source and page number), and who is most affected.",
    "exists": "> **Help wanted:** list tools, programmes, datasets and "
              "research that already tackle this. Link each one and say "
              "what it does not cover.",
    "solved": "> **Help wanted:** describe the change we want to see, in "
              "terms of the indicators above. What would a user, a "
              "community or an agency be able to do that they cannot "
              "do today?",
    "data": "> **Help wanted:** list open datasets and APIs we could use "
            "(name, link, licence, coverage, update frequency).",
    "questions": "> **Help wanted:** what do we still not know? Who should "
                 "we ask?",
}


def problem_body(blocks: dict[str, str]) -> str:
    return "\n".join([
        make_block("header", blocks["header"]),
        "",
        "## The problem (UN target)",
        "",
        make_block("target", blocks["target"]),
        "",
        "## How progress is measured (UN indicators)",
        "",
        make_block("indicators", blocks["indicators"]),
        "",
        "## Latest status",
        "",
        make_block("status", blocks["status"]),
        "",
        HELP["status"],
        "",
        "## What already exists",
        "",
        HELP["exists"],
        "",
        "## What \"solved\" looks like",
        "",
        HELP["solved"],
        "",
        "## Data we can use",
        "",
        HELP["data"],
        "",
        "## Open questions",
        "",
        HELP["questions"],
        "",
        "## Tasks",
        "",
        make_block("tasks", blocks["tasks"]),
        "",
    ])


RESEARCH_README = """# Research notes: {code} {title}

Put evidence about this problem here: summaries of papers and reports,
interview notes (anonymised), dataset reviews, maps of who is already
working on it.

- One file per topic, e.g. `existing-tools.md`, `datasets.md`.
- Always link the source and add the date you accessed it.
- No personal data. Read [privacy and safety](../../../../how-we-work/privacy-and-safety.md) first.
"""

SOLUTION_README = """# Solution: {code} {title}

**No solution yet - see [tasks](../problem.md#tasks).**

When a solution is scoped, copy
[`templates/solution-template/`](../../../../templates/solution-template/)
into this folder and fill in its README.
"""


def front_matter(goal: dict, target: dict, rep_t: dict) -> dict:
    n = int(goal["code"])
    return {
        "goal": n,
        "goal_title": GOALS[n]["short"],
        "target": target["code"],
        "title": rep_t["short_title"],
        "un_target_text": target["title"],
        "indicators": [
            {"code": i["code"], "description": i["description"],
             "tier": i["tier"]}
            for i in target["indicators"]
        ],
        "un_progress_2026": rep_t["progress"],
        "status": "suggested",
        "priority": PRIORITY_FROM_PROGRESS[rep_t["progress"]],
        "owner": "",
        "lead": "",
        "tags": [],
        "source_url": target_metadata_url(n, target["code"]),
    }


def update_problem(path: Path, goal: dict, target: dict, rep_t: dict,
                   extra: dict[str, tuple[str, str]] | None = None) -> str:
    """extra = {block name: (content, insert after block)}."""
    fresh = front_matter(goal, target, rep_t)
    blocks = problem_blocks(goal, target, rep_t)
    if not path.exists():
        body = problem_body(blocks)
    else:
        data, body = split_front_matter(path.read_text(encoding="utf-8"))
        for key in UN_FIELDS:
            data[key] = fresh[key]
        for key, value in fresh.items():
            data.setdefault(key, value)
        fresh = data
        for name, content in blocks.items():
            if block_re(name).search(body):
                body = replace_block(body, name, content)
    for name, (content, after) in (extra or {}).items():
        body = ensure_block(body, name, content, after)
    if not path.exists():
        write_if_changed(path, dump_front_matter(fresh) + "\n" + body)
        return "created"
    text = dump_front_matter(fresh) + body
    return "updated" if write_if_changed(path, text) else "unchanged"


def run() -> int:
    framework = load_json(FRAMEWORK_FILE)
    report = load_json(REPORT_FILE)
    plain = load_plain()
    snapshot = load_series()
    counts = {"created": 0, "updated": 0, "unchanged": 0}
    for goal in framework["goals"]:
        n = int(goal["code"])
        gdir = GOALS_DIR / goal_slug(n)
        readme = gdir / "README.md"
        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            for name, content in goal_blocks(goal, report).items():
                text = replace_block(text, name, content)
            write_if_changed(readme, text)
        else:
            write_if_changed(readme, goal_readme(goal, report))
        for target in sorted(goal["targets"],
                             key=lambda t: code_key(t["code"])):
            rep_t = report["targets"][target["code"]]
            target = dict(target, indicators=sorted(
                target["indicators"], key=lambda i: code_key(i["code"])))
            tdir = gdir / target_slug(target["code"], rep_t["short_title"])
            extra = {"plain": (plain_block(target["code"],
                                           plain.get(target["code"])),
                               "header")}
            if snapshot:
                extra["data"] = (data_block(target, snapshot), "status")
            counts[update_problem(tdir / "problem.md", goal, target,
                                  rep_t, extra)] += 1
            fmt = {"code": target["code"], "title": rep_t["short_title"]}
            for sub, tpl in (("research", RESEARCH_README),
                             ("solution", SOLUTION_README)):
                path = tdir / sub / "README.md"
                if not path.exists():
                    write_if_changed(path, tpl.format(**fmt))
    print("problem.md files: " + ", ".join(
        f"{v} {k}" for k, v in counts.items()))
    return build_index.main([])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--fetch", action="store_true",
                        help="download a fresh copy from the UN SDG API")
    parser.add_argument("--from-raw", metavar="FILE",
                        help="build data/ from a saved raw API response")
    args = parser.parse_args(argv)
    if args.fetch or args.from_raw:
        fetch(args.from_raw)
    return run()


if __name__ == "__main__":
    sys.exit(main())
