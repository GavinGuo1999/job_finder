# AGENTS.md

# Job Radar / 岗位机会雷达

本项目是一个本地自用的岗位机会雷达系统。

它不是单纯的“外企岗位爬虫”。外企只是公司性质、国际化程度和评分因素之一，不是硬过滤条件。

第一阶段采用 CSV-first 架构：每次运行只输出一个岗位大宽表。

```text
outputs/runs/<timestamp>/jobs.csv
```

---

## 1. 项目目标

本项目用于帮助用户发现、整理、比较和排序岗位机会。

用户重点关注：

* AI 应用
* LLM / Agent / RAG
* 企业信息化
* ERP / SAP / Odoo
* BI / 数据分析 / 数据工程
* Solution Architect / Technical Consultant
* Python / API / Integration / Automation
* 外企、合资、国际化公司环境
* 英语工作环境
* 上海、江浙沪、北上广深、中国大陆、新加坡等地区机会

系统应该采集公开岗位信息，标准化岗位字段，进行可解释评分，最后输出一个 CSV 文件供人工筛选和后续分析。

---

## 2. 当前阶段范围

当前阶段只做：

* 项目文档
* 规格说明
* CSV-first 数据合同
* 评分规则设计
* 测试策略设计
* 后续实现计划

不要直接写实现代码，除非用户明确要求。

---

## 3. MVP 范围

MVP 目标：

* 维护 50 家左右公司种子表
* 维护公司招聘源表
* 优先支持公开 ATS 岗位源
* 采集公开岗位
* 标准化岗位字段
* 按配置表打分
* 每次运行输出一个 `jobs.csv`
* 测试使用 fixtures，不在 CI 中访问真实网站

MVP 暂不做：

* 数据库
* Metabase
* Web UI
* 自动投递
* 简历生成
* LLM 抽取
* 定时任务
* 大规模分布式爬虫

---

## 4. 安全与合规规则

禁止：

* 绕过验证码
* 绕过登录墙
* 使用代理池规避封禁
* 使用盗取的 Cookie / Token
* 采集候选人个人隐私数据
* 自动投递岗位
* 高频请求压垮网站
* 爬取明确禁止访问的页面

必须：

* 优先使用公开 API
* 优先使用 ATS 公开岗位接口
* 尊重 robots.txt 和源策略
* 请求失败时优雅降级
* 某个来源失败不得导致整次运行崩溃
* 发现登录、验证码、强反爬时标记为人工检查

---

## 5. 文档分工

项目细节不要全部写在本文件里。

请按以下分工维护：

```text
AGENTS.md              给 AI agent 的总规则
README.md              给人看的项目说明
docs/PROJECT_PLAN.md   项目总计划
docs/specs/*.md        具体规格、字段、验收标准
docs/adr/*.md          架构决策记录
data/config/*.csv      评分权重和基础配置
data/seeds/*.csv       公司种子数据
```

---

## 6. 开发工作流

每次开始任务前：

1. 先读 `AGENTS.md`
2. 再读 `docs/PROJECT_PLAN.md`
3. 再读相关 `docs/specs/*.md`
4. 如果任务涉及架构选择，检查 `docs/adr/*.md`
5. 先写或更新测试，再实现功能
6. 保持改动小而清晰
7. 完成后说明改了哪些文件、如何验收
8. 完成开发或文档任务后，默认运行相关检查，然后执行 Git commit 和 push；用户说“提交”时也默认包含 commit + push 两步，除非用户明确要求不要提交或不要推送

---

## 7. 测试要求

测试优先使用本地 fixture。

CI 不允许访问真实网站。

重点测试：

* CSV 输出合同
* 地区评分
* 公司性质评分
* 岗位类型评分
* 语言要求评分
* 技能关键词评分
* 风险扣分
* ATS adapter 解析
* 空结果输出
* 单个来源失败不影响整体运行

---

## 8. 输出要求

第一阶段每次运行只输出一个 CSV：

```text
outputs/runs/<timestamp>/jobs.csv
```

一行代表一个岗位。

字段使用前缀分组：

```text
run__
source__
company__
job__
location__
language__
comp__
benefit__
text__
skill__
risk__
score__
debug__
```

具体字段合同放在：

```text
docs/specs/003-csv-output-contract.md
```

---

## 9. 给 Agent 的特别提醒

不要擅自扩大范围。

不要在没有用户确认的情况下加入数据库、BI、Web UI、Playwright、LLM、自动投递、登录爬取、验证码绕过、代理池。

如果发现需求和现有文档冲突，先更新文档或提出问题，不要直接硬编码实现。
