# Spec 002：数据合同

## 目的

定义第一阶段所有输入 CSV、配置 CSV 和内部标准记录的字段合同，为后续实现、测试和人工审核提供稳定依据。

## 范围

包含：

* 公司种子表合同。
* 招聘来源表合同。
* 评分配置表合同。
* 适配器输出的标准岗位记录合同。

不包含：

* 最终 `jobs.csv` 宽表字段，见 `003-csv-output-contract.md`。
* 具体爬取实现。
* 数据库存储模型。

## 输入

### `data/seeds/companies_50.csv`

必需字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `company_id` | string | 是 | 稳定唯一 ID，建议小写 snake_case。 |
| `company_name` | string | 是 | 公司正式名称。 |
| `company_display_name` | string | 否 | 输出展示名；为空时使用 `company_name`。 |
| `company_type` | enum | 是 | 见公司类型枚举。 |
| `industry` | string | 否 | 行业，如 SaaS、AI、制造、咨询。 |
| `hq_country` | string | 否 | 总部国家或地区。 |
| `priority` | integer | 否 | 人工关注优先级，1 最高；为空表示普通。 |
| `career_url` | url | 否 | 公司招聘主页。 |
| `notes` | string | 否 | 人工备注，不进入评分核心。 |

`company_type` 枚举：

| 值 | 说明 |
| --- | --- |
| `foreign_mnc` | 外资跨国公司。 |
| `foreign_tech_saas` | 外资科技或 SaaS 公司。 |
| `joint_venture` | 合资企业。 |
| `china_global` | 中国出海公司。 |
| `china_bigtech_ai` | 中国大厂或 AI 公司。 |
| `china_quality_enterprise_it` | 中国优质甲方信息化岗位所在公司。 |
| `private_company` | 普通民企。 |
| `state_owned` | 国企。 |
| `outsourcing_staffing` | 外包或派遣供应商。 |
| `unknown` | 暂无法判断。 |

### `data/sources/company_sources.csv`

必需字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source_id` | string | 是 | 稳定唯一 ID。 |
| `company_id` | string | 是 | 关联 `companies_50.csv.company_id`。 |
| `source_type` | enum | 是 | 招聘源类型，见 `004-company-source-model.md`。 |
| `source_name` | string | 是 | 来源展示名。 |
| `source_url` | url | 是 | 公开招聘源 URL。 |
| `adapter` | enum | 是 | `greenhouse`、`lever`、`ashby`、`smartrecruiters`、`json_ld`、`static_html`、`manual_review`。 |
| `enabled` | boolean | 是 | `true` 或 `false`。 |
| `crawl_priority` | integer | 否 | 越小越优先。 |
| `notes` | string | 否 | 人工备注。 |

### `data/config/*.csv`

配置表使用 UTF-8、逗号分隔、首行为表头。空值表示未知，不表示 0。

| 文件 | 必需字段 | 说明 |
| --- | --- | --- |
| `location_scores.csv` | `location_category`,`patterns`,`score`,`notes` | 地区评分。 |
| `remote_scores.csv` | `remote_scope`,`score`,`notes` | 远程申请范围评分。 |
| `company_type_scores.csv` | `company_type`,`score`,`notes` | 公司性质评分。 |
| `role_scores.csv` | `role_category`,`keywords`,`score`,`notes` | 岗位类别评分。 |
| `language_scores.csv` | `language_category`,`score`,`notes` | 语言环境评分。 |
| `skill_scores.csv` | `skill_category`,`keywords`,`points`,`max_points`,`notes` | 技能关键词加分。 |
| `risk_rules.csv` | `risk_flag`,`keywords`,`deduction`,`notes` | 风险扣分。 |
| `score_components.csv` | `component`,`enabled`,`max_score`,`weight`,`notes` | 分数组件开关与权重。 |

### 标准岗位记录

适配器输出到标准化模块前，至少应能表达：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source_id` | string | 是 | 来源 ID。 |
| `company_id` | string | 是 | 公司 ID。 |
| `source_job_id` | string | 否 | 来源站点岗位 ID。 |
| `job_url` | url | 否 | 岗位详情页。 |
| `title` | string | 是 | 岗位标题。 |
| `department` | string | 否 | 部门。 |
| `location_raw` | string | 否 | 原始地点。 |
| `description` | string | 否 | 原始岗位描述。 |
| `requirements` | string | 否 | 原始要求。 |
| `employment_type` | string | 否 | 全职、实习、合同等。 |
| `published_at` | datetime | 否 | 发布时间。 |
| `updated_at` | datetime | 否 | 更新时间。 |
| `raw_payload_hash` | string | 否 | 原始记录 hash，用于去重和调试。 |

## 输出

本 spec 输出的是稳定数据合同。实现阶段应基于这些合同读取输入文件，并产出符合 `003-csv-output-contract.md` 的 `jobs.csv`。

## 验收标准

* 每个输入 CSV 都有明确表头、类型和必填规则。
* 枚举值稳定，未知值使用 `unknown` 或 `manual_review`，不使用随意中文文本作为枚举。
* 配置表可人工编辑，不需要修改代码即可调整评分。
* 缺失非必填字段不得导致整次运行失败。
* 缺失必填字段时，应记录来源失败或配置错误，并给出可读错误。

## 测试要求

后续实现需覆盖：

* 最小合法 CSV 可以被读取。
* 缺失必填字段会产生明确错误。
* 多余字段被保留或忽略，但不破坏读取。
* 未知枚举进入 `unknown` 或 `manual_review` 分支。
* 配置 CSV 使用 UTF-8 读取，中文关键词不乱码。

