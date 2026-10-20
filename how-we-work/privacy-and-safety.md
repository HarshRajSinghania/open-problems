# Privacy and safety

Many SDG problems involve people in vulnerable situations: refugees,
survivors of violence, children, people in conflict zones or informal
settlements. Our first rule is **do no harm**.

## Never commit personal data

Do not put any of these in the repository, issues, discussions or pull
requests:

- names, phone numbers, emails, ID numbers or photos of identifiable people
  (other than public figures acting in a public role);
- exact home or shelter locations, or GPS traces of individuals;
- health, legal, immigration or financial information about any person;
- raw interview recordings or transcripts.

Use aggregated, anonymised or synthetic data. Sample data in `solution/`
folders must be synthetic or from an openly licensed public dataset.

If personal data is committed by mistake, **do not just delete it in a new
commit** (it stays in git history). Tell a maintainer privately straight
away so the history can be cleaned.

## Extra care with vulnerable people and places

- **Locations:** do not publish precise locations of shelters, clinics,
  safe houses, protected species, or groups at risk. Round coordinates or
  aggregate to a safe level.
- **Research with people:** get informed consent, explain how notes will be
  used, store raw notes outside this repo, and only publish anonymised
  summaries. If you work with children or survivors of violence, involve an
  organisation with safeguarding expertise.
- **Dual use:** ask "could this tool or dataset be used to target, track or
  exclude people?" If yes, say so in the issue and discuss mitigations
  before building.

## Do-no-harm checklist for every solution

Copy into `solution/README.md` and answer before going past "Ready to
build":

- [ ] Who could be harmed if this works as intended? If it fails? If it is
      misused?
- [ ] What personal data does it touch, and can we avoid it?
- [ ] Has the problem owner (and ideally the affected community) reviewed
      the design?
- [ ] Is there a human in the loop for decisions that affect people?
- [ ] Is it clear what the tool cannot do, so nobody over-trusts it?

## Reporting a safety concern

Contact a maintainer privately (see [roles](roles.md)). Do not open a
public issue about a security or safety problem.
