"""Day 7B：命令行入口（argparse + 调用 Ledger）

这一层只负责三件事：
1. 解析命令行参数（argv → 结构化数据）
2. 调用 Ledger 的方法
3. 把结果打印出来、返回退出码（0 成功，非 0 失败）

业务逻辑一行都不写在这里——这是"薄壳"原则（和 FastAPI 的路由层一样）。
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from day07 import Ledger


def build_parser() -> argparse.ArgumentParser:
    """定义命令和参数。argparse 的用法就是"声明式"：说清楚有哪些参数，它帮你解析和生成 --help。"""
    parser = argparse.ArgumentParser(prog="book", description="命令行记账本")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("book.json"),
        help="数据文件路径（默认 book.json）",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="记一笔")
    p_add.add_argument("amount", type=float, help="金额（必须大于 0）")
    p_add.add_argument("category", help="分类，如 餐饮/交通")
    p_add.add_argument("--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    p_add.add_argument("--note", default="", help="备注")

    p_list = sub.add_parser("list", help="列出记录")
    p_list.add_argument("--month", default=None, help="只列某月，如 2026-10")
    p_list.add_argument("--category", default=None, help="只列某分类")

    p_total = sub.add_parser("total", help="合计金额")
    p_total.add_argument("--month", default=None, help="只算某月")

    p_rm = sub.add_parser("remove", help="按 id 删除")
    p_rm.add_argument("id", type=int, help="记录 id")

    return parser


def cmd_add(ledger: Ledger, args: argparse.Namespace) -> int:
    """【已给示例】记一笔。看它怎么把异常变成友好提示 + 退出码。"""
    date_str = args.date or date.today().isoformat()
    try:
        record = ledger.add(args.amount, args.category, date_str, args.note)
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    print(
        f"已记录 #{record['id']}：{record['date']} {record['category']} {record['amount']} 元"
    )
    return 0


def cmd_list(ledger: Ledger, args: argparse.Namespace) -> int:
    """TODO：列出记录。

    要求：
    - 用 ledger.find(month=args.month, category=args.category) 拿数据；
    - 一条一行，格式：f"#{r['id']}  {r['date']}  {r['category']}  {r['amount']} 元  {r['note']}"
    - 没有记录时打印 "没有记录"；
    - 返回 0。
    """
    records = ledger.find(month=args.month, category=args.category)
    if not records:
        print("没有记录")
        return 0

    for r in records:
        print(
            f"#{r['id']}  {r['date']}  {r['category']}  {r['amount']} 元  {r['note']}"
        )
    return 0


def cmd_total(ledger: Ledger, args: argparse.Namespace) -> int:
    """TODO：打印合计。

    要求：
    - 用 ledger.total(args.month) 拿金额；
    - 有 month 时打印 f"{args.month} 合计：{amount} 元"，否则 f"合计：{amount} 元"；
    - 返回 0。
    """
    amount = ledger.total(args.month)
    if args.month:
        print(f"{args.month} 合计：{amount} 元")
    else:
        print(f"合计：{amount} 元")
    return 0


def cmd_remove(ledger: Ledger, args: argparse.Namespace) -> int:
    """【已给示例】按 id 删除。"""
    try:
        ledger.remove(args.id)
    except KeyError as exc:
        print(f"错误：{exc.args[0]}", file=sys.stderr)
        return 1
    print(f"已删除 #{args.id}")
    return 0


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "total": cmd_total,
    "remove": cmd_remove,
}


def main(argv: list[str] | None = None) -> int:
    """入口：解析参数 → 建 Ledger → 分发到对应命令 → 返回退出码。"""
    args = build_parser().parse_args(argv)
    ledger = Ledger(args.file)
    return COMMANDS[args.command](ledger, args)


if __name__ == "__main__":
    sys.exit(main())
