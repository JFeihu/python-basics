"""Day 8（W1 进阶）：装饰器 · 迭代器 · 生成器（90~120 分钟）

这三个是 Python "进阶三件套"，也是面试必问。它们的关系：

    迭代器  = 一个有 __next__ 的对象，能被 for 遍历
    生成器  = 用 yield 自动造出来的迭代器（写起来简单 10 倍）
    装饰器  = 接收函数、返回新函数 —— 在函数外面套一层

今天 9 题，分三组。每组都会在后面的 dupefinder 项目里用到：
- 装饰器 → 给 find_duplicates 加 @timed 看耗时
- 生成器 → 把 iter_files 改成 yield，扫描大目录不占内存
- 迭代器 → 理解 for 循环到底在干什么

怎么用：读 test_day08.py → 实现 → uv run pytest test_day08.py -q -x
"""

import functools
import time
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from typing import Any

# ================================================================ 第一组：装饰器


# 1.接收被装饰的函数
def timed(func: Callable[..., Any]) -> Callable[..., Any]:
    """【练习 1】计时装饰器：调用函数后打印耗时。

    用法：
        @timed
        def slow():
            time.sleep(0.1)

        slow()   # 打印 "slow 耗时 0.1003s"，返回值不变

    要求：
    - 用 @functools.wraps(func) 保留原函数的名字和文档（否则 slow.__name__ 会变成 "wrapper"）；
    - 用 time.perf_counter() 计时（比 time.time() 精度高）；
    - 打印格式：f"{func.__name__} 耗时 {cost:.4f}s"；
    - **必须返回原函数的返回值**。

    提示：内部定义一个 wrapper(*args, **kwargs)，在里面调用 func(*args, **kwargs)。
          用 try/finally 包裹，保证函数抛异常时也能打印耗时。
    """

    @functools.wraps(func)  # 2.复制元信息 ==> 保存导入函数的函数名称和文档字符串
    def wrapper(*args, **kwargs):  # 3.真正被调用的替代品
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)  # 4.执行原函数
        finally:
            print(f"{func.__name__} 耗时 {time.perf_counter() - start:.4f}s")

    return wrapper  # 5.返回“函数对象本身”（不是调用结果）


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    """【练习 2】统计调用次数：每次调用后，wrapper.calls 加 1。

    用法：
        @count_calls
        def hello(): return "hi"

        hello(); hello()
        print(hello.calls)    # 2

    要求：
    - 保留原函数元信息（functools.wraps）；
    - wrapper 上挂一个属性 calls，初始为 0；
    - 每次调用先 +1，再返回原函数结果。

    提示：wrapper.calls = 0 要写在 return wrapper 之前；
          函数对象可以随便挂属性（Python 里函数也是对象）。
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.calls += 1

    wrapper.calls = 0
    return wrapper


def retry(times: int = 3) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """【练习 3】**带参数**的装饰器：失败自动重试，最多 times 次。

    用法：
        @retry(times=3)
        def flaky():
            ...

    要求：
    - 最多尝试 times 次，只要有一次成功就返回结果；
    - 全部失败时，把**最后一次**的异常抛出去；
    - 保留原函数元信息。

    提示：带参装饰器是三层结构：
              def retry(times=3):        # 第一层：接收装饰器参数
                  def decorator(func):   # 第二层：接收函数
                      def wrapper(...):  # 第三层：真正被调用的
                          ...
                      return wrapper
                  return decorator
          @retry(times=3) 等价于 func = retry(times=3)(func)。
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001 — 重试要对任何异常生效
                    last_error = exc
            raise last_error

        return wrapper

    return decorator


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """【练习 4】缓存装饰器：同样的参数只真正计算一次。

    用法：
        @memoize
        def slow(x):
            time.sleep(0.5)
            return x * 2

        slow(10)   # 第一次：慢
        slow(10)   # 第二次：瞬间返回

    要求：
    - 用字典缓存，key 是参数元组 args；
    - 同样的参数第二次调用不再执行原函数；
    - 保留原函数元信息。

    提示：cache = {} 写在装饰器内部（闭包会记住它）；
          if args not in cache: cache[args] = func(*args)
          （day07 里 Ledger 的"记住状态"是同一个思路，这里是函数级的记忆）
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        print(args)
        if args in cache:
            print(cache)
            return cache[args]
        else:
            cache[args] = func(*args)
            return cache[args]

    return wrapper


# ================================================================ 第二组：迭代器


class Countdown:
    """【练习 5】手写一个迭代器：从 start 倒数到 1。

    用法：
        list(Countdown(3))    # [3, 2, 1]
        for x in Countdown(2):  # 3.. 不，是 2, 1
            print(x)

    要求：
    - __init__(start)：保存 self.current = start；
    - __iter__：返回 self（迭代器自己就是"下一个"的提供者）；
    - __next__：返回当前值，然后减 1；减到 0 时 raise StopIteration。

    提示：for 循环的本质就是"反复调用 __next__，直到 StopIteration"。
    """

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "Countdown":
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# ================================================================ 第三组：生成器


def take(iterable: Iterable[Any], n: int) -> Iterator[Any]:
    """【练习 6】生成器：只取前 n 个元素。

    用法：
        take([1, 2, 3], 2)        # 产出 1, 2
        list(take(fib(), 5))      # 从无限生成器里取 5 个

    要求：
    - 用 yield 逐个产出，最多产出 n 个；
    - n 大于元素个数时，产出全部（不报错）；
    - n <= 0 时不产出任何东西。

    提示：for 循环里计数，达到 n 就 return（生成器里 return 会触发 StopIteration）。
    """
    for i, v in enumerate(iterable):
        if i >= n:
            return
        yield v


def chunked(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    """【练习 7】生成器：把可迭代对象切成固定大小的块。

    用法：
        list(chunked([1, 2, 3, 4, 5], 2))   # [[1, 2], [3, 4], [5]]
        list(chunked(iter(range(4)), 2))    # [[0, 1], [2, 3]]  ← 生成器输入也行

    要求：
    - 每满 size 个就 yield 一个列表；
    - 最后不满一块也要 yield；
    - 空输入产出空。

    提示：攒一个 buffer 列表，满了就 yield 并清空；循环结束后如果 buffer 非空，再 yield 一次。
          （不要用 len(items)，因为 items 可能是生成器，没有长度）
    """
    buffer = []
    for i, v in enumerate(items):
        buffer.append(v)
        if len(buffer) >= size:
            yield buffer
            buffer = []
    if len(buffer) != 0:
        yield buffer


def fib() -> Iterator[int]:
    """【练习 8】无限斐波那契生成器：0, 1, 1, 2, 3, 5, 8, ...

    因为它无限，所以**不能** list()，要用 islice 或 take 限量：
        list(take(fib(), 5))          # [0, 1, 1, 2, 3]

    要求：
    - 用 yield，从 0 开始；
    - 用 a, b = b, a + b 递推；
    - 永远不停止（while True）。

    提示：这就是生成器最大的价值——**能表示无限序列**，因为它是"用的时候才算"。
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_lines_lazy(path: Path) -> Iterator[str]:
    """【练习 9】生成器读文件：逐行产出非空行。

    和 Day 4 的 read_lines 需求一样，但**不一次性把整个文件读进内存**：
        for line in read_lines_lazy(big_file):    # 1GB 的文件也只占几十 KB
            ...

    要求：
    - encoding="utf-8"；
    - 去掉首尾空白，跳过空行；
    - 文件不存在时让它抛 FileNotFoundError（不捕获）。

    提示：with path.open(...) as fh: for line in fh: ... yield ...
          （with 块会一直开着，直到生成器被耗尽——这是生成器的"延迟执行"特性）
    """
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # strip()方法会去掉首尾空白，跳过空行
            if line:
                yield line
