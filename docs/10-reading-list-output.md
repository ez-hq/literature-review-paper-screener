# 10. Reading List Output (Cloud)

## 10.1 Core rule — same pool

The Reading List is generated from **the same Screened Literature Pool** used for the Paper Sheet.

> **Paper Sheet and Reading List are generated from the same Screened Literature Pool.**
> Do **not** create a separate literature pool.

The Reading List does **not** represent a separately searched or separately screened pool.

## 10.2 Difference between the two outputs

| Output | Presents |
|---|---|
| **Paper Sheet** | The complete qualified literature set (full record view) |
| **Reading List** | The **same** literature organized by **Priority** and **Primary Reading Role** (reading-focused view) |

## 10.3 Reading List categories

Organize papers under these category headings:

### 📚 Foundational
> Build your theoretical and conceptual foundation.

### 🎯 Core Evidence
> Directly answer your Research Question.

### 🧩 Supporting
> Strengthen specific arguments or sections.

### ⚖️ Counterargument
> Understand conflicting findings and academic debates.

### 🆕 Recent
> Keep your Literature Review up to date.

### 🔬 Methodology
> Understand how the evidence was produced and evaluated.

Each paper appears under **exactly one** category (its Primary Reading Role — `08`), which prevents duplication in the Reading List.

## 10.4 Required columns

The Reading List **must** contain:

| Priority | Reading Role | Citation | Title | Notes | Summary | Links |

### Column definitions

#### Priority
The final reading importance:
- Priority 1 — Must Read
- Priority 2 — Recommended
- Priority 3 — Supplementary

#### Reading Role
One Primary Reading Role:
- Foundational
- Core Evidence
- Supporting
- Counterargument
- Recent
- Methodology

#### Citation
- Use an **internationally standard academic citation format**.
- The implementation documentation must specify how the product determines or defaults the citation style (see §10.5).
- **Do not remove this column.**

#### Title
Full title of the paper.

#### Notes
May contain detailed academic information, including:
- Research method
- Study design
- Main argument
- Key findings
- What the study demonstrates
- Important limitations where available

> **[NEW — Evidence Boundary]** Notes content is governed by the Evidence Boundary in `06`: detailed notes only at **Level A**; partial / evidence-based notes at **Level B**; abstract-based preliminary notes (with the caveat "Based on the abstract and available metadata. Full paper content was not reviewed.") at **Level C**; **no paper-content notes** at **Level D**.

#### Summary
Explain:
- What the paper did
- How it relates to the user's Research Question
- How it can be useful in the student's Literature Review

> **[NEW — Evidence Boundary]** Summary depth follows the Evidence Availability Level (same boundary as Notes). At Level D only a metadata-based record and an access/content-unavailable notice are produced.

#### Links
- Provide the available paper link, DOI link, database record, publisher page, or other **stable source link collected by the Local Agent**.
- The Cloud does not retrieve links (`05`, `09`).

## 10.5 Citation style determination (implementation requirement)

The spec requires the implementation documentation to specify how the product determines or defaults the citation style.

| Situation | Behavior |
|---|---|
| Assignment Requirements explicitly name a citation style | Use that style |
| Assignment Requirements imply a style (e.g., a rubric reference, institution requirement) | Use the implied style |
| No style information provided | **Default: APA (7th edition)** — an internationally standard academic citation format used across undergraduate and master's work |

Proposed default rationale and mechanics:

- **APA 7** is selected as the V1 default because it is a widely taught international standard across disciplines and institutions, matching the international student user base.
- Because the V1 disciplinary focus is **Medical Science**, a style such as **Vancouver (NLM)** is a likely near-term alternative; the citation style must therefore be a **configurable setting** rather than hard-coded.
- If the user later pastes assignment requirements naming another style, the output is regenerated in that style (the underlying data — title, authors, year, venue, identifiers — is style-independent).

> This is the required implementation decision point for the Citation column. It is recorded as an explicit decision with a proposed default in `14-implementation-considerations.md` (item 1).

## 10.6 Format and delivery

- Format: **Excel** or **Google Sheet** (same delivery options as the Paper Sheet).
- Suggested sheet conventions (implementation detail): one row per paper; frozen header; filters; papers grouped under the six category headings (or sorted by category with a category column).
- **Evidence Availability Level** is carried on each paper record (from the shared screening data) and may be surfaced as a supplementary indicator next to Notes/Summary so the user understands the depth of each entry. **(NEW)**

## 10.7 Completeness rule

- **All qualified literature remains available to the user.**
- Deadline, Available Reading Time, and Required Citation Count influence **what to read first and how many papers to initially focus on** — they never remove literature from the Reading List (`03`).
- The complete Reading List is delivered regardless of the recommended initial reading count.
- Papers with limited evidence (Levels C/D) **remain** in the Reading List with their preliminary classifications and evidence caveats — evidence availability never removes qualified literature (`05` §5.4). **(NEW)**