"""Day 7A：记账本核心类 Ledger（90 分钟）

这是一个"真正能用"的小项目，把前六天的东西全部串起来：

| 用到的 | 来自 |
| --- | --- |
| 类、`__init__`、实例属性 | Day 5 |
| 字典累加、排序 | Day 2 |
| JSON 读写、pathlib | Day 6 |
| 异常（ValueError、KeyError） | Day 4 |
| 函数复用（import day06） | Day 6 |

数据长这样（存在 JSON 文件里）：

[
  {"id": 1, "date": "2026-10-27", "amount": 100.0, "category": "餐饮", "note": "午饭"},
  {"id": 2, "date": "2026-10-28", "amount": 50.5, "category": "交通", "note": ""}
]

怎么用：读 test_day07.py → 实现 → uv run pytest test_day07.py -q -x
"""

import json
from pathlib import Path

from day06 import parse_date  # 复用你昨天写的日期解析


class Ledger:
    """一个记账本。创建时从文件加载，每次修改后自动保存。"""

    def __init__(self, path: Path) -> None:
        """path 是 JSON 文件路径。

        要求：
        - 文件不存在 → 空账本（self._records = []），**不要报错**；
        - 文件存在 → 读出 JSON 列表存进 self._records；
        - 把 path 存到 self.path（后面 save 要用）。

        提示：用 Day 6 的写法读：
              if path.exists():
                  self._records = json.loads(path.read_text(encoding="utf-8"))
              else:
                  self._records = []
        """
        self.path = path
        if path.exists():
            self._records = json.loads(path.read_text(encoding="utf-8"))
            # json.loads ===> 把传入的json格式的字符串转化为 python对象
        else:
            self._records = []

    def add(self, amount: float, category: str, date_str: str, note: str = "") -> dict:
        """新增一条记录，自动保存，返回这条记录。

        要求：
        - amount <= 0 → raise ValueError("金额必须大于 0")；
        - date_str 不是合法日期 → raise ValueError（用 parse_date 校验，让它自己抛）；
        - 记录格式：{"id": 自增, "date": date_str, "amount": float(amount),
                     "category": category, "note": note}；
        - id 从 1 开始递增，取"现有最大 id + 1"；
        - 加入 self._records 后调用 self.save()，然后返回这条记录。

        提示：max((r["id"] for r in self._records), default=0) + 1
        """
        if amount <= 0:
            raise ValueError("金额必须大于 0")
        parse_date(date_str)
        self._records.append(
            {
                "id": max((r["id"] for r in self._records), default=0) + 1,
                "date": date_str,
                "amount": float(amount),
                "category": category,
                "note": note,
            }
        )
        self.save()
        return self._records[-1]

    def records(self) -> list[dict]:
        """返回所有记录的**副本**（外部改了也不能影响账本本身）。"""
        return [dict(r) for r in self._records]

    def find(self, month: str | None = None, category: str | None = None) -> list[dict]:
        """按条件过滤记录，两个条件可以同时用。

        month 是 "2026-10" 这种格式（按前缀匹配）；
        category 是精确匹配；
        都不传 → 返回全部。

        提示：先复制一份 self.records()，再逐个条件筛：
              if month and not r["date"].startswith(month): 跳过
              if category and r["category"] != category: 跳过
        """
        find = []
        for r in self.records():
            if month and not r["date"].startswith(month):
                continue
            if category and r["category"] != category:
                continue
            find.append(r)

        return find

    def total(self, month: str | None = None) -> float:
        """所有记录金额之和；传 month 就只算那个月。"""
        amount = 0
        for dic in self.find(month):
            amount += dic["amount"]
        return amount

    def by_category(self) -> dict[str, float]:
        """按分类汇总：{"餐饮": 100.0, "交通": 50.5}。"""
        category_dic = {}
        for dic in self.records():
            category_dic[dic["category"]] = (
                category_dic.get(dic["category"], 0) + dic["amount"]
            )
        return category_dic

    def remove(self, record_id: int) -> None:
        """按 id 删除一条记录并保存；找不到 raise KeyError。

        提示：用列表推导式重建 self._records，或者遍历找下标后 del。
              找不到时 raise KeyError(f"没有 id={record_id} 的记录")。
        """

        remaining = [r for r in self._records if r["id"] != record_id]
        if len(remaining) == len(self._records):
            raise KeyError(f"没有 id={record_id} 的记录")
        self._records = remaining
        self.save()

    def save(self) -> None:
        """把 self._records 写回 JSON 文件（UTF-8，中文不转义，缩进 2）。"""
        self.path.write_text(
            json.dumps(self._records, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # json.dumps ===> 把传入的对象转化成 json 格式的、可以写入文件的字符串


if __name__ == "__main__":
    # 这一块已经写好：直接运行 python day07.py 就能看到效果
    demo = Path("demo_ledger.json")
    demo.unlink(missing_ok=True)  # 每次从空账本开始

    ledger = Ledger(demo)
    ledger.add(100, "餐饮", "2026-10-27", "午饭")
    ledger.add(50.5, "交通", "2026-10-28", "地铁")
    ledger.add(30, "餐饮", "2026-11-02")

    print("全部记录：", ledger.records())
    print("十月总计：", ledger.total("2026-10"))
    print("分类汇总：", ledger.by_category())
    print("十月餐饮：", ledger.find("2026-10", "餐饮"))
