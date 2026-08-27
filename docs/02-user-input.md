# 2. User Input

## 2.1 User experience principle

- Do **not** begin with a large form containing many fields.
- The user is guided through a **conversational flow**.
- Optional questions are asked **one at a time**.
- The system must ask about optional information, **but the user may skip it**.
- If the user skips optional information:
  > Continue using the default underlying search and screening logic.
- Missing optional information must **never block the workflow**.

## 2.2 V1 conversation flow

### Question 1 — What are you working on?

- V1 supports **Literature Review only**.
- This may be fixed rather than requiring a meaningful user selection (e.g., shown as the current task) — the user does not need to choose among task types in V1.

### Question 2 — Required: What is your question/topic?

- The user provides:
  - Research Question, **or**
  - Essay Question, **or**
  - Research Topic
- This is **the essential required input** for the entire run.

### Question 3 — Optional: How many papers do you need for citation?

- This is the **Required Citation Count**.
- Important rule:
  > Required Citation Count is used for recommendation and output guidance, **not** as a hard limit on search or screening.
- The system must **not** stop searching or screening after finding this number of papers.

### Question 4 — Optional: Paste any assignment requirements.

- The user may provide any of:
  - Assignment brief
  - Rubric
  - Lecturer requirements
  - Word count
  - Required population
  - Required demographic
  - Required country or region
  - Required research scope
  - Other assignment constraints
- If the user skips this:
  > Continue without assignment-specific restrictions.

### Question 5 — Optional: Any research restrictions?

- The user may specify:
  - Specific population
  - Specific country or region
  - Time period
  - Required source type
  - Preferred publication years
  - Other literature restrictions
- Example: *"Adolescents aged 13–18, preferably studies published after 2018."*
- The user may also select: **No specific requirements.**

### Question 6 — Optional: When is your deadline?

- Example: *"7 days from now."*
- This information is used **for reading recommendations**.
- It must **not** reduce the breadth of the literature search.

### Question 7 — Optional: How much time can you spend reading?

- This information is used for:
  - Reading recommendations
  - Recommended initial reading count
- It must **not** be used as a hard search limit.

## 2.3 Required vs optional inputs

| Input | Requirement |
|---|---|
| Research Question / Topic | **Required** |
| Required Citation Count | Optional |
| Assignment Requirements | Optional |
| Research Scope / Restrictions | Optional |
| Deadline | Optional |
| Available Reading Time | Optional |

## 2.4 Missing information rules

### 2.4.1 Topic too unclear

If the user does not provide enough information for the system to reasonably understand the research topic:

1. **Ask one clarification question.**
2. **Do not immediately run the workflow.**
3. If the user still chooses not to provide additional information:
   - **Proceed using the information available.**
   - **Do not permanently block the workflow.**

### 2.4.2 Other optional inputs missing

No clarification is required for skipped optional inputs (Q3–Q7). The workflow proceeds with default underlying logic:

- No Citation Count → the search and outputs are not constrained by a citation target; recommendations still run purely from Deadline / Reading Time where provided.
- No Assignment Requirements → no assignment-specific restrictions are applied.
- No Research Restrictions → no restrictions are applied; no restriction is invented (see `04`, STEP 0 rule).
- No Deadline → no initial-reading-count recommendation derived from the Deadline rule; search breadth is unaffected.
- No Reading Time → reading-time-based refinement is skipped.

## 2.5 Input → Search Profile mapping

Every user input is converted into Search Profile fields in `04-local-search-workflow.md` (STEP 0):

| User input | Feeds Search Profile field(s) |
|---|---|
| Research Question / Topic | Research Question; Core Concepts; Relationship / Research Focus (via decomposition, STEP 1) |
| Assignment Requirements | Assignment Requirements; may carry population / demographic / country / region / research scope |
| Research Restrictions | Population; Geographic Scope; Time Restrictions; Source Type Restrictions; Publication Year Preferences |
| Deadline | Not a search field. Used for reading recommendations (see `03`) |
| Required Citation Count | Not a search field. Guidance for output recommendations |
| Available Reading Time | Not a search field. Refines reading recommendations |

## 2.6 Implementation considerations

> These are recorded ambiguities, not product rules. They are consolidated in `14-implementation-considerations.md`.

1. **Definition of "too unclear to reasonably understand".** Not specified. Proposed working definition: the topic contains no identifiable core concepts at all (or only stop-words such as "medicine" with no focal area). A broad-but-meaningful topic (e.g., "physical activity and depression in adolescents") is *clear enough* — the search proceeds broadly, and coverage is validated later.
2. **Wording and scope of the single clarification question.** Proposed wording: ask the user to specify the main focus of their topic (e.g., the population, the intervention/exposure, and the outcome they care about). One question only, then proceed regardless of the answer.
3. **Question 1 presentation.** Whether Q1 is rendered as a fixed banner ("Current task: Literature Review"), a single-select with one enabled option, or is skipped entirely is a presentation choice; all are consistent with this spec.
4. **Whether skipped Question 6/7 still allow recommendations.** If the user skips Deadline *and* Reading Time, the system still produces the complete Paper Sheet and Reading List with no initial-read recommendation; this is the specified default behavior.