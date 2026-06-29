# Spec 009：测试策略

## 目的

定义第一阶段和后续实现阶段的测试边界，确保项目在不访问真实网站的情况下验证数据合同、标准化、评分和适配器行为。

## 范围

包含：

* 文档阶段人工验收。
* Python 项目骨架验收。
* CSV 合同测试。
* 配置与评分测试。
* ATS fixture 测试。
* 端到端 fixture 测试。

不包含：

* 真实网站 CI 抓取。
* 登录态浏览器自动化。
* 性能压测。

## 输入

测试输入应来自：

```text
tests/fixtures/
data/config/*.csv
data/seeds/*.csv
data/sources/*.csv
```

fixture 应覆盖：

* 正常岗位。
* 空岗位列表。
* 字段缺失。
* 来源失败。
* 需要人工检查的页面。
* 中文和英文关键词。

## 输出

测试应验证：

* 标准化岗位记录。
* 分数组件。
* `jobs.csv` 表头和内容。
* 错误和调试状态。

## 测试分层

### 合同测试

* 输入 CSV 必填字段。
* 输出 CSV 表头顺序。
* 空结果 CSV。
* 枚举值和空值处理。

### 标准化测试

* 地点分类。
* 远程范围。
* 语言分类。
* 技能关键词。
* 风险标记。

### 评分测试

* 地区、公司、岗位、语言、技能、风险。
* 总分计算。
* 排序。
* 评分理由。

### 适配器测试

* Greenhouse fixture。
* Lever fixture。
* Ashby fixture。
* SmartRecruiters fixture。
* JSON-LD fixture。
* 静态 HTML fixture。

### 端到端 fixture 测试

使用本地 fixture 从来源配置生成 `jobs.csv`，验证：

* timestamp 目录。
* 单一 `jobs.csv`。
* 一行一个岗位。
* 降序排序。
* 单个来源失败不影响整体输出。

## 验收标准

* CI 不访问真实网站。
* 所有网络相关测试都可用 fixture 替代。
* 窄测试优先于大范围端到端测试。
* 每个 bug 修复应尽量补充对应 fixture 或单元测试。
* 输出 CSV 合同变更必须显式更新快照测试。

## 测试要求

Phase 1 最低验收：

```text
python -m jobradar.cli --help
pytest
ruff check .
```

Phase 2 最低验收：

* fixture 岗位可以输出 `jobs.csv`。
* CSV 表头稳定。
* 分数可解释。
* 风险扣分可见。

Phase 4 最低验收：

* 每个适配器有成功、空结果、失败 fixture。
* 字段缺失不崩溃。
* CI 中没有真实网络访问。

