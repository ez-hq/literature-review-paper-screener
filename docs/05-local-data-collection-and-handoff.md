# 5. Literature Evidence Package, Evidence Availability Levels, and Cloud Handoff

> **[MODIFIED]** This document is now the home of the **Literature Evidence Package** data layer (`05` §5.2), the **Evidence Availability Levels A–D** (`05` §5.3), and the **Evidence Availability ≠ Quality** rule (`05` §5.4). It keeps the existing handoff structures from V1.

## 5.1 Mandatory data transfer rule

> **[UNCHANGED]**

> Before any cloud processing begins, the local internet-enabled agent must complete all required searching and collect all information needed by the cloud.

- The Cloud operates **only** on data already provided by the Local Agent in the **Structured Local-to-Cloud Handoff Dataset**.
- The Cloud must **not**:
  - Search the internet
  - Fetch additional papers
  - Open URLs to retrieve missing information
  - Depend on external databases
  - Assume that missing information can be retrieved later
- If required information is missing, the Cloud follows the **available-data rules** in `13-edge-cases-and-missing-information.md` and the **Evidence Availability Level** rules in this document (§5.3).

---

## 5.2 Literature Evidence Package

> **[NEW]**

The Local Agent must **not** simply send basic paper information (title, authors, year, abstract, link). For **every candidate paper**, it builds a structured **Literature Evidence Package** with three parts.

### A. Bibliographic Metadata

Collect where available:

```text
Title
Authors
Publication Year
Journal / Publisher
Source Type
DOI
ISBN
Stable URL
Database Record / Search Source
```

This information is primarily used by the Cloud for:

```text
Source Validity
Basic Credibility
Recency
```

### B. Abstract

Collect:

```text
Abstract
```

This information supports:

```text
Topic Relevance
Research Focus
Population
Context
Preliminary Findings
```

### C. Available Content

The Local Agent collects as much reliable paper content as available.

**Preferred:**

```text
Full Text
```

If full text is unavailable, collect available sections such as:

```text
Introduction
Methods
Results
Discussion
Conclusion
```

Or structured information where available:

```text
Methods Information
Key Findings
Results Information
Conclusion Information
Structured Database Information
```

#### Important rule — no full-text requirement

> The Local Agent must collect all reasonably available evidence, but must **NOT require full-text access for every paper**.

Many papers may have:

```text
Paywalls
No Open Access
Access Restrictions
PDF Retrieval Failure
Unavailable Full Text
```

Therefore:

> **A paper must not be automatically excluded simply because the full text is unavailable.**

Instead, the Local Agent records what is available, what is missing, and assigns the Evidence Availability Level (§5.3). The Cloud then assesses within the boundary of that level (`06` STEP 2C).

---

## 5.3 Evidence Availability Level

> **[NEW]**

Before sending a paper to the Cloud, the Local Agent classifies the amount of evidence available. Each paper receives **one** Evidence Availability Level.

| Level | Name | Package contains |
|---|---|---|
| **A** | Full Evidence | Full text, or substantial full-paper content (Methods, Results, Discussion, Conclusion) |
| **B** | Extended Evidence | Abstract + substantial structured information (Methods Information, Key Findings, Results, Conclusions, detailed database record) |
| **C** | Abstract Evidence | Title + metadata + Abstract |
| **D** | Metadata Only | Title, Authors, Year, Journal / Publisher / Source |

### Cloud capabilities by level

| Level | The Cloud may perform |
|---|---|
| **A** | Detailed screening; method analysis; findings extraction; limitation identification; content credibility assessment; detailed Notes; detailed Summary |
| **B** | Topic Relevance; Source Validity; Basic Credibility; **limited** Content Credibility assessment; Priority classification; Reading Role classification |
| **C** | **Preliminary** Topic Relevance; Source Validity; Basic Credibility; **preliminary** Priority; **preliminary** Reading Role classification |
| **D** | Verify provided metadata consistency; assess very preliminary relevance; assess available source information |

### Cloud prohibitions by level

| Level | The Cloud must NOT |
|---|---|
| **A** | — (full assessment supported) |
| **B** | Claim to have reviewed the full paper. It must clearly recognize: *the full paper has not been reviewed.* |
| **C** | Make a strong Content Credibility judgment. It must record `Content Credibility: Insufficient Evidence for Full Assessment` and must **not** record `Fail` simply because the full paper is unavailable. |
| **D** | Invent findings; infer methodology; assess evidence quality; generate detailed Notes; generate detailed Summary; claim to have reviewed the paper. It must record `Content Assessment: Not Available`. |

### Per-paper level record

Every paper carried in the handoff must include:

```text
Evidence Availability Level   (A / B / C / D)
Available Evidence            (what evidence is actually available)
Missing Evidence              (what evidence is missing)
Assessment Limitations        (what the Cloud can and cannot assess at this level)
```

These four fields are attached to the paper in the handoff dataset (§5.6) and passed into all downstream screening stages (`06` STEP 0A).

---

## 5.4 Core system rule — Evidence Availability Does Not Equal Quality

> **[NEW]**

```text
Evidence Availability must NOT be used as a quality score.

Limited access to a paper does not mean the paper is low quality.

Evidence Availability only determines how confidently
and how deeply the system can assess the paper.
```

Consequences enforced across the workflow:

- A Level C or Level D paper is **not** penalized in Topic Relevance, Priority, or Reading Role because of its level.
- The level changes only the **depth and confidence** of the assessment, the wording of Notes/Summary (Evidence Boundary in `06`), and the flags shown to the user.
- Evidence Availability is never an exclusion criterion (`06` Excluded Literature; `09` §9.2).

---

## 5.5 Structured Local-to-Cloud Handoff Dataset

### Definition

> **[MODIFIED]**

The **Structured Local-to-Cloud Handoff Dataset** is the complete structured candidate dataset delivered by the Local Agent to the Cloud. It contains:

1. **Run context block (user inputs):** *(unchanged)*
   - Research Question / Topic
   - Decomposed elements (Core Concepts, Relationship / Research Focus, Population, Context)
   - Research restrictions (if any)
   - Assignment requirements (if any)
   - Required Citation Count (if provided)
   - Deadline (if provided)
   - Available Reading Time (if provided)
   > This block lets the Cloud compute reading recommendations (initial reading count, reading-first sets) without internet access. These values remain **guidance only** in the Cloud.

2. **Paper records block — one Literature Evidence Package per unique candidate:**
   - Bibliographic Metadata (§5.2A)
   - Abstract (§5.2B)
   - Available Content (§5.2C)
   - **Evidence Availability Level + Available/Missing Evidence + Assessment Limitations (§5.3)**
   - Availability flags per field (`present` / `not available`)
   - Collected stable **links** (paper link, DOI link, database record, publisher page) — §5.7
   - Notes the local agent can legitimately add (e.g., verification notes, database origin) that do not pre-judge screening outcomes

### Format

Serialization (JSON lines / CSV / typed table) is an implementation choice; it must (a) carry every field above, (b) represent "missing" explicitly (never as fabricated data), and (c) be machine-readable by the Cloud's screening step.

### Rules for the handoff

- **Completeness over perfection:** collect everything obtainable; the Cloud works with what exists.
- **No fabrication:** never invent titles, years, abstracts, or content.
- **Levels travel with packages:** the Evidence Availability Level is assigned locally and re-validated by the Cloud (`06` STEP 0A).
- **Links are collected here:** the Cloud never retrieves links.
- **No pre-screening:** the handoff contains the **Unique Candidate Pool** — the Cloud's screening pipeline decides relevance/quality/recency; the Local Agent must not drop papers at collection time (deduplication in STEP 7 of `04` is the only local selection operation allowed).

---

## 5.6 What the Cloud must never do (restated)

> **[MODIFIED — evidence architecture additions]**

- Search the internet
- Fetch additional papers
- Open URLs to retrieve missing information
- Depend on external databases
- Assume missing information will be retrievable later
- Refuse to process a run because some fields are missing (available-data rules apply instead)
- **Assume full-text access to the original paper. (NEW)**
- **Claim to have reviewed information that was not included in the Literature Evidence Package. (NEW)**
- **Infer methodology, findings, or quality from metadata alone (Level D). (NEW)**

---

## 5.7 Link collection requirement

> **[UNCHANGED]**

- Every paper included in the **Paper Sheet** must have a link **where available**.
- The Local Agent collects the required links **before** cloud processing.
- Acceptable links: paper URL, DOI link (resolvable URL form), database record link (e.g., PubMed record), publisher page, or other stable source link.
- If no link is available for a paper, the record passes through with `Links = not available`; the paper is not penalized on the basis of missing links when other verification signals exist (see `13`).

---

## 5.8 Availability-first principle

> **[UNCHANGED]**

The handoff encoding must distinguish three states for every field:

| State | Meaning |
|---|---|
| `present` | Collected value |
| `not available` | Genuinely could not be collected |
| `not applicable` | Field does not apply (e.g., ISBN for a journal article) |

This distinction is what allows the Cloud to apply the available-data rules and the Evidence Availability Levels predictably instead of guessing.

---

## 5.9 Implementation considerations

1. **Handoff size / batching.** No cap is specified. Very large candidates should be handed off in full; if transport batching is needed, it must be lossless and preserve the run-context block on every batch.
2. **Verification notes.** The Spec makes the Local Agent responsible for "verifying publication information". How much verification evidence is passed down is unspecified; a lightweight `verification_notes` field (e.g., DOI resolved, metadata cross-checked across two databases) is a proposed, non-binding addition to aid Cloud-side Basic Credibility judgment — to be confirmed.
3. **User-visible confirmation of handoff.** Whether the user is shown the candidate count before the paid Cloud run is a product-flow decision (aligns with paid-run confirmation gates); not specified by the product spec.
4. **Level boundary precision (NEW).** The boundary between Level B ("substantial structured information") and Level C ("abstract only") needs an explicit operational definition. Proposed (unconfirmed): Level B requires at least two of (Methods Information, Results Information, Key Findings, Conclusion Information) in addition to the abstract; anything less is Level C. See `14` item 21.
5. **Full-text effort expectations (NEW).** The Local Agent should make a reasonable effort to obtain full text (open-access versions, institutional access, preprint servers, database links) but must stop at paywalls rather than bypassing them; failed retrieval simply lowers the Evidence Availability Level. See `14` item 22.