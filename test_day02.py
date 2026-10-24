"""Day 2 的测试 —— 先读这里，它就是题目要求。不要修改。"""

from day02 import (
    group_by_len,
    merge_sum,
    most_common_chars,
    top_n,
    unique_in_order,
    word_count,
)


def test_word_count_basic() -> None:
    assert word_count("apple banana apple") == {"apple": 2, "banana": 1}


def test_word_count_ignores_case() -> None:
    assert word_count("Apple apple APPLE") == {"apple": 3}
    assert word_count("") == {}


def test_top_n_orders_by_count_then_name() -> None:
    assert top_n({"a": 3, "b": 1, "c": 3}, 2) == [("a", 3), ("c", 3)]
    assert top_n({"z": 1, "y": 1}, 2) == [("y", 1), ("z", 1)]


def test_top_n_edge_cases() -> None:
    assert top_n({"a": 1}, 5) == [("a", 1)]
    assert top_n({"a": 1}, 0) == []


def test_group_by_len() -> None:
    result = group_by_len(["a", "bb", "cc", "d"])
    assert result == {2: ["bb", "cc"], 1: ["a", "d"]}
    assert group_by_len([]) == {}


def test_unique_in_order() -> None:
    assert unique_in_order([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert unique_in_order([]) == []


def test_merge_sum() -> None:
    assert merge_sum({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 5, "c": 4}
    assert merge_sum({}, {"a": 1}) == {"a": 1}


def test_most_common_chars() -> None:
    assert most_common_chars("aabbbcc", 2) == ["b", "a"]
    assert most_common_chars("Hello World", 3) == ["l", "o", "d"]
    assert most_common_chars("abc", 5) == ["a", "b", "c"]
