---
name: literature-review-paper-screener
description: >-
  Literature Review Paper Screener V1.1. The local agent (internet-enabled, free) searches for literature,
  collects evidence, builds per-paper Evidence Records with Evidence Availability Levels A-D, submits ONE
  paper per workbook row to the private LoomLoom Cloud template (rows run as independent parallel tasks, so
  screening never exceeds the platform per-activity timeout), then audits and merges the returned screening
  results and renders Excel Paper Sheet + Reading List. Cloud has no internet access; you gather the evidence
  and it evaluates it. Literature Review task type only; Medical Science focus.
---

# Literature Review Paper Screener — Local Agent Skill (V1.1)

The **Local Agent** is the internet research layer of the Literature Review Paper Screener. You have
internet access and do **all** research and evidence gathering. The **Cloud** (a private LoomLoom
template) has no internet access; it screens and organizes only the evidence you send it.

> **Core principle:** Local Agent gathers the evidence. Cloud evaluates and organizes the evidence.
> (Full product rules live in the project documentation set; this Skill is the executable guide.)

## What one task means and how it executes (V1.1)

One task = **one full literature review** for one student topic, delivered as:

- **Paper Sheet** — the complete screened pool, one row per retained paper (evidence level, screening verdicts, priority, reading role, evidence-bound notes/summary)
- **Reading List** — the same pool organized by Priority and Primary Reading Role

**Execution model (per-paper rows):** the Cloud template's screening step has a platform-fixed
per-activity timeout. Screening all N papers inside **one** activity times out for larger sets
(observed: 20 papers → `StartToClose timeout` failure, twice). V1.1 therefore submits **one paper
per workbook row**: N papers = N rows = N independent parallel cloud tasks, each screening a single
paper in seconds. The results are **merged locally** back into one Paper Sheet + Reading List.

- Never put more than one paper's evidence into a single workbook row.
- Total cloud tasks = total papers = total per-task fee units (Market: USD 0.10/task).
- Merging is local-only: no cloud aggregation step, no re-derivation.

## Prerequisites

- Python 3.9+ (validator/render scripts)
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

### 5. Collect evidence and build one Evidence Record per paper

For every unique candidate, collect as much as is reasonably available:

- Bibliographic metadata (title, authors, year, journal/publisher, source type, DOI, ISBN, stable URL, database record)
- Abstract
- Available content: full text where possible; otherwise sections (intro/methods/results/discussion/conclusion) or structured info (methods info, key findings, results info, conclusion info, database record detail)
- Stable links (paper link, DOI link, database record, publisher page)

Then assign **one Evidence Availability Level** per paper:

| Level | Record contains |
|---|---|
| A | Full text, or substantial full-paper content (Methods, Results, Discussion, Conclusion) |
| B | Abstract + substantial structured information (methods info, key findings, results, conclusions, detailed database record) |
| C | Title + metadata + Abstract |
| D | Title, authors, year, journal/publisher only |

Record per paper: Available Evidence, Missing Evidence, Assessment Limitations. Do **not** fabricate
evidence; do **not** require full text for every paper; failed retrieval only lowers the level.

**Output = one standalone JSON/text file per paper** (the per-paper Evidence Record, see
references/evidence-package-schema.md for the exact shape), named like `handoff_p001.json`…
`handoff_pNNN.json`. **One file must contain exactly one paper's record** — this is what keeps a
single cloud task small enough to finish inside the platform activity timeout. Do not bundle all
papers into one file.

### 6. Prepare the cloud workbook (one row per paper)

Download the workbook for the exact version:

```bash
loomloom template-spec download-workbook 76484632-796a-4980-bfc5-180c9fd4200f 4677c008-6780-425e-b2f7-c05bc7caba38
```

Fill **one row per paper** (N papers → N rows):

- `Research Question / Topic` — the same required topic text on every row
- `Assignment Requirements`, `Research Restrictions` — optional; same values on every row when provided
- `Required Citation Count`, `Deadline`, `Available Reading Time` — optional (collected for context only)
- `Screening Model` — select from the approved list once; leave default if fine
- `Literature Evidence Package` — **upload each per-paper record as its own text/plain asset and put
  that row's `input_asset_id` in the cell**:

```bash
# one upload per paper
loomloom input-asset upload handoff_p001.json
# -> asset id for row 1
loomloom input-asset upload handoff_p002.json
# -> asset id for row 2  ... and so on
```

Every row's evidence cell must reference a **different single-paper asset**. Reusing one
multi-paper asset on every row is forbidden (it reintroduces the timeout).

### 7. Validate and precheck (read-only)

```bash
loomloom template-spec validate-workbook <template-id> <version-id> <filled.xlsx>
loomloom template-spec precheck-workbook <template-id> <version-id> <filled.xlsx>
```

Show the owner, before any submission:

- task count = **paper count N** (rows in the workbook)
- per-task fee (Market: USD 0.10) and **total fee = 0.10 × N** (private-template precheck reports
  model cost only — state both clearly)
- estimated model/API cost from the precheck, plus balance and sufficiency

Do **not** submit yet.

### 8. Confirmed run (fee + count lock)

Get explicit owner confirmation against the shown numbers, phrased as: **"N papers → N cloud
tasks → total fee ≈ 0.10 × N + model cost. Confirm?"** The row count is the paper-count lock: the
number of tasks (and fee units) is fixed before submission and cannot change mid-run. Then:

```bash
loomloom template-spec submit-workbook <template-id> <version-id> <filled.xlsx> --client-request-id <new-uuid>
```

Preserve the returned `run_id`. Watch and retrieve **all** task results:

```bash
loomloom run watch <run-id>
loomloom run result-rows <run-id> --output result-rows.json
loomloom run result-workbook <run-id> --output-file results.xlsx
```

Every run needs its own confirmation and its own client-request-id. If input changes after
confirmation, re-validate, re-precheck, show a new estimate, and obtain a new confirmation.

### 9. Local audit (mandatory — merged)

Run the validator on the returned results (it merges all per-paper task outputs into one global
screened pool automatically):

```bash
python3 scripts/validate_results.py --input result-rows.json --manifest ../store-manifest.json --out-dir ../review
```

It must PASS before you render or claim success. The validator checks: parseable structured
output for every task row, evidence availability levels, content-credibility decision rule,
excluded papers never in the Paper Sheet, same pool across Paper Sheet and Reading List, one
Primary Reading Role per paper, no duplicate record IDs across batches, citations present,
explicit failures/partial results, and reproducible rerun conditions. If it reports issues, do not
fabricate fixes — record them and report to the owner.

### 10. Render and deliver (merged)

Run the Excel renderer over the audited result set (it merges every task row's output into one
Paper Sheet + one Reading List):

```bash
python3 scripts/render_excel.py --input result-rows.json --out-dir <deliverables>
```

Deliver: Paper Sheet (complete screened pool, one row per retained paper) + Reading List (same
pool by Priority and Reading Role) as Excel files, plus a short plain-language summary: how many
papers searched, screened, included, excluded (with reasons), the evidence-level breakdown
(A/B/C/D), and how many cloud tasks ran. Point out evidence-limited papers (Levels C/D) and
preliminary classifications.

## Rules you must not break

- **One paper per workbook row / per cloud task.** Never bundle multiple papers into one evidence
  asset or one row; multi-paper single rows time out on the platform (V1.1 fixes this by design).
  If a row's task fails or times out, retry that row alone — do not "merge" papers to retry.
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