# Evidence package schema (local → cloud handoff)

The handoff is one JSON object with a run context block and a papers array. Every paper record must
carry all available fields with explicit availability; never fabricate values.

## Run context block

```json
{
  "run_context": {
    "research_question": "...",
    "core_concepts": ["..."],
    "research_focus": "effect|impact|association|relationship|comparison|mechanism",
    "population": "...",
    "context": "...",
    "restrictions": "...",
    "assignment_requirements": "...",
    "deadline": "...",
    "reading_time": "...",
    "citation_count": "..."
  }
}
```

## Paper record

```json
{
  "record_id": "P001",
  "title": "...",
  "authors": "...",
  "publication_year": 2021,
  "source_journal_publisher": "...",
  "source_type": "peer-reviewed journal article",
  "doi": "...",
  "isbn": "",
  "url": "...",
  "database_record": "PMID: ...; PubMed",
  "abstract": "...",
  "available_content": {
    "full_text_available": true,
    "sections_available": ["introduction", "methods", "results", "discussion", "conclusion"],
    "methods_info": "...",
    "key_findings": "...",
    "results_info": "...",
    "conclusion": "..."
  },
  "links": ["https://doi.org/..."],
  "evidence_availability_level": "A",
  "available_evidence": "...",
  "missing_evidence": "...",
  "assessment_limitations": "..."
}
```

## Evidence Availability Level assignment

| Level | Package contains |
|---|---|
| A | Full text, or substantial full-paper content (Methods, Results, Discussion, Conclusion) |
| B | Abstract + substantial structured information |
| C | Title + metadata + Abstract |
| D | Title, authors, year, journal/publisher only |

Do not require full text for every paper. Paywalls, no open access, access restrictions, and PDF
retrieval failures are expected; they lower the level, never the paper's fate.
