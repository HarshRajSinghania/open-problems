# Tools

Small Python scripts that keep the repository consistent. They need
**Python 3.9+ and nothing else** (standard library only), except the
optional extractor in `extras/`.

| Script | What it does | When to run it |
|---|---|---|
| [`check_problems.py`](check_problems.py) | Validates every `problem.md`: front matter fields and values, folder names, sections, markers. | Before every pull request. Runs in CI. |
| [`build_index.py`](build_index.py) | Rebuilds the target tables in each goal README and the goal table in the root README from the front matter. `--check` only reports. | After changing a `status` or `priority`. |
| [`import_un_sdgs.py`](import_un_sdgs.py) | Creates missing goal/target folders and refreshes the UN-sourced parts from `data/`. Never touches human-written text. `--fetch` downloads a fresh copy from the UN SDG API first. | When UN data changes. |
| [`fetch_un_data.py`](fetch_un_data.py) | Downloads the latest and earliest **World** value of up to 3 data series per indicator from the UN SDG API into `data/un-series-world-latest.json`. Polite (one request at a time, pauses, retries) and resumable (raw responses cached; `--cache DIR`). Slow: about an hour for all 251 indicators. | When the UN publishes a new database release. Then run `import_un_sdgs.py`. |
| [`build_site.py`](build_site.py) | Writes `site/data/problems.json` for the [catalogue](https://harrythentrepreneur.github.io/open-problems/). Runs in the Pages workflow. | To preview `site/` locally (`python -m http.server -d site`). |
| [`sdg_common.py`](sdg_common.py) | Shared helpers: goal names and colours, slugs, front-matter reader/writer. | - |
| [`extras/extract_sdg_report_2026.py`](extras/extract_sdg_report_2026.py) | Reads the SDG Report 2026 PDF and writes `data/sdg-report-2026.json` (key messages, per-target progress). Needs `pip install pymupdf`. | Only if the report data must be rebuilt. |

## How "generated" and "human" text live together

In `problem.md` and goal READMEs, generated text sits between markers:

```markdown
<!-- UN:START indicators -->
...generated from UN data...
<!-- UN:END indicators -->
```

Tables between `<!-- INDEX:START ... -->` and `<!-- INDEX:END ... -->` come
from `build_index.py`. The `UN:START plain` block comes from
`data/plain-language.yml` (edit the summary there, not in `problem.md`),
and `UN:START data` from `data/un-series-world-latest.json`. Everything outside the markers belongs to people and
is never overwritten.

In the front matter, these fields are UN data and are refreshed by the
importer: `goal`, `goal_title`, `target`, `un_target_text`, `indicators`,
`un_progress_2026`, `source_url`. All other fields (`title`, `status`,
`priority`, `owner`, `lead`, `tags`, ...) are kept as you wrote them.

## Front matter format

A small subset of YAML: `key: value`, lists of `- item`, and lists of
mappings (the indicators). Strings are written in double quotes. You can
also write `tags: [water, sensors]`.
