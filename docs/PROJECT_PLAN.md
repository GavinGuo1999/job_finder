# PROJECT_PLAN.md

# Job Radar / 岗位机会雷达项目总计划

## 1. 项目定位

本项目是一个本地自用的岗位机会雷达系统。

它用于采集公开岗位信息，标准化岗位字段，根据用户偏好进行可解释评分，并输出一个岗位 CSV，帮助用户筛选值得关注和投递的机会。

本项目不局限于外企。外企、合资、中国出海公司、中国 AI 公司、中国优质甲方，都可以进入系统。公司性质只是评分因素之一。

---

## 2. 第一阶段目标

第一阶段采用 CSV-first 架构。

输入：

```text
data/seeds/companies_50.csv
data/sources/company_sources.csv
data/config/*.csv
```

输出：

```text
outputs/runs/<timestamp>/jobs.csv
```

每次运行只输出一个岗位大宽表。

一行代表一个岗位。

---

## 3. 用户偏好

### 地区偏好

优先级从高到低：

1. 上海
2. 江浙沪
3. 北京 / 广州 / 深圳
4. 中国大陆其他城市
5. 新加坡
6. 亚洲其他地区
7. 欧美澳加等其他地区
8. 地点未知

远程岗位单独判断：

* 允许中国 / APAC 申请：高分
* 限制 US / EU：低分
* 不明确：中低分

### 岗位偏好

优先级从高到低：

1. AI 应用 / LLM / Agent / RAG
2. 企业信息化 / ERP / SAP / Odoo
3. BI / 数据分析 / 数据工程
4. Solution Architect / Technical Consultant
5. Python / API / Integration / Automation
6. 数字化产品 / 项目管理
7. IT 系统 / IT Support
8. 普通软件开发
9. 业务运营
10. 销售 / 客服

### 公司偏好

外企优先，但不是硬过滤条件。

公司性质从高到低大致为：

1. 外资跨国公司
2. 外资科技 / SaaS 公司
3. 合资企业
4. 中国出海公司
5. 中国大厂 / AI 公司
6. 中国优质甲方信息化岗位
7. 普通民企
8. 国企
9. 外包 / 派遣供应商

### 语言偏好

英语友好环境加分。

优先级：

1. 英语 + 中文
2. 英语必需
3. 英语优先
4. 未知
5. 只中文
6. 用户不会的小语种硬性要求

---

## 4. 项目阶段

## Phase 0：文档阶段

目标：先写清楚规格，不写代码。

需要创建：

```text
docs/specs/001-product-scope.md
docs/specs/002-data-contracts.md
docs/specs/003-csv-output-contract.md
docs/specs/004-company-source-model.md
docs/specs/005-crawl-policy.md
docs/specs/006-ats-adapters.md
docs/specs/007-normalization.md
docs/specs/008-scoring.md
docs/specs/009-testing-strategy.md
docs/specs/010-acceptance-checklist.md
docs/adr/0001-csv-first.md
docs/adr/0002-config-driven-scoring.md
docs/adr/0003-prefer-public-ats-apis.md
docs/adr/0004-no-anti-bot-bypass.md
```

验收：

* 所有文件存在
* 每个 spec 有目的、范围、输入、输出、验收标准、测试要求
* 暂不写实现代码

---

## Phase 1：项目骨架

目标：创建最小可运行 Python 项目。

包括：

```text
pyproject.toml
README.md
src/jobradar/
tests/
data/seeds/
data/sources/
data/config/
outputs/runs/
```

验收：

```text
python -m jobradar.cli --help
pytest
ruff check .
```

---

## Phase 2：配置与评分核心

目标：先不爬真实网站，只对 fixture 岗位打分。

实现：

* 读取配置 CSV
* 地区评分
* 公司性质评分
* 岗位类型评分
* 语言评分
* 技能评分
* 风险扣分
* 总分计算
* CSV 输出

验收：

* fixture 岗位能输出 jobs.csv
* 分数可解释
* 风险扣分可见
* CSV 表头稳定

---

## Phase 3：公司与来源配置

目标：建立 50 家左右公司种子表和招聘源表。

包括：

```text
data/seeds/companies_50.csv
data/sources/company_sources.csv
```

验收：

* 公司性质字段规范
* 招聘源类型字段规范
* 不确定来源允许标记为 manual_review

---

## Phase 4：公开 ATS 适配器

优先支持：

1. Greenhouse
2. Lever
3. Ashby
4. SmartRecruiters
5. JSON-LD
6. 静态 HTML 兜底

验收：

* 每个适配器先有 fixture 测试
* CI 不访问真实网站
* 字段缺失不崩溃
* 空岗位列表不崩溃

---

## Phase 5：端到端运行

目标：从公司源配置到最终 CSV。

命令形式：

```text
python -m jobradar.cli crawl \
  --companies data/seeds/companies_50.csv \
  --sources data/sources/company_sources.csv \
  --config data/config \
  --output outputs/runs
```

验收：

* 生成 timestamp 文件夹
* 生成一个 jobs.csv
* 一行一个岗位
* 按 score__total 降序排序
* 某个来源失败不影响整体运行
* 空结果也输出只有表头的 CSV

---

## Phase 6：人工调权

目标：用真实输出校准评分。

流程：

1. 打开 jobs.csv
2. 按 score__total 降序排序
3. 看前 50 个岗位
4. 判断是否符合直觉
5. 调整 data/config/*.csv
6. 重新运行

验收：

* AI / 信息化 / BI 岗位靠前
* 上海 / 江浙沪岗位靠前
* 英语友好岗位加分明显
* 外包 / 派遣 / 纯销售岗位被扣分
* 推荐理由能看懂

---

## 5. 后续阶段

MVP 稳定后再考虑：

* PostgreSQL
* Metabase
* 历史趋势分析
* 每日/每周报告
* LLM 岗位摘要
* 简历匹配
* 投递优先级管理
