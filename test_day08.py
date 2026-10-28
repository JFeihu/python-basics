"""Day 8 的测试 —— 先读这里，它就是题目要求。不要修改。"""

from pathlib import Path

import pytest

from day08 import (
    Countdown,
    chunked,
    count_calls,
    fib,
    memoize,
    read_lines_lazy,
    retry,
    take,
    timed,
)

# ================================================================ 装饰器


def test_timed_keeps_result_and_metadata(capsys: pytest.CaptureFixture[str]) -> None:
    @timed
    def add(a: int, b: int) -> int:
        """加法"""
        return a + b

    assert add(1, 2) == 3
    assert add.__name__ == "add"  # functools.wraps 保住了名字
    assert add.__doc__ == "加法"

    out = capsys.readouterr().out
    assert "add" in out
    assert "耗时" in out


def test_count_calls() -> None:
    @count_calls
    def hello() -> str:
        return "hi"

    assert hello.calls == 0
    hello()
    hello()
    assert hello.calls == 2
    assert hello() == "hi"


def test_retry_succeeds_after_failures() -> None:
    attempts = {"n": 0}

    @retry(times=3)
    def flaky() -> str:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ValueError("还没成功")
        return "ok"

    assert flaky() == "ok"
    assert attempts["n"] == 3


def test_retry_gives_up_and_raises_last_error() -> None:
    attempts = {"n": 0}

    @retry(times=2)
    def always_fail() -> None:
        attempts["n"] += 1
        raise ValueError("永远失败")

    with pytest.raises(ValueError):
        always_fail()
    assert attempts["n"] == 2


def test_memoize_only_computes_once() -> None:
    calls = {"n": 0}

    @memoize
    def slow(x: int) -> int:
        calls["n"] += 1
        return x * 2

    assert slow(10) == 20
    assert slow(10) == 20
    assert calls["n"] == 1  # 第二次直接拿缓存

    assert slow(11) == 22
    assert calls["n"] == 2  # 不同参数要重算


# ================================================================ 迭代器


def test_countdown_iterates() -> None:
    assert list(Countdown(3)) == [3, 2, 1]
    assert list(Countdown(1)) == [1]


def test_countdown_empty() -> None:
    assert list(Countdown(0)) == []


def test_countdown_is_its_own_iterator() -> None:
    c = Countdown(2)
    assert iter(c) is c


def test_countdown_exhausts_once() -> None:
    c = Countdown(2)
    assert list(c) == [2, 1]
    assert list(c) == []  # 迭代器只能消费一次


# ================================================================ 生成器


def test_take() -> None:
    assert list(take(fib(), 5)) == [0, 1, 1, 2, 3]
    assert list(take([1, 2, 3], 2)) == [1, 2]


def test_take_more_than_available() -> None:
    assert list(take([1, 2], 10)) == [1, 2]
    assert list(take([1, 2], 0)) == []


def test_chunked() -> None:
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunked_accepts_iterator() -> None:
    """生成器没有 len()，不能靠切片实现。"""
    assert list(chunked(iter(range(4)), 2)) == [[0, 1], [2, 3]]


def test_chunked_empty() -> None:
    assert list(chunked([], 3)) == []


def test_fib() -> None:
    assert list(take(fib(), 6)) == [0, 1, 1, 2, 3, 5]


def test_read_lines_lazy(tmp_path: Path) -> None:
    file = tmp_path / "a.txt"
    file.write_text("第一行\n\n第二行\n   \n第三行\n", encoding="utf-8")

    assert list(read_lines_lazy(file)) == ["第一行", "第二行", "第三行"]


def test_read_lines_lazy_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        list(read_lines_lazy(tmp_path / "nope.txt"))
