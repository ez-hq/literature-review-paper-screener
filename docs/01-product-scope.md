# 1. Product Scope — V1

## 1.1 What the product is

The Literature Review Paper Screener is an AI product that helps students build a **Literature Review** for their academic work. It searches the literature broadly, screens it carefully, and produces two structured outputs:

1. **Paper Sheet** — the complete qualified literature set (`09-paper-sheet-output.md`).
2. **Reading List** — the same literature organized by Priority and Primary Reading Role (`10-reading-list-output.md`).

## 1.2 Supported task type

V1 supports **one** task type only:

> Literature Review

### Non-goals — supported in later versions or not at all

| Task type | V1 status |
|---|---|
| Literature Review | ✅ Supported |
| Essay writing | ❌ Not supported in V1 |
| Dissertation | ❌ Not supported in V1 |
| Research Proposal | ❌ Not supported in V1 |
| Any other academic task type | ❌ Not supported in V1 |

The user-facing "What are you working on?" flow may show "Literature Review" as a fixed value for V1 rather than requiring a meaningful selection (see `02-user-input.md`, Question 1).

## 1.3 Target users

- Undergraduate students
- Master's students
- International students
- Overseas university students

## 1.4 Initial disciplinary focus

- Initial disciplinary focus: **Medical Science**.

### Expansion principle

The documentation and implementation must **not unnecessarily hard-code logic** that makes future expansion to other academic disciplines impossible. In practice this means:

- Terminology (e.g., "peer-reviewed journal") is defined generically so that it is valid in other disciplines.
- Discipline-relative judgments (recency thresholds, appropriate source types, relevant databases) are expressed as **configurable judgment factors**, not as hard-coded Medical Science values, even though V1 concentrates on Medical Science.
- The pipeline structure (search → collect → screen → classify → output) is discipline-neutral.

## 1.5 Outputs

V1 produces exactly two cloud-generated products, both in Excel / Google Sheet format:

1. **Paper Sheet** — the complete Screened Literature Pool (`09-paper-sheet-output.md`).
2. **Reading List** — the same Screened Literature Pool organized by Priority and Primary Reading Role (`10-reading-list-output.md`).

## 1.6 Non-goals for V1

| Feature | V1 status |
|---|---|
| Detailed **Reading Plan** (e.g., day-by-day plan) | ❌ V2 feature — must not be added to V1 |
| Internet access inside the Cloud | ❌ Forbidden by architecture |
| Any cloud-side search / fetch / URL opening | ❌ Forbidden by architecture (`11-local-vs-cloud-responsibilities.md`) |
| Hard limits on search, screening, or pool size from Citation Count / Deadline / Reading Time | ❌ Forbidden (`02`, `03`) |
| Multiple reading roles per paper in outputs | ❌ V1 assigns exactly one Primary Reading Role (`08`) |
| Task types other than Literature Review | ❌ See §1.2 |

## 1.7 Guidance vs limits (core principle)

The following user inputs are **guidance only** and must never behave as hard limits on search or screening:

- **Required Citation Count** — recommendation and output guidance only; the system must not stop searching or screening after reaching this number.
- **Deadline** — affects only what to read first, never the breadth of the search.
- **Available Reading Time** — affects reading recommendations and the recommended initial reading count, never the pools.

> **Core principle: Search broadly. Screen carefully. Keep all qualified literature. Use deadline and available reading time to recommend what the user should read first — not to limit how much literature the agent searches for.**

See `04` (search), `10` (reading recommendation logic) for enforcement points.

## 1.8 Local vs cloud scope (summary)

| Activity | Owner |
|---|---|
| All internet-dependent research (search, source access, metadata/abstract collection, verification, deduplication) | Local Agent (free) |
| All paid screening, evaluation, classification, and structured output generation | Cloud (paid) |

Full detail: `11-local-vs-cloud-responsibilities.md`.