# Data

Snapshots of the UN sources this repository is generated from. Keeping them
here makes the build reproducible and shows exactly what we used.

| File | Source | Retrieved | Contents |
|---|---|---|---|
| [`un-sdg-framework.json`](un-sdg-framework.json) | [UN SDG API](https://unstats.un.org/sdgapi/v1/sdg/Goal/List?includechildren=true), UN Statistics Division | 2026-10-20 | 17 goals, 169 targets, 251 indicators with tier. Trimmed: data series removed. |
| [`sdg-report-2026.json`](sdg-report-2026.json) | [The Sustainable Development Goals Report 2026](https://unstats.un.org/sdgs/report/2026/The-Sustainable-Development-Goals-Report-2026.pdf) | 2026-10-20 | Goal key messages (quoted, with page), target short titles and the UN progress status of each target (chart on pp.44-45). |
| [`plain-language.yml`](plain-language.yml) | Community-written | – | One plain-English summary per target (and who it is about). Must restate the official target text only: no new facts or numbers. Shown at the top of each `problem.md`. |
| `un-series-world-latest.json` | [UN SDG API](https://unstats.un.org/sdgapi/v1/sdg/), `Indicator/Data` with `areaCode=1` | see file | Latest and earliest World value of up to 3 data series per indicator, made by [`tools/fetch_un_data.py`](../tools/fetch_un_data.py). Shown as "Latest global numbers" in each `problem.md`. |

## How the progress status was extracted

The report's "SDG progress by target" chart shows one symbol per target.
[`tools/extras/extract_sdg_report_2026.py`](../tools/extras/extract_sdg_report_2026.py)
finds each target code on the page, samples the colour of the symbol next
to it (filled or hollow; green, yellow, red or grey) and maps it with the
chart legend:

| Symbol | Status (`un_progress_2026`) |
|---|---|
| filled green | `on-track` (On track or target met) |
| filled yellow | `moderate` (Moderate progress, but acceleration needed) |
| hollow yellow | `marginal` (Marginal progress, and significant acceleration needed) |
| hollow red | `stagnation` |
| filled red | `regression` |
| filled grey | `insufficient-data` |

All 169 targets were matched. A sample was checked by eye against the
rendered pages. Result: 21 on track, 29 moderate, 44 marginal,
24 stagnation, 21 regression, 30 insufficient data.

If you find a mismatch with the PDF, please
[report it](https://github.com/harrythentrepreneur/open-problems/issues/new?template=03-report-a-bug.yml).

## Terms

UN data and text remain under the
[United Nations terms of use](https://www.un.org/en/about-us/terms-of-use).
See [licensing](../how-we-work/licensing.md).
