# Spec 004：公司与招聘来源模型

## 目的

定义公司种子数据与招聘来源之间的关系，确保 50 家左右公司可以被稳定维护、人工审查和逐步接入公开 ATS 或网页来源。

## 范围

包含：

* 公司种子表维护规则。
* 招聘来源表维护规则。
* 公司与来源的一对多关系。
* 来源类型、适配器和人工检查状态。

不包含：

* 适配器解析细节，见 `006-ats-adapters.md`。
* 评分细则，见 `008-scoring.md`。

## 输入

### 公司种子表

```text
data/seeds/companies_50.csv
```

字段合同见 `002-data-contracts.md`。

维护规则：

* `company_id` 必须稳定，后续不要因公司展示名变化而修改。
* `company_type` 必须使用枚举。
* 无法判断公司性质时使用 `unknown`，不要臆测。
* 一个集团下多个招聘品牌可以拆成多个公司记录，但需在 `notes` 中说明。

### 招聘来源表

```text
data/sources/company_sources.csv
```

字段合同见 `002-data-contracts.md`。

`source_type` 枚举：

| 值 | 说明 |
| --- | --- |
| `ats_api` | 公开 ATS API 或公开 JSON 端点。 |
| `ats_board` | 公开 ATS 职位板页面。 |
| `company_career_page` | 公司官网招聘页。 |
| `job_board_company_page` | 第三方招聘网站公司页，仅限公开可访问。 |
| `json_ld_page` | 带结构化数据的公开页面。 |
| `static_html_page` | 静态 HTML 页面。 |
| `manual_review` | 暂无法自动判断，需要人工检查。 |

`adapter` 枚举：

| 值 | 说明 |
| --- | --- |
| `greenhouse` | Greenhouse 公开岗位源。 |
| `lever` | Lever 公开岗位源。 |
| `ashby` | Ashby 公开岗位源。 |
| `smartrecruiters` | SmartRecruiters 公开岗位源。 |
| `json_ld` | JSON-LD 结构化岗位数据。 |
| `static_html` | 静态 HTML 兜底解析。 |
| `manual_review` | 不自动抓取。 |

## 输出

来源模型应为后续流程提供：

* 可启用来源列表。
* 每个来源关联的公司信息。
* 每个来源应该使用的适配器。
* 每个来源的错误、空结果或人工检查状态。

输出到最终 CSV 的字段包括：

* `source__id`
* `source__type`
* `source__name`
* `source__url`
* `source__status`
* `company__id`
* `company__name`
* `company__type`
* `company__career_url`

## 验收标准

* 一个公司可以有多个招聘来源。
* 一个来源只能归属一个公司。
* 禁用来源不会参与抓取，但可以保留在 CSV 配置中。
* 不确定来源可标记为 `manual_review`，不会导致运行失败。
* 来源失败只影响该来源，不影响整次运行。

## 测试要求

后续实现需覆盖：

* 公司和来源可以正确关联。
* 找不到 `company_id` 的来源会产生配置错误。
* `enabled=false` 的来源被跳过。
* `manual_review` 来源不自动抓取。
* 同一公司多个来源可以合并输出，并能去重。

