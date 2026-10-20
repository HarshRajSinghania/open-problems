# 0001. One repository with 17 goal folders, generated from UN data

- Date: 2026-10-20
- Status: accepted
- Deciders: @harrythentrepreneur

## Context

We want a single place where anyone can see all UN Sustainable Development
Goal targets as concrete problems, pick one and contribute. 169 targets in
169 repositories would be impossible to browse or maintain. One flat list
would be hard to organise.

## Decision

- One repository, `open-problems`, with one folder per goal
  (`goals/06-clean-water-and-sanitation/`) and one folder per target
  (`6.3-water-quality/`), each with `problem.md`, `research/` and
  `solution/`.
- The UN parts are generated from the UN SDG Global Database and the
  *SDG Report 2026* by `tools/import_un_sdgs.py`, inside marked blocks, so
  they can be refreshed without touching human writing.
- Tasks are GitHub issues labelled by goal, type and size.
- Starting priority comes from the UN's 2026 progress assessment.

## Consequences

- Easy to browse and search; one set of rules, labels and checks.
- When one goal gets busy (many contributors, real code), it can be split
  into its own repository with `git subtree split --prefix goals/<goal>`
  and linked from here. Record that as a new decision.
- Issue volume could grow large; we create issues only for targets someone
  is actively working on, not for all 169 up front.
