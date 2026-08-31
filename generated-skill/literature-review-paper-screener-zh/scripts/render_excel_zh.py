#!/usr/bin/env python3
"""中文版：把校验通过的云端结果渲染为中文 Excel（论文清单 + 阅读清单）。

读取 loomloom result-rows JSON（每行一篇文献，逐篇执行模式），提取每个已完成行的
stp_build01 产物（paper_sheet + reading_list），合并为一份全局论文清单与阅读清单，
写出两个 .xlsx：

- 论文清单.xlsx — 每篇保留文献一行，完整记录字段（跨所有任务行合并）
- 阅读清单.xlsx — 按六个阅读角色分类组织（跨所有任务行合并）

仅使用 Python 标准库；不依赖 openpyxl（直接写 xlsx 兼容 XML）。
"""

import argparse
import json
import zipfile
from pathlib import Path

ROLES = ["基础文献", "核心证据", "支撑文献", "反方观点", "近期文献", "方法论"]
PAPER_COLS = [
    ("record_id", "记录ID"), ("priority", "优先级"), ("primary_reading_role", "主要阅读角色"),
    ("citation", "引用"), ("title", "标题"), ("authors", "作者"), ("publication_year", "出版年份"),
    ("source_journal_publisher", "期刊/出版方"), ("source_type", "文献类型"), ("doi", "DOI"),
    ("isbn", "ISBN"), ("url", "网址"), ("database_record", "数据库记录"), ("links", "链接"),
    ("evidence_availability_level", "证据可用级别"), ("available_evidence", "已有证据"),
    ("missing_evidence", "缺失证据"), ("assessment_limitations", "评估局限"),
    ("topic_relevance", "主题相关度"), ("source_validity", "来源有效性"),
    ("basic_credibility", "基础可信度"), ("content_credibility_status", "内容可信度"),
    ("recency_status", "时效性"), ("summary", "摘要评价"), ("notes", "备注"),
]
LIST_COLS = [
    ("priority", "优先级"), ("reading_role", "阅读角色"), ("citation", "引用"),
    ("title", "标题"), ("notes", "备注"), ("summary", "摘要评价"), ("links", "链接"),
]


def collect_build_artifacts(rows):
    """返回每个已完成行的 stp_build01 inlineText。"""
    texts = []
    for row in rows:
        if row.get("status") != "completed":
            continue
        for a in row.get("artifacts", []):
            if a.get("stepId") == "stp_build01" and a.get("inlineText"):
                texts.append(a["inlineText"])
                break
    return texts


def strip_fence(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1]
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def merge_builds(texts):
    """把每行构建输出合并为全局 paper_sheet + reading_list。"""
    paper_sheet = []
    reading_list = {}
    for t in texts:
        b = json.loads(strip_fence(t))
        paper_sheet.extend(b.get("paper_sheet", []))
        for cat, items in b.get("reading_list", {}).items():
            reading_list.setdefault(cat, []).extend(items)
    return paper_sheet, reading_list


def xml_escape(v):
    if v is None:
        return ""
    s = str(v)
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def write_xlsx(path, sheets):
    """sheets: list of (sheet_name, headers, rows)。"""
    parts = []
    for idx, (name, headers, rows) in enumerate(sheets, start=1):
        col_letters = [chr(ord("A") + i) if i < 26 else "A" + chr(ord("A") + i - 26) for i in range(len(headers))]
        row_xmls = []

        def emit(r, values):
            cells = []
            for ci, v in enumerate(values):
                cells.append(f'<c r="{col_letters[ci]}{r}" t="inlineStr"><is><t xml:space="preserve">{xml_escape(v)}</t></is></c>')
            row_xmls.append(f'<row r="{r}">{"".join(cells)}</row>')

        emit(1, headers)
        for ri, row in enumerate(rows, start=2):
            emit(ri, row)
        sheet_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f"<sheetData>{''.join(row_xmls)}</sheetData></worksheet>"
        )
        parts.append((name, sheet_xml))

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(parts) + 1))
        + "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>"
        + "".join(f'<sheet name="{xml_escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i, (name, _) in enumerate(parts, start=1))
        + "</sheets></workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(parts) + 1))
        + "</Relationships>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        for i, (_, sheet_xml) in enumerate(parts, start=1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="result-rows JSON（每行一篇；全部行合并）")
    ap.add_argument("--out-dir", default=".", help="输出目录")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = data.get("rows", data if isinstance(data, list) else [])
    texts = collect_build_artifacts(rows)
    if not texts:
        raise SystemExit("未找到 stp_build01 产物")
    paper_sheet, reading_list = merge_builds(texts)

    paper_headers = [zh for _, zh in PAPER_COLS]
    paper_rows = [[p.get(k, "") for k, _ in PAPER_COLS] for p in paper_sheet]
    list_headers = [zh for _, zh in LIST_COLS]
    list_rows = []
    for cat in ROLES:
        for it in reading_list.get(cat, []):
            list_rows.append([it.get(k, "") for k, _ in LIST_COLS])

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paper_path = out_dir / "论文清单.xlsx"
    list_path = out_dir / "阅读清单.xlsx"
    write_xlsx(paper_path, [("论文清单", paper_headers, paper_rows)])
    write_xlsx(list_path, [("阅读清单", list_headers, list_rows)])
    print(f"已写出 {paper_path}（{len(paper_rows)} 行，合并自 {len(texts)} 个任务行）")
    print(f"已写出 {list_path}（{len(list_rows)} 行）")


if __name__ == "__main__":
    main()