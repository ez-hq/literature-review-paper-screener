# 6. Cloud Literature Screening Workflow (Cloud — paid function)

> **[MODIFIED]** Added **STEP 0A — Assess Evidence Availability**, level-aware Topic Relevance, level-aware Content Credibility (with the **Content Credibility Decision Rule**), and the **Evidence Boundary for Notes and Summary**. The V1 screening pipeline (Topic Relevance → Quality Filters → Recency → Priority) and its classification tables are preserved.

## 6.0 Scope of this document

The Cloud performs **all** paid screening and output processing. It has **no internet access** and operates **only** on the **Structured Local-to-Cloud Handoff Dataset** produced by the Local Agent (`05`). Each candidate arrives as a **Literature Evidence Package** with an **Evidence Availability Level** (`05` §5.2–5.3).

> The Cloud must not search, fetch, open URLs, or depend on external databases at any step of this workflow. Missing information is handled by the available-data rules (`13`) and bounded by the Evidence Availability Level (`05` §5.3).

**Input:** UNIQUE CANDIDATE POOL (as Literature Evidence Packages from the handoff dataset).

---

## STEP 0 — Prepare Literature Records

> **[UNCHANGED]**

For every paper, prepare a structured literature record containing all available:

- Title
- Author(s)
- Publication Year
- Source / Journal / Publisher
- Abstract / Available Content
- DOI / ISBN / URL / Database Record
- Source Type

### Rule

> Do not remove literature at this stage based on:
> - Relevance
> - Quality
> - Recency
> - Evidence Availability Level

STEP 0 is pure record preparation. No filtering happens here.

---

## STEP 0A — Assess Evidence Availability

> **[NEW]**

Immediately after STEP 0, for every candidate paper:

1. **Inspect all available evidence** in the package.
2. **Determine the Evidence Availability Level** (A / B / C / D) per `05` §5.3.
3. **Assign Level A / B / C / D.**
4. **Record what evidence is actually available** (Available Evidence).
5. **Record missing evidence** (Missing Evidence).
6. **Record assessment limitations** (Assessment Limitations).
7. **Pass the Evidence Package and Evidence Level into all downstream screening stages.**

Each paper therefore carries, throughout screening:

```text
Evidence Availability Level
Available Evidence
Missing Evidence
Assessment Limitations
```

Rules:

- The Cloud may **correct** a level if the packaged evidence clearly contradicts the locally assigned level (e.g., full text included but marked Level C); correction does not reject the record.
- The level never excludes a paper by itself (`05` §5.4).

---

## STEP 1 — Topic Relevance

> **[MODIFIED — evidence-aware]**

Evaluate **every paper independently**, using **Title + Abstract + Available Content**.

### Topic Relevance Score

| Score | Classification |
|---|---|
| 3 | Priority |
| 2 | Include |
| 1 | Supplementary |
| 0 | Exclude |

### Routing

| Score | Routing |
|---|---|
| 3 | Continue to Quality Filters |
| 2 | Continue to Quality Filters |
| 1 | Continue to Quality Filters |
| 0 | **Exclude** |

### Important rule — Topic Relevance is a broad inclusion filter

> **[UNCHANGED]**

Do **not** automatically exclude a paper because:

- Population is not perfectly identical
- Context is not perfectly identical
- Method differs
- Geography differs
- Variables are not perfectly identical

**Keep the paper** if it may provide meaningful value to:

- The Research Question
- Core Concepts
- Theory
- Relevant Variables
- Background
- Related Evidence

### Depth of assessment follows the Evidence Level (NEW)

- Higher Evidence Availability → more detailed relevance assessment.
- Lower Evidence Availability → more preliminary relevance assessment.
- **However, the Evidence Availability Level itself must NOT increase or decrease the Topic Relevance score.** A highly relevant paper with limited accessible content does not receive a lower relevance score merely because full text is unavailable (`05` §5.4).

### Scoring guidance (operational, consistent with the broad-inclusion rule)

| Score | Guidance (illustrative, not exhaustive) |
|---|---|
| 3 | Directly addresses the Research Question / all core concepts and the research focus with close alignment |
| 2 | Addresses most core concepts or the relationship of interest, with some differences (population, context, geography, variables, method); clearly meaningful to the question |
| 1 | Adjacent value: theory, background, related concepts, variables, context, or related evidence that informs the review |
| 0 | No meaningful connection to the Research Question, core concepts, theory, variables, background, or related evidence |

Score boundaries are judged from the **available record** (title, abstract, available content). When the record is thin (Level C/D), the paper is not automatically dropped; it falls back to the lowest defensible score above 0 only if any plausible connection exists — otherwise 0.

---

## STEP 2 — Quality Filters

Only papers with **Topic Relevance ≥ 1** enter the Quality Filters.

> Quality Filters must be applied **in order**: Source Validity → Basic Credibility → Content Credibility.

### STEP 2A — Source Validity

> **[MODIFIED — clarifies reliance on bibliographic evidence]**

> **Question:** Is this source an acceptable and verifiable academic or authoritative source?

This assessment relies primarily on (from the Evidence Package):

```text
Journal / Publisher
Source Type
Database Record
DOI
ISBN
Stable URL
Other Available Bibliographic Metadata
```

This assessment can be performed even when full text is unavailable — the level does not change the standard.

**Pass examples:**

- Peer-reviewed journal article
- Academic book
- Academic book chapter
- Recognized conference paper, where appropriate for the discipline
- Authoritative institutional publication
- Government publication

| Outcome | Action |
|---|---|
| PASS | Continue |
| FAIL | **Exclude** |

### STEP 2B — Basic Credibility

> **[MODIFIED — relies only on evidence actually provided]**

> **Question:** Can the basic publication information of this source be verified?

This assessment relies primarily on (from the Evidence Package):

```text
Authors
Publication Venue
Publication Date
Source Type
DOI / ISBN
Database Record
Other Available Bibliographic Evidence
```

> **[NEW RULE]** Basic Credibility assessment must rely **only on evidence actually provided to the Cloud**. The Cloud must not assume or invent missing information. Missing bibliographic fields are evaluated under the available-data rules (`13`), never silently filled.

| Outcome | Action |
|---|---|
| PASS | Continue |
| FAIL | **Exclude** |

Verification uses **only** the information collected by the Local Agent (including any local verification notes). The Cloud does not verify against the internet. If the available information is insufficient to establish basic verifiability, treat as FAIL (exclude) under the available-data rules — see `13` for the exact missing-field behavior per field.

### STEP 2C — Content Credibility (level-aware)

> **[MODIFIED — redefined by Evidence Availability Level]**

> **Question:** Does the source contain sufficient evidence and reasoning to be academically usable?

Evaluate the available information for:

- Evidence
- Data
- References
- Academic reasoning
- Serious factual problems
- Serious unsupported claims
- Material credibility problems

The **depth** of the assessment depends on the Evidence Availability Level:

#### Level A — Full Evidence

Record:

```text
Content Credibility Assessment: Full Assessment
```

The Cloud may perform: method analysis, evidence analysis, findings assessment, limitation identification.

#### Level B — Extended Evidence

Record:

```text
Content Credibility Assessment: Limited Assessment
```

The system must clearly state internally: *assessment based only on available evidence; full-paper assessment not completed.*

#### Level C — Abstract Evidence

Do **not** make a strong Content Credibility judgment. Record:

```text
Content Credibility: Insufficient Evidence for Full Assessment
```

The system must **not** automatically classify the paper as `Fail`, `Low Quality`, or `Not Credible` unless the available evidence itself demonstrates a clear and material credibility problem.

#### Level D — Metadata Only

Do **not** perform a Content Credibility Assessment. Record:

```text
Content Assessment: Not Available
```

The Cloud must not: infer methodology, infer findings, infer research quality, generate detailed Notes, or generate detailed Summary.

### Important rule — do not over-exclude

> **[UNCHANGED]**

Do **not** automatically exclude a source because:

- It contains a viewpoint
- It has some bias
- Its conclusions are controversial
- Its findings differ from other research

**Exclude only when** credibility problems **materially reduce its value as academic evidence**.

### Content Credibility Decision Rule

> **[NEW]**

```text
Material Credibility Problem Identified
            ↓
Exclude / Fail

No Material Credibility Problem Identified
            ↓
Pass

Insufficient Evidence for Full Assessment
            ↓
Do Not Automatically Exclude
            ↓
Retain with Assessment Limitation
```

> **Core rule: Lack of evidence is not itself evidence of poor quality.** (`05` §5.4)

---

## STEP 3 — Recency Assessment

> **[UNCHANGED]**

Evaluate recency **only after** a paper passes the Quality Filters.

### Possible outcomes

| Outcome | Action |
|---|---|
| **Current** | No adjustment |
| **Older but still useful** | Lower Priority |
| **Clearly outdated / replaced** | Exclude |

### Default principle

> Recency is primarily a **ranking and priority adjustment factor**.
> Recency is **not normally a hard exclusion filter**.
> A paper should only be excluded when it is **clearly outdated or materially replaced**.

Older literature is not automatically excluded. Definitions and discipline-relative judgment for these three outcomes are discussed in `07` and `14`. Recency relies on the Publication Year from the Bibliographic Metadata and is independent of the Evidence Availability Level.

---

## STEP 4 — Build Screened Literature Pool

> **[UNCHANGED — with a clarifying note]**

All retained papers form the **SCREENED LITERATURE POOL**. It includes:

| Type | Condition |
|---|---|
| Priority-level Topic Relevance | Topic Relevance = 3, Quality = Pass, Recency = Current or Still Useful |
| Include-level Topic Relevance | Topic Relevance = 2, Quality = Pass, Recency = Current or Still Useful |
| Supplementary-level Topic Relevance | Topic Relevance = 1, Quality = Pass, Recency = Current or Still Useful |

Papers that fail Quality, score Topic Relevance 0, or are clearly outdated/replaced are **not** part of this pool.

> **[NEW — clarifying note]** Papers retained under the Content Credibility Decision Rule (Limited Assessment at Level B, Insufficient Evidence at Level C, Content Assessment Not Available at Level D) **are** part of the Screened Literature Pool. They appear in the outputs with their Evidence Availability Level and Assessment Limitations clearly attached (`09`, `10`).

---

## STEP 5 — Final Priority Classification

> **[UNCHANGED]** (Full detail in `07-priority-classification.md`; level compatibility in `07` §7.10.)

### Priority 1 — Must Read

Usually:
- Topic Relevance = 3
- Quality = Pass
- Recency = Current or Still Useful

These papers directly answer or strongly support the Research Question.

### Priority 2 — Recommended

Usually:
- Topic Relevance = 2, Quality = Pass
- **Or** Topic Relevance = 3, Quality = Pass, Recency materially lowers priority

### Priority 3 — Supplementary

Usually:
- Topic Relevance = 1, Quality = Pass
- **Or** Topic Relevance = 2, Quality = Pass, Recency materially lowers priority

These papers may provide theory, background, related concepts, variables, context, or adjacent research.

### Core Priority Rule

> - Final Priority is determined by **Topic Relevance first**, then adjusted **downward only** when Recency materially reduces its priority.
> - **Quality is a pass/fail gate, not a priority score.**
> - Do **not** convert Quality into a numerical ranking score.
> - **[NEW]** The Evidence Availability Level does **not** adjust Priority (`05` §5.4, `07` §7.10).

---

## Evidence Boundary for Notes and Summary

> **[NEW]**

The Cloud must follow a strict **Evidence Boundary** when generating Notes, Summary, Key Findings, Method Description, and Limitations.

| Level | The Cloud may generate | The Cloud must NOT |
|---|---|---|
| **A** | Detailed Notes; Detailed Summary; Method Summary; Key Findings; Limitations | — (all statements must be supported by the available content) |
| **B** | Partial Notes; Evidence-Based Summary; Available Findings; Available Method Information | Fill missing sections with inference; pretend to have reviewed the full paper; invent limitations |
| **C** | Abstract-Based Summary; Preliminary Notes (marked "Based on the abstract and available metadata. Full paper content was not reviewed.") | Generate content findings or limitations beyond the abstract |
| **D** | Metadata-Based Record; Access / Content Unavailable Notice | Generate any paper-content summary |

This boundary applies to the Paper Sheet Notes/Summary columns (`09`) and the Reading List Notes/Summary columns (`10`).

---

## Excluded Literature

Exclude papers when **any** of the following holds:

- Topic Relevance = 0
- Source Validity = Fail
- Basic Credibility = Fail
- Content Credibility = Fail because of a material credibility problem
- Recency = Clearly Outdated / Replaced

> **[NEW — clarifying note]** The following are **NOT** exclusion reasons: Evidence Availability Level; missing full text; "Insufficient Evidence for Full Assessment" (Level C); "Content Assessment: Not Available" (Level D). Exclusion for content credibility requires a **material credibility problem** visible in the available evidence (`05` §5.4).

---

## Final Classification Logic

> **[UNCHANGED]**

| Topic Relevance | Quality | Recency | Final Result |
|---|---|---|---|
| 3 | Pass | Current | Priority 1 — Must Read |
| 3 | Pass | Older but still useful | Priority 2 — Recommended |
| 2 | Pass | Current | Priority 2 — Recommended |
| 2 | Pass | Older but still useful | Priority 3 — Supplementary |
| 1 | Pass | Current or older but useful | Priority 3 — Supplementary |
| 0 | — | — | Excluded |
| 3 | Fail | — | Excluded |

> **Note on the table:** the row "3 / Fail / — / Excluded" expresses the general rule that **any** Topic Relevance ≥ 1 that fails a Quality filter is excluded (the exclusion is not limited to Topic Relevance 3). The rows "2 / Fail / — / Excluded" and "1 / Fail / — / Excluded" follow from the same rule and are restated here so implementers do not misread the table as restricting quality-fail exclusion to score 3 only. Recency results of "Clearly outdated / replaced" are handled as exclusions in STEP 3 regardless of Topic Relevance. "Pass" in the table includes the level-appropriate Content Credibility outcomes (Full / Limited / Insufficient-Evidence / Not-Available), per the Content Credibility Decision Rule.

---

## Cloud workflow responsibilities recap

| Step | Owner | Internet needed? |
|---|---|---|
| Prepare Literature Records | Cloud | No |
| **Assess Evidence Availability (STEP 0A)** | **Cloud** | **No** |
| Topic Relevance (evidence-aware) | Cloud | No |
| Quality Filters (2A/2B/2C) | Cloud | No |
| Recency Assessment | Cloud | No |
| Screened Literature Pool | Cloud | No |
| Final Priority Classification | Cloud | No |
| (Next: Reading Role Classification → Paper Sheet → Reading List — `08`, `09`, `10`) | Cloud | No |