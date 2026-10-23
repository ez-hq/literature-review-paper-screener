---
name: literature-review-paper-screener-zh
version: 1.5.0
description: >-
  文献智筛（中文版）V1.4.6。本地 Agent（可联网、免费）检索文献、采集证据、构建带证据可用级别（A-D）的单篇证据记录，
  提交给私有的胜算云云端模板进行全中文筛选，再校验并合并云端结果，输出中文论文清单与阅读清单 Excel。云端无互联网，
  只评估收到的证据；本地负责检索与采集。仅文献综述任务类型；医学科学方向。中文版仅使用胜算云平台（人民币支付）。
  包内文件仅为本机辅助脚本（输入预检、结果校验、Excel 渲染），不联网、不调用云端、不做筛选；
  检索、下载与云端提交均由 Agent 通过本技能声明的 loomloom 命令行完成。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - loomloom
    homepage: https://github.com/ez-hq/literature-review-paper-screener/releases
---

# 文献智筛（中文版）— 本地 Agent 技能

**本地 Agent** 是文献智筛的互联网调研层：你有互联网访问权限，负责全部检索与证据采集。**云端**（私有胜算云模板）没有互联网，只对你提交的证据进行筛选与组织。

> **核心原则：本地采集证据，云端评估与组织证据。**（产品完整规则见项目文档集；本技能是可执行指南。）

## 一项任务的含义与执行方式

一项任务 = 一次完整的文献综述，交付：

- **论文清单（Paper Sheet）** — 完整筛选后的文献池，每篇保留文献一行（证据级别、筛选结论、优先级、阅读角色、备注与摘要评价）
- **阅读清单（Reading List）** — 同一文献池按优先级与主要阅读角色组织

**执行模型（每篇一行）**：云端模板的筛选步骤有平台固定的单活动超时。把 N 篇文献塞进一个活动会在较大规模时超时（实测：20 篇 → `StartToClose timeout` 失败两次）。因此中文版采用**每行一篇**：N 篇 = N 行 = N 个并行云端任务，每个任务在数秒内完成单篇筛选，结果在**本地合并**为一份论文清单与阅读清单。

- 绝不要把多篇文献的证据放进同一行。
- 云端任务数 = 文献篇数 = 计费单位数（胜算云：¥0.70/任务）。
- 合并只发生在本地：云端不做聚合步骤，不做二次推导。

## 前置条件

- Python 3.9+（校验/渲染脚本）
- `loomloom` 技能与命令行已安装，`loomloom doctor` 报告 `healthy=true`
- 胜算云账户（人民币充值）有余额用于云端运行

## 开始之前：选择语言与支付渠道

你装的是**中文包（-zh）**，默认输出**简体中文**（英文包 `-en` 默认英文）。**运行前先与用户确认交付语言**：若作业要求其他语言，保留本包并按作业要求书写交付的评价与摘要（见第 5 步语言规则）；若用户希望全程以英文为默认，可改用 `-en` 包。
支付/运行渠道：
- 国内 / 人民币：胜算云，¥0.7 / 次；
- 海外 / 美元：CogFoundry，USD 0.10 / 次。

> ⚠️ 模板**必须有输入文本**（文献证据包，一行一篇）；**云端无网络访问**，只评估你提交的内容。
> 完整本地包（-zh / -en）在 GitHub：https://github.com/ez-hq/literature-review-paper-screener/releases

## 工作流

### 0. 云端上手（强制 — 开工前必须先说清）

**本 Skill 必须走 LoomLoom 云端完成文献筛选，没有纯本地模式。**
开始任何工作前，你必须先向用户说明以下全部内容，并确认用户愿意走付费云端路径：

1. **必须用云端**：本地部分只做检索与证据采集，真正的筛选在 LoomLoom 云端执行，是**付费**服务。
2. **必须先装 LoomLoom**（Skill 不会自动安装）。由**用户自己在终端安装**（agent 不执行全局安装）：
   ```bash
   npm install -g @cogfoundry/loomloom
   ```
   装好后验证：`loomloom doctor --output json`，须为 `healthy=true`。
3. **需要 LoomLoom 账号**：在所选平台（中文场景用胜算云）按平台自己的注册流程开通账号。
4. **用户用 `loomloom login` 交互式登录** — agent 不接触、不保存用户凭据。
5. **费用**：胜算云 ¥0.70/任务、CogFoundry $0.10/任务；费用与余额走平台自己的支付流程。运行前必须把预估费用报给用户并确认。

> 若用户不愿安装、无账号或不接受付费云端：停下并说明本 Skill 无法完成筛选，**不得**用其他方式替代。

### 1. 安装/验证 loomloom

```bash
loomloom doctor --output json
```

若 `healthy=false`，先完成认证（优先浏览器登录：`loomloom login`；或平台控制台获取 API token）。Doctor 不健康前不得进入云端步骤。

### 1.5 平台说明（中文版固定使用胜算云）

中文版技能**仅使用胜算云**（人民币支付，云端模板为全中文输出）。若用户坚持使用 CogFoundry：明确提示——CogFoundry 模板为英文输出约束，结果可能为英文，建议中文场景一律走胜算云。

```bash
loomloom server list
loomloom server use shengsuanyun
loomloom doctor --output json
```

### 2. 了解市场 Listing（买家路径，不要臆造 ID）

本 Skill 通过**市场 Listing** 运行（买家自己的账号付费），不走私有模板：

| 平台 | Listing ID | 市场费用 |
|---|---|---|
| 胜算云（中文版默认） | `01a0465b-5d0e-7279-bcea-f206544521b0` | ¥0.70 / 任务 |
| CogFoundry（国际） | `01a0423e-fdcd-7428-b388-4711b67b0e03` | $0.10 / 任务 |

用 `loomloom market workbook download <Listing ID>` 核实绑定。绑定变更时询问所有者，绝不猜 ID。

### 3. 收集用户输入（对话式）

一次一个问题，用通俗中文提问（除主题外均可选）：

1. **研究问题 / 主题** — 必填
2. 引用数量 — 可选（仅参考）
3. 作业要求（任务说明、评分标准、字数、目标人群等）— 可选
4. 研究限制（人群、国家/地区、时间段、文献类型、年份）— 可选
5. 截止日期 — 可选（仅阅读建议）
6. 可阅读时间 — 可选

缺失的可选项不要阻塞；跳过时使用默认规则。主题过于含糊时，先提**一个**澄清问题，然后按已有信息继续。

### 4. 检索文献（本地、可联网）

按检索工作流规则（见 references/architecture-zh.md）：

- 依据可用输入构建检索画像；绝不虚构用户未提供的限制。
- 把问题拆解为核心概念、研究重点、人群、背景。
- 构建关键词表（同义词、替代术语、学术用语）。
- 生成多组检索式（直接、关系、术语扩展、人群/背景）。
- 执行检索；最大化召回；检索阶段**不做质量筛选**。
- 做覆盖检查；新检索不再带来新文献时停止。
- 合并为**主候选池**，再按 DOI/入藏号/标题**去重**得到**唯一候选池**。

### 5. 采集证据并生成单篇证据记录

对每篇唯一候选，尽量采集：

- 书目元数据（标题、作者、年份、期刊/出版方、文献类型、DOI、ISBN、稳定链接、数据库记录）
- 摘要
- 可得内容：尽量全文；否则章节（引言/方法/结果/讨论/结论）或结构化信息（方法信息、关键发现、结果信息、结论信息、数据库记录详情）
- 稳定链接（论文链接、DOI 链接、数据库记录、出版方页面）

然后为每篇文献分配**一个证据可用级别**：

| 级别 | 记录包含 |
|---|---|
| A | 全文，或大量全文内容（方法、结果、讨论、结论） |
| B | 摘要 + 大量结构化信息（方法信息、关键发现、结果、结论、详细数据库记录） |
| C | 标题 + 元数据 + 摘要 |
| D | 仅标题、作者、年份、期刊/出版方 |

每篇记录：已有证据、缺失证据、评估局限。**不得虚构证据**；**不必要求每篇都有全文**；获取失败只降低级别。

**输出 = 每篇一个独立的 JSON/文本文件**（单篇证据记录，形状见 references/evidence-package-schema-zh.md），命名如 `handoff_p001.json`…`handoff_pNNN.json`。**一个文件必须恰好包含一篇文献的记录**——这是单篇云端任务足够小、能在平台活动超时内完成的关键。禁止把多篇合并进一个文件。

**语言规则：证据记录默认中文。**

- **默认**：由本地 Agent 书写的字段默认中文：`available_content`、`available_evidence`、`missing_evidence`、`assessment_limitations`、`metadata_gate_notes` 及备注。该默认值来自本包绑定的云端模板（全中文输出约束），中文输入可保证云端摘要/备注、论文清单与阅读清单口径一致。
- **可覆盖**：作业要求优先于默认值。若用户作业要求以其他语言交付评价与摘要，就用该语言书写这些字段并在交接备注中说明；用户直接要求更换输出语言时同样照办，并记录所用语言。
- 文献标题（`title`）保留原文：中文文献用中文名，英文文献保留英文标题——这是引用原文，不属于语言夹杂。
- JSON 的 key（`run_context`、`papers`、`record_id` 等）是机器协议，保持英文；**值**用默认或约定语言。
- 若需要以英文为默认的包，请安装 `-en` 英文包。

### 5.5 元数据校验门（强制，写入 handoff 前）

任何单篇记录写成 `handoff_p<record_id>.json` 之前，必须执行**元数据校验门**（见 references/metadata-validation-gate-zh.md），依据权威来源（PubMed / Crossref）校验。本门只校验**书目身份**——绝不触碰检索逻辑、筛选逻辑、CRAAP、主题相关度、阅读角色、优先级、云端 DAG 或工作簿批处理。

- 每篇唯一候选恰好得到一个结果：`VERIFIED` | `PARTIALLY VERIFIED` | `MISMATCH` | `INVALID`（状态值保留英文，记录到 JSON 中）。
- **VERIFIED / PARTIALLY VERIFIED** → 可继续；在记录中写入 `"metadata_status": "VERIFIED"|"PARTIALLY VERIFIED"`，并把无法核验的标识符显式标为 `NOT VERIFIED`。
- **MISMATCH / INVALID** → 该记录在 `handoff_p<record_id>.json`、云端上传、筛选、最终交付之前**一律拦截**，退回证据采集（第 5 步）复核；绝不猜测、推断或用语义相似度修复身份。复核仍无法确认身份的，把冲突值提交给所有者决定保留/剔除（丢弃时记录原因）。
- 无 DOI/PMID 且权威库查无的记录：保留为 `PARTIALLY VERIFIED`、标识符标 `NOT VERIFIED`，绝不静默丢弃，并在校验台账与交付摘要中标注供所有者知晓。
- 维护每轮校验台账（记录ID → 状态 → 核查项 → 结果说明）。
- 核心原则：**摘要正确 ≠ 文献记录正确。**证据内容与书目身份分开校验。

> 可选：粘贴前先本地 `python3 scripts/check_evidence.py 证据.json` 预检，抓格式错误（不联网）。
## 包内文件与各自职责

本包含文档与三个本机辅助脚本。它们都不联网、不调用云端、不做筛选：

| 路径 | 是什么 | 联网 |
|---|---|---|
| `README-zh.md`、`LICENSE` | 包来源与许可 | 否 |
| `references/architecture-zh.md` | 检索与证据采集规则 | 否 |
| `references/evidence-package-schema-zh.md` | 交给云端的单篇证据记录形状 | 否 |
| `references/metadata-validation-gate-zh.md` | 写入交接前的书目身份校验 | 否 |
| `agents/openai.yaml` | 供读取 agent 描述符的平台使用的元数据 | 否 |
| `scripts/check_evidence.py` | 本地预检：粘贴前校验单篇证据记录的 JSON 与字段 | 否 |
| `scripts/validate_results.py` | 本地校验：合并每行结果并检查产品契约 | 否 |
| `scripts/render_excel_zh.py` | 本地渲染：写出中文论文清单与阅读清单 | 否 |

检索、证据采集、元数据校验门、填写工作簿与云端提交，均由 **Agent** 使用自身工具加本技能
frontmatter 中声明的 `loomloom` 命令行完成，并非由包内脚本实现。

**这些脚本读写的文件。** 读取：传给 `--input` 的云端结果导出（`result-rows.json`），以及输入预检
用到的单篇证据 JSON。写出：审计产物 `review/local-audit.json` 与 `review/validation-report.json`，
以及 `--out-dir` 下的交付文件 `论文清单.xlsx`、`阅读清单.xlsx`。除此之外不读写任何文件、不发起
网络请求；其他路径均不在本技能范围内。

### 5.6 什么会离开你的机器（云端交接、隐私与数据最小化）

第 1 至 5.5 步（检索、证据采集、元数据校验门、输入预检）全部在本机完成。第 6 步的交接是数据
唯一离开本机的地方。粘贴或上传之前：

1. **先披露再发送**：用通俗语言告诉用户哪个平台会收到数据、它是第三方云服务、本次运行的费用。
   仅确认"平台与费用"不等于同意传输数据——数据外发必须单独取得同意。
2. **最小化发送内容**：只发送筛选所需字段（见 `references/evidence-package-schema-zh.md`）。从
   载荷中剔除其他一切内容——姓名、学号、邮箱、电话、住址、证件号、成绩，以及任何其他个人或可
   识别信息。若研究问题或作业要求本身含此类信息，先替换为中性占位符再上云，并告知用户已做替换。
3. **本地替代方案**：直到证据记录、校验台账与输入预检为止，全部本地且免费。若用户不同意把数据
   发往第三方云端，就停在这里，交付本地产物（单篇证据记录 + 校验台账），并明确说明未运行云端
   筛选、因此未生成论文清单与阅读清单。绝不擅自外发，也绝不拿本地猜测冒充筛选结果。
4. **载荷中不含凭据**：任何交接载荷都不得包含 API token、密钥或账号标识。

### 6. 准备云端工作簿（每行一篇）

下载该 Listing 的输入工作簿：

```bash
# 胜算云（中文版默认）
loomloom market workbook download 01a0465b-5d0e-7279-bcea-f206544521b0 --output-file input.xlsx -s https://loomloom.shengsuanyun.com/loom/v1
# CogFoundry（国际）
loomloom market workbook download 01a0423e-fdcd-7428-b388-4711b67b0e03 --output-file input.xlsx -s https://loomloom.cogfoundry.ai/loom/v1
```

**先删除工作簿自带的示例行**（否则会被当作额外付费任务提交）。填完后核对：数据行数 = 文献篇数。

**每篇文献一行**（N 篇 → N 行）：

- `研究问题 / 主题` — 每行填写相同的主题文本（必填）
- `作业要求`、`研究限制` — 可选；提供时每行相同
- `引用数量`、`截止日期`、`可阅读时间` — 可选（仅上下文）
- `筛选模型` — 从批准列表选择一次；默认即可
- `文献证据包（粘贴）` — **把该篇证据记录以紧凑单行 JSON 粘贴到单元格**（胜算云 v2 语法无文本上传端口；Excel 单元格上限 32767 字符，单篇紧凑记录 1-3KB 安全；超过约 25000 字符需压缩内容）

每行证据必须对应**不同的单篇记录**（不同行粘贴不同的单篇 JSON）。禁止在每行复用同一个多篇合并包（会重新引入超时）。

### 7. 校验与预检（只读）

```bash
loomloom market workbook validate <Listing ID> --file input.xlsx -s <所选平台服务器>
loomloom market workbook quote    <Listing ID> --file input.xlsx -s <所选平台服务器>
```

提交前向所有者展示（全部来自 quote 返回值）：

- 任务数 = **文献篇数 N**（= `taskCount`，必须与工作簿数据行数一致）
- 每任务费用（胜算云 ¥0.70 / CogFoundry $0.10）与**总费用 = 单价 × N**（`task_fixed_fee` × N）
- 加上模型执行成本估算（`estimated_execution_cost`）、余额与是否充足

**此时不要提交。**

### 8. 确认运行（平台 + 费用 + 篇数锁定）

提交前先与所有者**再次确认平台与费用**：**"平台：胜算云（人民币，¥0.70/任务）。N 篇 → N 个云端任务 → 总费用 ≈ 0.70 × N + 模型成本。确认？"** 行数即篇数锁：任务数（与计费单位数）在提交前确定，运行中不可更改。同时核验 `loomloom doctor` 的当前 profile 为胜算云。然后：

```bash
# 胜算云（中文版默认）
loomloom market workbook run 01a0465b-5d0e-7279-bcea-f206544521b0 --file input.xlsx --confirm --client-request-id <新UUID> -s https://loomloom.shengsuanyun.com/loom/v1
# CogFoundry（国际）
loomloom market workbook run 01a0423e-fdcd-7428-b388-4711b67b0e03 --file input.xlsx --confirm --client-request-id <新UUID> -s https://loomloom.cogfoundry.ai/loom/v1
```

保存返回的 `run_id`。监视并取回**全部**任务结果：

```bash
loomloom run watch <run-id>
loomloom run result-rows <run-id> --output result-rows.json
loomloom run result-workbook <run-id> --output-file results.xlsx
```

每次运行都要自己的确认与自己的 client-request-id。输入在确认后变更的，重新校验、重新预检、展示新估算、取得新确认。某行任务失败/超时，只单独重试该行——不要"合并"文献重试。

### 9. 本地校验（强制 — 合并）

对返回的结果运行校验器（自动把所有单篇任务输出合并为一个全局筛选池）：

```bash
python3 scripts/validate_results.py --input result-rows.json --manifest ../store-manifest.json --out-dir ../review
```

必须 PASS 才能渲染或宣称成功。校验器检查：每个已完成行的结构化输出可解析、证据可用级别、内容可信度决策规则、被排除文献绝不进论文清单、论文清单与阅读清单同池、每篇恰好一个主要阅读角色、跨行记录ID无重复、引用存在、失败/部分结果显式化、可复现条件。发现问题不要编造修复——记录并报告所有者。

### 10. 渲染与交付（中文）

对校验后的结果运行中文渲染器（把所有任务行的输出合并为一份中文论文清单 + 一份中文阅读清单）：

```bash
python3 scripts/render_excel_zh.py --input result-rows.json --out-dir <交付目录>
```

交付：论文清单（完整筛选池，每篇保留文献一行）+ 阅读清单（同一池按优先级与阅读角色组织）Excel 文件，外加简短中文总结：检索、筛选、纳入、排除（含原因）各多少篇，证据级别分布（A/B/C/D），跑了多少个云端任务。指出证据受限文献（C/D 级）与初步分类。

**交付前，验证产物语言与约定一致**（默认中文；作业要求指定其他语言时以作业要求为准）——扫描渲染数据与 handoff，除协议字段（JSON key、A/B/C/D 字母、pass/fail、DOI/ISBN/URL、文献标题原文）外，不得出现与约定语言不符的成句文本或语言混杂；发现则回到第 5 步（证据采集）重写相应字段并重跑受影响阶段：

```bash
# 快速检查：打印含大量英文单词（非协议字段）的文本所在位置
python3 -c "
import sys, json, re
for f in sys.argv[1:]:
    d = json.load(open(f, encoding='utf-8'))
    def scan(o, path=''):
        hits = []
        if isinstance(o, dict):
            for k, v in o.items(): hits += scan(v, path+'/'+k)
        elif isinstance(o, list):
            for i, v in enumerate(o): hits += scan(v, path+f'[{i}]')
        elif isinstance(o, str) and re.search(r'[\u4e00-\u9fff]', o) and len(re.findall(r'[A-Za-z]{4,}', o)) > 3:
            hits.append(path)
        return hits
    print(f, '-> 混排字段:', scan(d) or 'OK')
" result-rows.json handoff_p*.json
```

## 运行规则

- **每次云端运行（含测试与验证运行）前必须先确认平台与费用。** 中文版固定胜算云（¥0.70/任务）；不得默认使用当前 profile 而不询问；任何运行（测试或正式）都不得跳过"平台 + 费用 + 篇数"确认仪式。确认必须在展示数字之后由用户给出：沉默、上一次运行的同意、或早先的平台选择都不构成确认；用户未回应则不得提交。未经询问就花钱的运行是违规，不是内部捷径。
- **每行一篇 / 每个云端任务一篇。** 绝不把多篇证据塞进一个文件或一行；多篇单行会在平台超时（v1.1 起按设计规避）。某行失败/超时，单独重试该行。
- 云端**无互联网**：它只评估你提交的证据。绝不让它搜索、抓取、打开网址，绝不声称它审阅了你未提供的全文。
- **证据可用性 ≠ 质量。** C/D 级文献不是质量更低，而是评估更浅，必须标注而不是剔除。
- **广泛检索、谨慎筛选、保留全部合格文献。** 截止日期/阅读时间/引用数量只影响先读什么，绝不从输出中移除文献。
- 被排除文献绝不进入论文清单或阅读清单。
- **产出语言遵循第 5 步的语言规则**（默认中文；作业要求指定其他语言时以作业要求为准）。协议字段与文献标题原文除外；不要让对话语言静默改变记录语言，若与约定语言不一致，先说明再继续。
- 绝不暴露 loomloom token、原始用户数据或私有云端模板的内容。
- loomloom 依赖缺失或 Doctor 不健康时，停止云端阶段并报告 `BLOCKED`——不要臆造命令或远程创建状态。