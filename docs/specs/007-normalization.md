# Spec 007：标准化规则

## 目的

定义从不同来源解析出的岗位数据如何标准化为稳定字段，减少来源差异对评分和 CSV 输出的影响。

## 范围

包含：

* 岗位 ID 与去重。
* 地点标准化。
* 远程范围标准化。
* 语言要求标准化。
* 薪酬、福利、文本和技能字段整理。
* 风险标记预处理。

不包含：

* 评分权重，见 `008-scoring.md`。
* 最终 CSV 表头，见 `003-csv-output-contract.md`。

## 输入

来自适配器的标准岗位记录，字段见 `002-data-contracts.md` 和 `006-ats-adapters.md`。

## 输出

输出为可评分岗位记录，并最终映射到 `jobs.csv` 字段：

* `job__*`
* `location__*`
* `language__*`
* `comp__*`
* `benefit__*`
* `text__*`
* `skill__*`
* `risk__*`
* `debug__*`

## 标准化规则

### 岗位 ID

`job__id` 生成规则：

```text
<source_id>:<source_job_id>
```

当 `source_job_id` 缺失时：

```text
<source_id>:<hash(job_url|title|location_raw)>
```

### 地点

`location__preference_band` 枚举：

| 值 | 说明 |
| --- | --- |
| `shanghai` | 上海。 |
| `jiangzhehu` | 江苏、浙江、上海周边或明确江浙沪。 |
| `beijing_guangzhou_shenzhen` | 北京、广州、深圳。 |
| `mainland_china_other` | 中国大陆其他城市。 |
| `singapore` | 新加坡。 |
| `asia_other` | 亚洲其他地区。 |
| `western_other` | 欧美澳加等其他地区。 |
| `unknown` | 地点未知。 |

### 远程

`location__remote_type`：

* `onsite`
* `hybrid`
* `remote`
* `unknown`

`location__remote_scope`：

* `china`
* `apac`
* `global`
* `us_eu_only`
* `unknown`

如果岗位写明 Remote 但限制美国或欧盟申请，标记为 `us_eu_only`。

### 语言

`language__category`：

| 值 | 说明 |
| --- | --- |
| `english_chinese` | 英语和中文均友好或需要。 |
| `english_required` | 英语必需。 |
| `english_preferred` | 英语优先或加分。 |
| `unknown` | 未知。 |
| `chinese_only` | 只中文。 |
| `unsupported_language_required` | 用户不会的小语种硬性要求。 |

### 薪酬

薪酬无法可靠解析时保留 `comp__raw`，其他薪酬字段为空。不要为了补全字段臆测薪资。

### 技能

技能命中以标题、描述和要求文本为输入。第一阶段至少识别：

* AI / LLM / Agent / RAG
* ERP / SAP / Odoo / 企业信息化
* BI / 数据分析 / 数据工程
* Python / API
* Integration / Automation

### 风险

第一阶段至少识别：

* 外包
* 派遣
* 纯销售倾向
* 语言硬门槛
* 岗位低相关

风险标记进入 `risk__flags`，扣分规则见 `008-scoring.md`。

## 验收标准

* 原始字段尽量保留，标准字段可为空但不能乱填。
* 未知值统一使用 `unknown` 或空字符串。
* 同一岗位可稳定生成同一 `job__id`。
* 中文和英文关键词都能被识别。
* 标准化输出能完整映射到 CSV 合同。

## 测试要求

后续实现需覆盖：

* 上海、江浙沪、北上广深、中国大陆其他城市、新加坡、未知地点。
* Remote China/APAC、Remote US/EU only、Remote unknown。
* 英中、英语必需、英语优先、只中文、小语种硬门槛。
* 缺少岗位 ID 时 fallback hash 稳定。
* 风险关键词可以进入 `risk__flags`。

