# 每日配套资料

> 约定：每天下发 `test_dayXX.py` 时，同步给出三段——**今天学什么 / 官方文档 / 扩展知识**。
> 每天 60~120 分钟，视当天内容而定：文档 25~40 分钟，写题 50~80 分钟，扩展知识当"睡前读物"，不要求当天全懂。

## 进度总表

| Day | 主题 | 文件 | 状态 |
| --- | --- | --- | --- |
| 1 | 字符串、列表、循环、函数入门 | day01.py | ✅ 7 测试 |
| 2 | 字典、集合、排序、去重 | day02.py | ✅ 8 测试 |
| 3 | 函数：默认参数、*args、**kwargs、闭包、lambda | day03.py | ✅ 8 测试 |
| 4 | 文件读写、with、编码、异常处理 | day04.py | ✅ 8 测试 |
| 5 | 类与对象、dataclass、继承 | day05.py | ✅ 20 测试（`1ed5db0`） |
| 6 | 模块、导入、标准库（pathlib/json/datetime） | day06.py | 🔄 进行中（12 测试） |
| 7 | 小综合：命令行记账本 | day07.py | ⬜ 待下发 |

当前累计：**51 个测试全绿**（Day 1~5）。

---

## Day 1 · 字符串与列表

**今天学什么**：字符串方法、列表索引与切片、`for`/`range`、f-string、函数定义与返回值。

**官方文档**

- [3.1.2 字符串 / 3.1.3 列表](https://docs.python.org/zh-cn/3/tutorial/introduction.html)
- [4.2 for 语句 / 4.3 range()](https://docs.python.org/zh-cn/3/tutorial/controlflow.html)
- [5.1 列表详解](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)
- [7.1.1 f-string](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html)
- 当字典查：[字符串方法](https://docs.python.org/zh-cn/3/library/stdtypes.html#string-methods)

**扩展知识**

- 字符串不可变：所有 `str` 方法都返回新串，不是原地改
- `split()` 不带参数 vs `split(" ")` 的区别（连续空格的处理）
- `"".join(list)` 比循环里 `+=` 拼字符串快得多（后者 O(n²)）

---

## Day 2 · 字典、集合、排序

**今天学什么**：`dict` 增删改查与 `get`、`set` 去重、`sorted` 的 `key` 多条件排序、`setdefault` 分组。

**官方文档**

- [5.5 字典](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries)
- [5.4 集合](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#sets)
- [5.6 循环的技巧](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#looping-techniques)（`items()`、`enumerate`、`zip`）
- 内置函数：[sorted](https://docs.python.org/zh-cn/3/library/functions.html#sorted)
- [list.sort 与 sorted 的区别](https://docs.python.org/zh-cn/3/howto/sorting.html)

**扩展知识**

- `sorted` 是**稳定排序**：先排次要关键字、再排主要关键字，等价于多条件 key
- `key=lambda kv: (-kv[1], kv[0])` 里的负号：升序排序模拟降序
- 字典查找 O(1)、列表 `in` 查找 O(n)——去重判断为什么要用 `set`
- `collections.Counter` 是 `word_count` 的现成版本（第 3 周再引入）

---

## Day 3 · 函数

**今天学什么**：默认参数、关键字参数、`*args`/`**kwargs`、函数作为值、闭包、`lambda`、`key` 函数。

**官方文档**

- [4.7 定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)
- [4.8 函数定义详解](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#more-on-defining-functions)：4.8.1 默认参数值、4.8.2 关键字参数、4.8.4 任意参数列表、4.8.5 解包参数列表、4.8.6 Lambda 表达式
- 内置函数：`sorted` / `sum` / `abs` / `max` / `min`
- 选读：[9.2 Python 作用域和命名空间](https://docs.python.org/zh-cn/3/tutorial/classes.html#python-scopes-and-namespaces)（闭包的底层）

**扩展知识**

- **可变默认参数的坑**：`def f(x, items=[])` 的 `items` 只在定义时创建一次，所有调用共享
- 位置参数 `/`、关键字参数 `*` 在函数签名里的含义（文档 4.8.3）
- lambda 只能写一个表达式，不能写语句；能传函数名就别包 lambda
- 闭包 + 装饰器：第 4 周会用到（`@router.get` 就是装饰器）

---

## Day 4 · 文件读写与异常

**今天学什么**：`with open(...)`、`encoding`、`Path` 对象、`try/except`、异常类型、什么时候不该捕获异常。

**官方文档**

- [7.2 读写文件](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files)
- [8.3 异常处理](https://docs.python.org/zh-cn/3/tutorial/errors.html#handling-exceptions)
- [8.4 抛出异常](https://docs.python.org/zh-cn/3/tutorial/errors.html#raising-exceptions)
- [pathlib 基础](https://docs.python.org/zh-cn/3/library/pathlib.html)（只看 `Path` 的构造、`open`、`read_text`、`write_text`）
- 当字典查：[内置异常层次](https://docs.python.org/zh-cn/3/library/exceptions.html)

**扩展知识**

- **`encoding="utf-8"` 必写**：Windows 默认 GBK，写中文再读会乱码
- **EAFP 风格**（Easier to Ask Forgiveness than Permission）：Python 鼓励"先做，出错再处理"，而不是先判断再做
- 只捕获具体异常：`except ValueError` ✅ / `except:` ❌（会吞掉 Ctrl+C）
- `with` 背后是上下文管理器协议 `__enter__` / `__exit__`——第 4 周你自己写一个就懂了
- 常见异常：`ValueError`（值不对）、`TypeError`（类型不对）、`KeyError`（字典没这个键）、`FileNotFoundError`、`PermissionError`
- `raise` 主动抛异常、`raise ... from e` 保留原始错误链（排查问题靠它）
- `pathlib.Path` 正在取代 `os.path`，新代码优先用它
- 文件读写还有 `newline=` 参数（处理 `\r\n`）、`errors="ignore"`（坏字节），遇到再查

---

## Day 5 · 类与对象

**今天学什么**：`class`、`__init__` 与 `self`、实例属性 vs 类属性、方法、魔术方法（`__repr__`/`__eq__`/`__len__`）、`@dataclass`、继承与重写。

**官方文档**

- [9. 类](https://docs.python.org/zh-cn/3/tutorial/classes.html)：9.1 名称与对象、9.2 作用域（选读）、**9.3 初探类**、9.4 补充说明（重点：类属性 vs 实例属性）、9.5 继承
- [dataclasses](https://docs.python.org/zh-cn/3/library/dataclasses.html)：只看开头的示例和"自动生成的方法"那段
- [数据模型 · 特殊方法名](https://docs.python.org/zh-cn/3/reference/datamodel.html#special-method-names)：只查 `__repr__`、`__eq__`、`__len__` 三个
- 选读：[9.5 继承](https://docs.python.org/zh-cn/3/tutorial/classes.html#inheritance)（今天只要会"重写一个方法"）

**扩展知识**

- **`self` 不是关键字**，只是约定俗成的第一个参数名（写成 `this` 也能跑，但别这么干）
- **可变类属性的坑**：`class A: items = []` —— 所有实例共享这一个列表，改一个全变。需要每个实例独立，就在 `__init__` 里 `self.items = []`
- **`@dataclass` 帮你生成 `__init__`/`__repr__`/`__eq__`**，但不会生成 `__hash__`（放进 set 会报错，需要 `frozen=True`）
- `__repr__` 给开发者看（调试），`__str__` 给用户看（`print`）；只写一个就写 `__repr__`
- 继承要克制：**组合优于继承**，能"有一个"就别"是一个"
- 为什么 FastAPI 全是类：`BaseModel` 管**校验**（请求数据对不对），`Base` 管**映射**（表怎么存）——同一个对象两种职责，各自用类封装

---

## Day 5 配套：对照真实代码（20 分钟）

打开 `E:\deepseek\workspace\fastapi-starter`，在下面三个文件里各找一个今天学过的语法点：

| 文件 | 找什么 |
| --- | --- |
| `app/schemas/todo.py` | `class TodoCreate(BaseModel)` —— 继承、类属性（字段声明）、`ConfigDict` |
| `app/db/models.py` | `class User(Base, TimestampMixin)` —— 多继承、`Mapped[...]` 类属性 |
| `app/core/config.py` | `class Settings(BaseSettings)` —— 继承 + 默认值 + 实例化 `Settings()` |

看完回答一句：**"Pydantic 的 `BaseModel` 和 SQLAlchemy 的 `Base` 都是类，它们分别在干什么？"**

---

## Day 6 · 模块与标准库

**今天学什么**：`json` 读写、`datetime`/`date` 解析与计算、`pathlib` 遍历与路径拼接、`if __name__ == "__main__"`。

**官方文档**

- [6. 模块](https://docs.python.org/zh-cn/3/tutorial/modules.html)：6.1 更多关于模块、**6.4 包**、6.1.1 以脚本方式执行模块（就是 `__main__` 那段）
- [json](https://docs.python.org/zh-cn/3/library/json.html)：只看 `dumps` / `loads` / `dump` / `load` 四个函数和 `ensure_ascii` 参数
- [datetime](https://docs.python.org/zh-cn/3/library/datetime.html)：只看 `date`、`datetime`、`timedelta` 三个类，以及 `strftime` / `strptime` 的格式符表
- [pathlib](https://docs.python.org/zh-cn/3/library/pathlib.html)：只看 `Path`、`/` 运算符、`read_text`/`write_text`、`rglob`、`relative_to`、`as_posix`

**扩展知识**

- **`if __name__ == "__main__":` 的作用**：模块被 `import` 时 `__name__` 是模块名，直接运行时才是 `"__main__"`。用它把"被别人用"和"自己跑"分开，测试才不会误触发
- **json 只认 6 种类型**：对象、数组、字符串、数字、`true/false`、`null`。`date`、`datetime`、`Decimal`、`set` 都不能直接存，要么转字符串，要么自定义 `default=`
- **`ensure_ascii=False`**：不写的话中文会变成 `\u5f20\u4e09`，机器能读、人不能
- **时区**：`datetime.now()` 是"本地时间但不带时区"，`datetime.now(timezone.utc)` 才是明确的 UTC。**存库用 UTC，展示时转本地**（starter 里的 `created_at` 就是 UTC）
- **`strftime` / `strptime` 记 4 个格式符就够**：`%Y` 年、`%m` 月、`%d` 日、`%H:%M:%S` 时分秒
- **`Path` 的 `/` 运算符**：`root / "sub" / "a.txt"`，比字符串拼接安全（自动处理分隔符）
- **`relative_to` + `as_posix()`**：Windows 上是 `sub\a.txt`，`as_posix()` 统一成 `sub/a.txt`，写日志和接口时不会被反斜杠坑
- **`rglob` 会匹配目录**：`rglob("*.txt")` 可能返回叫 `xxx.txt` 的文件夹，记得 `is_file()` 过滤

---

## Day 7 · 小综合（预告）

**预计内容**：命令行记账本——读 JSON 文件、增删记录、统计汇总、异常兜底。把 Day 1~6 全部用一遍。

**预计文档**： argparse（[教程](https://docs.python.org/zh-cn/3/library/argparse.html)）、json（同上）
