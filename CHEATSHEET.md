# 命令速查表

> 不用背。忘了就打开这个文件，`Ctrl + F` 搜关键词。
> 同一个命令敲三次就记住了，敲十次之前都靠查。

---

## 一、每天开工（就这三条）

```powershell
cd E:\deepseek\workspace\python-basics
uv run pytest test_day04.py -q -x      # 把 04 换成当天的天数
```

改代码 → 再跑一次 → 红了变绿 → 下一题。

---

## 二、pytest（最常用的 8 条）

| 我想要…… | 命令 |
| --- | --- |
| 跑**当天**的测试 | `uv run pytest test_day04.py -q` |
| 跑**今天**的，**遇到第一个失败就停** | `uv run pytest test_day04.py -q -x` |
| 跑**全部**（Day1~4 一起） | `uv run pytest -q` |
| 只看**一个**测试 | `uv run pytest test_day04.py::test_safe_int_ok` |
| 按**关键词**筛（名字含 safe_int 的都跑） | `uv run pytest test_day04.py -k safe_int -q` |
| **不知道测试叫什么**，先列出来 | `uv run pytest test_day04.py --collect-only -q` |
| 看到**详细**过程（每个用例一个名字） | `uv run pytest test_day04.py -v` |
| 重跑**上一次失败**的那些 | `uv run pytest --lf -q` |

补充两条：

| 场景 | 命令 |
| --- | --- |
| 想看代码里的 `print` 输出 | `uv run pytest test_day04.py -q -s` |
| 想看覆盖率 | `uv run pytest --cov=. --cov-report=term-missing` |

### 名字的写法（`::` 后面跟什么）

```
test_day04.py::test_safe_int_ok
└─ 文件 ─────┘  └─ 测试函数 ──┘
```

- `::` 后面**永远是测试函数名**（以 `test_` 开头的那个），不是被测函数名；
- 写 `test_day04.py::safe_int` 会报 `not found`；
- 想按"被测功能"筛，用 `-k safe_int`。

---

## 三、uv（环境和依赖）

| 目的 | 命令 |
| --- | --- |
| 装依赖 / 同步环境 | `uv sync` |
| 在项目里跑命令 | `uv run <命令>` |
| 装一个新库 | `uv add requests` |
| 装一个只在开发时用的库 | `uv add --dev ruff` |
| 看 uv 版本 | `uv --version` |

> 记住一句话：**`uv run` 是"在当前这个项目里执行"**。
> 报 `program not found` 或者 `no project`，先 `pwd` 看一眼是不是站错目录了。

---

## 四、ruff（代码检查与格式化）

| 目的 | 命令 |
| --- | --- |
| 检查问题 | `uv run ruff check .` |
| 检查并**自动修**能修的 | `uv run ruff check . --fix` |
| 格式化代码 | `uv run ruff format .` |
| 只检查格式（不改文件） | `uv run ruff format --check .` |

**提交前跑一遍**：`ruff check . --fix` → `ruff format .` → `pytest`。

---

## 五、git（每天收工）

| 目的 | 命令 |
| --- | --- |
| 看当前状态 | `git status` |
| 看精简状态 | `git status --short` |
| 看改了什么内容 | `git diff` |
| 暂存所有改动 | `git add -A` |
| 提交 | `git commit -m "day04: 完成文件与异常练习"` |
| 推送 | `git push` |
| 看提交历史 | `git log --oneline` |
| 撤销某个文件的修改（**谨慎**） | `git restore 文件名` |
| 把文件从仓库里移除但保留在磁盘 | `git rm --cached 文件名` |

**每天收工标准动作**：

```powershell
uv run ruff check . --fix
uv run ruff format .
uv run pytest -q                 # 必须全绿
git status                       # ← 先看一眼要提交什么
git add -A
git commit -m "dayXX: 一句话说明"
git push
```

---

## 六、常见报错对照

| 报错 | 原因 | 怎么办 |
| --- | --- | --- |
| `program not found`（在 `uv run xxx` 后） | 目录不对，或这个项目里没有这个命令 | `pwd` 确认目录 |
| `failed to spawn: uv` | uv 没装 / 没重开终端 | 重装 uv，或重开 PowerShell |
| `not found: test_day04.py::safe_int` | `::` 后面写了被测函数名 | 用 `-k safe_int`，或 `--collect-only` 查名字 |
| `NotImplementedError: TODO` | 这题还没写 | 正常，去实现它 |
| `AssertionError: assert ...` | 结果和期望不一致 | 看 `+ 实际`、`- 期望`，从最后一行往上读 |
| `ModuleNotFoundError: No module named 'day04'` | 文件名/位置不对，或没在项目根目录 | 确认 `day04.py` 和测试在同一目录 |
| `Repository not found` | GitHub 上没建这个仓库 | 去 github.com/new 建，名字要一致 |
| `remote origin already exists` | 重复添加远端 | `git remote set-url origin <地址>` |
| `port 8000 is already in use` | 上次的服务没关 | 关掉旧终端，或换端口 `--port 8001` |
| `UnicodeDecodeError` | 读文件没指定 utf-8 | `open(..., encoding="utf-8")` |

---

## 七、每天要查的两个网址

- Python 中文文档：<https://docs.python.org/zh-cn/3/>
- 那天的资料：`DAILY.md`（今天学什么 / 官方文档 / 扩展知识）
