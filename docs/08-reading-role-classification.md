# 8. Reading Role Classification (Cloud)

## 8.1 Two independent dimensions

Every paper in the Screened Literature Pool must be evaluated using **two separate dimensions**:

### Dimension 1 — Priority

- Answers: *How important is this paper for the user to read?*
- Values: Priority 1 — Must Read / Priority 2 — Recommended / Priority 3 — Supplementary
- Determines **reading importance**. (Rules in `07-priority-classification.md`.)

### Dimension 2 — Reading Role

- Answers: *What function does this paper serve in the Literature Review?*
- Each paper receives **one Primary Reading Role**.
- Values: Foundational / Core Evidence / Supporting / Counterargument / Recent / Methodology
- Determines **the function of the paper**.

## 8.2 Core Rule

> **Priority ≠ Reading Role.**
> Each paper must have:
> - **One Priority**
> - **One Primary Reading Role**

### Examples

| Paper | Priority | Primary Reading Role |
|---|---|---|
| Paper A | Priority 1 — Must Read | Foundational |
| Paper B | Priority 1 — Must Read | Core Evidence |
| Paper C | Priority 2 — Recommended | Counterargument |
| Paper D | Priority 3 — Supplementary | Methodology |

## 8.3 Classification rule

- Priority is determined by: **how important the paper is for the user's Research Question** (`07`).
- Reading Role is determined by: **how the paper contributes to the Literature Review** (this document).
- A paper may potentially fit multiple Reading Roles. However, **for V1, assign only one Primary Reading Role**.
- Assigning exactly one role **prevents duplication in the Reading List** (a paper must appear under exactly one category).

## 8.4 Reading Role definitions

### Foundational

- **Purpose:** Build the theoretical and conceptual foundation.
- **Includes:** Core theories, key concepts, seminal papers, landmark studies, important frameworks.
- **User meaning:** Read this to understand the foundation of the topic.

### Core Evidence

- **Purpose:** Directly answer the Research Question.
- **Includes:** Directly relevant empirical studies, key findings, strong evidence addressing the topic.
- **User meaning:** Read this because it provides the main evidence for answering your research question.

### Supporting

- **Purpose:** Support core arguments.
- **Includes:** Evidence for sub-arguments, relevant variables, mechanisms, related populations, related contexts.
- **User meaning:** Read this to strengthen specific parts of your argument.

### Counterargument

- **Purpose:** Show disagreement, debate, or alternative perspectives.
- **Includes:** Contradictory findings, inconsistent evidence, alternative explanations, different theoretical perspectives.
- **User meaning:** Read this to understand what researchers disagree about.

### Recent

- **Purpose:** Represent recent developments.
- **Includes:** Recent evidence, new developments, emerging trends, updated findings.
- **User meaning:** Read this to make sure your Literature Review reflects the current state of research.
- **Important rule:**
  > "Recent" should only be assigned when the paper's **main value is representing recent developments** rather than serving primarily as Foundational, Core Evidence, Supporting, Counterargument, or Methodology.

### Methodology

- **Purpose:** Understand how the research was conducted.
- **Includes:** Important research designs, measurement approaches, method comparisons, methodological limitations.
- **User meaning:** Read this to understand how researchers study this topic and why methods may affect findings.
- **Important rule:**
  > Methodology should only be used when the **main reason to read the paper is understanding research methods**, methodological choices, or methodological limitations.

## 8.5 Assignment procedure (implementation guidance)

Consistent with the definitions and the important rules above:

1. Determine the paper's **primary contribution** to the Literature Review.
2. Check the *special-use* roles first: assign **Recent** only if its main value is representing recent developments; assign **Methodology** only if its main reason for reading is methods.
3. Otherwise select the single best fit among **Foundational / Core Evidence / Supporting / Counterargument**.
4. Output **exactly one** Primary Reading Role per paper.

A paper's Priority and its Reading Role are independent: a Priority 2 paper can legitimately be Core Evidence (e.g., slightly lower relevance but still central evidence); a Priority 1 paper can be Counterargument (overwhelmingly important to read precisely because it challenges the consensus).

## 8.6 Implementation considerations

1. **Tie-breaking when a paper genuinely fits multiple roles.** Not specified. Proposed (unconfirmed): assign the role that best describes the paper's *primary* contribution given the Research Question; when roles are genuinely tied, apply a **fixed, deterministic order** (configuration option) so the classifier never re-rolls between runs. No particular order is prescribed by the spec. See `14-implementation-considerations.md`.
2. **Judging "main value"** for Recent / Methodology: requires the abstract/content; when the record is thin, do not default to Recent/Methodology — prefer the role closest to the paper's evident contribution, or Supporting when only a plausible, generic connection exists.
3. **No secondary role field in V1 outputs.** V1 stores and displays only the Primary Reading Role to avoid duplication; a secondary-role concept is V2 territory and must not be added.

## 8.7 Reading Role across Evidence Availability Levels

> **[NEW]**

Reading Role classification **continues to function at every Evidence Availability Level**. The role definitions and the one-primary-role rule (§8.2–§8.4) are unchanged; only the depth and confidence of the classification changes:

| Level | Reading Role behavior |
|---|---|
| **A — Full Evidence** | Full-confidence role classification |
| **B — Extended Evidence** | Role classification based on abstract + substantial structured information |
| **C — Abstract Evidence** | **Preliminary** Reading Role classification |
| **D — Metadata Only** | Best-effort role indication from metadata (title/venue/year) where defensible; otherwise flagged as not assessable from available evidence |

Rules:

> The Evidence Availability Level must **not** determine the Reading Role by itself. Evidence Availability ≠ Quality (`05` §5.4): a Level C paper can still be classified Core Evidence from its abstract.
>
> Each paper still receives exactly **one Primary Reading Role**; where evidence is thin (Levels C/D) the role is flagged as preliminary per the Evidence Boundary (`06`), and may be revisited by the student after reading the full paper.

## 8.7 Reading Role across Evidence Availability Levels

> **[NEW]**

Reading Role classification **continues to function at every Evidence Availability Level** — the role definitions and the one-primary-role rule (§8.2–8.4) are unchanged:

- **Level A (Full Evidence):** full-confidence role classification.
- **Level B (Extended Evidence):** role classification based on abstract + substantial structured information.
- **Level C (Abstract Evidence):** **preliminary** Reading Role classification.
- **Level D (Metadata Only):** role assignment must be treated as very preliminary / best-effort from metadata; per `05` §5.3 and `06` STEP 2C the Cloud must not claim to have reviewed the paper.

Rules:

> The Evidence Availability Level must **not** determine the Reading Role itself. A Level C/D paper can still be classified Core Evidence or Foundational on the basis of title/metadata — the difference is only the **confidence and depth** of the classification, which must be flagged as preliminary when the underlying evidence is limited.
>
> Assigning one Primary Reading Role remains mandatory for every paper in the Screened Literature Pool; at Levels C/D the role is provisional and the output indicates the evidence limitation.