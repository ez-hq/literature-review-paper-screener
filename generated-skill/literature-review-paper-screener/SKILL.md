---
name: literature-review-paper-screener
description: >-
  Literature Review Paper Screener V1. The local agent (internet-enabled, free) searches for literature,
  collects evidence, builds a Literature Evidence Package with Evidence Availability Levels A-D,
  submits it to the private LoomLoom Cloud template for screening, then audits the returned Paper
  Sheet + Reading List data and renders Excel outputs. Cloud has no internet access; you gather the
  evidence and it evaluates it. Literature Review task type only (V1); Medical Science focus.
---

# Literature Review Paper Screener — Local Agent Skill

The **Local Agent** is the internet research layer of the Literature Review Paper Screener. You have
internet access and do **all** research and evidence gathering. The **Cloud** (a private LoomLoom
template) has no internet access; it screens and organizes only the evidence you send it.

> **Core principle:** Local Agent gathers the evidence. Cloud evaluates and organizes the evidence.
> (Full product rules live in the project documentation set; this Skill is the executable guide.)

## What one task means

One task = **one full literature review** for one student topic. Per task the Cloud returns:

- **Screening data** — per-paper verdicts (topic relevance, quality filters, recency, priority, reading role, notes, summary, evidence-bound)
- **Paper Sheet data** — the complete screened pool
- **Reading List data** — the same pool organized by Priority and Primary Reading Role

Your local job before the Cloud run: search, collect, deduplicate, and package evidence. Your local
job after the Cloud run: audit the results and render the Excel deliverables.

## Prerequisites

- Python 3.9+ (validator script)
- `loomloom` Skill + CLI installed and `loomloom doctor` reports `healthy=true`
- A CogFoundry (or configured) LoomLoom account with balance for cloud runs

## Workflow

### 1. Install/verify LoomLoom

```bash
loomloom doctor --output json
```

If `healthy=false`, complete authentication first (browser login preferred: `loomloom login`;
fallback API token in the platform console). Do not proceed to cloud steps without a healthy Doctor.

### 2. Understand your template binding

This Skill orchestrates a **private template version**. Current binding (do not invent IDs):

- Template ID: `76484632-796a-4980-bfc5-180c9fd4200f`
- Version ID: `4677c008-6780-425e-b2f7-c05bc7caba38` (v1)
- Name: `Literature Review Paper Screener — V1`

Verify with `loomloom template-spec get 76484632-796a-4980-bfc5-180c9fd4200f` before running.
If the binding changes, ask the owner; never guess IDs.

### 3. Gather user input (conversational)

Ask, one question at a time, in plain language (all optional except the topic):

1. **Research Question / Topic** — required
2. Required Citation Count — optional (guidance only)
3. Assignment Requirements (brief, rubric, word count, population, etc.) — optional
4. Research Restrictions (population, country/region, time period, source type, years) — optional
5. Deadline — optional (reading recommendation only)
6. Available Reading Time — optional

Never block on missing optional inputs; skipped fields use default rules. If the topic is too
unclear, ask **one** clarification question, then proceed with what you have.

### 4. Search the literature (you, local, internet-enabled)

Per the search workflow rules (see references/architecture.md):

- Build a search profile from available input; never invent restrictions the user did not provide.
- Decompose the question into core concepts, research focus, population, context.
- Build a keyword map (synonyms, alternative terminology, academic terms).
- Generate multiple search queries (direct, relationship, terminology expansion, population/context).
- Run them; maximize recall; do NOT screen for quality during search.
- Run a coverage check (all core concepts, synonyms, population, context, direct evidence,
  alternative perspectives, foundational + recent research). Expand only when new searches still
  add new literature; stop when new searches produce mainly duplicates/covered/low-relevance.
- Combine everything into a **Master Candidate Pool**, then **deduplicate** (DOI, accession, title)
  into the **Unique Candidate Pool**.

### 5. Collect evidence and build the Literature Evidence Package

For every unique candidate, collect as much as is reasonably available:

- Bibliographic metadata (title, authors, year, journal/publisher, source type, DOI, ISBN, stable URL, database record)
- Abstract
- Available content: full text where possible; otherwise sections (intro/methods/results/discussion/conclusion) or structured info (methods info, key findings, results info, conclusion info, database record detail)
- Stable links (paper link, DOI link, database record, publisher page)

Then assign **one Evidence Availability Level** per paper:

| Level | Package contains |
|---|---|
| A | Full text, or substantial full-paper content (Methods, Results, Discussion, Conclusion) |
| B | Abstract + substantial structured information (methods info, key findings, results, conclusions, detailed database record) |
| C | Title + metadata + Abstract |
| D | Title, authors, year, journal/publisher only |

Record per paper: Available Evidence, Missing Evidence, Assessment Limitations. Do **not** fabricate
evidence; do **not** require full text for every paper; failed retrieval only lowers the level.

Output: a **Structured Local-to-Cloud Handoff Dataset** (see references/evidence-package-schema.md
for the exact JSON shape) — one row of paper records + the run-context block.

### 6. Prepare the cloud workbook

Download the workbook for the exact version:

```bash
loomloom template-spec download-workbook 76484632-796a-4980-bfc5-180c9fd4200f 4677c008-6780-425e-b2f7-c05bc7caba38
```

Fill one row:

- `Research Question / Topic` — required (text)
- `Assignment Requirements`, `Research Restrictions` — optional (text)
- `Required Citation Count`, `Deadline`, `Available Reading Time` — optional (text; collected for context only)
- `Screening Model` — select from the approved list; leave default if fine
- `Literature Evidence Package` — **upload the handoff dataset as a text/plain asset and put the returned `input_asset_id` in the cell**:

```bash
loomloom input-asset upload handoff.txt
```

### 7. Validate and precheck (read-only)

```bash
loomloom template-spec validate-workbook <template-id> <version-id> <filled.xlsx>
loomloom template-spec precheck-workbook <template-id> <version-id> <filled.xlsx>
```

Show the owner the precheck estimate (template name, version, task count, estimated cost, currency,
balance, sufficiency). Do **not** submit yet.

### 8. Confirmed run

Get explicit owner confirmation in the current conversation against the shown estimate. Then:

```bash
loomloom template-spec submit-workbook <template-id> <version-id> <filled.xlsx> --client-request-id <new-uuid>
```

Preserve the returned `run_id`. Watch and retrieve:

```bash
loomloom run watch <run-id>
loomloom run result-rows <run-id>
loomloom run result-workbook <run-id> --output-file results.xlsx
```

Every run needs its own confirmation and its own client-request-id. If input changes after
confirmation, re-validate, re-precheck, show a new estimate, and obtain a new confirmation.

### 9. Local audit (mandatory)

Run the validator on the returned results:

```bash
python3 scripts/validate_results.py --input result-rows.json --manifest ../store-manifest.json --out-dir ../review
```

It must PASS before you render or claim success. The validator checks: parseable structured output,
input/output correspondence, evidence presence, citation completeness, no fabricated claims,
explicit failures/partial results, and reproducible rerun conditions. If the validator reports
issues, do not fabricate fixes — record them and report to the owner.

### 10. Render and deliver

Run the Excel renderer over the audited results:

```bash
python3 scripts/render_excel.py --input result-rows.json --out PaperSheet.xlsx ReadingList.xlsx
```

Deliver: Paper Sheet (complete screened pool) + Reading List (same pool by Priority and Reading Role)
as Excel files, plus a short plain-language summary: how many papers searched, screened, included,
excluded (with reasons), and the evidence-level breakdown (A/B/C/D). Point out evidence-limited
papers (Levels C/D) and preliminary classifications.

## Rules you must not break

- The Cloud has **no internet**: it evaluates only the evidence you send. Never ask it to search,
  fetch, or open URLs, and never claim it reviewed full text you did not provide.
- **Evidence Availability ≠ Quality.** A Level C/D paper is not lower quality; its assessment is
  shallower and must be flagged, not dropped.
- **Search broadly. Screen carefully. Keep all qualified literature.** Deadline / reading time /
  citation count recommend what to read first — they never remove literature from the outputs.
- Never include excluded papers in the Paper Sheet or Reading List.
- Never expose your LoomLoom token, raw user data, or the private Cloud template prompt.
- If the LoomLoom dependency is missing or Doctor is unhealthy, stop cloud stages and report
  `BLOCKED` — do not invent commands or remotely create state.