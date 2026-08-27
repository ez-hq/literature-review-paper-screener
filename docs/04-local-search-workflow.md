# 4. Local Search Workflow (Local Agent — free function)

> **[MODIFIED]** The Local Agent is the **Internet Research Layer**. It gathers evidence; the Cloud evaluates it. A new handoff step (STEP 7.5 — Build Literature Evidence Package) builds the structured evidence package sent to the Cloud.

## 4.0 Scope of this document

This document defines the **Local Agent's** search workflow. The Local Agent:

- Has **internet access**.
- Performs **all** internet-dependent research operations:
  - Searching for literature
  - Accessing online academic sources and databases
  - Collecting literature metadata
  - Collecting available abstracts and content
  - Collecting available full text, paper sections, and structured methods/findings/conclusions where accessible
  - Verifying publication information
  - Deduplicating literature
  - Gathering all information required for later cloud processing
  - Building the **Literature Evidence Package** and assigning **Evidence Availability Levels** (STEP 7.5)

The Cloud must never repeat, outsource, or depend on any of this. Every step below runs **before** the handoff (`05-local-data-collection-and-handoff.md`).

---

## STEP 0 — Build Search Profile

Convert available user input into a structured Search Profile:

| Search Profile field | Source |
|---|---|
| Research Question | User's topic (Q2) |
| Core Concepts | Decomposed from the topic (STEP 1) |
| Population | Research restrictions / assignment requirements / clearly implied by the topic |
| Context | Restriction inputs and topic |
| Geographic Scope | Research restrictions / assignment requirements |
| Time Restrictions | Research restrictions |
| Source Type Restrictions | Research restrictions |
| Publication Year Preferences | Research restrictions |
| Assignment Requirements | Assignment requirements input |

### Rules

- **User-provided restrictions must be followed.**
- **Do not invent restrictions the user did not provide.**
- A restriction that was never stated (e.g., a country, population, or year range) must not silently enter the Search Profile.
- Where the topic itself clearly implies population/context (see STEP 1), that explicit interpretation is allowed and must be recorded as derived from the topic.

---

## STEP 1 — Decompose the Research Question

Identify and record:

| Element | Definition | Trigger |
|---|---|---|
| **Core Concepts** | The main concepts being studied | Always |
| **Relationship / Research Focus** | e.g., Effect, Impact, Association, Relationship, Comparison, Mechanism | Always (where present) |
| **Population** | The population under study | Only if explicitly specified **or** clearly implied by the research question |
| **Context** | e.g., Country, Region, Industry, Education, Healthcare, Social context | When identifiable |

Rules:

- Population is included only when explicit or clearly implied; otherwise it stays empty and is not invented (STEP 0 rule).
- Context is recorded when identifiable from the topic or user input; otherwise empty.

---

## STEP 2 — Build Keyword Map

For **each Core Concept**, identify:

- Primary Keywords
- Synonyms
- Alternative Terminology
- Related Academic Terms

For the **research focus** (relationship/outcome/mechanism), identify relevant:

- Relationship Terms
- Outcome Terms
- Mechanism Terms

### Rule

> Do not rely on a single keyword or a single search query.

The Keyword Map is the basis for generating multiple, distinct search approaches (STEP 3).

---

## STEP 3 — Generate Multiple Search Queries

Generate several relevant search approaches:

| Approach | Formula |
|---|---|
| **Direct search** | Core Concept + Core Concept + Population / Context |
| **Relationship search** | Core Concept + Effect / Impact / Association + Outcome |
| **Terminology expansion** | Synonyms, alternative terminology, related academic terminology (from the Keyword Map) |
| **Population / Context search** | Add population restrictions, geographic restrictions, or contextual restrictions when relevant |

Each approach should yield one or more concrete queries. Queries must differ meaningfully (different keyword combinations), not be cosmetic variants.

---

## STEP 4 — Multi-Query Search

- Run **multiple** relevant search queries.
- All potentially relevant results enter the **Master Candidate Pool**.

### Search Rule

> Do not apply strict quality or final relevance screening during search.
> The search stage is designed to **maximise recall**.
> If a paper has reasonable potential relevance, include it in the Candidate Pool.

Screening (relevance, quality, recency) is exclusively a Cloud activity (`06`).

---

## STEP 5 — Search Coverage Check

Check whether search coverage includes:

- **All Core Concepts**
- **Important Synonyms**
- **Alternative Terminology**
- **Relevant Population**
- **Relevant Context**
- **Major Related Concepts**

Also check whether coverage includes:

- **Direct evidence**
- **Alternative perspectives**
- **Foundational research**
- **Recent research**

### Behaviors

- If important areas are missing → **generate additional queries and search again.**
- If coverage is sufficient → **stop expanding the search.**

### Stop Rule

> Stop expanding search when new searches mainly produce:
> - Duplicate papers
> - Already-covered literature
> - Clearly low-relevance results

---

## STEP 6 — Build Master Candidate Pool

- Combine all search results into the **Master Candidate Pool**.
- This pool is the union of every query's potentially relevant results (before deduplication).

---

## STEP 7 — Deduplicate

- Remove:
  - Duplicate records
  - Duplicate database entries
  - Multiple records representing the same paper
- Output: **UNIQUE CANDIDATE POOL**

### Deduplication keys (implementation detail)

Deduplication should prefer the strongest identifier available, then fall back to weaker signals:

1. DOI (same DOI → same paper)
2. Database accession (e.g., PMID in PubMed) where recorded
3. Exact title match (normalized: case, whitespace, punctuation)
4. Strong fuzzy title match (same title with minor differences, e.g., subtitle variants) combined with first-author family name and publication year

When two records clearly represent the same paper, keep the **richest record** (most metadata/content) and mark the source databases in the surviving record.

---

## STEP 7.5 — Build Literature Evidence Package

> **[NEW — formal Local → Cloud Handoff Module]**

This step sits **between** the Local Search Workflow (this document) and the Cloud Screening Workflow (`06`). It converts the Unique Candidate Pool into the **Structured Local-to-Cloud Handoff Dataset** (`05`).

Workflow:

```
Local Agent identifies a paper
        ↓
Collect available bibliographic information
        ↓
Collect abstract
        ↓
Collect full text or available sections where possible
        ↓
Collect structured methods / findings / conclusions where available
        ↓
Record unavailable or missing evidence
        ↓
Assign Evidence Availability Level A / B / C / D
        ↓
Build Structured Literature Evidence Package
        ↓
Send to Cloud
```

### Rules

- Every paper in the Unique Candidate Pool receives a **Literature Evidence Package** (`05` §5.2).
- For every paper, the Local Agent assigns **one Evidence Availability Level: A / B / C / D** (`05` §5.3).
- Collect as much reliable evidence as available, but **do not fabricate missing evidence** and **do not require full-text access for every paper** (paywalls, no open access, access restrictions, and PDF retrieval failures are expected; they change the Evidence Availability Level, never the paper's fate).
- Output of STEP 7.5: the **Structured Local-to-Cloud Handoff Dataset**, where each paper record is a complete Literature Evidence Package carrying its level, available/missing evidence, assessment limitations, and links.

---

## Local Agent responsibility summary

| Responsibility | Owner |
|---|---|
| All searching and database access | Local Agent only |
| Query generation and coverage validation | Local Agent only |
| Candidate pooling and deduplication | Local Agent only |
| Evidence collection (metadata, abstract, full text / sections where possible) | Local Agent only |
| Building Literature Evidence Packages + assigning Evidence Availability Levels (STEP 7.5) | Local Agent only |
| Any later re-search due to an empty/missing result | Local Agent only (Cloud cannot search) |

## Implementation considerations

1. **Sources and databases.** Not enumerated by product spec; for the Medical Science focus the local agent should use recognized scholarly sources (e.g., PubMed/MEDLINE, Scopus, Web of Science, institutional library databases, publisher sites, Google Scholar). The list is configurable and should not be hard-coded into the Cloud pipeline.
2. **Search depth / number of queries.** No cap is specified; the coverage check (STEP 5) is the termination condition. "Reasonable potential relevance" is defined as: the record plausibly touches one or more Core Concepts and/or the research focus.
3. **Failed queries / transient failures.** Search infrastructure errors should be retried locally before concluding coverage; final behavior on persistent failure is a local operational decision and must not result in the Cloud being asked to search.
4. **No hard pool caps.** Candidate Pool size is not limited by Citation Count, Deadline, or Reading Time (<u>spec rule</u>). Performance handling of very large pools is an implementation concern (see `14`).
5. **Full-text effort.** Attempt full text and structured sections where legal and practical (open access, institutional access, preprint versions); do not bypass paywalls; failed retrieval simply lowers the Evidence Availability Level (see `05` §5.9, item 5). **(NEW)**