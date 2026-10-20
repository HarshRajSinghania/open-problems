# AI use policy

AI tools (chat assistants, code assistants, translation, summarising) can
help you work faster. They also invent facts, sources and code that looks
right but is not. These rules keep the work trustworthy.

## The rules

1. **Disclose.** If an AI tool helped with a contribution, say so in the
   pull request: which tool and what for ("drafted the summary", "suggested
   the regex", "translated the interview notes").
2. **Understand every line.** You must understand, and be able to explain
   when asked, every line of code, every number and every claim you submit.
   "The AI wrote it" is not an answer in review.
3. **Verify every fact and source yourself.** Open every link. Check every
   number against the original, with a page number. Never cite a source you
   have not seen.
4. **No personal or sensitive data in AI tools.** Do not paste interview
   notes, names, locations of vulnerable people or private datasets into
   third-party AI services. See [privacy and safety](privacy-and-safety.md).
5. **Respect licences.** Do not submit generated content you have reason to
   think copies someone else's work.
6. **You are the author.** Your sign-off (`git commit -s`) means you take
   responsibility for the contribution, whoever or whatever helped.

## For reviewers

- Ask for the disclosure if it is missing.
- Spot-check sources and numbers, especially in AI-assisted work.
- It is fine to close a pull request whose author cannot explain it.

## Automated agents

Bots and AI agents may not open pull requests on their own. A human must
review, understand and submit the work under their own name.
