# 7. Priority Classification (Cloud)

## 7.1 What Priority answers

Priority answers:

> How important is this paper for the user to read?

Priority determines **reading importance**.

## 7.2 Priority levels

| Value | Label |
|---|---|
| Priority 1 | Must Read |
| Priority 2 | Recommended |
| Priority 3 | Supplementary |

## 7.3 Rules determining Final Priority

1. **Topic Relevance first.** Final Priority is determined by Topic Relevance first.
2. **Recency adjusts downward only.** Recency may only adjust Priority **downward**, and only when it **materially reduces** the paper's usefulness.
3. **Quality is a gate.** Quality is a pass/fail gate, not a priority score. Do not convert Quality into a numerical ranking score.

### Priority 1 — Must Read

Usually:
- Topic Relevance = 3
- Quality = Pass
- Recency = Current or Still Useful

These papers **directly answer or strongly support** the Research Question.

### Priority 2 — Recommended

Usually:
- Topic Relevance = 2, Quality = Pass
- **Or** Topic Relevance = 3, Quality = Pass, Recency materially lowers priority

### Priority 3 — Supplementary

Usually:
- Topic Relevance = 1, Quality = Pass
- **Or** Topic Relevance = 2, Quality = Pass, Recency materially lowers priority

These papers may provide:
- Theory
- Background
- Related Concepts
- Variables
- Context
- Adjacent Research

## 7.4 Core Priority Rule (normative)

> Final Priority is determined by **Topic Relevance first**, then adjusted **downward only** when **Recency** materially reduces its priority.
> **Quality is a pass/fail gate, not a priority score.**
> Do **not** convert Quality into a numerical ranking score.

## 7.5 Full classification table

| Topic Relevance | Quality | Recency | Final Result |
|---|---|---|---|
| 3 | Pass | Current | Priority 1 — Must Read |
| 3 | Pass | Older but still useful | Priority 2 — Recommended |
| 2 | Pass | Current | Priority 2 — Recommended |
| 2 | Pass | Older but still useful | Priority 3 — Supplementary |
| 1 | Pass | Current or older but useful | Priority 3 — Supplementary |
| 0 | — | — | Excluded |
| 3 | Fail | — | Excluded |

## 7.6 Excluded conditions

A paper is excluded when **any** of:

- Topic Relevance = 0
- Source Validity = Fail
- Basic Credibility = Fail
- Content Credibility = Fail because of a material credibility problem
- Recency = Clearly Outdated / Replaced

Excluded papers are **not** part of the Screened Literature Pool and never appear in the Paper Sheet or Reading List.

## 7.7 Topic Relevance ≠ Priority (examples)

Priority is not a straight copy of the Topic Relevance score:

| Paper | Topic Relevance | Recency | Final Priority |
|---|---|---|---|
| Recent landmark RCT directly answering the question | 3 | Current | Priority 1 |
| Older landmark study, superseded for current claims but still foundational | 3 | Older but still useful | Priority 2 |
| Closely related empirical study, current | 2 | Current | Priority 2 |
| Older related study with meaningful value | 2 | Older but still useful | Priority 3 |
| Theory/background paper, current | 1 | Current | Priority 3 |

## 7.8 "Materially reduces" operationalization

The spec fixes the **rule** (adjust only when Recency *materially* reduces usefulness) but does not define "materially". This is an implementation consideration — see `14-implementation-considerations.md`. Indicative triggers (to be confirmed):

- The paper's core findings are superseded by a more recent systematic review / meta-analysis / updated authoritative guidance addressing the same question.
- The paper's claims have been contradicted by strong, well-cited later evidence.
- The paper is so old relative to the field's evidence base that its findings are no longer indicative of the current state of research (e.g., a treatment study whose intervention is no longer in use) — while it may still be valuable as a **Foundational** or **Methodology** reading (that judgment belongs to Reading Role, `08`).

**Boundary:** doubt about "older but still useful" vs "clearly outdated/replaced" must be resolved in favor of **keeping** the paper (recency is not normally a hard exclusion filter — `06`, STEP 3). Only genuinely clearly-outdated/materially-replaced papers are excluded.

## 7.9 Interaction with the other dimension

Priority is one of two independent per-paper dimensions. The other is **Primary Reading Role** (`08`). Priority ≠ Reading Role; every paper gets exactly one of each.

## 7.10 Priority across Evidence Availability Levels

> **[NEW]**

Priority classification **continues to function at every Evidence Availability Level**. The classification logic in §7.3–§7.5 is unchanged; only the depth and confidence of the judgment changes:

| Level | Priority behavior |
|---|---|
| **A — Full Evidence** | Full-confidence priority classification |
| **B — Extended Evidence** | Priority classification based on abstract + substantial structured information |
| **C — Abstract Evidence** | **Preliminary** Priority assessment |
| **D — Metadata Only** | Very preliminary relevance-based priority indication |

Rules:

> The Evidence Availability Level must **not** increase or decrease Priority by itself. Evidence Availability ≠ Quality (`05` §5.4): a Level C paper that directly answers the Research Question is still Priority 1 — it is simply flagged as preliminary pending full-text confirmation.
>
> Where Priority is preliminary (Levels C/D), the output flags it (e.g., "preliminary — based on abstract/metadata only") per the Evidence Boundary (`06`), and the student is expected to confirm after reading the full paper.

## 7.10 Priority across Evidence Availability Levels

> **[NEW]**

Priority classification **continues to function at every Evidence Availability Level** — the classification logic (§7.3–7.5) is unchanged:

- **Level A (Full Evidence):** full confidence priority classification.
- **Level B (Extended Evidence):** priority classification based on abstract + substantial structured information.
- **Level C (Abstract Evidence):** **preliminary** priority assessment (per `05` §5.3 / `06` STEP 2C).
- **Level D (Metadata Only):** very preliminary relevance-based priority indication, flagged as such.

Rules:

> The Evidence Availability Level must **not** adjust Priority. Evidence Availability ≠ Quality (`05` §5.4). Limited access never improves or lowers a paper's Priority class by itself.
>
> When Priority is preliminary (Levels C/D), the output must flag it (e.g., "preliminary — based on abstract/metadata only") and the priority is suggested for re-check by the student after reading the full paper.