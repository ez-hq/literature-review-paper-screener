# 14. Implementation Considerations (Appendix)

> **[MODIFIED]** Updated for the Evidence Package architecture: several register items added (21–26); existing item references adjusted for renumbered sections in `05`.

## 14.1 Purpose and status of this appendix

The product specification is intentionally precise but leaves a small number of rules **not fully specified**. Per the documentation mandate, each ambiguity is recorded here **explicitly** — with a clearly-marked **proposed default** — instead of being silently invented as product behavior.

- A "proposed default" is **not a product rule**; it is a recommendation to confirm during implementation.
- Once confirmed, the decision should be recorded back into the relevant document.
- Product rules in the other documents must not be changed by this appendix.

## 14.2 Consolidated register

| # | Ambiguity | Where it matters | Proposed default (unconfirmed) |
|---|---|---|---|
| 1 | Citation style default | `10` §10.5 | APA 7th edition; configurable; Vancouver (NLM) as likely near-term alternative for Medical Science |
| 2 | Definition of "materially reduces" (Recency) | `07` §7.8 | Superseded by more recent systematic review/meta-analysis/authoritative guidance; contradicted by strong later evidence; findings no longer indicative of current research |
| 3 | Topic missing after one clarification | `13` §13.4 | End run with explicit "cannot start" notice; resumable; no empty search; no cloud run |
| 4 | Deadline already passed / "today" | `03`, `13` §13.4 | Treat as 1 day → initial reading count 5 |
| 5 | Contradictory user restrictions | `13` §13.4 | Surface conflict; apply the more specific restriction if unresolved |
| 6 | Non-English topic/content | `13` §13.4 | Original title kept; English translation in Notes where available |
| 7 | Very large pools / batching | `05` §5.9, `13` §13.5 | No caps; lossless batching with run-context on every batch |
| 8 | Preprint vs published version | `13` §13.6 | Keep published version; record preprint link |
| 9 | Retracted papers | `13` §13.6 | Verified retraction = material credibility problem → Exclude |
| 10 | Predatory/unknown journals | `13` §13.6 | Source Validity judgment; not an automatic pass |
| 11 | Recency time-window definitions | `07` §7.8 | No universal year cut-off; discipline/topic-relative, favor keeping (boundary rule in `07` §7.8) |
| 12 | Reading-role tie-breaking | `08` §8.6 | Fixed deterministic order (configurable); unconfirmed which order |
| 13 | Deadline + Reading Time + Citation Count combination | `03` §3.6 | Deadline rule sets the initial count; reading time adds pacing; citation count adds coverage indication; all guidance only |
| 14 | Empty screened pool | `13` §13.5 | Outputs produced empty with explicit notice; no cloud re-search; local agent advises user |
| 15 | Summary/Notes generation reuse | `09` §9.4 | Generate once per paper; reuse in Paper Sheet and Reading List for consistency |
| 16 | Ordering within Reading List categories & Paper Sheet rows | `10`, `09` | Within category: Priority, then Recency (Current first), then Year descending; Paper Sheet rows: Priority, then Topic Relevance, then Year descending |
| 17 | Discipline expansion points | `01` §1.4 | Keep configurable: source-type norms, recency judgment, database list, citation styles — never hard-coded in cloud pipeline |
| 18 | Language of user-facing outputs | `10`, `09` | Default English (matches international academic norm); assignment requirements may override; unconfirmed |
| 19 | Verification evidence passed to Cloud | `05` §5.9 | Optional lightweight `verification_notes` field; unconfirmed |
| 20 | Rounding for fractional deadline days | `03` §3.6 | Round to nearest whole day, minimum 1 day |
| 21 | **Level B vs Level C threshold** | `05` §5.9 | "Substantial structured information" = at least Methods Information + Key Findings (or ≥ 2 of the 4 structured sections); otherwise Level C. *(NEW)* |
| 22 | **How much full-text effort the Local Agent should make** | `04` §4 impl. (item 5), `05` §5.9 | Attempt open access / institutional / preprint sources; do not bypass paywalls; 1 retrieval attempt per candidate, then fall to lower level. *(NEW)* |
| 23 | **Priority/Role flags at Levels C/D in outputs** | `07` §7.10, `08` §8.7, `09`, `10` | Flag as "preliminary — based on abstract/metadata only" in Paper Sheet and Reading List; never adjust the class itself. *(NEW)* |
| 24 | **Surface Evidence Availability Level to the user?** | `09` §9.4, `10` §10.6 | Yes — Paper Sheet always shows level + limitations (cols. 16–19); Reading List may show a lightweight indicator next to Notes/Summary. *(NEW)* |
| 25 | **Insufficient content credibility in Screened Pool** | `06` STEP 4 | Retained-with-limitation papers are part of the Screened Literature Pool; they appear in both outputs with the limitation visible. *(NEW)* |
| 26 | **How "clearly outdated/replaced" interacts with Level D** | `13` §13.2 | Standalone — recency exclusion is independent of evidence level; a Level D paper with a clearly outdated publication year follows normal Recency rules. *(NEW)* |

## 14.3 Detail notes

### 14.3.1 Citation style (item 1) — required implementation decision

The spec **requires** the implementation documentation to specify citation-style determination. The rule in `10` §10.5:

1. If assignment requirements name or imply a style → use it.
2. Otherwise → **default APA 7th edition**.
3. The style must be a configurable setting (Medical Science likely to prefer Vancouver/NLM later).

### 14.3.2 "Materially reduces" (item 2)

The spec fixes the rule ("adjust downward only when Recency materially reduces usefulness") but not the threshold. The triggers in `07` §7.8 are proposed operationalizations. When in doubt between "older but still useful" and "clearly outdated/replaced", keep the paper (`07` §7.8 boundary rule).

### 14.3.3 Recency windows (item 11)

No fixed year cut-offs. Recency judgment should be relative to: the field's evidence half-life (Medical Science: rapidly-changing clinical evidence vs stable foundational theory), existence of newer systematic reviews, and whether the paper's claims still represent current understanding. V1 implementation should treat this as an LLM-judgment factor with a discipline-aware prompt, not a hard-coded year rule.

### 14.3.4 Role tie-breaking (item 12)

V1 requires exactly one Primary Reading Role. When a paper plausibly fits several, the classifier must be deterministic. Recommended tie-break direction (unconfirmed): assign the role matching the paper's primary contribution to the Literature Review for the given Research Question, with a fixed precedence order configured at deployment so results are reproducible.

### 14.3.5 Guidance-input combination (item 13)

All three guidance inputs remain non-limiting (spec rule). The proposed (unconfirmed) behavior: initial reading count from Deadline rule; pacing notes from Available Reading Time; a "citation coverage" indicator (does the qualified pool meet the Required Citation Count?) in the Reading List. Nothing filters or truncates the pool.

### 14.3.6 Discipline expansion (item 17)

Everything discipline-sensitive lives in configurable judgment factors (source-type pass norms, recency windows, database preferences, citation styles). V1 ships configured for Medical Science but structurally open — the pipeline itself (search → collect → screen → classify → output) is discipline-neutral. Do not add discipline-specific branches inside the screening logic.

## 14.4 Change log

| Date | Change |
|---|---|
| V1 initial | First issue of the documentation set. All product rules preserved from specification; ambiguities recorded as unconfirmed proposals. |
| V1 — Evidence Package amendment | Added the Literature Evidence Package data layer (`05`), Evidence Availability Levels A–D (`05` §5.3), STEP 0A + level-aware screening + Evidence Boundary (`06`), STEP 7.5 handoff module (`04`), level-compatible Priority/Reading Role (`07`, `08`), evidence columns in outputs (`09`, `10`), architecture principle (`11` §11.7), updated E2E flow (`12`), level-based missing-content rules (`13`), and register items 21–26 (this document). Core screening logic, classification tables, user-input flow, and output requirements were **not** redesigned. |
