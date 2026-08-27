# Literature Review Paper Screener — V1 Documentation Set

| | |
|---|---|
| **Product** | Literature Review Paper Screener |
| **Version** | V1 |
| **Documentation language** | English |
| **Scope** | Literature Review only (V1) |
| **Initial disciplinary focus** | Medical Science (designed for expansion to other disciplines) |

This document set is the single source of truth for implementing the V1 Literature Review Paper Screener. It converts the product specification into implementation-ready rules. Every product rule stated in the specification is preserved here. Where a rule was not fully specified, the ambiguity is recorded explicitly as an *Implementation consideration* rather than silently inventing new behavior (see `14-implementation-considerations.md`).

> **Evidence Package amendment (V1):** the architecture now carries a **Literature Evidence Package** per candidate with an **Evidence Availability Level (A–D)**. The Local Agent gathers the evidence; the Cloud evaluates and organizes it, bounded strictly by what it received. See `04` STEP 7.5, `05`, `06` STEP 0A, and the change log in `14` §14.4.

---

## 1. Architecture at a glance

The product has two strictly separated functions:

| Function | Environment | Internet access | Role |
|---|---|---|---|
| **Local Agent** | Runs on the user's local agent runtime | ✅ Yes — unrestricted | Free function; **Evidence Gathering** — all internet research + evidence collection |
| **Cloud** | Runs in the batch cloud execution environment | ❌ No — no internet | Paid function; **Evidence Evaluation + Reasoning + Organization** — screening and generation |

> **Mandatory Data Transfer Rule (applies to every run)**
> Before any cloud processing begins, the local (internet-enabled) agent must complete all required searching and collect all information needed by the cloud.
> The cloud operates **only** on the data provided by the local agent — the **Structured Local-to-Cloud Handoff Dataset** (a set of **Literature Evidence Packages**).
> The cloud must never search the internet, fetch additional papers, open URLs to retrieve missing information, or depend on external databases. Missing information is handled by the **available-data rules** defined in `13-edge-cases-and-missing-information.md` and the **Evidence Availability Levels** defined in `05`.
>
> **Final architecture principle: Local Agent gathers the evidence. Cloud evaluates and organizes the evidence.** (`11` §11.7)

---

## 2. Documentation map

| # | Document | Purpose |
|---|---|---|
| — | `README.md` | This index: architecture summary, document map, glossary, reading order |
| 01 | `01-product-scope.md` | V1 scope: task types, users, discipline focus, non-goals, guidance-vs-limit principles |
| 02 | `02-user-input.md` | Conversational user input flow (Q1–Q7), required vs optional, missing-information rules |
| 03 | `03-deadline-recommendation.md` | Deadline recommendation rule and recommended initial reading counts |
| 04 | `04-local-search-workflow.md` | Local search workflow STEP 0–7 + **STEP 7.5 build Literature Evidence Package** (search → unique candidate pool → evidence packages) |
| 05 | `05-local-data-collection-and-handoff.md` | **Literature Evidence Package**, **Evidence Availability Levels A–D**, and the structured handoff dataset |
| 06 | `06-cloud-screening-workflow.md` | Cloud screening pipeline: preparation, **STEP 0A evidence availability**, relevance, quality filters (level-aware content credibility), recency, priority, **Evidence Boundary for Notes/Summary** |
| 07 | `07-priority-classification.md` | Final priority classification rules, the full classification table, and priority across evidence levels |
| 08 | `08-reading-role-classification.md` | Reading role definitions, the one-primary-role rule, and role across evidence levels |
| 09 | `09-paper-sheet-output.md` | Paper Sheet output: inclusion rule, link requirement, implementation-ready schema |
| 10 | `10-reading-list-output.md` | Reading List output: same-pool rule, categories, required columns, citation handling |
| 11 | `11-local-vs-cloud-responsibilities.md` | Full responsibility matrix between Local Agent and Cloud |
| 12 | `12-end-to-end-workflow.md` | Complete end-to-end workflow with artifacts and gates |
| 13 | `13-edge-cases-and-missing-information.md` | Edge cases and the available-data rules for missing information |
| 14 | `14-implementation-considerations.md` | Consolidated list of flagged ambiguities and proposed (unconfirmed) defaults |

### Reading order

1. `01-product-scope.md` — what V1 is and is not
2. `02-user-input.md` + `03-deadline-recommendation.md` — what comes in
3. `04-local-search-workflow.md` + `05-local-data-collection-and-handoff.md` — what the Local Agent does
4. `06-cloud-screening-workflow.md` + `07-priority-classification.md` + `08-reading-role-classification.md` — what the Cloud does
5. `09-paper-sheet-output.md` + `10-reading-list-output.md` — what comes out
6. `11-local-vs-cloud-responsibilities.md` + `12-end-to-end-workflow.md` — how it all fits
7. `13-edge-cases-and-missing-information.md` + `14-implementation-considerations.md` — what to do when things are incomplete

---

## 3. Terminology (glossary)

| Term | Definition |
|---|---|
| **Research Question / Topic** | The essential required user input (research question, essay question, or research topic). |
| **Required Citation Count** | Optional user input: number of papers the user needs for citation. Recommendation/guidance only — never a search or screening limit. |
| **Assignment Requirements** | Optional user input: brief, rubric, lecturer requirements, word count, population, demographic, country/region, research scope, or other constraints. |
| **Research Restrictions** | Optional user input: population, country/region, time period, source type, publication years, or other literature restrictions. |
| **Deadline** | Optional user input. Drives reading recommendations only. Never limits search coverage. |
| **Available Reading Time** | Optional user input. Informs reading recommendations and the recommended initial reading count. Never a hard search limit. |
| **Search Profile** | Structured interpretation of all available user input that drives the search (see `04`, STEP 0). |
| **Master Candidate Pool** | All results from all search queries, before deduplication. |
| **Unique Candidate Pool** | The Master Candidate Pool after local deduplication; the input to cloud screening. |
| **Screened Literature Pool** | All papers retained after cloud screening (Topic Relevance ≥ 1, Quality = Pass, Recency = Current or Still Useful). |
| **Topic Relevance** | Per-paper score 0–3 (0 = Exclude, 1 = Supplementary, 2 = Include, 3 = Priority). A broad inclusion filter, not a strict match test. |
| **Quality** | A **pass/fail gate** composed of Source Validity, Basic Credibility, and Content Credibility. Never converted into a numerical score. |
| **Recency Status** | Current / Older but still useful / Clearly outdated or replaced. Primarily a ranking and priority-adjustment factor. |
| **Priority** | Final reading importance: Priority 1 — Must Read; Priority 2 — Recommended; Priority 3 — Supplementary. |
| **Primary Reading Role** | The single role a paper plays in the Literature Review: Foundational, Core Evidence, Supporting, Counterargument, Recent, or Methodology. |
| **Structured Local-to-Cloud Handoff Dataset** | The complete structured candidate dataset the Local Agent prepares for the Cloud — a set of **Literature Evidence Packages** with levels. The Cloud's only allowed input. |
| **Literature Evidence Package** | The per-paper structured package built by the Local Agent: Bibliographic Metadata (A) + Abstract (B) + Available Content (C) (`05` §5.2). |
| **Evidence Availability Level** | Per-paper classification A (Full Evidence) / B (Extended Evidence) / C (Abstract Evidence) / D (Metadata Only) — determines how deeply the Cloud may assess, never the paper's quality or fate (`05` §5.3). |
| **Assessment Limitations** | Per-paper record of what the Cloud could not assess given the Evidence Availability Level (`06` STEP 0A). |
| **Evidence Boundary** | Rules governing how deep Notes / Summary / Key Findings / Limitations may go at each Evidence Availability Level (`06`). |
| **Paper Sheet** | Cloud output 1: the complete Screened Literature Pool (Excel / Google Sheet). |
| **Reading List** | Cloud output 2: the same Screened Literature Pool organized by Priority and Primary Reading Role (Excel / Google Sheet). |
| **Available-data rules** | Rules the Cloud follows when information is missing: work with what exists, never fetch more (see `13`). |
| **Initial reading count** | The recommended number of papers to read first, derived from the Deadline rule (see `03`). Not a limit. |
| **Evidence Availability ≠ Quality** | Core rule: limited access never means low quality; the level only sets how confidently/deeply the system can assess (`05` §5.4). |

---

## 4. Version and change control

- This documentation describes **V1 only**.
- V2 features — such as a detailed Reading Plan — must **not** be added to V1 and are out of scope (see `01-product-scope.md`).
- Product rules in this set must not be changed during implementation except to resolve a contradiction; any such resolution must be recorded at the point of change (see `14-implementation-considerations.md` for the change log).
- **Evidence Package amendment:** one architectural amendment was applied to close the gap created by the Cloud having no internet access — the Literature Evidence Package data layer and Evidence Availability Levels A–D were added and integrated into the existing workflow. The original product rules (search/screen/classify/output logic, guidance-vs-limit principles) were preserved. Every change is labeled **[NEW]** / **[MODIFIED]** / **[UNCHANGED]** in the affected documents.