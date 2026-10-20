# Roles

Everyone starts as a contributor. Roles are about responsibility, not rank.

| Role | Who | Does |
|---|---|---|
| **Contributor** | Anyone | Picks tasks, opens pull requests, reviews others' work, joins discussions. |
| **Problem lead** (`lead` in `problem.md`) | A regular contributor who volunteers for one target | Keeps `problem.md` up to date, splits work into tasks, welcomes newcomers, moves the status along the [lifecycle](problem-lifecycle.md). |
| **Problem owner** (`owner` in `problem.md`) | An organisation or community that has the problem and will use the result | Confirms the problem is real, says what "solved" means, tests prototypes, takes over the solution at hand-over. |
| **Maintainer** | Listed in [CODEOWNERS](../.github/CODEOWNERS) | Reviews and merges pull requests, manages labels and releases, enforces the [code of conduct](code-of-conduct.md). |

## Good to know

- A problem should not move to **Ready to build** without a problem owner,
  or a written reason why none is needed. Building without a user is the
  most common way open-source social-good projects fail.
- Anyone can become a problem lead: comment on the target's main tracking
  issue. Maintainers confirm within a week.
- If a lead steps away, they set `lead: ""` or ask a maintainer to.
- New maintainers are invited by existing maintainers after sustained,
  good-quality contributions. Record it in [decisions](decisions/README.md).
