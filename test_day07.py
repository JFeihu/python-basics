"""Day 7A 的测试 —— 先读这里，它就是题目要求。不要修改。"""

import json
from pathlib import Path

import pytest

from day07 import Ledger


@pytest.fixture
def ledger(tmp_path: Path) -> Ledger:
    """每个测试都拿到一个干净的账本（临时文件，互不影响）。"""
    return Ledger(tmp_path / "data.json")


def test_new_ledger_is_empty(tmp_path: Path) -> None:
    book = Ledger(tmp_path / "new.json")
    assert book.records() == []


def test_add_returns_record_with_incrementing_id(ledger: Ledger) -> None:
    first = ledger.add(100, "餐饮", "2026-10-27", "午饭")
    second = ledger.add(50.5, "交通", "2026-10-28")

    assert first["id"] == 1
    assert second["id"] == 2
    assert first["amount"] == 100
    assert second["note"] == ""
    assert len(ledger.records()) == 2


def test_add_rejects_invalid_amount(ledger: Ledger) -> None:
    with pytest.raises(ValueError):
        ledger.add(0, "餐饮", "2026-10-27")
    with pytest.raises(ValueError):
        ledger.add(-5, "餐饮", "2026-10-27")


def test_add_rejects_invalid_date(ledger: Ledger) -> None:
    with pytest.raises(ValueError):
        ledger.add(10, "餐饮", "2026-13-01")


def test_add_saves_to_file(tmp_path: Path) -> None:
    path = tmp_path / "book.json"
    book = Ledger(path)
    book.add(100, "餐饮", "2026-10-27", "午饭")

    assert path.exists()
    # 换一个对象重新加载同一个文件，数据还在
    assert Ledger(path).records()[0]["note"] == "午饭"


def test_loads_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "old.json"
    path.write_text(
        json.dumps(
            [{"id": 7, "date": "2026-01-01", "amount": 1.5, "category": "其他"}]
        ),
        encoding="utf-8",
    )

    book = Ledger(path)

    assert book.records()[0]["id"] == 7
    # 新加的 id 要接着最大的往下走，而不是从 1 开始
    assert book.add(2, "其他", "2026-01-02")["id"] == 8


def test_records_returns_a_copy(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")

    snapshot = ledger.records()
    snapshot[0]["amount"] = 999  # 外部乱改这份快照

    assert ledger.records()[0]["amount"] == 100  # 账本本身没被污染


def test_find_by_month(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")
    ledger.add(20, "交通", "2026-11-02")

    result = ledger.find(month="2026-10")

    assert len(result) == 1
    assert result[0]["category"] == "餐饮"


def test_find_by_category(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")
    ledger.add(20, "交通", "2026-11-02")

    assert len(ledger.find(category="交通")) == 1


def test_find_combined(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")
    ledger.add(30, "餐饮", "2026-11-02")
    ledger.add(20, "交通", "2026-10-28")

    result = ledger.find(month="2026-10", category="餐饮")

    assert len(result) == 1
    assert result[0]["amount"] == 100


def test_total(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")
    ledger.add(50.5, "交通", "2026-10-28")
    ledger.add(30, "餐饮", "2026-11-02")

    assert ledger.total() == 180.5
    assert ledger.total("2026-10") == 150.5
    assert ledger.total("2026-12") == 0


def test_by_category(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")
    ledger.add(50.5, "交通", "2026-10-28")
    ledger.add(30, "餐饮", "2026-11-02")

    assert ledger.by_category() == {"餐饮": 130, "交通": 50.5}


def test_remove(ledger: Ledger) -> None:
    first = ledger.add(100, "餐饮", "2026-10-27")
    ledger.add(20, "交通", "2026-10-28")

    ledger.remove(first["id"])

    assert len(ledger.records()) == 1
    assert ledger.records()[0]["category"] == "交通"


def test_remove_missing_raises(ledger: Ledger) -> None:
    ledger.add(100, "餐饮", "2026-10-27")

    with pytest.raises(KeyError):
        ledger.remove(99)


def test_remove_persists(ledger: Ledger, tmp_path: Path) -> None:
    """删除之后要落盘，重新加载不能"复活"。"""
    first = ledger.add(100, "餐饮", "2026-10-27")
    ledger.remove(first["id"])

    assert Ledger(ledger.path).records() == []
