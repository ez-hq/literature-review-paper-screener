# Literature Review Paper Screener

A Literature Review SkillBot (V1) that helps students screen and organize academic literature.

## What it is

- **Local Agent Skill** (this repository, MIT licensed) — the free, internet-enabled layer:
  searches literature, collects evidence, builds a **Literature Evidence Package** with
  Evidence Availability Levels A–D, submits it to the private Cloud template for screening,
  audits the results, and renders Excel **Paper Sheet** + **Reading List** outputs.
- **Cloud template** (proprietary, NOT in this repository) — the paid screening engine:
  topic relevance, quality filters (source validity, basic credibility, level-aware content
  credibility), recency, priority, reading role, and evidence-bound notes/summary.

> **Local Agent gathers the evidence. Cloud evaluates and organizes the evidence.**
> The Cloud has no internet access; it evaluates only the evidence you send it.

## Contents

- `generated-skill/literature-review-paper-screener/` — the installable local Agent Skill
  (`SKILL.md`, `agents/`, `references/`, `scripts/`, LICENSE)
- `docs/` — the V1 product documentation set (product scope, workflows, rules, outputs)

## Install the local Skill

Download the latest release ZIP and install it as an Agent Skill, or use the
`literature-review-paper-screener` release asset:

```text
https://github.com/ez-hq/literature-review-paper-screener/releases/latest/download/literature-review-paper-screener.zip
```

## License

MIT — covers the local Agent Skill code in this repository only.

⚠️ **The Cloud template (screening prompts, step definitions, model configuration) is
proprietary and is NOT covered by the MIT License. It is not distributed here.**

Copyright (c) 2026 ez-hq
