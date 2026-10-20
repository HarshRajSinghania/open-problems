<p align="center">
  <img src="assets/banner.svg" alt="Open Problems: the UN Sustainable Development Goals as open-source tasks" width="900">
</p>

<p align="center">
  <b>A community map of the UN Sustainable Development Goals, turned into open-source tasks.</b><br>
  Pick a problem, pick a task, ship a fix.<br>
  <a href="https://harrythentrepreneur.github.io/open-problems/"><b>Browse the catalogue →</b></a>
</p>

<p align="center">
  <a href="https://github.com/harrythentrepreneur/open-problems/actions/workflows/check-problems.yml"><img src="https://github.com/harrythentrepreneur/open-problems/actions/workflows/check-problems.yml/badge.svg" alt="Check problems"></a>
  <img src="https://img.shields.io/badge/goals-17-19486A?style=flat-square" alt="17 goals">
  <img src="https://img.shields.io/badge/targets-169-26BDE2?style=flat-square" alt="169 targets">
  <img src="https://img.shields.io/badge/indicators-251-4C9F38?style=flat-square" alt="251 indicators">
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-Apache--2.0-blue?style=flat-square" alt="Code: Apache-2.0"></a>
  <a href="LICENSE-docs.md"><img src="https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey?style=flat-square" alt="Docs: CC BY 4.0"></a>
</p>

In 2015 every UN member state agreed 17 goals to reach by 2030. The UN's own
2026 report says most of the 169 targets are off track. Many of them need
things open-source people are good at: tools, data pipelines, maps, apps,
clear writing. This repo breaks the goals down into problems small enough
to work on, and keeps the research, tasks and code for each in one place.

## Start here

New to the project or the SDGs? Here’s a quick path:

1. **Browse the catalogue** — open the [live catalogue](https://harrythentrepreneur.github.io/open-problems/) and pick a goal or a high-priority target.
2. **Read a problem** — each target has a `problem.md` that explains the UN indicator, current status, and what “solved” means.
3. **Find a task** — look for open issues labelled `good first issue` or `help wanted`. Comment `/assign` (or say you’d like to take it) on the issue.
4. **Contribute** — follow the [CONTRIBUTING](CONTRIBUTING.md) guide. You don’t need to be a programmer; research, writing, data cleaning and design are all welcome.
5. **Ask questions** — open a discussion or comment on an issue. The maintainers are happy to help.

If something in this README was confusing, please open an issue or pull request — that’s useful feedback.

## How it works

```text
Goal (17)          e.g. Goal 6  Clean water and sanitation
 └─ Target (169)   e.g. 6.3     Water quality      -> one folder = one problem
     ├─ Indicator  e.g. 6.3.2   Share of water bodies with good quality
     │             (how the UN measures progress)
     └─ Tasks      GitHub issues: research, data, design, code, writing
```

Each problem moves through the same steps, from *suggested* to *handed
over*. See the [problem lifecycle](how-we-work/problem-lifecycle.md)
(with a diagram).

<details>
<summary><b>What is inside a target folder?</b></summary>

```text
goals/06-clean-water-and-sanitation/6.3-water-quality/
├── problem.md          the problem, UN indicators, latest numbers, what exists, what "solved" means
├── research/           evidence, notes, datasets
└── solution/           code and docs, once a solution is scoped
```

The UN parts (target text, indicators, progress, latest World numbers) are
generated from UN data by [`tools/`](tools/). Everything else is written by
people like you.

</details>

<details>
<summary><b>Glossary: words we use</b></summary>

| Word | Meaning |
|---|---|
| **Goal** | One of the 17 big aims the UN agreed in 2015, such as "Zero hunger". |
| **Target** | A specific aim under a goal, such as 6.3 "improve water quality". There are 169. Here, one target = one problem folder. |
| **Indicator** | A number the UN uses to measure a target, such as 6.3.2 "share of water bodies with good water quality". There are 251 unique ones. |
| **Tier** | How mature an indicator is. Tier 1: agreed method and regular data from most countries. Tier 2: agreed method, but patchy data. |
| **UN progress** | The UN's own 2026 rating of each target, from "on track" to "regression" (*SDG Report 2026*, pp.44-45). |
| **Priority** | Our view of where help is most needed. It starts from UN progress: stagnation or regression = `high`. |
| **Problem owner** | A real organisation or community that has the problem and will use and keep running the solution. We look for one before we build. |

</details>

## The 17 goals

<!-- INDEX:START goals -->
| | Goal | Targets | Indicators | UN progress 2026 | High priority | Active |
|---|---|---:|---:|---|---:|---:|
| ![1](https://img.shields.io/badge/-01-E5243B?style=flat-square) | [No poverty](goals/01-no-poverty/README.md) | 7 | 13 | 🟡2 🟧3 🔻1 ⚪1 | 1 | 0 |
| ![2](https://img.shields.io/badge/-02-DDA63A?style=flat-square) | [Zero hunger](goals/02-zero-hunger/README.md) | 8 | 15 | 🟩1 🟡1 🟧2 🔴1 🔻2 ⚪1 | 3 | 0 |
| ![3](https://img.shields.io/badge/-03-4C9F38?style=flat-square) | [Good health and well-being](goals/03-good-health-and-well-being/README.md) | 13 | 28 | 🟩1 🟡2 🟧10 | 0 | 0 |
| ![4](https://img.shields.io/badge/-04-C5192D?style=flat-square) | [Quality education](goals/04-quality-education/README.md) | 10 | 12 | 🟡2 🟧1 🔴5 ⚪2 | 5 | 0 |
| ![5](https://img.shields.io/badge/-05-FF3A21?style=flat-square) | [Gender equality](goals/05-gender-equality/README.md) | 9 | 14 | 🟧5 ⚪4 | 0 | 0 |
| ![6](https://img.shields.io/badge/-06-26BDE2?style=flat-square) | [Clean water and sanitation](goals/06-clean-water-and-sanitation/README.md) | 8 | 11 | 🟡1 🟧2 🔴3 ⚪2 | 3 | 1 |
| ![7](https://img.shields.io/badge/-07-FCC30B?style=flat-square) | [Affordable and clean energy](goals/07-affordable-and-clean-energy/README.md) | 5 | 6 | 🟩2 🟡3 | 0 | 0 |
| ![8](https://img.shields.io/badge/-08-A21942?style=flat-square) | [Decent work and economic growth](goals/08-decent-work-and-economic-growth/README.md) | 12 | 17 | 🟡1 🟧6 🔴1 🔻3 ⚪1 | 4 | 0 |
| ![9](https://img.shields.io/badge/-09-FD6925?style=flat-square) | [Industry, innovation and infrastructure](goals/09-industry-innovation-and-infrastructure/README.md) | 8 | 12 | 🟩1 🟡4 🟧1 🔻1 ⚪1 | 1 | 0 |
| ![10](https://img.shields.io/badge/-10-DD1367?style=flat-square) | [Reduced inequalities](goals/10-reduced-inequalities/README.md) | 10 | 14 | 🟩1 🟡2 🟧2 🔴2 🔻3 | 5 | 0 |
| ![11](https://img.shields.io/badge/-11-FD9D24?style=flat-square) | [Sustainable cities and communities](goals/11-sustainable-cities-and-communities/README.md) | 10 | 16 | 🟩3 🟧1 🔴1 ⚪5 | 1 | 0 |
| ![12](https://img.shields.io/badge/-12-BF8B2E?style=flat-square) | [Responsible consumption and production](goals/12-responsible-consumption-and-production/README.md) | 11 | 13 | 🟩4 🟧1 🔴1 🔻4 ⚪1 | 5 | 0 |
| ![13](https://img.shields.io/badge/-13-3F7E44?style=flat-square) | [Climate action](goals/13-climate-action/README.md) | 5 | 8 | 🟩2 🟧1 ⚪2 | 0 | 0 |
| ![14](https://img.shields.io/badge/-14-0A97D9?style=flat-square) | [Life below water](goals/14-life-below-water/README.md) | 10 | 10 | 🟡3 🟧3 🔻3 ⚪1 | 3 | 0 |
| ![15](https://img.shields.io/badge/-15-56C02B?style=flat-square) | [Life on land](goals/15-life-on-land/README.md) | 12 | 14 | 🟩3 🟡1 🟧2 🔴2 🔻2 ⚪2 | 4 | 0 |
| ![16](https://img.shields.io/badge/-16-00689D?style=flat-square) | [Peace, justice and strong institutions](goals/16-peace-justice-and-strong-institutions/README.md) | 12 | 24 | 🟡3 🟧1 🔴4 🔻1 ⚪3 | 5 | 0 |
| ![17](https://img.shields.io/badge/-17-19486A?style=flat-square) | [Partnerships for the Goals](goals/17-partnerships-for-the-goals/README.md) | 19 | 24 | 🟩3 🟡4 🟧3 🔴4 🔻1 ⚪4 | 5 | 0 |
| | **Total** | **169** | **251** | | **45** | **1** |

UN progress legend: 🟩 On track or target met · 🟡 Moderate progress · 🟠 Marginal progress · 🔴 Stagnation · 🔻 Regression · ⚪ Insufficient data.  
Indicators are counted once even when the UN lists them under more than one target. High priority = targets the UN rates as *stagnation* or *regression*. Active = status beyond `suggested`.
<!-- INDEX:END goals -->

Source for UN progress: "SDG progress by target", *The Sustainable
Development Goals Report 2026*, pp.44-45
([PDF](https://unstats.un.org/sdgs/report/2026/The-Sustainable-Development-Goals-Report-2026.pdf)).

## 🔥 Most needed right now

<details open>
<summary>Targets where the UN sees no progress or things getting worse</summary>

<!-- INDEX:START needed -->
**45 targets** where the UN sees *stagnation* (🔴) or *regression* (🔻) in 2026. Each one needs research first.

| Goal | Targets |
|---|---|
| **1** No poverty | 🔻 [1.a Government spending on essential services](goals/01-no-poverty/1.a-government-spending-essential-services/problem.md) |
| **2** Zero hunger | 🔻 [2.1 Undernourishment and food security](goals/02-zero-hunger/2.1-undernourishment-food-security/problem.md) · 🔴 [2.2 Malnutrition](goals/02-zero-hunger/2.2-malnutrition/problem.md) · 🔻 [2.a Investment in agriculture](goals/02-zero-hunger/2.a-investment-agriculture/problem.md) |
| **4** Quality education | 🔴 [4.1 Effective learning outcomes](goals/04-quality-education/4.1-effective-learning-outcomes/problem.md) · 🔴 [4.2 Early childhood education](goals/04-quality-education/4.2-early-childhood-education/problem.md) · 🔴 [4.3 TVET and tertiary education](goals/04-quality-education/4.3-tvet-tertiary-education/problem.md) · 🔴 [4.6 Adult literacy and numeracy](goals/04-quality-education/4.6-adult-literacy-numeracy/problem.md) · 🔴 [4.c Qualified teachers](goals/04-quality-education/4.c-qualified-teachers/problem.md) |
| **6** Clean water and sanitation | 🔴 [6.3 Water quality](goals/06-clean-water-and-sanitation/6.3-water-quality/problem.md) · 🔴 [6.5 Transboundary water cooperation](goals/06-clean-water-and-sanitation/6.5-transboundary-water-cooperation/problem.md) · 🔴 [6.6 Water-related ecosystems](goals/06-clean-water-and-sanitation/6.6-water-related-ecosystems/problem.md) |
| **8** Decent work and economic growth | 🔻 [8.2 Economic productivity](goals/08-decent-work-and-economic-growth/8.2-economic-productivity/problem.md) · 🔻 [8.3 Formalization of SMEs](goals/08-decent-work-and-economic-growth/8.3-formalization-smes/problem.md) · 🔴 [8.4 Material resource efficiency](goals/08-decent-work-and-economic-growth/8.4-material-resource-efficiency/problem.md) · 🔻 [8.8 Labour rights and safe working environment](goals/08-decent-work-and-economic-growth/8.8-labour-rights-safe-working/problem.md) |
| **9** Industry, innovation and infrastructure | 🔻 [9.2 Sustainable/inclusive industrialization](goals/09-industry-innovation-and-infrastructure/9.2-sustainable-inclusive-industrialization/problem.md) |
| **10** Reduced inequalities | 🔻 [10.3 Eliminate discrimination](goals/10-reduced-inequalities/10.3-eliminate-discrimination/problem.md) · 🔻 [10.4 Fiscal and social protection policies](goals/10-reduced-inequalities/10.4-fiscal-social-protection-policies/problem.md) · 🔴 [10.6 Inclusive global governance](goals/10-reduced-inequalities/10.6-inclusive-global-governance/problem.md) · 🔴 [10.7 Safe migration and mobility](goals/10-reduced-inequalities/10.7-safe-migration-mobility/problem.md) · 🔻 [10.a Special and differential treatment (WTO)](goals/10-reduced-inequalities/10.a-special-differential-treatment/problem.md) |
| **11** Sustainable cities and communities | 🔴 [11.1 Housing and basic services](goals/11-sustainable-cities-and-communities/11.1-housing-basic-services/problem.md) |
| **12** Responsible consumption and production | 🔴 [12.2 Sustainable use of natural resources](goals/12-responsible-consumption-and-production/12.2-sustainable-use-natural-resources/problem.md) · 🔻 [12.3 Food waste and losses](goals/12-responsible-consumption-and-production/12.3-food-waste-losses/problem.md) · 🔻 [12.5 Reduction in waste generation](goals/12-responsible-consumption-and-production/12.5-reduction-waste-generation/problem.md) · 🔻 [12.b Sustainable tourism monitoring](goals/12-responsible-consumption-and-production/12.b-sustainable-tourism-monitoring/problem.md) · 🔻 [12.c Fossil fuel subsidies](goals/12-responsible-consumption-and-production/12.c-fossil-fuel-subsidies/problem.md) |
| **14** Life below water | 🔻 [14.3 Ocean acidification](goals/14-life-below-water/14.3-ocean-acidification/problem.md) · 🔻 [14.4 Sustainable fishing](goals/14-life-below-water/14.4-sustainable-fishing/problem.md) · 🔻 [14.a Research capacity and marine technology](goals/14-life-below-water/14.a-research-capacity-marine-technology/problem.md) |
| **15** Life on land | 🔴 [15.1 Terrestrial and freshwater ecosystems](goals/15-life-on-land/15.1-terrestrial-freshwater-ecosystems/problem.md) · 🔻 [15.3 Desertification and land degradation](goals/15-life-on-land/15.3-desertification-land-degradation/problem.md) · 🔴 [15.4 Conservation of mountain ecosystems](goals/15-life-on-land/15.4-conservation-mountain-ecosystems/problem.md) · 🔻 [15.5 Loss of biodiversity](goals/15-life-on-land/15.5-loss-biodiversity/problem.md) |
| **16** Peace, justice and strong institutions | 🔴 [16.3 Justice for all](goals/16-peace-justice-and-strong-institutions/16.3-justice-for-all/problem.md) · 🔴 [16.7 Inclusive decision-making](goals/16-peace-justice-and-strong-institutions/16.7-inclusive-decision-making/problem.md) · 🔴 [16.8 Inclusive global governance](goals/16-peace-justice-and-strong-institutions/16.8-inclusive-global-governance/problem.md) · 🔴 [16.10 Public access to information](goals/16-peace-justice-and-strong-institutions/16.10-public-access-information/problem.md) · 🔻 [16.b Non-discriminatory laws](goals/16-peace-justice-and-strong-institutions/16.b-non-discriminatory-laws/problem.md) |
| **17** Partnerships for the Goals | 🔴 [17.1 Tax and other revenue collection](goals/17-partnerships-for-the-goals/17.1-tax-other-revenue-collection/problem.md) · 🔴 [17.2 ODA commitment by developed countries](goals/17-partnerships-for-the-goals/17.2-oda-commitment-developed-countries/problem.md) · 🔴 [17.12 Duty-free market access for LDCs](goals/17-partnerships-for-the-goals/17.12-duty-free-market-access-ldcs/problem.md) · 🔴 [17.13 Global macroeconomic stability](goals/17-partnerships-for-the-goals/17.13-global-macroeconomic-stability/problem.md) · 🔻 [17.15 Respect country’s policy space](goals/17-partnerships-for-the-goals/17.15-policy-space/problem.md) |
<!-- INDEX:END needed -->

</details>

## Who we need

You do not need to be a programmer. We need:

- **Researchers** to find what already exists, and the latest numbers, with sources.
- **Data people** to find, clean and check open datasets.
- **Developers** to build tools once a problem is scoped.
- **Designers** and writers to make the work clear and usable.
- **Anyone** who can help with the tasks labelled `good first issue`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started, and the
[code of conduct](CODE_OF_CONDUCT.md).

## Licence

Code is [Apache-2.0](LICENSE). Documentation is [CC BY 4.0](LICENSE-docs.md).
