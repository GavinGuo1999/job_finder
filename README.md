# Job Radar

Job Radar 是一个本地自用的岗位机会雷达系统。第一阶段采用 CSV-first 架构：维护公司和招聘源配置，后续基于公开岗位信息做标准化、评分和 CSV 输出。

当前处于 Phase 1：项目骨架阶段。

## 当前范围

已包含：

* 最小 Python 包结构。
* CLI 入口：`python -m jobradar.cli --help`。
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

```powershell
python -m jobradar.cli --help
```

## 测试

```powershell
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

