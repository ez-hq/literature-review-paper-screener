# 13. Edge Cases and Missing Information (Available-Data Rules)

> **[MODIFIED]** Missing-information handling is now expressed through the **Evidence Availability Level** system (`05` §5.3) and the **Content Credibility Decision Rule** (`06`).

## 13.1 The available-data principle

The Cloud has no internet access and operates only on the Structured Local-to-Cloud Handoff Dataset. Whenever information is missing:

> The Cloud works with the available information. It never fetches, searches, or waits for missing data.

Missing information is **never** a reason to silently drop a paper — each case below has an explicit rule. Missing **content** is handled by Evidence Availability Levels; missing **fields within a level** are handled per §13.2.

## 13.2 Missing metadata (per-field behavior)

| Missing field | Cloud behavior |
|---|---|
| **Title** | If the record cannot be identified at all, it cannot be screened meaningfully: treat as Basic Credibility FAIL → Exclude (a paper with no identifiable title and no other identifier cannot be verified — rule in `06` STEP 2B). |
| **Author(s)** | Basic Credibility can still pass if title + venue + date are present and verifiable from the record; missing authors alone is not an automatic fail. If no verifiable combination exists → Basic Credibility FAIL → Exclude. |
| **Publication Year** | Recency cannot be assessed → **no recency adjustment and no recency exclusion**; the paper is retained with `Recency Status = Not assessable (year missing)` and flagged in the outputs. Priority then rests on Topic Relevance alone. |
| **Source / Journal / Publisher** | If the venue is missing and the record cannot be identified as an acceptable source → Source Validity cannot be established → Source Validity FAIL → Exclude. If the venue is missing but source type is otherwise identifiable (e.g., government publication via record origin), judge on what exists. |
| **Abstract / Available Content** | Content Credibility cannot be fully assessed → the paper is assigned the appropriate **Evidence Availability Level** (`05` §5.3); the **Content Credibility Decision Rule** applies (`06`): no material problem → retained; insufficient information → retained with assessment limitation. Never auto-exclude. |
| **Full text / most content (paywall, no OA, retrieval failure)** | **Not an exclusion reason.** The paper is assigned Level B, C, or D depending on what evidence is actually available (see §13.2A). |
| **DOI** | No effect on inclusion; DOI is an additional credibility indicator, not a requirement. `DOI = Not available`. |
| **ISBN** | No effect on inclusion; `ISBN = Not available` (or Not applicable for journal articles). |
| **URL / Links** | No effect on inclusion; `Links = Not available` in both outputs. The "link where available" requirement (`09` §9.3) is satisfied by what the Local Agent collected. |
| **Database Record** | No effect on inclusion; `Database Record = Not available`. |
| **Source Type** | Judged from available evidence (venue, record origin, publisher); when genuinely unknown, the source is evaluated against the Source Validity question using available signals; failure to establish acceptability → Exclude. |

## 13.2A Missing content — Evidence Availability Level mapping

> **[NEW]**

| Situation | Available evidence | Level |
|---|---|---|
| Full text (or substantial full-paper content: Methods + Results + Discussion + Conclusion) collected | Full text | **A — Full Evidence** |
| No full text, but Abstract + substantial structured information (methods info, key findings, results, conclusions, detailed database record) | Abstract + structured info | **B — Extended Evidence** |
| Only Title + metadata + Abstract | Abstract only | **C — Abstract Evidence** |
| Only Title + authors + year + venue | Metadata only | **D — Metadata Only** |

The Local Agent assigns the level at STEP 7.5 (`04`); the Cloud re-validates it at STEP 0A (`06`). The level is recorded per paper and never changes pool membership or Topic Relevance/Priority/Reading Role by itself (`05` §5.4).

## 13.3 Missing content — the insufficient-information rule (Content Credibility)

> **[MODIFIED — now governed by the Content Credibility Decision Rule in `06`]**

> If there is insufficient information to fully assess content credibility:
> - Do **not** automatically exclude.
> - The Cloud must work with the available information provided by the Local Agent.

Behavior: the paper continues through the pipeline and is recorded as:

- **Level B:** `Content Credibility Assessment: Limited Assessment`
- **Level C:** `Content Credibility: Insufficient Evidence for Full Assessment`
- **Level D:** `Content Assessment: Not Available`

The limitation is flagged in the Paper Sheet (cols. 16–19, 23) and Notes/Summary so the user can judge for themselves. Only a *material credibility problem that is actually visible in the available evidence* causes exclusion (`06`, Content Credibility Decision Rule).

## 13.4 User-input edge cases

| Case | Behavior |
|---|---|
| **No Research Question at all** (user provides nothing after the required question) | The required input is missing. The clarification rule (`02` §2.4.1) applies: ask **one** clarification question; do not run immediately. If the user still provides nothing, there is no topic to search for — V1 ends the run with an explicit "cannot start" notice (no empty search, no cloud run) rather than a silent failure. This is **not a permanent block**: the user can resume by providing a topic. (Flagged as an implementation consideration — item 3 in `14`.) |
| **Topic too unclear** (e.g., no identifiable core concepts) | Ask one clarification question; if refused, **proceed with the information available** (broad search, coverage check drives expansion) — never permanently block. |
| **Required Citation Count = 0 or "not sure"** | Guidance only; treated as "no citation target". Search and screening are unaffected. |
| **Deadline already passed / "today"** | Treat as 1 day for the recommendation rule (initial reading count = 5). Search breadth unaffected. (Consideration item 4.) |
| **Deadline very far away (e.g., 12 months)** | 15+ days → initial reading count = 60 (maximum). No other effect. |
| **Available Reading Time = extremely small** (e.g., 1 minute) | Informs recommendations only (e.g., smaller pacing suggestion); never reduces pools or outputs. |
| **Restrictions contradict each other** (e.g., "all countries" + "UK only") | The Local Agent surfaces the conflict to the user for a quick correction (one follow-up, not a blocking gate); if unresolved, apply the more specific restriction and note it. (Consideration item 5.) |
| **Topic in a non-English language** | Keep the original title; add an English translation in Notes where the Local Agent can provide one. Screening works on available content. (Consideration item 6.) |

## 13.5 Pool edge cases

| Case | Behavior |
|---|---|
| **Search returns zero results** | Coverage check runs; queries are expanded (synonyms, alternative terminology, broader angles) before concluding. If still zero, the handoff contains an empty candidate dataset; the Cloud returns empty Paper Sheet / Reading List with an explicit notice. The Cloud never re-searches. The user is advised (by the Local Agent) to broaden the topic or relax restrictions. |
| **Screened Literature Pool is empty** (all candidates excluded) | Same as above: outputs are produced (empty, with an explicit notice). No qualified literature is invented. |
| **Very large Candidate Pool** | No caps are specified and none may be introduced via guidance inputs. Large pools are processed in full; batching is a transport/implementation concern (`05` §5.9, `14` item 7). |
| **Duplicate records across databases** | Handled by Local Agent deduplication (`04` STEP 7). The Cloud assumes uniqueness and does not re-deduplicate. |

## 13.6 Duplicate / version edge cases

| Case | Behavior (implementation considerations unless stated) |
|---|---|
| **Preprint + published version of the same paper** | Local dedup keeps the **published version** (richer, verifiable) and records the preprint link if present. (Consideration item 8.) |
| **Retracted paper** | Not specified by the spec. Proposed: a verified retraction is a **material credibility problem** → Content Credibility FAIL → Exclude. Flag in `14` item 9. |
| **Predatory / unknown journal** | Judged under Source Validity ("acceptable and verifiable academic or authoritative source"); not an automatic pass just because it is a "journal". (Consideration item 10.) |
| **Same paper, different years (e.g., conference → journal)** | Kept as distinct records only when they are genuinely distinct works; otherwise deduplicated. |
| **Erratum / corrections** | Merged into the primary record by the Local Agent where identifiable. |

## 13.7 Clarification procedure (recap)

1. Topic unclear or missing → **one** clarification question.
2. Do **not** run the workflow immediately after the initial input if the topic is unclear.
3. If the user declines to give more information → **proceed with available information** (or, for a completely absent topic, end with an explicit non-blocking notice — §13.4).
4. The workflow must **never be permanently blocked** by missing optional inputs.

## 13.8 Rules recap (normative)

- Missing optional inputs never block the workflow (`02`).
- Missing metadata is handled per §13.2 — most missing fields do not cause exclusion.
- Missing **content** is handled through Evidence Availability Levels (§13.2A) — never auto-excludes (`06` STEP 2C; §13.3).
- Evidence Availability Level is **not** a quality score and never changes relevance/priority/role/pool membership (`05` §5.4).
- Missing publication year → no recency adjustment or exclusion (§13.2).
- The Cloud never fetches missing data under any circumstance (`11` §11.3).