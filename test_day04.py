"""Day 4 的测试 —— 先读这里，它就是题目要求。不要修改。"""

from pathlib import Path

import pytest

from day04 import count_words_in_file, read_lines, safe_int, write_report


def test_safe_int_ok() -> None:
    assert safe_int("42") == 42
    assert safe_int("  7  ") == 7


def test_safe_int_bad_input() -> None:
    assert safe_int("abc") == 0
    assert safe_int("3.5") == 0
    assert safe_int("abc", -1) == -1


def test_read_lines_skips_blank_lines(tmp_path: Path) -> None:
    file = tmp_path / "a.txt"
    file.write_text("第一行\n\n第二行\n   \n第三行\n", encoding="utf-8")

    assert read_lines(file) == ["第一行", "第二行", "第三行"]


def test_read_lines_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_lines(tmp_path / "not-exists.txt")


def test_count_words_in_file(tmp_path: Path) -> None:
    file = tmp_path / "words.txt"
    file.write_text("Apple banana\napple\n", encoding="utf-8")

    assert count_words_in_file(file) == {"apple": 2, "banana": 1}


def test_write_report(tmp_path: Path) -> None:
    file = tmp_path / "report.txt"
    counts = {"apple": 2, "banana": 1, "cherry": 2}

    written = write_report(file, counts)

    assert written == 3
    assert file.read_text(encoding="utf-8") == "apple: 2\ncherry: 2\nbanana: 1\n"


def test_write_report_chinese(tmp_path: Path) -> None:
    file = tmp_path / "cn.txt"
    write_report(file, {"中文": 1})

    assert file.read_text(encoding="utf-8") == "中文: 1\n"


def test_round_trip(tmp_path: Path) -> None:
    """写出去、再读回来，数据要一致（这就是最朴素的持久化）。"""
    file = tmp_path / "round.txt"
    file.write_text("one two two\n", encoding="utf-8")

    counts = count_words_in_file(file)
    write_report(file, counts)

    assert file.read_text(encoding="utf-8") == "two: 2\none: 1\n"
