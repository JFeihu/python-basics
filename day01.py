"""Day 1：字符串与列表（60~90 分钟）

怎么用：
1. 先打开 test_day01.py 读测试 —— 那就是题目要求，每行 assert 就是一句"必须满足"；
2. 回到本文件，把函数里的 raise NotImplementedError 换成你的实现；
3. 每写完一个，运行：uv run pytest test_day01.py -q
4. 全绿就过关。不许改测试文件。

规则：一个函数卡住超过 20 分钟，再看 README 里的提示，别硬耗。
"""

# ---------------------------------------------------------------- 示例（不用改）


def add(a: int, b: int) -> int:
    """示例：返回 a + b。照着它的样子写下面的题。"""
    return a + b


# ---------------------------------------------------------------- 练习 1


def greet(name: str) -> str:
    """返回 "Hello, <name>!" 这样的问候语。
    greet("小明")  ->  "Hello, 小明!"
    greet("Tom")   ->  "Hello, Tom!"

    提示：用 f-string，例如 f"前缀{变量}后缀"
    """
    return f"Hello, {name}!"


# ---------------------------------------------------------------- 练习 2


def count_vowels(text: str) -> int:
    """数一数字符串里有几个元音字母（a e i o u），不区分大小写。

    count_vowels("Hello")  ->  2      （e 和 o）
    count_vowels("XYZ")    ->  0
    count_vowels("AEIOU")  ->  5

    提示：先把 text 用 .lower() 变小写，再 for 循环逐字符判断 in "aeiou"
    """
    count = 0
    text = text.lower()
    for char in text:
        if char in "aeiou":
            count += 1
    return count


# ---------------------------------------------------------------- 练习 3


def reverse_words(text: str) -> str:
    """把句子里的单词顺序反过来，单词本身的字母不动。

    reverse_words("hello world")  ->  "world hello"
    reverse_words("a b c")        ->  "c b a"
    reverse_words("")             ->  ""

    提示：text.split() 会按空白切成列表；" ".join(列表) 会拼回字符串
    """

    return " ".join(text.split()[::-1])


# ---------------------------------------------------------------- 练习 4


def normalize_spaces(text: str) -> str:
    """去掉首尾空格，并把中间连续的空格压成一个空格。

    normalize_spaces("  a   b  ")  ->  "a b"
    normalize_spaces("a b")        ->  "a b"

    提示：这题一行就能写完。想想 text.split() 对连续空格是什么行为，
          再想想 " ".join(...) 拼回来会怎样。
    """
    return " ".join(text.split())


# ---------------------------------------------------------------- 练习 5


def second_largest(nums: list[int]) -> int | None:
    """返回第二大的数（重复的值只算一次）；不够两个不同的数就返回 None。

    second_largest([1, 2, 3])      ->  2
    second_largest([3, 1, 9, 9])   ->  3
    second_largest([5])            ->  None
    second_largest([])             ->  None
    second_largest([2, 2])         ->  None

    提示：set(nums) 去重 → sorted(...) 排序 → 取倒数第二个；注意长度不够时返回 None
    """
    nums = list(set(nums))
    nums.sort(reverse=True)
    return nums[1] if len(nums) > 1 else None


# ---------------------------------------------------------------- 练习 6


def chunk(items: list[int], size: int) -> list[list[int]]:
    """把列表按 size 个一组切开，最后一组可以不满。
    chunk([1, 2, 3, 4, 5], 2)  ->  [[1, 2], [3, 4], [5]]
    chunk([], 3)               ->  []

    提示：range(0, len(items), size) 会给你 0, size, 2*size...；
          切片 items[i:i+size] 能取一段。
    """
    res = []
    for i in range(0, len(items), size):
        res.append(items[i : i + size])
    return res
