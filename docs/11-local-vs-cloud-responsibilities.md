# 11. Local vs Cloud Responsibilities

> **[MODIFIED]** Updated for the Evidence Package architecture: Local Agent = **Evidence Gathering**; Cloud = **Evidence Evaluation + Reasoning + Organization**.

## 11.1 Architecture

```text
USER
  │  (conversational input: topic required; citation count, assignment
  │   requirements, restrictions, deadline, reading time optional)
  ▼
LOCAL AGENT (internet access — FREE function)
  │  search, access sources/databases, collect metadata/abstracts/content,
  │  collect full text / sections where possible, verify publication info,
  │  deduplicate — all research operations
  ▼
LOCAL AGENT — BUILD LITERATURE EVIDENCE PACKAGES + ASSIGN EVIDENCE AVAILABILITY LEVELS (STEP 7.5)
  ▼
STRUCTURED LOCAL-TO-CLOUD HANDOFF DATASET
  │  (Literature Evidence Packages with levels — the only input the Cloud ever receives)
  ▼
CLOUD (NO internet access — PAID function)
  │  validate evidence availability, record assessment limitations,
  │  screening, evaluation, classification, structured output generation
  ▼
OUTPUTS: Paper Sheet + Reading List  (Excel / Google Sheet)
```

## 11.2 Responsibility matrix

| # | Operation | Owner | Notes |
|---|---|---|---|
| 1 | Conversational input collection (Q1–Q7) | Local Agent | See `02` |
| 2 | Clarification question (topic unclear) | Local Agent | One question; never permanently blocks |
| 3 | Build Search Profile | Local Agent | From available user input; never invent restrictions |
| 4 | Decompose Research Question | Local Agent | Core concepts, focus, population, context |
| 5 | Build Keyword Map | Local Agent | Synonyms, alternative terminology, academic terms |
| 6 | Generate multiple search queries | Local Agent | Direct / relationship / terminology / population-context |
| 7 | Multi-query search (maximise recall) | Local Agent | All potentially relevant results → Master Candidate Pool |
| 8 | Search coverage check & expansion | Local Agent | Stop rule: duplicates / covered / low-relevance only |
| 9 | Build Master Candidate Pool | Local Agent | Union of all query results |
| 10 | Deduplicate → Unique Candidate Pool | Local Agent | DOI / accession / title-based |
| 11 | Collect all available metadata, abstract, and content (incl. full text / sections where possible) | Local Agent | Per-paper fields in `05` §5.2 |
| 12 | Verify publication information | Local Agent | Where feasible, without fabricating |
| 13 | **Build Literature Evidence Packages + assign Evidence Availability Levels A–D (STEP 7.5)** | Local Agent | `04` STEP 7.5; `05` §§5.2–5.3 |
| 14 | Assemble Structured Local-to-Cloud Handoff Dataset | Local Agent | Run context + Evidence Packages + levels + availability flags + links |
| 15 | Prepare literature records | Cloud | No removal at this stage |
| 16 | **Assess / re-validate Evidence Availability (STEP 0A)** | Cloud | Correct the level if the evidence contradicts it; record limitations; pass downstream |
| 17 | Topic Relevance (score 0–3) | Cloud | 0 → Exclude; 1/2/3 → continue; broad inclusion filter; depth by level, score never changed by level |
| 18 | Source Validity filter | Cloud | Bibliographic evidence only; pass examples in `06`; fail → Exclude |
| 19 | Basic Credibility filter | Cloud | Only evidence actually provided; never assume or invent; fail → Exclude |
| 20 | Content Credibility filter (level-aware) | Cloud | Full (A) / Limited (B) / Insufficient Evidence (C) / Not Available (D); Fail only on material credibility problem |
| 21 | Recency assessment | Cloud | Current / Older but useful / Clearly outdated or replaced |
| 22 | Build Screened Literature Pool | Cloud | TR ≥ 1, Quality = Pass, Recency = Current/Still useful |
| 23 | Final Priority classification | Cloud | Relevance first; recency adjusts downward only when material; quality = gate; level never adjusts priority |
| 24 | Primary Reading Role classification | Cloud | One role per paper (6 roles); preliminary at low levels |
| 25 | Generate Paper Sheet | Cloud | Complete pool; links passed through, never fetched; evidence fields included |
| 26 | Generate Reading List | Cloud | Same pool; organized by priority + role; Notes/Summary follow Evidence Boundary |
| 27 | Reading recommendations (initial reading count, read-first sets) | Cloud | Computed from handoff user inputs (deadline, reading time, citation count); guidance only |
| 28 | Any re-search / re-fetch due to missing info | **Forbidden in Cloud** | Only the Local Agent can search; Cloud applies available-data rules and level rules |

## 11.3 Prohibited Cloud operations (normative)

The Cloud must **never**:

- Search the internet
- Fetch additional papers
- Open URLs to retrieve missing information
- Depend on external databases
- Assume that missing information can be retrieved later
- Refuse to process because fields are missing (available-data rules apply)
- Assume access to the original paper
- Claim to have reviewed information not included in the Literature Evidence Package
- Invent missing evidence (make up findings, methodology, or quality judgments) — **(NEW)**

## 11.4 Handoff contract requirements

For every run, before the Cloud starts:

1. The Local Agent has completed all required searching.
2. The handoff dataset contains the run context (topic, decomposed elements, all provided optional inputs) and one Literature Evidence Package per unique candidate.
3. Every package carries: all collectible fields (`05` §5.2), its **Evidence Availability Level**, Available Evidence, Missing Evidence, Assessment Limitations, and explicit availability flags.
4. Links required for the Paper Sheet have been collected locally.
5. The packages contain everything needed for Cloud-side evaluation of source validity, basic credibility, content credibility (per level), recency, and topic relevance.

## 11.5 Free vs paid boundary

| Function | What the user pays for |
|---|---|
| **Local Agent (free)** | Research + evidence gathering: search, source access, collection (metadata/abstract/content/full text where possible), verification, deduplication, package building, level assignment, handoff preparation |
| **Cloud (paid)** | Evidence evaluation + reasoning + organization: availability validation, screening, evaluation, classification, recommendation logic, and both structured outputs |

The boundary is also a **data dependency**: the Cloud's output quality depends entirely on the completeness of the local evidence packages; the product compensates for incompleteness via the Evidence Availability Levels and the available-data rules (`13`) rather than by Cloud-side fetching.

## 11.6 Recommendation inputs inside the Cloud

Deadline, Available Reading Time, and Required Citation Count are passed into the handoff's run-context block so the Cloud can compute reading recommendations offline:

- Deadline → initial reading count (`03`)
- Available Reading Time → pacing / refinement of the recommendation
- Required Citation Count → output guidance (e.g., coverage indication in the Reading List)

None of these values is permitted to constrain the Screened Literature Pool or the delivered outputs (`01` §1.7, `10` §10.7).

## 11.7 Final architecture principle (normative)

> **[NEW]**

```text
LOCAL AGENT = EVIDENCE GATHERING
CLOUD      = EVIDENCE EVALUATION + REASONING + ORGANIZATION
```

> **Local Agent gathers the evidence. Cloud evaluates and organizes the evidence.**
>
> The Cloud does not independently "judge" paper content it has not received. Because the Cloud has no internet access, it can only reason over what the Local Agent delivered — therefore the Local Agent must gather, and the Cloud must explicitly bound its judgments by the Evidence Availability Level (`05` §5.3, `06`).