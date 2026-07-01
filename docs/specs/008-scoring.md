# Spec 008：评分规则

## 目的

定义第一阶段可解释、配置驱动的岗位评分规则。评分用于排序和人工筛选，不作为硬过滤条件。

## 范围

包含：

* 分数组件。
* 默认分值。
* 风险扣分。
* 总分公式。
* 评分理由输出。

不包含：

* 机器学习排序。
* LLM 评分。
* 用户在线反馈学习。

## 输入

评分输入来自标准化岗位记录和配置 CSV：

```text
data/config/location_scores.csv
data/config/remote_scores.csv
data/config/company_type_scores.csv
data/config/role_scores.csv
data/config/language_scores.csv
data/config/skill_scores.csv
data/config/risk_rules.csv
data/config/score_components.csv
```

## 输出

评分输出字段：

* `score__location`
* `score__company`
* `score__role`
* `score__language`
* `score__skill`
* `score__risk`
* `score__total`
* `score__recommendation`
* `score__reasons`

## 总分公式

第一阶段采用加法评分，再将总分 clamp 到 0 到 100。不要把各组件按百分比加权平均，也不要同时混用“加法评分”和“百分比权重评分”。

```text
raw_total =
  score__location
  + score__company
  + score__role
  + score__language
  + score__skill
  + score__risk

score__total = clamp(round(raw_total), 0, 100)
```

风险分为 0 或负数。第一阶段不做硬过滤，除非来源策略禁止访问。

如果配置表中保留 `score_components.weight` 字段，Phase 1 不应把它解释为百分比权重；它只能作为未来扩展或人工备注参考。Phase 1 的实际排序必须以上述加法公式为准。

## 默认地区分

`score__location` 取地点分和远程分中的较高值。

| 分类 | 分值 |
| --- | ---: |
| 上海 | 25 |
| 江浙沪 | 22 |
| 北京 / 广州 / 深圳 | 18 |
| 中国大陆其他城市 | 14 |
| 新加坡 | 12 |
| 亚洲其他地区 | 8 |
| 欧美澳加等其他地区 | 5 |
| 地点未知 | 2 |

远程范围：

| 远程范围 | 分值 |
| --- | ---: |
| 允许中国申请 | 24 |
| 允许 APAC 申请 | 22 |
| 全球远程且未限制地区 | 20 |
| 不明确 | 8 |
| 限制 US / EU | 3 |

## 默认公司分

| 公司类型 | 分值 |
| --- | ---: |
| `foreign_mnc` | 20 |
| `foreign_tech_saas` | 19 |
| `joint_venture` | 17 |
| `china_global` | 16 |
| `china_bigtech_ai` | 15 |
| `china_quality_enterprise_it` | 14 |
| `private_company` | 8 |
| `state_owned` | 6 |
| `outsourcing_staffing` | 2 |
| `unknown` | 5 |

## 默认岗位类别分

`score__role` 取命中类别中的最高值。

| 岗位类别 | 关键词示例 | 分值 |
| --- | --- | ---: |
| AI 应用 / LLM / Agent / RAG | AI, LLM, Agent, RAG, GenAI, Copilot | 30 |
| 企业信息化 / ERP / SAP / Odoo | ERP, SAP, Odoo, enterprise system, 信息化 | 28 |
| BI / 数据分析 / 数据工程 | BI, analytics, data analyst, data engineer | 25 |
| Solution Architect / Technical Consultant | solution architect, technical consultant, pre-sales engineer | 23 |
| Python / API / Integration / Automation | Python, API, integration, automation | 21 |
| 数字化产品 / 项目管理 | digital product, product manager, project manager | 17 |
| IT 系统 / IT Support | IT system, IT support, system administrator | 12 |
| 普通软件开发 | software engineer, backend, frontend | 10 |
| 业务运营 | operations, business operations | 5 |
| 销售 / 客服 | sales, account executive, customer service | 2 |
| 未知 | 无法判断 | 4 |

## 默认语言分

| 语言分类 | 分值 |
| --- | ---: |
| `english_chinese` | 15 |
| `english_required` | 14 |
| `english_preferred` | 12 |
| `unknown` | 7 |
| `chinese_only` | 4 |
| `unsupported_language_required` | 0 |

## 默认技能分

技能分可累加，上限 20。

| 技能类别 | 关键词示例 | 分值 |
| --- | --- | ---: |
| AI / LLM / Agent / RAG | LLM, Agent, RAG, GenAI, prompt | 8 |
| ERP / SAP / Odoo / 信息化 | ERP, SAP, Odoo, enterprise system | 7 |
| BI / 数据 | BI, SQL, dashboard, data pipeline | 6 |
| Python / API | Python, REST API, FastAPI | 5 |
| Integration / Automation | integration, workflow, automation, ETL | 5 |
| Cloud / SaaS | SaaS, cloud, AWS, Azure, GCP | 3 |

## 默认风险扣分

风险分可累加，最低不低于 -40。

| 风险 | 关键词示例 | 扣分 |
| --- | --- | ---: |
| 外包 | outsourcing, vendor, 外包 | -12 |
| 派遣 | staffing, contractor dispatch, 派遣 | -15 |
| 纯销售倾向 | cold call, quota, 纯销售, 电话销售 | -10 |
| 客服低相关 | customer service, call center, 客服 | -8 |
| 小语种硬门槛 | Japanese required, German required, 日语必须 | -12 |
| 地区不适配 | US only, EU only, work authorization required | -10 |
| 岗位低相关 | warehouse, retail, finance accountant | -15 |

## 评分理由

`score__reasons` 使用分号分隔，格式建议：

```text
location:上海 +25; role:AI应用 +30; language:英语优先 +12; risk:外包 -12
```

理由必须让人工审核者能理解分数来源。

## 验收标准

* 总分范围为 0 到 100。
* 分数组件可在 CSV 中直接看到。
* 配置表可调整分值，不需要改代码。
* AI / 信息化 / BI 岗位整体靠前。
* 上海 / 江浙沪岗位整体靠前。
* 英语友好岗位有明显加分。
* 外包 / 派遣 / 纯销售岗位有明显扣分。

## 测试要求

后续实现需覆盖：

* 每个分数组件的单元测试。
* 多关键词命中时岗位类别取最高分。
* 技能分累加但不超过 20。
* 风险分累加但不低于 -40。
* 总分 clamp 到 0 到 100。
* `score__reasons` 包含主要加分和扣分来源。
