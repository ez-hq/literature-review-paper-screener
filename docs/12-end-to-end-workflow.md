# 12. End-to-End Workflow

## 12.1 The complete workflow

```text
USER INPUT
        │
        ▼
LOCAL AGENT — BUILD SEARCH PROFILE
        │
        ▼
LOCAL AGENT — DECOMPOSE RESEARCH QUESTION
        │
        ▼
LOCAL AGENT — BUILD KEYWORD MAP
        │
        ▼
LOCAL AGENT — GENERATE MULTIPLE SEARCH QUERIES
        │
        ▼
LOCAL AGENT — MULTI-QUERY SEARCH
        │
        ▼
LOCAL AGENT — SEARCH COVERAGE CHECK
        │
        ▼
LOCAL AGENT — EXPAND SEARCH IF REQUIRED
        │
        ▼
LOCAL AGENT — BUILD MASTER CANDIDATE POOL
        │
        ▼
LOCAL AGENT — DEDUPLICATE
        │
        ▼
UNIQUE CANDIDATE POOL
        │
        ▼
LOCAL AGENT — COLLECT ALL AVAILABLE EVIDENCE (METADATA / ABSTRACT / FULL TEXT OR SECTIONS / STRUCTURED INFO)
        │
        ▼
LOCAL AGENT — STEP 7.5 BUILD LITERATURE EVIDENCE PACKAGE + ASSIGN EVIDENCE AVAILABILITY LEVEL A/B/C/D
        │
        ▼
STRUCTURED LOCAL-TO-CLOUD HANDOFF DATASET (EVIDENCE PACKAGES)
        │
        ▼
CLOUD — PREPARE LITERATURE RECORDS
        │
        ▼
CLOUD — STEP 0A ASSESS EVIDENCE AVAILABILITY (REVALIDATE LEVEL, RECORD LIMITATIONS)
        │
        ▼
CLOUD — TOPIC RELEVANCE
        │
        0 → EXCLUDE
        1 / 2 / 3 → CONTINUE
        │
        ▼
CLOUD — SOURCE VALIDITY
        │
        FAIL → EXCLUDE
        PASS → CONTINUE
        │
        ▼
CLOUD — BASIC CREDIBILITY
        │
        FAIL → EXCLUDE
        PASS → CONTINUE
        │
        ▼
CLOUD — CONTENT CREDIBILITY (LEVEL-AWARE: FULL / LIMITED / INSUFFICIENT / NOT AVAILABLE)
        │
        MATERIAL CREDIBILITY PROBLEM → EXCLUDE
        NO PROBLEM / INSUFFICIENT INFO → CONTINUE ACCORDING TO AVAILABLE-DATA RULES
        │
        ▼
CLOUD — RECENCY ASSESSMENT
        │
        CURRENT → NO ADJUSTMENT
        OLDER BUT STILL USEFUL → LOWER PRIORITY
        OUTDATED / REPLACED → EXCLUDE
        │
        ▼
SCREENED LITERATURE POOL (each paper carries its Evidence Availability Level + limitations)
        │
        ▼
CLOUD — FINAL PRIORITY CLASSIFICATION
        │
        ▼
CLOUD — PRIMARY READING ROLE CLASSIFICATION
        │
        ▼
CLOUD — GENERATE PAPER SHEET (evidence-bound Notes/Summary)
        │
        ▼
CLOUD — GENERATE READING LIST (evidence-bound Notes/Summary)
```

## 12.2 Annotated walkthrough

| # | Stage | Owner | Artifact / decision | Ref |
|---|---|---|---|---|
| 1 | User input (conversational, Q1–Q7) | Local Agent + user | Topic (required); optional inputs | `02` |
| 2 | Build Search Profile | Local Agent | Search Profile | `04` STEP 0 |
| 3 | Decompose Research Question | Local Agent | Core Concepts, Focus, Population, Context | `04` STEP 1 |
| 4 | Build Keyword Map | Local Agent | Keyword Map | `04` STEP 2 |
| 5 | Generate multiple search queries | Local Agent | Query set (≥ several angles) | `04` STEP 3 |
| 6 | Multi-query search | Local Agent | Master Candidate Pool (recall-first) | `04` STEP 4 |
| 7 | Coverage check (+ expand if required) | Local Agent | Coverage verdict; extra queries when gaps exist | `04` STEP 5 |
| 8 | Build Master Candidate Pool | Local Agent | Master Candidate Pool | `04` STEP 6 |
| 9 | Deduplicate | Local Agent | **Unique Candidate Pool** | `04` STEP 7 |
| 10 | Collect all available evidence (metadata, abstract, full text / sections / structured info) | Local Agent | Evidence per paper | `05` §5.2 |
| 11 | **Build Literature Evidence Package + assign Evidence Availability Level (STEP 7.5)** | Local Agent | **Literature Evidence Packages with levels A–D** | `04` STEP 7.5, `05` §5.3 |
| 12 | Assemble handoff | Local Agent | **Structured Local-to-Cloud Handoff Dataset** | `05` §5.5 |
| 13 | Prepare literature records | Cloud | Structured records (no removal) | `06` STEP 0 |
| 14 | **Assess / re-validate Evidence Availability (STEP 0A)** | Cloud | **Level + Available/Missing Evidence + Assessment Limitations passed downstream** | `06` STEP 0A |
| 15 | Topic Relevance | Cloud | Score 0–3; 0 → Exclude; ≥1 → continue; depth by level, score never changed by level | `06` STEP 1 |
| 16 | Quality Filters (2A→2B→2C) | Cloud | Pass/fail per filter (content credibility is level-aware); fail → Exclude | `06` STEP 2 |
| 17 | Recency assessment | Cloud | Current / Older but useful / Outdated → exclude | `06` STEP 3 |
| 18 | Build Screened Literature Pool | Cloud | **Screened Literature Pool** | `06` STEP 4 |
| 19 | Final Priority classification | Cloud | Priority 1 / 2 / 3 per paper | `07` |
| 20 | Primary Reading Role classification | Cloud | One role per paper | `08` |
| 21 | Generate Paper Sheet | Cloud | Output 1 (complete pool, evidence-bound) | `09` |
| 22 | Generate Reading List | Cloud | Output 2 (same pool, organized, evidence-bound) | `10` |
| 23 | Reading recommendations | Cloud | Initial reading count + read-first guidance (guidance only) | `03`, `10` |

## 12.3 Artifacts summary

| Artifact | Owner | Produced at |
|---|---|---|
| Search Profile | Local | STEP 0 |
| Keyword Map | Local | STEP 2 |
| Master Candidate Pool | Local | STEP 6 |
| Unique Candidate Pool | Local | STEP 7 |
| **Literature Evidence Package (per paper, with Evidence Availability Level)** | **Local** | **STEP 7.5** |
| Structured Local-to-Cloud Handoff Dataset | Local | §5.5 |
| **Evidence Availability Level + Assessment Limitations (per paper)** | **Cloud (re-validated)** | **STEP 0A** |
| Screened Literature Pool | Cloud | STEP 4 |
| Paper Sheet | Cloud | output |
| Reading List | Cloud | output |

## 12.4 Invariants enforced by the architecture

1. No internet-dependent operation ever executes in the Cloud (single handoff boundary).
2. Search and screening are fully decoupled: search maximises recall; screening narrows to the Screened Literature Pool.
3. The Screened Literature Pool is the single source for **both** outputs.
4. Guidance inputs (deadline, reading time, citation count) affect recommendations only — never pool membership.
5. All qualified literature remains available in the final outputs.
6. **Local Agent gathers the evidence; Cloud evaluates and organizes it.** The Cloud reasons only over the Literature Evidence Packages received, bounded by their Evidence Availability Levels. **(NEW)**
7. **Evidence Availability ≠ Quality**: the level never changes Topic Relevance, Priority, Reading Role, or pool membership — it only sets assessment depth and flags limitations. **(NEW)**