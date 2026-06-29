# Spec 006：ATS 适配器

## 目的

定义第一阶段优先支持的公开 ATS 适配器及其统一输出，确保不同来源的岗位可以进入同一套标准化和评分流程。

## 范围

优先支持：

1. Greenhouse
2. Lever
3. Ashby
4. SmartRecruiters
5. JSON-LD
6. 静态 HTML 兜底

不包含：

* 登录后招聘后台。
* 需要验证码或强反爬的网站。
* 第三方招聘平台的非公开接口。

## 输入

来自 `company_sources.csv` 的单行来源配置：

| 字段 | 说明 |
| --- | --- |
| `source_id` | 来源 ID。 |
| `company_id` | 公司 ID。 |
| `source_type` | 来源类型。 |
| `source_url` | 公开 URL。 |
| `adapter` | 指定适配器。 |

适配器测试输入必须优先使用本地 fixture，不在 CI 中请求真实站点。

## 输出

适配器统一输出 `AdapterResult` 概念记录：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `source_id` | string | 来源 ID。 |
| `status` | enum | `ok`、`empty`、`failed`、`manual_review`、`skipped`。 |
| `fetched_at` | datetime | 读取时间。 |
| `jobs` | list | 标准岗位记录列表。 |
| `error_message` | string | 失败原因，成功时为空。 |
| `adapter_name` | string | 适配器名称。 |

每个岗位至少尝试输出：

* `source_job_id`
* `job_url`
* `title`
* `department`
* `location_raw`
* `description`
* `requirements`
* `employment_type`
* `published_at`
* `updated_at`
* `raw_payload_hash`

字段缺失时不要报错退出，应交给标准化和调试字段处理。

## 适配器要求

### Greenhouse

* 优先使用公开 job board JSON 或公开页面中可解析的数据。
* 保留岗位 ID、标题、地点、部门、详情 URL、描述。

### Lever

* 优先使用公开 postings 数据。
* 保留岗位 ID、标题、团队、地点、详情 URL、描述。

### Ashby

* 优先使用公开 job board 数据。
* 如果页面需要动态接口但无需登录，可作为公开来源处理。

### SmartRecruiters

* 优先使用公开 postings 数据。
* 保留地点、职位族、详情 URL、发布时间。

### JSON-LD

* 解析公开页面中的 `JobPosting` 结构化数据。
* 多个 `JobPosting` 应输出多条岗位记录。

### 静态 HTML

* 只作为兜底。
* 允许解析标题、链接、地点等低置信字段。
* 不确定时标记 `manual_review`，不要硬猜。

## 验收标准

* 每个适配器都有 fixture 测试。
* 空列表返回 `empty`，不视为失败。
* 字段缺失不导致崩溃。
* 解析失败只影响当前来源。
* 输出字段可被 `007-normalization.md` 接收。

## 测试要求

后续实现需覆盖：

* 每个适配器至少一个成功 fixture。
* 每个适配器至少一个空结果 fixture。
* 错误 JSON、缺字段 HTML、未知结构不会崩溃。
* 同一岗位多次出现可通过 `source_job_id` 或 `raw_payload_hash` 去重。
* CI 禁止访问真实网站。

