# Job Radar

Job Radar 是一个本地自用的岗位机会雷达系统。第一阶段采用 CSV-first 架构：维护公司和招聘源配置，基于岗位数据做标准化、评分和 CSV 输出。

当前处于 Phase 2：配置与评分核心。

本仓库当前提供本地 fixture 岗位评分闭环：读取 fixture CSV、读取本地配置 CSV、计算加法评分，并输出 `jobs.csv`。

项目文本文件在 Git 中统一使用 LF 行尾。

## 当前范围

已包含：

* 最小 Python 包结构。
* CLI 入口：`python -m jobradar.cli --help`。
* 本地 fixture 评分命令：`python -m jobradar.cli score-fixtures ...`。
* 配置驱动的地区、公司性质、岗位方向、语言、技能和风险评分。
* CSV-first 输出：`outputs/runs/<timestamp>/jobs.csv`。
* pytest 和 ruff 配置。
* 文档、规格和 ADR。
* 数据目录骨架。

暂不包含：

* 真实爬虫。
* 真实网站访问。
* 数据库。
* Metabase。
* Playwright。
* LLM。

## 安装

建议在虚拟环境中安装开发依赖：

```powershell
python -m pip install -e ".[dev]"
```

## 运行

查看 CLI 帮助：

```powershell
python -m jobradar.cli --help
```

对本地 fixture 岗位评分并输出 `jobs.csv`：

```powershell
python -m jobradar.cli score-fixtures `
  --input tests/fixtures/sample_jobs.csv `
  --config data/config `
  --output outputs/runs
```

输出路径：

```text
outputs/runs/<timestamp>/jobs.csv
```

## 测试

```powershell
pytest
ruff check .
```

Phase 2 验收命令：

```powershell
python -m pip install -e ".[dev]"
python -m jobradar.cli --help
python -m jobradar.cli score-fixtures --input tests/fixtures/sample_jobs.csv --config data/config --output outputs/runs
pytest
ruff check .
```

## 项目结构

```text
AGENTS.md
docs/
src/jobradar/
tests/
data/seeds/
data/sources/
data/config/
outputs/runs/
```

`outputs/runs/` 用于后续运行输出，并被 `.gitignore` 忽略。
