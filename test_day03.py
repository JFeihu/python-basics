"""Day 3 的测试 —— 先读这里，它就是题目要求。不要修改。"""

from day03 import (
    apply_twice,
    build_query,
    clamp,
    make_multiplier,
    sort_by_abs,
    sum_all,
)


def test_apply_twice() -> None:
    assert apply_twice(lambda x: x + 1, 5) == 7
    assert apply_twice(str.upper, "ab") == "AB"


def test_make_multiplier() -> None:
    triple = make_multiplier(3)
    assert triple(4) == 12

    double = make_multiplier(2)
    assert double(5) == 10
    assert triple(5) == 15  # 两个闭包互不影响


def test_sum_all() -> None:
    assert sum_all() == 0
    assert sum_all(1, 2) == 3
    assert sum_all(1, 2, 3, 4) == 10


def test_build_query_no_params() -> None:
    assert build_query("https://api.com/users") == "https://api.com/users"


def test_build_query_sorts_keys() -> None:
    assert (
        build_query("https://api.com/users", b="2", a="1")
        == "https://api.com/users?a=1&b=2"
    )


def test_clamp() -> None:
    assert clamp(150) == 100
    assert clamp(-5) == 0
    assert clamp(50) == 50


def test_clamp_custom_bounds() -> None:
    assert clamp(150, high=200) == 150
    assert clamp(-5, low=-10) == -5


def test_sort_by_abs() -> None:
    numbers = [-3, 1, -2]
    assert sort_by_abs(numbers) == [1, -2, -3]
    assert numbers == [-3, 1, -2]  # 原列表没被改
    assert sort_by_abs([5, -5, 0]) == [0, 5, -5]
