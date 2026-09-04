#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-flight checker for a Literature Evidence Package before pasting into the Cloud.
纯本地，不联网、不收费。
用法: python3 check_evidence.py <证据.json>   (或管道读入)
返回 0 = 就绪；非0 = 列出原因。
"""
import json
import sys

REQUIRED = [
    "record_id", "title", "authors", "publication_year",
    "evidence_availability_level", "metadata_status",
]

def slurp():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        raw = open(sys.argv[1], encoding="utf-8").read()
    else:
        raw = sys.stdin.read()
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").lstrip("json").strip()
    return raw

def main():
    try:
        data = json.loads(slurp())
    except json.JSONDecodeError as e:
        print("无效 — 不是合法 JSON:", e); sys.exit(1)

    issues = []
    rc = data.get("run_context")
    if not isinstance(rc, dict) or not str(rc.get("research_question", "")).strip():
        issues.append("run_context.research_question 为空（必填）。")

    papers = data.get("papers")
    if not isinstance(papers, list) or not papers:
        issues.append("papers 必须是非空数组。")
    else:
        for i, p in enumerate(papers):
            if not isinstance(p, dict):
                issues.append(f"papers[{i}] 不是对象。"); continue
            for k in REQUIRED:
                if not str(p.get(k, "")).strip():
                    issues.append(f"papers[{i}] 缺失/为空 '{k}'.")
            lvl = str(p.get("evidence_availability_level", "")).strip()
            if lvl and lvl[0] not in "ABCD":
                issues.append(f"papers[{i}] 证据级别首字符应为 '{lvl[0]}' （A/B/C/D）。")
    if issues:
        print("无效 — 修正后可提交云端："); [print("  -", x) for x in issues]; sys.exit(1)
    print("OK — 证据包结构就绪（一行一）。")

if __name__ == "__main__":
    main()