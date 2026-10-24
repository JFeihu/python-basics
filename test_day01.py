"""Day 1 的测试 —— 先读这里，它就是题目要求。

不要修改这个文件。就算你觉得自己写对了、测试却红着，也先怀疑代码，别怀疑测试。
"""

from day01 import (
    add,
    chunk,
    count_vowels,
    greet,
    normalize_spaces,
    reverse_words,
    second_largest,
)


def test_add() -> None:
    # 这是示例题，一开始就应该是绿的。如果它红了，说明环境有问题。
    assert add(1, 2) == 3


def test_greet() -> None:
    assert greet("小明") == "Hello, 小明!"
    assert greet("Tom") == "Hello, Tom!"


def test_count_vowels() -> None:
    assert count_vowels("Hello") == 2
    assert count_vowels("XYZ") == 0
    assert count_vowels("AEIOU") == 5


def test_reverse_words() -> None:
    assert reverse_words("hello world") == "world hello"
    assert reverse_words("a b c") == "c b a"
    assert reverse_words("") == ""


def test_normalize_spaces() -> None:
    assert normalize_spaces("  a   b  ") == "a b"
    assert normalize_spaces("a b") == "a b"


def test_second_largest() -> None:
    assert second_largest([1, 2, 3]) == 2
    assert second_largest([3, 1, 9, 9]) == 3
    assert second_largest([5]) is None
    assert second_largest([]) is None
    assert second_largest([2, 2]) is None


def test_chunk() -> None:
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([], 3) == []
