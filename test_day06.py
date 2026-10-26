"""Day 6 的测试 —— 先读这里，它就是题目要求。不要修改。"""

import json
from datetime import date
from pathlib import Path

import pytest

from day06 import (
    build_month_report,
    days_between,
    list_files_by_suffix,
    load_json,
    parse_date,
    save_json,
)

# ---------------------------------------------------------------- 练习 1


def test_save_json_keeps_chinese_readable(tmp_path: Path) -> None:
    file = tmp_path / "config.json"
    save_json(file, {"name": "张三", "age": 18})

    text = file.read_text(encoding="utf-8")

    assert "张三" in text  # 中文没有被转义成 \u5f20\u4e09
    assert "\n" in text  # indent=2 会产生换行
    assert json.loads(text) == {"name": "张三", "age": 18}


# ---------------------------------------------------------------- 练习 2


def test_load_json_roundtrip(tmp_path: Path) -> None:
    file = tmp_path / "data.json"
    save_json(file, {"items": [1, 2, 3]})

    assert load_json(file) == {"items": [1, 2, 3]}


def test_load_json_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_json(tmp_path / "nope.json")


def test_load_json_invalid_raises(tmp_path: Path) -> None:
    file = tmp_path / "bad.json"
    file.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_json(file)


# ---------------------------------------------------------------- 练习 3


def test_parse_date() -> None:
    assert parse_date("2026-10-26") == date(2026, 10, 26)


def test_parse_date_invalid() -> None:
    with pytest.raises(ValueError):
        parse_date("2026-13-01")
    with pytest.raises(ValueError):
        parse_date("2026/10/26")


# ---------------------------------------------------------------- 练习 4


def test_days_between() -> None:
    assert days_between("2026-10-01", "2026-10-26") == 25
    assert days_between("2026-10-01", "2026-10-01") == 0


def test_days_between_negative() -> None:
    assert days_between("2026-10-26", "2026-10-01") == -25


# ---------------------------------------------------------------- 练习 5


def test_list_files_by_suffix(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.txt").write_text("c", encoding="utf-8")
    (tmp_path / "sub" / "d.py").write_text("d", encoding="utf-8")

    assert list_files_by_suffix(tmp_path, ".txt") == ["a.txt", "sub/c.txt"]
    assert list_files_by_suffix(tmp_path, ".py") == ["sub/d.py"]


def test_list_files_by_suffix_empty(tmp_path: Path) -> None:
    assert list_files_by_suffix(tmp_path, ".md") == []


# ---------------------------------------------------------------- 练习 6


def test_build_month_report() -> None:
    dates = ["2026-01-05", "2026-01-20", "2026-02-01"]

    assert build_month_report(dates) == {"2026-01": 2, "2026-02": 1}


def test_build_month_report_empty() -> None:
    assert build_month_report([]) == {}
