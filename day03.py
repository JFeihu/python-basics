"""Day 3：函数的三副面孔（60~90 分钟）

前两天你写的是「一个函数干一件事」。今天学的是 Python 函数的三层能力：

1. **参数可以灵活**：默认值、`*args`、`**kwargs`
2. **函数本身可以当值传**：作为参数、作为返回值（闭包）
3. **lambda**：临时用一次的小函数

这三层，就是后面 FastAPI 依赖注入、装饰器、回调的基础。

怎么用：读 test_day03.py → 实现下面 6 个函数 → uv run pytest test_day03.py -q -x
"""

# ---------------------------------------------------------------- 练习 1


def apply_twice(func, value):
    """把 func 连续作用两次。

    apply_twice(lambda x: x + 1, 5)  ->  7        （5 → 6 → 7）
    apply_twice(str.upper, "ab")      ->  "AB"     （ab → AB → AB）

    提示：函数也是值，可以接收、可以调用。直接 return func(func(value))。
          （这题没有类型注解，是因为"任意函数"不好写类型，明天不这么干）
    """
    return func(func(value))


# ---------------------------------------------------------------- 练习 2


def make_multiplier(factor: int):
    """返回一个函数，这个函数把传入的数乘以 factor。

    三倍 = make_multiplier(3)
    三倍(4)  ->  12

    两个不同的乘数互不影响：
    double = make_multiplier(2)
    triple = make_multiplier(3)
    double(5)  ->  10
    triple(5)  ->  15

    提示：在函数里面再定义一个函数并 return 它，内层函数能"记住" factor。
          这种「内层函数 + 外层变量」就叫闭包。
    """
    return lambda x: x * factor


# ---------------------------------------------------------------- 练习 3


def sum_all(*numbers: int) -> int:
    """把所有传进来的数加起来，传几个都行。

    sum_all()           ->  0
    sum_all(1, 2)       ->  3
    sum_all(1, 2, 3, 4) ->  10

    提示：*numbers 会把所有位置参数打包成一个元组，所以 numbers 是 (1, 2, 3)。
          可以直接用内置的 sum(numbers)。
    """

    return sum(numbers)


# ---------------------------------------------------------------- 练习 4


def build_query(base: str, **params: str) -> str:
    """把参数拼成 URL 查询串，参数按 key 字母序排列。

    build_query("https://api.com/users")                          ->  "https://api.com/users"
    build_query("https://api.com/users", b="2", a="1")             ->  "https://api.com/users?a=1&b=2"
    build_query("https://api.com/s", q="fastapi", page="2")        ->  "https://api.com/s?page=2&q=fastapi"

    提示：**params 会把所有关键字参数打包成字典。
          字典为空时直接返回 base（不要加 ?）。
          有参数时：先 sorted(params.items()) 按 key 排序，再拼 "k=v" 用 & 连接。
    """

    if not params:
        return base

    pairs = sorted(params.items())
    query = "&".join(f"{k}={v}" for k, v in pairs)
    return f"{base}?{query}"


# ---------------------------------------------------------------- 练习 5


def clamp(value: int, low: int = 0, high: int = 100) -> int:
    """把数值夹在 [low, high] 之间，超出就取边界值。

    clamp(150)              ->  100     （默认上限 100）
    clamp(-5)               ->  0       （默认下限 0）
    clamp(50)               ->  50
    clamp(150, high=200)    ->  150     （只改上限）
    clamp(-5, low=-10)      ->  -5      （只改下限）

    提示：这题是练「默认参数」。注意调用时可以用名字指定参数（high=200），
          也可以按位置传（clamp(150, 0, 200)）——两种都合法。
    """

    return low if value < low else min(value, high)


# ---------------------------------------------------------------- 练习 6


def sort_by_abs(numbers: list[int]) -> list[int]:
    """按绝对值从小到大排序，原列表不变。

    sort_by_abs([-3, 1, -2])  ->  [1, -2, -3]
    sort_by_abs([5, -5, 0])   ->  [0, 5, -5]      （绝对值相同保持原顺序）

    提示：sorted(numbers, key=lambda x: abs(x))。
          注意用 sorted 而不是 numbers.sort()——sort() 会改原列表，
          sorted 返回新列表，符合「原列表不变」的要求。
    """

    return sorted(numbers, key=lambda x: abs(x))
