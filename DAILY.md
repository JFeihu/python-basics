# 每日配套资料

> 约定：每天下发 `test_dayXX.py` 时，同步给出三段——**今天学什么 / 官方文档 / 扩展知识**。
> 每天 60~90 分钟：文档 25~35 分钟，写题 50 分钟，扩展知识当"睡前读物"，不要求今天全懂。

## 进度总表

| Day | 主题 | 文件 | 状态 |
| --- | --- | --- | --- |
| 1 | 字符串、列表、循环、函数入门 | day01.py | ✅ |
| 2 | 字典、集合、排序、去重 | day02.py | ✅ |
| 3 | 函数：默认参数、*args、**kwargs、闭包、lambda | day03.py | ✅ |
| 4 | 文件读写、with、编码、异常处理 | day04.py | 🔄 进行中 |
| 5 | 类与对象、dataclass | day05.py | ⬜ 待下发 |
| 6 | 模块、导入、标准库（pathlib/json/datetime） | day06.py | ⬜ 待下发 |
| 7 | 小综合：命令行记账本 | day07.py | ⬜ 待下发 |

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

## Day 5 · 类与对象（预告）

**预计内容**：`class`、`__init__`、`self`、属性与方法、继承（了解）、`@dataclass`、`__repr__`/`__eq__`。

**预计文档**：[9. 类](https://docs.python.org/zh-cn/3/tutorial/classes.html)、[dataclasses](https://docs.python.org/zh-cn/3/library/dataclasses.html)

**预计扩展**：为什么 FastAPI 里到处是类（Pydantic 模型、ORM 模型）；`dataclass`  vs 普通类的取舍。

---

## Day 6 · 模块与标准库（预告）

**预计内容**：`import` 的几种写法、`if __name__ == "__main__"`、`pathlib`、`json`、`datetime`。

**预计文档**：[6. 模块](https://docs.python.org/zh-cn/3/tutorial/modules.html)、[json](https://docs.python.org/zh-cn/3/library/json.html)、[datetime](https://docs.python.org/zh-cn/3/library/datetime.html)

**预计扩展**：绝对导入 vs 相对导入；为什么项目里要分“包”；时区与 UTC（Day 4 的 starter 里已经见过一次）。

---

## Day 7 · 小综合（预告）

**预计内容**：命令行记账本——读 JSON 文件、增删记录、统计汇总、异常兜底。把 Day 1~6 全部用一遍。

**预计文档**： argparse（[教程](https://docs.python.org/zh-cn/3/library/argparse.html)）、json（同上）
