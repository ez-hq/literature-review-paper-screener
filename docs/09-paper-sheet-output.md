# 9. Paper Sheet Output (Cloud)

> **[MODIFIED]** The Paper Sheet now exposes the **Evidence Availability Level**, **Available Evidence**, **Missing Evidence**, and **Assessment Limitations** for every included paper, and its Notes/Summary columns respect the **Evidence Boundary** (`06`).

## 9.1 Definition

The Paper Sheet contains **the complete Screened Literature Pool**.

- It must **not** contain excluded literature.
- It is the "complete qualified literature set" view: everything the user needs to review all retained literature and understand why each paper is relevant.
- Evidence-limited papers (Levels B/C/D) are included with their limitations visible — evidence availability is not an exclusion criterion (`05` §5.4, `06` Excluded Literature).

## 9.2 Paper Sheet inclusion rule

Include a paper **if and only if** all of the following hold:

1. Topic Relevance ≥ 1
2. Not excluded because of a major credibility problem
3. Passes Source Validity
4. Passes Basic Credibility
5. Passes Content Credibility — where "passes" is governed by the **Content Credibility Decision Rule** (`06`): Fail only on a **material credibility problem**; Limited Assessment (Level B), Insufficient Evidence for Full Assessment (Level C), and Content Assessment Not Available (Level D) are **retained**, not excluded
6. Not Clearly Outdated / Replaced

(These conditions define membership of the Screened Literature Pool — `06`, STEP 4.)

> **[NEW]** Evidence Availability Level does not itself affect inclusion: a Level C or Level D paper that meets the six conditions is included, with its evidence limitations explicitly recorded in the sheet.

## 9.3 Link requirement

- Every included paper must have a **link where available**.
- The **Local Agent** collects the required links **before** cloud processing (`05`).
- The **Cloud must not** attempt to retrieve links from the internet.
- Where no link exists, the record is included with `Links = not available` (available-data rules, `13`).

## 9.4 Implementation-ready schema

All columns below are produced from the **Screened Literature Pool** using only the handoff data — the Cloud retrieves nothing additional. Column provenance is marked:

- **[L]** = collected locally, passed through
- **[C]** = computed by the Cloud
- **[U]** = user-facing presentation / formatting

| # | Column | Source | Description |
|---|---|---|---|
| 1 | Record ID | [C] | Internal unique identifier for the paper in this run (e.g., `P001`) |
| 2 | Priority | [C] | Priority 1 — Must Read / Priority 2 — Recommended / Priority 3 — Supplementary |
| 3 | Primary Reading Role | [C] | Foundational / Core Evidence / Supporting / Counterargument / Recent / Methodology |
| 4 | Citation | [U] | Formatted citation in the configured citation style (see `10` §10.5 for the style rule) |
| 5 | Title | [L] | Full title of the paper |
| 6 | Author(s) | [L] | All authors where available |
| 7 | Publication Year | [L] | Year of publication |
| 8 | Source / Journal / Publisher | [L] | Publishing venue |
| 9 | Source Type | [L] | e.g., Peer-reviewed journal article, academic book, book chapter, conference paper, institutional publication, government publication, other |
| 10 | DOI | [L] | DOI where available |
| 11 | ISBN | [L] | ISBN where available (chiefly books/book chapters) |
| 12 | Database Record | [L] | Identifier and origin of the database record (e.g., PMID + database name) |
| 13 | URL | [L] | Stable source URL where available |
| 14 | Links | [L] | All collected stable links (paper link, DOI link, database record, publisher page) — the "link where available" requirement |
| 15 | Abstract / Available Content | [L] | Abstract or available content excerpt where collected (or "Not available") |
| 16 | **Evidence Availability Level** | [L/C] | **A — Full Evidence / B — Extended / C — Abstract / D — Metadata Only** (assigned locally, re-validated in Cloud STEP 0A) |
| 17 | **Available Evidence** | [L] | **Description of evidence actually present (e.g., "Full text", "Abstract + methods + key findings")** |
| 18 | **Missing Evidence** | [L] | **Description of evidence not present (e.g., "Full text unavailable", "No abstract")** |
| 19 | **Assessment Limitations** | [C] | **What the Cloud could not assess given the level (e.g., "Content credibility not assessed — metadata only")** |
| 20 | Topic Relevance | [C] | Score 1–3 and label (Supplementary / Include / Priority) |
| 21 | Source Validity | [C] | Pass (all papers in the sheet have passed; shown for transparency) |
| 22 | Basic Credibility | [C] | Pass |
| 23 | Content Credibility | [C] | Pass (niveau: Full Assessment / Limited Assessment), or Pass with limitation (Insufficient Evidence for Full Assessment), or Content Assessment Not Available — per the Content Credibility Decision Rule (`06`) |
| 24 | Recency Status | [C] | Current / Older but still useful |
| 25 | Summary | [C] | What the paper did; how it relates to the user's Research Question; how it can be useful in the student's Literature Review — **content governed by the Evidence Boundary** (`06`): depth follows the Evidence Availability Level |
| 26 | Notes | [C] | Detailed academic information: research method, study design, main argument, key findings, what the study demonstrates, important limitations where available — **content governed by the Evidence Boundary** (`06`) |
| 27 | Reading Guidance | [C] | Where derivable: "Included in recommended initial reading" marker when the paper falls within the Deadline-based initial reading count (`03`) — presentation aid, not a filter |

### Notes on the schema

- **[MODIFIED]** The schema now includes the **Evidence Availability Level** plus **Available Evidence / Missing Evidence / Assessment Limitations** (cols. 16–19), per the Literature Evidence Package (`05`) and STEP 0A (`06`). Content-related columns (Summary, Notes) respect the **Evidence Boundary** in `06`.
- **Why these columns:** the spec requires the sheet to (a) contain the complete qualified set, (b) let users review retained literature, and (c) explain why each paper is relevant. Columns 2–4, 20, and 25–26 cover (c); columns 5–15 cover reviewability; columns 16–19 make the evidence basis of every assessment transparent.
- **No excluded papers** appear in the sheet under any circumstances.
- **No internet retrieval** is performed by the Cloud to fill any column; missing values are rendered as `Not available` / `—` per the available-data rules (`13`).
- **Citation (col. 4) and Summary/Notes (cols. 25–26)** are produced **once per paper** and reused by the Reading List (`10`) so the two outputs never disagree.

## 9.5 Format and delivery

- Format: **Excel** or **Google Sheet** (V1 supports either; the choice is a delivery option).
- Suggested sheet conventions (implementation detail): one row per paper; frozen header row; filters enabled; sensible column order as above; the initial-reading marker (col. 27) styled distinctly; evidence-limited papers (Levels C/D) visually flagged (e.g., ▸ aside or colour) so the user immediately sees the assessment depth.

## 9.6 Cloud constraints (restated)

- The Cloud never retrieves links or any other data from the internet.
- The Cloud never re-screens from scratch using external data; it outputs only what is in the Screened Literature Pool.