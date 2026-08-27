# 3. Deadline Recommendation Rule

## 3.1 Purpose and boundaries

- The **Deadline** must **not** limit search coverage in any way.
- It is used **only** to recommend **what the student should read first**.
- The recommendation produced by this rule is a **recommended initial reading count**: the number of papers the student should begin reading.

## 3.2 V1 recommendation rule

| Time until deadline | Recommended initial reading count |
|---|---|
| 1 day | 5 papers |
| 2 days | 10 papers |
| 3 days | 15 papers |
| 4 days | 20 papers |
| 5 days | 25 papers |
| 6 days | 30 papers |
| 7 days | 35 papers |
| 8–14 days | Add approximately 5 papers per additional day (capped at the global maximum, see below) |
| 15+ days | Maximum recommended initial reading count: 60 papers |

### Explicit reconciliation of the 8–14 day and 15+ day rows

The specification states both "add approximately 5 papers per additional day" for days 8–14 **and** "Maximum recommended initial reading count: 60 papers" for 15+ days. Taken literally, linear growth reaching 65–70 papers on days 13–14 would exceed the 60-paper maximum.

**Resolution (recorded explicitly, not a new product rule):** the recommended initial reading count grows by approximately 5 papers per additional day from day 8 onward and is **capped at 60 papers** (the global maximum). Concretely:

| Day | Count |
|---|---|
| 7 | 35 |
| 8 | 40 |
| 9 | 45 |
| 10 | 50 |
| 11 | 55 |
| 12 | 60 (capped) |
| 13 | 60 (capped) |
| 14 | 60 (capped) |
| 15+ | 60 (maximum) |

This preserves both statements: growth of ~5/day across 8–14 days, and a hard maximum of 60 initial papers.

## 3.3 Available Reading Time interplay

- **Available Reading Time** may further inform the recommendation (e.g., pacing guidance, splitting the initial reading count across the available days).
- It is **not** a modifier that reduces the Screened Literature Pool or the final outputs.

## 3.4 How the initial reading count is used

The count identifies the first papers to focus on. Recommended behavior consistent with the spec:

1. The initial set is drawn from the **Screened Literature Pool**, prioritizing **Priority 1 — Must Read**, then Priority 2, then Priority 3.
2. The complete Reading List still contains **all qualified literature**, regardless of the initial count.
3. This is a reading recommendation — it never truncates, removes, or hides any qualified paper.

## 3.5 Rules recap

- Deadline does not limit: search coverage, Candidate Pool size, Screened Literature Pool size, or the complete literature output.
- Deadlines may be as short as 1 day (5 initial papers); search breadth is unaffected.
- The "maximum" of 60 applies to the **recommended initial reading count** only, not to the total number of qualified papers delivered.

## 3.6 Implementation considerations

1. **Combining Deadline rule with Reading Time.** Not specified. Proposed (unconfirmed): the Deadline-based count is the target "read first" set; Reading Time is used to add pacing (e.g., "~3 papers/day") and to flag where the recommended count is unrealistic; neither reduces the pool.
2. **Deadline given as a date vs a duration.** The local agent converts a date into days remaining; a passed or same-day deadline is treated as "1 day" for recommendation purposes (see `13-edge-cases-and-missing-information.md`).
3. **Fractional days.** Rounding convention (e.g., round to the nearest whole day, minimum 1) is an implementation detail to fix during implementation.
4. **Citation Count interplay.** If the user also provided a Required Citation Count, both are guidance; the spec does not define a merge formula. Proposed (unconfirmed): the initial reading recommendation reflects the Deadline rule; the Reading List additionally highlights whether the qualified pool covers the Citation Count. See `14-implementation-considerations.md`.