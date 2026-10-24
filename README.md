# 7 天 Python 基础加固

给「上过课、看得懂语法，但一写就卡、读测试发懵」的阶段准备的一周。

**这一周只有一个目标：手感。** 不碰 async、不碰 FastAPI、不碰项目结构，每天就一个文件、6 个小函数。

## 每天怎么用（60~90 分钟）

1. **5 分钟**：打开当天的 `test_dayXX.py`，从头读一遍。每行 `assert` 就是一句「必须满足」。
2. **50 分钟**：打开 `dayXX.py`，从第一题开始，把 `raise NotImplementedError` 换成你的实现。
3. **每写完一个函数**，就跑一次测试（见下面的命令），红的变绿就下一个。
4. **15 分钟**：全部绿了之后，把当天代码看一遍，问自己「这行能不能更简单」。

## 命令

```powershell
cd E:\deepseek\workspace\python-basics
uv sync                                  # 只第一次需要
uv run pytest test_day01.py -q           # 跑当天
uv run pytest test_day01.py -q -x        # 遇到第一个失败就停（推荐，一次只解决一个问题）
uv run pytest test_day01.py::test_greet  # 只跑一题
```

## 三条规矩

1. **不许改测试文件。** 测试红了，先改自己的代码。
2. **不许搜答案。** 卡住 20 分钟看 README 的提示，提示还不行再来问我，说明你卡在哪一行。
3. **每天把代码存一次**（复制到 `done/day01.py` 也行），一周后回头看第一天的代码，你会发现自己进步了。

## 怎么读报错（这个技能比语法重要）

```
FAILED test_day01.py::test_greet - AssertionError: assert 'hi Tom' == 'Hello, Tom!'
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                     + 实际结果              - 期望结果
```

读报错的顺序永远是从**最后一行往上**：

1. 最后一行：错在哪个用例、期望什么、实际是什么；
2. 中间：`day01.py` 第几行，把你写的那行代码指出来（`^` 指向出错位置）；
3. 最上面：调用栈，现在可以忽略。

## 一周安排

| 天 | 主题 | 文件 |
| --- | --- | --- |
| Day 1 | 字符串与列表 | `day01.py` |
| Day 2 | 字典、集合、排序 | `day02.py`（完成 Day 1 后发放） |
| Day 3 | 函数：参数、返回值、作用域、lambda | `day03.py` |
| Day 4 | 文件读写与异常处理 | `day04.py` |
| Day 5 | 类与对象、dataclass | `day05.py` |
| Day 6 | 模块、导入、标准库（pathlib / json / datetime） | `day06.py` |
| Day 7 | 小综合：命令行记账本（一个文件，200 行内） | `day07.py` |

> 只有 Day 1 现在就给你，后面的做完一个发一个——一次给七天，等于又把你淹了。

## Day 1 提示（卡住 20 分钟后再看）

<details>
<summary>点开提示</summary>

**greet**：`f"Hello, {name}!"` —— f-string 里花括号包变量。

**count_vowels**：先 `text.lower()`，再 `for ch in text:`，`if ch in "aeiou": count += 1`。

**reverse_words**：`words = text.split()` 得到列表；`" ".join(words[::-1])` 反转并拼回。
注意空字符串：`"".split()` 是 `[]`，`" ".join([])` 是 `""`，正好符合要求。

**normalize_spaces**：`" ".join(text.split())` —— 一行。`split()` 不带参数会自动处理连续空格和首尾空格。

**second_largest**：`unique = sorted(set(nums))`；`if len(unique) < 2: return None`；否则 `return unique[-2]`。

**chunk**：`[items[i:i + size] for i in range(0, len(items), size)]` —— 列表推导式 + 切片。
如果这个写法看着陌生，先用 for 循环 + `result.append(...)` 写一遍，能过测试就行。

</details>

## 做完 Day 1 之后

把 `uv run pytest` 的结果截图发我，我给你 Day 2。
如果有一题怎么都过不去，把那题的**报错原文**贴过来，我们一起读——学「读报错」比学语法更值钱。
