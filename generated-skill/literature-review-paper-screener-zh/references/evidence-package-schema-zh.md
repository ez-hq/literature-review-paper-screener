# 证据包结构（本地 → 云端交接）

**一个文件 = 一篇文献（逐篇执行模式）。** 云端模板每个云端任务只筛选一篇文献，因此每个证据文件必须恰好包含一篇文献的记录。每个文件保持云端已验证的形状：一个运行上下文块 + 一个 `papers` 数组，其中**恰好一条**记录。绝不把多篇文献并入一个文件——那会重新引入单任务超时故障（20 篇单行提交的 `StartToClose timeout`）。

- 文件命名：`handoff_p<record_id>.json`（如 `handoff_p001.json`）。
- 每个文件携带**相同的 `run_context`**（完全一致的副本）+ 该篇文献的**唯一**记录。
- 云端读取每行的 `papers[0]`；记录字段必须如实标明可用性；绝不虚构。

## 序列化规则

- 紧凑 JSON（不美化）；key 顺序按本文件所示固定；字节稳定（`ensure_ascii=False`、UTF-8、无尾随空白），同一记录始终序列化为相同字节（可复现条件）。
- 缺失字段用 `""` / `false` / `[]` 补齐，不省略 key。
- **记录文本一律中文。** 文献内容（摘要、全文摘录、结构化信息）保持原文——学术文献多为英文，不要翻译成中文；由本地 Agent 书写的字段（`available_content`、`available_evidence`、`missing_evidence`、`assessment_limitations`、`metadata_gate_notes` 等）用中文。JSON key 是机器协议，保持英文。

## 运行上下文块

```json
{
  "run_context": {
    "research_question": "体育活动对青少年抑郁症状的影响",
    "core_concepts": ["体育活动", "抑郁症状", "青少年"],
    "research_focus": "association",
    "population": "青少年",
    "context": "学校与社区环境"
  }
}
```

这五个 key 是云端已验证的运行上下文形状。可选上下文（限制、作业要求、截止日期、阅读时间、引用数量）通过工作簿字段（作业要求 / 研究限制 等）传给云端——不必重复进证据文件（重复无害但不必要）。

## 单篇记录（papers[0] — 每文件恰好一条）

```json
{
  "run_context": {
    "research_question": "体育活动对青少年抑郁症状的影响",
    "core_concepts": ["体育活动", "抑郁症状", "青少年"],
    "research_focus": "association",
    "population": "青少年",
    "context": "学校与社区环境"
  },
  "papers": [
    {
      "record_id": "C001",
      "title": "Physical Activity, Sedentary Behavior, and Depressive Symptoms Among Adolescents",
      "authors": "Hume, C.; Timperio, A.; Veitch, J.; Salmon, J.; Crawford, D.; Ball, K.",
      "publication_year": 2011,
      "source_journal_publisher": "Journal of Physical Activity and Health",
      "source_type": "同行评审期刊论文",
      "doi": "10.1123/jpah.8.2.152",
      "isbn": "",
      "url": "https://doi.org/10.1123/jpah.8.2.152",
      "database_record": "Crossref; 10.1123/jpah.8.2.152",
      "abstract": "未获取到摘要",
      "available_content": {
        "full_text_available": false,
        "sections_available": [],
        "methods_info": "",
        "key_findings": "",
        "results_info": "",
        "conclusion": ""
      },
      "links": ["https://doi.org/10.1123/jpah.8.2.152"],
      "evidence_availability_level": "D",
      "available_evidence": "仅通过 Crossref 核验的文献元数据（标题/年份/期刊/作者与 DOI 一致）",
      "missing_evidence": "摘要与全文均未提供",
      "assessment_limitations": "仅含元数据，无内容可评估，评估深度受限",
      "metadata_status": "VERIFIED",
      "metadata_gate_notes": "DOI 在 Crossref 解析成功；标题/年份/期刊/作者与记录一致。VERIFIED。"
    }
  ]
}
```

> 上述 `run_context` 在每个单篇文件中完全相同地重复。`papers` 数组恰好一条记录——即本文件的文献。（前面的独立 `run_context` 块是每个文件内嵌的共享副本。）

> `metadata_status` 由本地**元数据校验门**（references/metadata-validation-gate-zh.md）产出——只允许 `VERIFIED` 或 `PARTIALLY VERIFIED`。PARTIALLY VERIFIED 的记录把每个无法核验的标识符标为 `NOT VERIFIED`（如 `"doi": "NOT VERIFIED"`）。MISMATCH / INVALID 的记录绝不会到达本文件。云端忽略此字段——它只评估证据内容。

## 证据可用级别划分

| 级别 | 记录包含 |
|---|---|
| A | 全文，或大量全文内容（方法、结果、讨论、结论） |
| B | 摘要 + 大量结构化信息 |
| C | 标题 + 元数据 + 摘要 |
| D | 仅标题、作者、年份、期刊/出版方 |

不要强求每篇都有全文。付费墙、无开放获取、访问限制、PDF 获取失败都是预期情况；它们降低级别，绝不决定文献的命运。