"""Day 2：字典、集合与排序（60~90 分钟）

昨天你练的是「一个字符串进来、一个数出去」。今天练的是**把数据装进字典再按规则排序**——
后端开发里 80% 的业务代码都在干这件事（统计、分组、排序、去重）。

怎么用：读 test_day02.py → 实现下面 6 个函数 → uv run pytest test_day02.py -q -x
"""


# ---------------------------------------------------------------- 练习 1


def word_count(text: str) -> dict[str, int]:
    """统计每个单词出现几次，单词统一转小写。

    word_count("apple banana apple")  ->  {"apple": 2, "banana": 1}
    word_count("Apple apple")          ->  {"apple": 2}
    word_count("")                     ->  {}

    提示：words = text.lower().split()；遍历 words，
          用 dict.get(word, 0) + 1 或者 if word in counts 判断。
    """

    res = {}
    for word in text.lower().split():
        res[word] = res.get(word, 0) + 1
    return res


# ---------------------------------------------------------------- 练习 2


def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """取出出现次数最多的 n 个，返回 (单词, 次数) 的列表。

    排序规则：次数从大到小；次数相同按字母从小到大。
    top_n({"a": 3, "b": 1, "c": 3}, 2)  ->  [("a", 3), ("c", 3)]
    top_n({"a": 1}, 5)                  ->  [("a", 1)]     （不够就全给）
    top_n({"a": 1}, 0)                  ->  []

    提示：sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])) 一次搞定两个排序条件，
          然后切片 [:n]。注意 n=0 时 [ :0] 正好是空列表。
    """
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


# ---------------------------------------------------------------- 练习 3


def group_by_len(words: list[str]) -> dict[int, list[str]]:
    """按单词长度分组，组内保持原来的先后顺序。

    group_by_len(["a", "bb", "cc", "d"])  ->  {2: ["bb", "cc"], 1: ["a", "d"]}

    提示：result.setdefault(len(word), []).append(word) —— 这一行是今天最值钱的技巧，
          它等价于「如果 key 不存在就先放一个空列表，然后追加」。
    """
    res = {}
    for word in words:
        res.setdefault(len(word), []).append(word)
        # res[len(word)] = res.get(len(word), []) + [word]
    return res


# ---------------------------------------------------------------- 练习 4


def unique_in_order(items: list[int]) -> list[int]:
    """去重，并且保留第一次出现的顺序。

    unique_in_order([3, 1, 3, 2, 1])  ->  [3, 1, 2]
    unique_in_order([])               ->  []

    提示：不能直接 list(set(items))，那样顺序会乱。
          用一个 seen = set() 记录见过的，再往 result 里 append。
    """
    seen = set(items)
    result = []
    for i in items:
        if i in seen:
            result.append(i)
            seen.remove(i)
    return result


# ---------------------------------------------------------------- 练习 5


def merge_sum(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """合并两个字典，相同 key 的值相加。

    merge_sum({"a": 1, "b": 2}, {"b": 3, "c": 4})  ->  {"a": 1, "b": 5, "c": 4}

    提示：先 result = dict(a) 复制一份，再遍历 b 的 items 往 result 里累加。
    """
    result = a.copy()
    for k, v in b.items():
        result[k] = result.get(k, 0) + v

    return result


# ---------------------------------------------------------------- 练习 6


def most_common_chars(text: str, n: int) -> list[str]:
    """返回出现次数最多的 n 个字符（忽略空格，不区分大小写）。

    排序规则和 top_n 一样：次数降序，次数相同按字母升序。
    most_common_chars("aabbbcc", 2)       ->  ["b", "a"]
    most_common_chars("Hello World", 3)   ->  ["l", "o", "d"]
    most_common_chars("abc", 5)           ->  ["a", "b", "c"]

    提示：先把 text.lower() 里的空格去掉（str.replace(" ", "") 或者循环时跳过），
          再复用你写的 word_count 思路统计每个字符，最后复用 top_n 的排序。
          这题就是在练「把昨天的函数拼起来」。
    """
    dic = {}
    for char in text.lower().replace(" ", ""):
        dic[char] = dic.get(char, 0) + 1
    return [x[0] for x in sorted(dic.items(), key=lambda kv: (-kv[1], kv[0]))[:n]]
