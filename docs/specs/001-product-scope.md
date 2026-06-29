# Spec 001：产品范围

## 目的

定义 Job Radar 第一阶段的产品边界，确保项目优先交付一个本地自用、CSV-first、可人工审核的岗位机会雷达系统。

## 范围

本阶段包含：

* 维护公司种子表和招聘来源表。
* 采集公开岗位信息。
* 标准化岗位、公司、地点、语言、技能和风险字段。
* 根据用户偏好进行可解释评分。
* 每次运行输出一个 `jobs.csv` 大宽表。
* 使用本地 fixture 做测试，CI 不访问真实网站。

本阶段不包含：

* 数据库、Web UI、Metabase、日报周报。
* 自动投递、登录态采集、简历生成。
* LLM 抽取、代理池、验证码绕过、反爬绕过。
* 候选人个人隐私数据采集。

## 输入

```text
data/seeds/companies_50.csv
data/sources/company_sources.csv
data/config/*.csv
```

输入文件的字段合同见：

* `docs/specs/002-data-contracts.md`
* `docs/specs/004-company-source-model.md`
* `docs/specs/008-scoring.md`

## 输出

```text
outputs/runs/<timestamp>/jobs.csv
```

输出 CSV 合同见：

* `docs/specs/003-csv-output-contract.md`

## 用户偏好

系统排序应优先体现以下方向：

* 地区：上海、江浙沪、北京/广州/深圳、中国大陆其他城市、新加坡、亚洲其他地区、欧美澳加等其他地区、地点未知。
* 岗位：AI 应用、LLM、Agent、RAG、企业信息化、ERP、SAP、Odoo、BI、数据分析、数据工程、Solution Architect、Technical Consultant、Python、API、Integration、Automation。
* 公司：外资跨国公司、外资科技/SaaS、合资、中国出海、中国大厂/AI、优质甲方信息化岗位。
* 语言：英语友好环境加分，小语种硬性要求且用户不会时扣分。

## 验收标准

* 所有 Phase 0 文档存在。
* 每个 spec 都包含目的、范围、输入、输出、验收标准、测试要求。
* 项目范围没有扩大到数据库、Web UI、LLM 或自动投递。
* 字段、评分、CSV 合同放在 `docs/specs`，不写入 `AGENTS.md`。
* 文档足以支撑下一阶段创建最小 Python 项目骨架。

## 测试要求

文档阶段不运行实现测试。人工审核时检查：

* 本文件与 `docs/PROJECT_PLAN.md` 不冲突。
* 非 MVP 项没有进入验收清单。
* 风险和合规边界清晰可执行。

