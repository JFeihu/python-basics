"""Day 7B 的测试 —— 命令行层的测试：参数进、输出出、退出码对。

这里不启进程，直接调 main([...])，所以又快又稳。
"""

from pathlib import Path

import pytest

from cli import main


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    return tmp_path / "book.json"


def run(data_file: Path, *args: str) -> int:
    return main(["--file", str(data_file), *args])


def test_add_and_list(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        run(data_file, "add", "100", "餐饮", "--date", "2026-10-27", "--note", "午饭")
        == 0
    )
    assert "已记录 #1" in capsys.readouterr().out

    assert run(data_file, "list") == 0
    out = capsys.readouterr().out
    assert "餐饮" in out
    assert "100" in out


def test_add_invalid_amount_returns_1(
    data_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(data_file, "add", "0", "餐饮", "--date", "2026-10-27") == 1
    assert "错误" in capsys.readouterr().err


def test_total(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run(data_file, "add", "100", "餐饮", "--date", "2026-10-27")
    run(data_file, "add", "50.5", "交通", "--date", "2026-11-02")
    capsys.readouterr()

    assert run(data_file, "total") == 0
    assert "150.5" in capsys.readouterr().out

    assert run(data_file, "total", "--month", "2026-11") == 0
    assert "50.5" in capsys.readouterr().out


def test_list_filters(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run(data_file, "add", "100", "餐饮", "--date", "2026-10-27")
    run(data_file, "add", "50.5", "交通", "--date", "2026-11-02")
    capsys.readouterr()

    assert run(data_file, "list", "--month", "2026-10") == 0
    out = capsys.readouterr().out
    assert "餐饮" in out
    assert "交通" not in out


def test_list_empty(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(data_file, "list") == 0
    assert "没有记录" in capsys.readouterr().out


def test_remove(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run(data_file, "add", "100", "餐饮", "--date", "2026-10-27")
    capsys.readouterr()

    assert run(data_file, "remove", "1") == 0
    assert "已删除 #1" in capsys.readouterr().out


def test_remove_missing_returns_1(
    data_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(data_file, "remove", "99") == 1
    assert "错误" in capsys.readouterr().err
