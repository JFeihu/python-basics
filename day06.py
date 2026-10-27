"""Day 6：模块与标准库（60~90 分钟）

今天不设计新东西，只学"用现成的工具"。三个库，对应三类天天要干的活：

- `json`     —— 把数据存成文件 / 从文件读出来（配置文件、接口数据、缓存）
- `datetime` —— 处理日期和时间（创建时间、统计、过期判断）
- `pathlib`  —— 处理路径（遍历目录、拼接路径、取扩展名）

还有一个"模块"的概念：`if __name__ == "__main__":` 是干什么的。

怎么用：读 test_day06.py → 实现 → uv run pytest test_day06.py -q -x
"""

import json
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- 练习 1：json 写


def save_json(path: Path, data: dict) -> None:
    """把字典写成 JSON 文件（UTF-8，中文不转义，缩进 2 空格）。

    要求：
    - 用 encoding="utf-8" 写；
    - json.dumps(..., ensure_ascii=False, indent=2) —— ensure_ascii=False 才能让中文原样显示，
      否则 "中文" 会被写成 "\\u4e2d\\u6587"，人能看懂才叫配置文件；
    - 不加其他额外处理。
    ensure_ascii: bool True时对所有非ASCII码的值进行转义，False时，所有字符原样输出，除了反斜杠或引号以外
    indent: 缩进，

    提示：path.write_text(json.dumps(...), encoding="utf-8") 一行搞定。
    """
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- 练习 2：json 读


def load_json(path: Path) -> dict:
    """读取 JSON 文件并解析成字典。

    要求：
    - 用 encoding="utf-8" 读；
    - 文件不存在时**不要捕获**，让它抛 FileNotFoundError；
    - 文件内容不是合法 JSON 时，也**不要捕获**，让它抛 json.JSONDecodeError。

    提示：json.loads(path.read_text(encoding="utf-8"))。
          为什么要"不捕获"？因为调用方才知道该提示用户还是用默认值（Day 4 讲过）。
    """
    # 在读取文件前，要先创建文件通道
    with path.open("r", encoding="utf-8") as f:
        return json.loads(f.read())


# ---------------------------------------------------------------- 练习 3：日期解析


def parse_date(text: str) -> date:
    """把 "2026-10-26" 这样的字符串解析成 date 对象。

    parse_date("2026-10-26")  ->  date(2026, 10, 26)
    parse_date("2026-13-01")  ->  抛 ValueError（13 月不存在）
    parse_date("2026/10/26")  ->  抛 ValueError（格式不对）

    提示：date.fromisoformat(text) 是最省事的写法（Python 3.7+ 支持）。
          也可以 datetime.strptime(text, "%Y-%m-%d").date()。
    """

    return date.fromisoformat(text)


# ---------------------------------------------------------------- 练习 4：日期计算


def days_between(start: str, end: str) -> int:
    """算两个日期相差几天（end - start，可以是负数）。

    days_between("2026-10-01", "2026-10-26")  ->  25
    days_between("2026-10-26", "2026-10-01")  ->  -25
    days_between("2026-10-01", "2026-10-01")  ->  0

    提示：两个 date 相减得到 timedelta，取 .days 属性。
          别忘了先 parse_date 转成 date 对象。
    """

    timedelta1 = parse_date(end) - parse_date(start)
    return timedelta1.days


# ---------------------------------------------------------------- 练习 5：遍历目录


def list_files_by_suffix(root: Path, suffix: str) -> list[str]:
    """递归找出 root 下所有以 suffix 结尾的**文件**，返回相对路径（用 / 分隔，已排序）。

    list_files_by_suffix(root, ".py")  ->  ["a.py", "sub/b.py"]
    list_files_by_suffix(root, ".md")  ->  ["README.md"]

    要求：
    - 结果是字符串，不是 Path 对象；
    - 用 `/` 分隔（Windows 上也要，方便前端/日志统一）；
    - 按路径字符串升序；
    - 目录不算（`rglob` 也会匹配到名字相符的目录）。

    提示：root.rglob(f"*{suffix}") 递归匹配；
          p.relative_to(root).as_posix() 得到 "sub/b.py" 这种字符串；
          过滤 `p.is_file()`；最后 sorted()。
    """

    p = [
        i.relative_to(root).as_posix() for i in root.rglob(f"*{suffix}") if i.is_file()
    ]
    res = sorted(p)
    return res


# ---------------------------------------------------------------- 练习 6：综合


def build_month_report(dates: list[str]) -> dict[str, int]:
    """按月统计日期出现次数，返回 {"2026-01": 2, "2026-02": 1} 这样的字典。

    build_month_report(["2026-01-05", "2026-01-20", "2026-02-01"])  ->  {"2026-01": 2, "2026-02": 1}
    build_month_report([])                                          ->  {}

    提示：遍历 dates → parse_date 转成 date → d.strftime("%Y-%m") 得到 "2026-01"
          → 用 Day 2 的字典累加（.get(key, 0) + 1）。
          这题把 Day 2、Day 4、Day 6 的东西串起来了。
    """

    res = {}
    for date1 in dates:
        d = parse_date(date1).strftime("%Y-%m")
        res[d] = res.get(d, 0) + 1
    return res
