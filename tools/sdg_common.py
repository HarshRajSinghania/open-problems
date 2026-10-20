"""Shared helpers for the open-problems tools.

Pure standard library (Python 3.9+). Nothing here talks to the network.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, quote_plus

ROOT = Path(__file__).resolve().parents[1]
GOALS_DIR = ROOT / "goals"
DATA_DIR = ROOT / "data"
FRAMEWORK_FILE = DATA_DIR / "un-sdg-framework.json"
REPORT_FILE = DATA_DIR / "sdg-report-2026.json"

REPO = "harrythentrepreneur/open-problems"
REPO_URL = f"https://github.com/{REPO}"
REPORT_URL = (
    "https://unstats.un.org/sdgs/report/2026/"
    "The-Sustainable-Development-Goals-Report-2026.pdf"
)

# Official short titles and colours of the 17 SDGs.
# Label = short name used for the GitHub label "goal NN: <label>".
GOALS: dict[int, dict[str, str]] = {
    1: {"short": "No poverty", "colour": "E5243B", "label": "no poverty"},
    2: {"short": "Zero hunger", "colour": "DDA63A", "label": "zero hunger"},
    3: {"short": "Good health and well-being", "colour": "4C9F38",
        "label": "good health"},
    4: {"short": "Quality education", "colour": "C5192D",
        "label": "education"},
    5: {"short": "Gender equality", "colour": "FF3A21",
        "label": "gender equality"},
    6: {"short": "Clean water and sanitation", "colour": "26BDE2",
        "label": "clean water"},
    7: {"short": "Affordable and clean energy", "colour": "FCC30B",
        "label": "clean energy"},
    8: {"short": "Decent work and economic growth", "colour": "A21942",
        "label": "decent work"},
    9: {"short": "Industry, innovation and infrastructure",
        "colour": "FD6925", "label": "industry and innovation"},
    10: {"short": "Reduced inequalities", "colour": "DD1367",
         "label": "reduced inequalities"},
    11: {"short": "Sustainable cities and communities", "colour": "FD9D24",
         "label": "sustainable cities"},
    12: {"short": "Responsible consumption and production",
         "colour": "BF8B2E", "label": "responsible consumption"},
    13: {"short": "Climate action", "colour": "3F7E44",
         "label": "climate action"},
    14: {"short": "Life below water", "colour": "0A97D9",
         "label": "life below water"},
    15: {"short": "Life on land", "colour": "56C02B", "label": "life on land"},
    16: {"short": "Peace, justice and strong institutions",
         "colour": "00689D", "label": "peace and justice"},
    17: {"short": "Partnerships for the Goals", "colour": "19486A",
         "label": "partnerships"},
}

STATUSES = [
    "suggested", "researching", "ready-to-build", "being-built",
    "solved", "handed-over", "paused",
]
PRIORITIES = ["high", "medium", "low", "unassessed"]

# UN "SDG progress by target" chart legend (SDG Report 2026, p.45)
PROGRESS = {
    "on-track": ("\U0001F7E2", "On track or target met"),
    "moderate": ("\U0001F7E1", "Moderate progress, acceleration needed"),
    "marginal": ("\U0001F7E0",
                 "Marginal progress, significant acceleration needed"),
    "stagnation": ("\U0001F534", "Stagnation"),
    "regression": ("\U0001F53B", "Regression"),
    "insufficient-data": ("\u26AA", "Insufficient data"),
}
# How a starting priority is derived from the UN assessment.
PRIORITY_FROM_PROGRESS = {
    "regression": "high",
    "stagnation": "high",
    "marginal": "medium",
    "moderate": "low",
    "on-track": "low",
    "insufficient-data": "unassessed",
}

# Hand-picked slugs where the automatic 4-word slug reads badly.
SLUG_OVERRIDES = {
    "1.5": "disaster-resilience",
    "6.a": "international-cooperation",
    "8.a": "aid-for-trade",
    "9.3": "small-industry-finance",
    "10.1": "income-growth-bottom-40",
    "12.a": "sustainability-research-capacity",
    "14.6": "illegal-fishing",
    "15.c": "species-trafficking-global",
    "16.1": "reduce-violence",
    "16.3": "justice-for-all",
    "17.8": "internet-use",
    "17.15": "policy-space",
    "17.17": "multi-stakeholder-partnerships",
}
_STOP = {"and", "of", "the", "for", "on", "to", "in", "with", "by", "a", "an"}


def slugify(text: str, max_words: int = 4) -> str:
    text = text.replace("R&D", "research").replace("\u2019", "")
    text = re.sub(r"\(.*?\)", "", text).lower().replace("/", " ")
    words = [w for w in re.split(r"[^a-z0-9-]+", text) if w and w not in _STOP]
    return "-".join(words[:max_words])


def goal_slug(goal: int) -> str:
    """'06-clean-water-and-sanitation' (keeps every word of the UN title)."""
    words = re.split(r"[^a-z0-9-]+", GOALS[goal]["short"].lower())
    return f"{goal:02d}-" + "-".join(w for w in words if w)


def target_slug(code: str, short_title: str) -> str:
    return f"{code}-{SLUG_OVERRIDES.get(code) or slugify(short_title)}"


def goal_label(goal: int) -> str:
    return f"goal {goal:02d}: {GOALS[goal]['label']}"


def code_key(code: str) -> list[int]:
    """Sort key for '6.3', '6.a', '6.3.1', '17.10' ..."""
    return [int(p) if p.isdigit() else 100 + ord(p) for p in code.split(".")]


def issues_url(goal: int, target: str | None = None) -> str:
    q = f'is:issue is:open label:"{goal_label(goal)}"'
    if target:
        q += f' "{target}" in:title'
    return f"{REPO_URL}/issues?q={quote_plus(q)}"


def new_issue_url(template: str, title: str = "") -> str:
    url = f"{REPO_URL}/issues/new?template={template}"
    if title:
        url += f"&title={quote(title)}"
    return url


def target_metadata_url(goal: int, target: str) -> str:
    return (f"https://unstats.un.org/sdgs/metadata/"
            f"?Text=&Goal={goal}&Target={target}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Front matter: a small YAML subset, written with JSON-style quoted strings
# (valid YAML), so we need no third-party parser.
# --------------------------------------------------------------------------
FM_ORDER = [
    "goal", "goal_title", "target", "title", "un_target_text", "indicators",
    "un_progress_2026", "status", "paused_reason", "priority", "owner",
    "lead", "tags", "source_url",
]


def _scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def dump_front_matter(data: dict[str, Any]) -> str:
    keys = [k for k in FM_ORDER if k in data]
    keys += [k for k in data if k not in FM_ORDER]
    out = ["---"]
    for key in keys:
        value = data[key]
        if isinstance(value, list):
            if not value:
                out.append(f"{key}: []")
                continue
            out.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    first = True
                    for k, v in item.items():
                        prefix = "  - " if first else "    "
                        out.append(f"{prefix}{k}: {_scalar(v)}")
                        first = False
                else:
                    out.append(f"  - {_scalar(item)}")
        else:
            out.append(f"{key}: {_scalar(value)}")
    out.append("---")
    return "\n".join(out) + "\n"


def _parse_value(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return ""
    if raw.startswith(("'",)) and raw.endswith("'") and len(raw) >= 2:
        return raw[1:-1].replace("''", "'")
    if raw.startswith('"'):
        return json.loads(raw)
    if raw.startswith("["):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            inner = raw.strip("[]").strip()
            return [_parse_value(x) for x in inner.split(",")] if inner else []
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if raw in ("true", "false"):
        return raw == "true"
    if raw in ("null", "~"):
        return None
    return raw


class FrontMatterError(ValueError):
    pass


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Return (front_matter, body). Raises FrontMatterError."""
    if not text.startswith("---\n"):
        raise FrontMatterError("file must start with '---' front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise FrontMatterError("front matter is not closed with '---'")
    block = text[4:end]
    body = text[end + 5:]
    data: dict[str, Any] = {}
    key = None
    for n, line in enumerate(block.split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z_][\w-]*):(.*)$", line)
        if top:
            key, rest = top.group(1), top.group(2)
            data[key] = _parse_value(rest) if rest.strip() else []
            continue
        item = re.match(r"^  - (.*)$", line)
        cont = re.match(r"^    ([A-Za-z_][\w-]*):(.*)$", line)
        if key is None or not isinstance(data.get(key), list):
            raise FrontMatterError(f"line {n}: unexpected '{line.strip()}'")
        if item:
            sub = re.match(r"^([A-Za-z_][\w-]*):(.*)$", item.group(1))
            if sub and not item.group(1).startswith('"'):
                data[key].append({sub.group(1): _parse_value(sub.group(2))})
            else:
                data[key].append(_parse_value(item.group(1)))
        elif cont and data[key] and isinstance(data[key][-1], dict):
            data[key][-1][cont.group(1)] = _parse_value(cont.group(2))
        else:
            raise FrontMatterError(f"line {n}: cannot parse '{line.strip()}'")
    return data, body


# --------------------------------------------------------------------------
# Generated blocks inside markdown files
# --------------------------------------------------------------------------
def block_re(name: str, kind: str = "UN") -> re.Pattern[str]:
    return re.compile(
        rf"<!-- {kind}:START {re.escape(name)} -->\n.*?"
        rf"<!-- {kind}:END {re.escape(name)} -->",
        re.S,
    )


def make_block(name: str, content: str, kind: str = "UN") -> str:
    return (f"<!-- {kind}:START {name} -->\n{content.rstrip()}\n"
            f"<!-- {kind}:END {name} -->")


def replace_block(text: str, name: str, content: str,
                  kind: str = "UN") -> str:
    pattern = block_re(name, kind)
    if not pattern.search(text):
        raise KeyError(f"block {kind}:{name} not found")
    return pattern.sub(lambda _m: make_block(name, content, kind), text, 1)


def write_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")
