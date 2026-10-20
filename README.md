# Open Problems

**A community map of the UN Sustainable Development Goals, turned into
open-source tasks.** Pick a problem, pick a task, ship a fix.

[![Check problems](https://github.com/harrythentrepreneur/open-problems/actions/workflows/check-problems.yml/badge.svg)](https://github.com/harrythentrepreneur/open-problems/actions/workflows/check-problems.yml)
![Goals](https://img.shields.io/badge/goals-17-19486A?style=flat-square)
![Targets](https://img.shields.io/badge/targets-169-26BDE2?style=flat-square)
![Indicators](https://img.shields.io/badge/indicators-251-4C9F38?style=flat-square)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue?style=flat-square)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey?style=flat-square)](LICENSE-docs.md)

In 2015 every UN member state agreed 17 goals to reach by 2030. The UN's own
2026 report says most of the 169 targets are off track. Many of them need
things open-source people are good at: tools, data pipelines, maps, apps,
clear writing. This repo breaks the goals down into problems small enough
to work on, and keeps the research, tasks and code for each in one place.

## How it works

```text
Goal (17)          e.g. Goal 6  Clean water and sanitation
 └─ Target (169)   e.g. 6.3     Water quality      -> one folder = one problem
     ├─ Indicator  e.g. 6.3.2   Share of water bodies with good quality
     │             (how the UN measures progress)
     └─ Tasks      GitHub issues: research, data, design, code, writing
                   -> research/  -> solution/  -> handed over to people who use it
```

Every target folder has the same shape:

```text
goals/06-clean-water-and-sanitation/6.3-water-quality/
├── problem.md          the problem, UN indicators, what exists, what "solved" means
├── research/           evidence, notes, datasets
└── solution/           code and docs, once a solution is scoped
```

The UN parts (target text, indicators, progress) are generated from UN data
by [`tools/import_un_sdgs.py`](tools/import_un_sdgs.py). Everything else is
written by people like you.

## The 17 goals

<!-- INDEX:START goals -->
| | Goal | Targets | Indicators | UN progress 2026 | High priority | Active |
|---|---|---:|---:|---|---:|---:|
| ![1](https://img.shields.io/badge/-01-E5243B?style=flat-square) | [No poverty](goals/01-no-poverty/README.md) | 7 | 13 | 🟡2 🟠3 🔻1 ⚪1 | 1 | 0 |
| ![2](https://img.shields.io/badge/-02-DDA63A?style=flat-square) | [Zero hunger](goals/02-zero-hunger/README.md) | 8 | 15 | 🟢1 🟡1 🟠2 🔴1 🔻2 ⚪1 | 3 | 0 |
| ![3](https://img.shields.io/badge/-03-4C9F38?style=flat-square) | [Good health and well-being](goals/03-good-health-and-well-being/README.md) | 13 | 28 | 🟢1 🟡2 🟠10 | 0 | 0 |
| ![4](https://img.shields.io/badge/-04-C5192D?style=flat-square) | [Quality education](goals/04-quality-education/README.md) | 10 | 12 | 🟡2 🟠1 🔴5 ⚪2 | 5 | 0 |
| ![5](https://img.shields.io/badge/-05-FF3A21?style=flat-square) | [Gender equality](goals/05-gender-equality/README.md) | 9 | 14 | 🟠5 ⚪4 | 0 | 0 |
| ![6](https://img.shields.io/badge/-06-26BDE2?style=flat-square) | [Clean water and sanitation](goals/06-clean-water-and-sanitation/README.md) | 8 | 11 | 🟡1 🟠2 🔴3 ⚪2 | 3 | 1 |
| ![7](https://img.shields.io/badge/-07-FCC30B?style=flat-square) | [Affordable and clean energy](goals/07-affordable-and-clean-energy/README.md) | 5 | 6 | 🟢2 🟡3 | 0 | 0 |
| ![8](https://img.shields.io/badge/-08-A21942?style=flat-square) | [Decent work and economic growth](goals/08-decent-work-and-economic-growth/README.md) | 12 | 17 | 🟡1 🟠6 🔴1 🔻3 ⚪1 | 4 | 0 |
| ![9](https://img.shields.io/badge/-09-FD6925?style=flat-square) | [Industry, innovation and infrastructure](goals/09-industry-innovation-and-infrastructure/README.md) | 8 | 12 | 🟢1 🟡4 🟠1 🔻1 ⚪1 | 1 | 0 |
| ![10](https://img.shields.io/badge/-10-DD1367?style=flat-square) | [Reduced inequalities](goals/10-reduced-inequalities/README.md) | 10 | 14 | 🟢1 🟡2 🟠2 🔴2 🔻3 | 5 | 0 |
| ![11](https://img.shields.io/badge/-11-FD9D24?style=flat-square) | [Sustainable cities and communities](goals/11-sustainable-cities-and-communities/README.md) | 10 | 16 | 🟢3 🟠1 🔴1 ⚪5 | 1 | 0 |
| ![12](https://img.shields.io/badge/-12-BF8B2E?style=flat-square) | [Responsible consumption and production](goals/12-responsible-consumption-and-production/README.md) | 11 | 13 | 🟢4 🟠1 🔴1 🔻4 ⚪1 | 5 | 0 |
| ![13](https://img.shields.io/badge/-13-3F7E44?style=flat-square) | [Climate action](goals/13-climate-action/README.md) | 5 | 8 | 🟢2 🟠1 ⚪2 | 0 | 0 |
| ![14](https://img.shields.io/badge/-14-0A97D9?style=flat-square) | [Life below water](goals/14-life-below-water/README.md) | 10 | 10 | 🟡3 🟠3 🔻3 ⚪1 | 3 | 0 |
| ![15](https://img.shields.io/badge/-15-56C02B?style=flat-square) | [Life on land](goals/15-life-on-land/README.md) | 12 | 14 | 🟢3 🟡1 🟠2 🔴2 🔻2 ⚪2 | 4 | 0 |
| ![16](https://img.shields.io/badge/-16-00689D?style=flat-square) | [Peace, justice and strong institutions](goals/16-peace-justice-and-strong-institutions/README.md) | 12 | 24 | 🟡3 🟠1 🔴4 🔻1 ⚪3 | 5 | 0 |
| ![17](https://img.shields.io/badge/-17-19486A?style=flat-square) | [Partnerships for the Goals](goals/17-partnerships-for-the-goals/README.md) | 19 | 24 | 🟢3 🟡4 🟠3 🔴4 🔻1 ⚪4 | 5 | 0 |
| | **Total** | **169** | **251** | | **45** | **1** |

UN progress legend: 🟢 On track or target met · 🟡 Moderate progress · 🟠 Marginal progress · 🔴 Stagnation · 🔻 Regression · ⚪ Insufficient data.  
Indicators are counted once even when the UN lists them under more than one target. High priority = targets the UN rates as *stagnation* or *regression*. Active = status beyond `suggested`.
<!-- INDEX:END goals -->

Source for UN progress: "SDG progress by target", *The Sustainable
Development Goals Report 2026*, pp.44-45
([PDF](https://unstats.un.org/sdgs/report/2026/The-Sustainable-Development-Goals-Report-2026.pdf)).

## Start here

| I want to... | Go to |
|---|---|
| See a fully worked example | [6.3 Water quality](goals/06-clean-water-and-sanitation/6.3-water-quality/problem.md) |
| Find something small to do | [Good first issues](https://github.com/harrythentrepreneur/open-problems/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) |
| Understand the rules | [CONTRIBUTING.md](CONTRIBUTING.md) · [How we work](how-we-work/) |
| Suggest a new problem | [Open a suggestion](https://github.com/harrythentrepreneur/open-problems/issues/new?template=01-suggest-a-problem.yml) |
| Ask a question | [Discussions](https://github.com/harrythentrepreneur/open-problems/discussions) |

## How to help in 3 steps

1. **Pick a problem.** Browse the goal table above and open a target's
   `problem.md`. Anything marked *Help wanted* is open.
2. **Pick a task.** Open the target's task list, find an issue you like and
   comment `/assign` (or just say you would like to take it).
3. **Ship it.** Open a pull request, signed off with `git commit -s`.
   See [CONTRIBUTING.md](CONTRIBUTING.md) for the details.

No code needed for most tasks: research, data hunting, writing and design
count just as much.

## Repository map

| Folder | What is in it |
|---|---|
| [`goals/`](goals/) | 17 goal folders, 169 target folders |
| [`how-we-work/`](how-we-work/) | Roles, code of conduct, AI use, licensing, privacy and safety, problem lifecycle, decisions |
| [`templates/`](templates/) | Templates for new problems and solutions |
| [`shared/`](shared/) | Code and data reused across goals |
| [`tools/`](tools/) | Scripts that import UN data, check files and rebuild these tables |
| [`data/`](data/) | Snapshots of the UN data we use, with dates |

## Disclaimer

Independent community project, not affiliated with or endorsed by the
United Nations. Goal, target and indicator text comes from the
[UN SDG Global Database](https://unstats.un.org/sdgs/) (unstats.un.org),
used with attribution. Progress assessments and key messages are quoted from
*The Sustainable Development Goals Report 2026* (United Nations). We do not
use the UN emblem or the SDG icons. Goal colours are used only as plain
colours.

Code is [Apache-2.0](LICENSE); documentation and research are
[CC BY 4.0](LICENSE-docs.md).
