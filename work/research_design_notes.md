# ML-11 research and design notes

## Sources reviewed

- FlyRank, *The State of AI-Driven SEO in Numbers* (March 2026), included at `docs/flyrank-seo-research-march-2026.pdf`. The report distinguishes its 341,701-piece portfolio study from its exploratory ML appendix, and explicitly frames its evidence as observational. That led me to describe this capstone's starter-slice results as a separate, narrower experiment.
- [Scientific Reports submission guidance](https://www.nature.com/srep/author-instructions/submission-guidelines): used for readable title/abstract and a clear statement of the study question, method and evidence.
- [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist): used to check claim scope, limitations, experimental settings and reproducibility details.
- [Datawrapper Academy: complex charts](https://www.datawrapper.de/academy/complex-charts): reviewed the idea that chart choices should fit the message and uncertainty, not just decorate a page.

## Decisions taken

- Use a question-shaped title and five-part abstract (question, data, method, result, intended use).
- Keep base rate visible beside ranking metrics, because precision on a 91.1% positive holdout needs context.
- Show one top-of-queue chart and one full-ranking chart, with a one-sentence takeaway under each.
- State the exact data slice, label windows, grouped split, seed, feature list, exclusions and rerun instructions.
- Keep public output aggregate-only; do not publish pseudonymous row IDs or queue rows.
- Separate this 30,000-row starter-slice experiment from the FlyRank report's 341,701-item portfolio analysis and the 78.8-million-row warehouse table.

## Time note

The resources and the FlyRank PDF were reviewed before the paper was drafted. A timed 30-minute research session was not logged, so this file does not claim that the half-hour requirement was met.
