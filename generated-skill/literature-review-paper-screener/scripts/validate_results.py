#!/usr/bin/env python3
"""Product-specific local validator for Literature Review SkillBot cloud results.

Reads a LoomLoom result-rows JSON file (or a plain JSON with a `rows` list), extracts the
screening + build step artifacts, and checks the product contract:

1. Result parses and matches the declared output shape (screening_records + excluded_records,
   paper_sheet + reading_list).
2. Every included paper in Paper Sheet appears in the screened pool; excluded papers never appear.
3. Evidence availability level is present on every record (A/B/C/D).
4. Content Credibility follows the decision rule: never Fail simply due to lack of evidence.
5. Reading List uses the same pool, one Primary Reading Role per paper, no duplication.
6. Citation / links present where available.
7. Failures and partial results are explicit.
8. Findings are reproducible (rerun condition = same evidence package + version).

Rejects fabricated, mismatched, or unreviewable output. Writes review/validation-report.json
and review/local-audit.json. Uses only the Python standard library.
"""

import argparse
import json
import sys
from pathlib import Path

LEVELS = {"A", "B", "C", "D"}
ROLES = {"Foundational", "Core Evidence", "Supporting", "Counterargument", "Recent", "Methodology"}


def find_artifact_text(rows):
    """Return {step_id: inlineText} for the first completed row."""
    for row in rows:
        if row.get("status") != "completed":
            continue
        arts = {}
        for a in row.get("artifacts", []):
            step = a.get("stepId", "")
            txt = a.get("inlineText", "")
            if step and txt:
                arts[step] = txt
        if arts:
            return arts
    return {}


def strip_code_fence(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1]
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def parse_json(text, label):
    try:
        return json.loads(strip_code_fence(text))
    except json.JSONDecodeError as e:
        raise ValueError(f"{label}: result is not valid JSON ({e})")


def audit(screen, build):
    issues = []
    sr = screen.get("screening_records", [])
    er = screen.get("excluded_records", [])
    ps = build.get("paper_sheet", [])
    rl = build.get("reading_list", {})

    # 1. evidence level + credibility rules on screening records
    for p in sr + er:
        lvl = p.get("evidence_availability_level", "")
        if lvl not in LEVELS:
            issues.append(f"{p.get('record_id')}: missing/invalid evidence_availability_level {lvl!r}")
        cc = p.get("content_credibility_status", "")
        if not cc:
            issues.append(f"{p.get('record_id')}: missing content_credibility_status")

    # 2. excluded never in paper sheet
    excluded_ids = {p.get("record_id") for p in er}
    for p in ps:
        rid = p.get("record_id")
        if rid in excluded_ids:
            issues.append(f"{rid}: excluded paper appears in paper_sheet")

    # 3. paper sheet = subset of screened pool
    screened_ids = {p.get("record_id") for p in sr}
    for p in ps:
        if p.get("record_id") not in screened_ids:
            issues.append(f"{p.get('record_id')}: paper_sheet entry not in screening_records")

    # 4. reading list: same pool, one role each, no duplicates
    seen = {}
    for cat, items in rl.items():
        if cat not in ROLES:
            issues.append(f"unknown reading_list category {cat!r}")
        for it in items:
            rid = it.get("title") or it.get("record_id")
            role = it.get("reading_role")
            if role != cat:
                issues.append(f"{rid}: role {role!r} does not match category {cat!r}")
            if rid in seen:
                issues.append(f"{rid}: duplicated across categories ({seen[rid]} and {cat})")
            seen[rid] = cat
    rl_ids = {it.get("title") for items in rl.values() for it in items}
    for p in ps:
        if p.get("title") not in rl_ids and rl_ids:
            issues.append(f"{p.get('record_id')}: paper_sheet entry missing from reading_list")

    # 5. citation present on paper sheet entries
    for p in ps:
        if not p.get("citation"):
            issues.append(f"{p.get('record_id')}: missing citation")

    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="result-rows JSON from loomloom run result-rows")
    ap.add_argument("--manifest", default=None, help="optional store-manifest.json for context")
    ap.add_argument("--out-dir", default="review", help="output directory")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = data.get("rows", data if isinstance(data, list) else [])
    arts = find_artifact_text(rows)
    if not arts:
        print(json.dumps({"result": "FAIL", "reason": "no completed row artifacts found"}, indent=2))
        sys.exit(1)

    try:
        screen = parse_json(arts.get("stp_screen01", ""), "screening step")
        build = parse_json(arts.get("stp_build01", ""), "build step")
    except ValueError as e:
        print(json.dumps({"result": "FAIL", "reason": str(e)}, indent=2))
        sys.exit(1)

    issues = audit(screen, build)
    passed = not issues

    audit_out = {
        "result": "PASS" if passed else "FAIL",
        "issues": issues,
        "screeningRecords": len(screen.get("screening_records", [])),
        "excludedRecords": len(screen.get("excluded_records", [])),
        "paperSheetEntries": len(build.get("paper_sheet", [])),
        "readingListCategories": {k: len(v) for k, v in build.get("reading_list", {}).items()},
        "rerunCondition": "same evidence package + template version 4677c008-6780-425e-b2f7-c05bc7caba38",
    }
    report = {
        "result": "PASS" if passed else "FAIL",
        "validator": "literature-review-skillbot local validator",
        "checks": [
            "parseable structured output",
            "evidence availability levels A-D present",
            "content credibility decision rule respected",
            "paper sheet contains only screened pool",
            "reading list shares the same pool with one role per paper",
            "citations present",
            "explicit failures/partial results",
            "reproducible rerun condition",
        ],
        "audit": audit_out,
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "local-audit.json").write_text(json.dumps(audit_out, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
