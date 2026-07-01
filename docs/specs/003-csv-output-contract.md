# Spec 003：CSV 输出合同

## 目的

定义 `outputs/runs/<timestamp>/jobs.csv` 的稳定表头、字段含义、排序规则和兼容性要求，确保人工审核、测试和后续数据库导入都基于同一份合同。

## 范围

包含：

* 输出路径。
* CSV 编码和格式。
* 表头顺序。
* 字段含义。
* 空结果行为。
* 排序与兼容性规则。

不包含：

* 输入 CSV 合同，见 `002-data-contracts.md`。
* 评分细则，见 `008-scoring.md`。
* 爬取策略，见 `005-crawl-policy.md`。

## 输入

来自标准化和评分后的岗位记录：

* 公司信息。
* 来源信息。
* 岗位信息。
* 地点、语言、薪酬、技能、风险和评分信息。

## 输出

输出文件：

```text
outputs/runs/<timestamp>/jobs.csv
```

CSV 格式：

* 编码：UTF-8 with BOM 可接受；默认 UTF-8。
* 分隔符：`,`。
* 换行：平台默认可接受；测试中按标准 CSV 解析。
* 首行必须为表头。
* 一行代表一个岗位。
* 字段内换行、逗号、引号必须按 CSV 标准转义。
* 空值输出为空字符串，不输出 `None`、`null`、`NaN`。

### 表头顺序

第一阶段表头固定如下：

| 顺序 | 字段 | 类型 | 说明 |
| --- | --- | --- | --- |
| 1 | `run__id` | string | 本次运行 ID，通常等于 timestamp。 |
| 2 | `run__timestamp` | datetime | 本次运行时间。 |
| 3 | `run__date` | date | 本次运行日期。 |
| 4 | `source__id` | string | 来源 ID。 |
| 5 | `source__type` | enum | 来源类型。 |
| 6 | `source__name` | string | 来源名称。 |
| 7 | `source__url` | url | 来源 URL。 |
| 8 | `source__status` | enum | `ok`、`empty`、`failed`、`manual_review`、`skipped`。 |
| 9 | `source__fetched_at` | datetime | 抓取或读取时间。 |
| 10 | `company__id` | string | 公司 ID。 |
| 11 | `company__name` | string | 公司正式名称。 |
| 12 | `company__display_name` | string | 公司展示名。 |
| 13 | `company__type` | enum | 公司性质。 |
| 14 | `company__industry` | string | 行业。 |
| 15 | `company__hq_country` | string | 总部国家或地区。 |
| 16 | `company__is_multinational` | boolean | 是否跨国或明显国际化。 |
| 17 | `company__career_url` | url | 公司招聘主页。 |
| 18 | `job__id` | string | 系统内岗位 ID。 |
| 19 | `job__source_job_id` | string | 来源岗位 ID。 |
| 20 | `job__url` | url | 岗位详情 URL。 |
| 21 | `job__title` | string | 岗位标题。 |
| 22 | `job__department` | string | 部门。 |
| 23 | `job__employment_type` | string | 全职、合同、实习等。 |
| 24 | `job__seniority` | string | 经验层级。 |
| 25 | `job__published_at` | datetime | 发布时间。 |
| 26 | `job__updated_at` | datetime | 更新时间。 |
| 27 | `job__is_active` | boolean | 是否仍有效。 |
| 28 | `location__raw` | string | 原始地点文本。 |
| 29 | `location__country` | string | 标准化国家或地区。 |
| 30 | `location__region` | string | 标准化区域，如 APAC、Mainland China。 |
| 31 | `location__city` | string | 标准化城市。 |
| 32 | `location__district` | string | 区县或片区。 |
| 33 | `location__remote_type` | enum | `onsite`、`hybrid`、`remote`、`unknown`。 |
| 34 | `location__remote_scope` | enum | `china`、`apac`、`global`、`us_eu_only`、`unknown`。 |
| 35 | `location__preference_band` | enum | 用户地区偏好档位。 |
| 36 | `language__raw` | string | 原始语言要求。 |
| 37 | `language__category` | enum | 语言评分分类。 |
| 38 | `language__english_required` | boolean | 是否明确要求英语。 |
| 39 | `language__chinese_required` | boolean | 是否明确要求中文。 |
| 40 | `comp__raw` | string | 原始薪酬文本。 |
| 41 | `comp__currency` | string | 币种。 |
| 42 | `comp__min` | number | 薪酬下限。 |
| 43 | `comp__max` | number | 薪酬上限。 |
| 44 | `comp__period` | enum | `year`、`month`、`day`、`hour`、`unknown`。 |
| 45 | `benefit__raw` | string | 原始福利文本。 |
| 46 | `benefit__highlights` | string | 关键福利摘要，分号分隔。 |
| 47 | `text__summary` | string | 岗位简要摘要，可为空。 |
| 48 | `text__description` | string | 岗位描述。 |
| 49 | `text__requirements` | string | 岗位要求。 |
| 50 | `skill__matched_keywords` | string | 命中关键词，分号分隔。 |
| 51 | `skill__ai` | boolean | 是否命中 AI/LLM/Agent/RAG。 |
| 52 | `skill__erp` | boolean | 是否命中 ERP/SAP/Odoo/企业信息化。 |
| 53 | `skill__bi` | boolean | 是否命中 BI/数据分析/数据工程。 |
| 54 | `skill__python_api` | boolean | 是否命中 Python/API。 |
| 55 | `skill__integration` | boolean | 是否命中 Integration/Automation。 |
| 56 | `risk__flags` | string | 风险标记，分号分隔。 |
| 57 | `risk__outsourcing` | boolean | 是否疑似外包。 |
| 58 | `risk__staffing` | boolean | 是否疑似派遣。 |
| 59 | `risk__sales_heavy` | boolean | 是否偏纯销售。 |
| 60 | `risk__language_barrier` | boolean | 是否存在语言硬门槛。 |
| 61 | `risk__low_relevance` | boolean | 是否明显低相关。 |
| 62 | `score__location` | number | 地区分。 |
| 63 | `score__company` | number | 公司性质分。 |
| 64 | `score__role` | number | 岗位类别分。 |
| 65 | `score__language` | number | 语言分。 |
| 66 | `score__skill` | number | 技能分。 |
| 67 | `score__risk` | number | 风险扣分，通常为 0 或负数。 |
| 68 | `score__total` | number | 总分，0 到 100。 |
| 69 | `score__reasons` | string | 可读评分理由，分号分隔。 |
| 70 | `debug__adapter` | string | 使用的适配器。 |
| 71 | `debug__raw_hash` | string | 原始数据 hash。 |
| 72 | `debug__missing_fields` | string | 缺失字段，分号分隔。 |
| 73 | `debug__notes` | string | 调试备注。 |
| 74 | `job__apply_url` | url | 直接投递 URL；未知时为空。为兼容性追加在表头末尾。 |
| 75 | `score__recommendation` | enum | 推荐档位，如 `strong_match`、`match`、`maybe`、`low_priority`。 |
| 76 | `debug__parse_confidence` | number | 解析置信度，范围 0 到 1；未知时为空。 |

### 排序规则

* 默认按 `score__total` 降序。
* 总分相同按 `score__location` 降序。
* 仍相同按 `company__display_name`、`job__title` 升序。

### 空结果

当没有岗位或所有来源失败时，仍必须输出 `jobs.csv`，且只包含表头。

### 兼容性

* 表头新增字段只能追加到末尾。
* 已发布字段不得改名或改变含义。
* 枚举新增值需要同步更新对应 spec 和测试。

## 验收标准

* 输出路径符合 `outputs/runs/<timestamp>/jobs.csv`。
* 表头与本 spec 完全一致，顺序稳定。
* 一行只代表一个岗位。
* 空结果也有表头。
* 分数字段可被表格软件识别为数字。
* 布尔字段统一输出 `true`、`false` 或空字符串。

## 测试要求

后续实现需覆盖：

* 表头快照测试。
* 空结果 CSV 测试。
* 包含逗号、引号、换行的文本字段转义测试。
* 排序测试。
* 空值不输出 `None/null/NaN`。
* `score__total` 范围为 0 到 100。
