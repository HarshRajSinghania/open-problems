---
goal: 6
goal_title: "Clean water and sanitation"
target: "6.3"
title: "Water quality"
un_target_text: "By 2030, improve water quality by reducing pollution, eliminating dumping and minimizing release of hazardous chemicals and materials, halving the proportion of untreated wastewater and substantially increasing recycling and safe reuse globally"
indicators:
  - code: "6.3.1"
    description: "Proportion of domestic and industrial wastewater flows safely treated"
    tier: "2"
  - code: "6.3.2"
    description: "Proportion of bodies of water with good ambient water quality"
    tier: "1"
un_progress_2026: "stagnation"
status: "researching"
priority: "high"
owner: ""
lead: ""
tags:
  - "earth-observation"
  - "remote-sensing"
  - "sensors"
  - "citizen-science"
  - "rivers"
  - "lakes"
source_url: "https://unstats.un.org/sdgs/metadata/?Text=&Goal=6&Target=6.3"
---

<!-- UN:START header -->
# 6.3 · Water quality

**Goal 6: Clean water and sanitation** · UN progress 2026: 🔴 Stagnation · [All targets in this goal](../README.md)
<!-- UN:END header -->

## The problem (UN target)

<!-- UN:START target -->
> **Target 6.3:** By 2030, improve water quality by reducing pollution, eliminating dumping and minimizing release of hazardous chemicals and materials, halving the proportion of untreated wastewater and substantially increasing recycling and safe reuse globally
<!-- UN:END target -->

## How progress is measured (UN indicators)

<!-- UN:START indicators -->
| Indicator | What it measures | Tier |
|---|---|---|
| 6.3.1 | Proportion of domestic and industrial wastewater flows safely treated | Tier 2 |
| 6.3.2 | Proportion of bodies of water with good ambient water quality | Tier 1 |

**Tier 1** = the method is agreed and countries regularly produce data. **Tier 2** = the method is agreed, but data are patchy. Tiers are set by the UN expert group (IAEG-SDGs). Full metadata: [UN SDG indicator metadata](https://unstats.un.org/sdgs/metadata/?Text=&Goal=6&Target=6.3).
<!-- UN:END indicators -->

## Latest status

<!-- UN:START status -->
**UN progress assessment:** 🔴 Stagnation  
Source: "SDG progress by target", *The Sustainable Development Goals Report 2026*, pp.44-45 ([PDF](https://unstats.un.org/sdgs/report/2026/The-Sustainable-Development-Goals-Report-2026.pdf)). For goal-level facts see [Why it matters](../README.md#why-it-matters).
<!-- UN:END status -->

**What the UN report says** (*SDG Report 2026*, p.21, unless noted):

- **More countries measure water quality.** 124 countries reported on water
  quality in 2023, up from 72 in 2017.
- **Only about half of monitored water bodies are in good shape.** Around half
  of monitored lakes, rivers and groundwater showed good ambient quality.
  Long-term data show minimal change or gradual deterioration.
- **Main drivers:** agricultural runoff and untreated wastewater.
- **Coverage is uneven.** Europe and Northern America have robust networks;
  Asia and Latin America have persistent gaps; Africa has expanded monitoring
  but coverage is still limited.
- **The report's own call:** Earth observation, citizen science and low-cost
  sensors are essential to spot pollution early.
- **The key gap** (p.20): "monitoring gains have yet to drive operational
  change". Measuring more does not yet lead to faster action.

Who is most affected: people in low- and middle-income countries, where
pollution is harder to detect early (p.21).

## What already exists

| Tool | What it does | What it does not cover |
|---|---|---|
| [Copernicus Global Land Service: Lake Water Quality](https://land.copernicus.eu) | Satellite turbidity, trophic state and surface reflectance for 4,200+ lakes | Lakes only; most rivers are too narrow |
| [UNESCO World Water Quality Portal](https://www.unesco.org/en/articles/unesco-launches-pioneering-tool-monitor-water-quality) | Global Earth-observation water quality maps | Monitoring view; no alerting or follow-up workflow |
| [UNEP Freshwater Ecosystems Explorer](https://sdg661.app) | Country data on lakes, rivers, wetlands (SDG 6.6.1) | Ecosystem extent and quality trends, not day-to-day pollution events |
| [eoapp AQUA](https://eoapp.de) | Commercial satellite water quality service | Paid; same river-width limits as other satellites |
| [CyanoLakes](https://www.cyanolakes.com) | Satellite algal-bloom and cyanobacteria monitoring | Focus on blooms in lakes and reservoirs |
| Camera-based river turbidity ([HESS 2025](https://hess.copernicus.org/articles/29/4133/2025/hess-29-4133-2025.pdf), [USGS comparison](https://pubs.usgs.gov/publication/70273951)) | Research: estimate turbidity from ordinary cameras | Research stage; not packaged for communities |

**The gap:**

1. **Rivers are poorly covered by satellites.** Sentinel-2 pixels are 10-60 m,
   so many rivers are narrower than one pixel.
2. **Clouds and revisit gaps** mean days or weeks without a usable image.
3. **No tool turns a detection into an action.** Data reach dashboards, but
   nobody is told "this stretch of river looks wrong today, here is who should
   check it".

## What "solved" looks like

Working hypothesis (to be tested with a problem owner):

- A water agency, NGO or community group in a data-poor region gets an
  **alert within days** when a lake or river stretch they care about shows
  a likely pollution event, with a simple "what to check next" step.
- The tool combines **satellite data** with **cheap ground data** (cameras,
  low-cost sensors or citizen reports) to cover rivers and cloudy days.
- Its outputs can feed national reporting on **indicator 6.3.2**
  (share of water bodies with good ambient water quality).
- It is open source, runs on free data, and the people who use it own it.

## Data we can use

| Dataset | Link | Licence | Notes |
|---|---|---|---|
| Sentinel-2 L2A imagery | [AWS Open Data: Sentinel-2](https://registry.opendata.aws/sentinel-2-l2a-cogs/) | Copernicus open licence | 10-60 m, ~5-day revisit, cloud-affected |
| Copernicus Lake Water Quality | [land.copernicus.eu](https://land.copernicus.eu) | Copernicus open licence | Ready-made lake products |
| UN SDG Global Database, indicator 6.3.2 | [unstats.un.org/sdgs/dataportal](https://unstats.un.org/sdgs/dataportal) | UN terms of use | Country-level, yearly |

> **Help wanted:** add in-situ datasets (e.g. GEMStat), and check each
> licence before we use it.

## Open questions

- Which organisation would use an alert tool and act on it? (We need a
  **problem owner** before we build.)
- Which rivers or lakes should a first pilot cover?
- How good are camera or low-cost sensor readings compared with lab samples?
- How do we keep alerts useful and avoid alarm fatigue?
- How do outputs map onto the official 6.3.2 method?

## Tasks

<!-- UN:START tasks -->
- [Open tasks for 6.3](https://github.com/harrythentrepreneur/open-problems/issues?q=is%3Aissue+is%3Aopen+label%3A%22goal+06%3A+clean+water%22+%226.3%22+in%3Atitle)
- [Add a task](https://github.com/harrythentrepreneur/open-problems/issues/new?template=02-add-a-task.yml&title=%5B6.3%20)
- Notes and sources go in [research/](research/); code goes in [solution/](solution/).
<!-- UN:END tasks -->

Main tracking issue: [#1 \[6.3 Water quality\] Main tracking issue](https://github.com/harrythentrepreneur/open-problems/issues/1), with sub-issues #2-#8.
