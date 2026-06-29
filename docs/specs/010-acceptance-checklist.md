# Spec 010：验收清单

## 目的

提供跨阶段验收清单，帮助人工审核当前阶段是否完成，并为后续实现阶段提供明确退出条件。

## 范围

包含 Phase 0 到 Phase 6 的验收点。

不包含：

* 具体实现任务拆分。
* 发布流程。
* 长期数据库或 BI 演进验收。

## 输入

验收依据：

* `AGENTS.md`
* `docs/PROJECT_PLAN.md`
* `docs/specs/*.md`
* `docs/adr/*.md`
* 后续实现产物和测试输出。

## 输出

输出为人工审核结论：

* 通过。
* 有条件通过。
* 不通过，需要补充文档或实现。

## Phase 0：文档阶段

必须存在：

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

验收点：

* 每个 spec 有目的、范围、输入、输出、验收标准、测试要求。
* 字段、评分、CSV 合同在 spec 中，不写入 agent 指令文件。
* 没有实现代码变更。
* 没有引入生产依赖。

## Phase 1：项目骨架

验收点：

* 存在最小 Python 项目结构。
* CLI help 可运行。
* `pytest` 可运行。
* `ruff check .` 可运行。
* 没有真实网络访问。

## Phase 2：配置与评分核心

验收点：

* 可读取配置 CSV。
* fixture 岗位可输出 `jobs.csv`。
* 地区、公司、岗位、语言、技能、风险分可见。
* `score__total` 降序排序。
* `score__reasons` 可读。

## Phase 3：公司与来源配置

验收点：

* `companies_50.csv` 存在并符合合同。
* `company_sources.csv` 存在并符合合同。
* 公司性质字段使用枚举。
* 来源类型字段使用枚举。
* 不确定来源允许 `manual_review`。

## Phase 4：公开 ATS 适配器

验收点：

* Greenhouse、Lever、Ashby、SmartRecruiters、JSON-LD、静态 HTML 均有 fixture 测试。
* 空岗位列表不崩溃。
* 字段缺失不崩溃。
* CI 不访问真实网站。
* 登录、验证码或强反爬标记为人工检查。

## Phase 5：端到端运行

验收点：

* 生成 timestamp 文件夹。
* 生成一个 `jobs.csv`。
* 一行一个岗位。
* 按 `score__total` 降序排序。
* 某个来源失败不影响整体运行。
* 空结果也输出只有表头的 CSV。

## Phase 6：人工调权

验收点：

* AI / 信息化 / BI 岗位靠前。
* 上海 / 江浙沪岗位靠前。
* 英语友好岗位加分明显。
* 外包 / 派遣 / 纯销售岗位被扣分。
* 推荐理由能看懂。
* 调整 `data/config/*.csv` 后无需改代码即可改变排序。

## 验收标准

当前 Phase 0 完成条件：

* 清单中的 Phase 0 文件全部存在。
* 文档内容与项目计划一致。
* 没有写实现代码。
* 人工审核者可以基于文档进入 Phase 1。

## 测试要求

文档阶段使用人工检查和文件存在性检查。后续实现阶段按 `009-testing-strategy.md` 执行自动化测试。
