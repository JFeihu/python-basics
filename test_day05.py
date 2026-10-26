"""Day 5 的测试 —— 先读这里，它就是题目要求。不要修改。"""

import pytest

from day05 import (
    Animal,
    BankAccount,
    Cat,
    Counter,
    Dog,
    Item,
    Point,
    TodoList,
    WordCounter,
)

# ---------------------------------------------------------------- 练习 1


def test_counter_basics() -> None:
    c = Counter()
    assert c.count == 0
    assert c.add() == 1
    assert c.add(3) == 4
    assert c.count == 4


def test_counter_reset() -> None:
    c = Counter()
    c.add(5)
    c.reset()
    assert c.count == 0


# ---------------------------------------------------------------- 练习 2


def test_point_repr_and_move() -> None:
    p = Point(1, 2)
    assert repr(p) == "Point(1, 2)"

    p.move(1, -1)
    assert (p.x, p.y) == (2, 1)


def test_point_equality() -> None:
    assert Point(1, 2) == Point(1, 2)
    assert Point(1, 2) != Point(2, 1)


def test_point_compares_with_other_types() -> None:
    """和完全不相关的类型比较，应该返回 False，而不是报错。"""
    assert Point(1, 2) != "Point(1, 2)"
    assert Point(1, 2) != 42


# ---------------------------------------------------------------- 练习 3


def test_bank_deposit_and_withdraw() -> None:
    acc = BankAccount(100)
    assert acc.deposit(50) == 150
    assert acc.withdraw(30) == 120
    assert acc.balance == 120


def test_bank_insufficient_balance() -> None:
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(1000)
    assert acc.balance == 100  # 失败后余额不变


def test_bank_invalid_amounts() -> None:
    with pytest.raises(ValueError):
        BankAccount(-1)

    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(0)
    with pytest.raises(ValueError):
        acc.withdraw(-10)


# ---------------------------------------------------------------- 练习 4


def test_item_defaults_and_total() -> None:
    assert Item("apple", 3.0).qty == 1
    assert Item("apple", 3.0).total() == 3.0
    assert Item("apple", 3.0, 2).total() == 6.0


def test_item_equality() -> None:
    """dataclass 自动生成了 __eq__，所以要自己写。"""
    assert Item("apple", 3.0) == Item("apple", 3.0)
    assert Item("apple", 3.0) != Item("apple", 4.0)


# ---------------------------------------------------------------- 练习 5


def test_dog_class_attribute() -> None:
    assert Dog.species == "Canis familiaris"

    rex = Dog("rex")
    assert rex.name == "rex"
    assert rex.species == "Canis familiaris"
    assert rex.describe() == "rex is a Canis familiaris"

    # name 是实例属性，species 不在实例的 __dict__ 里
    assert "name" in rex.__dict__
    assert "species" not in rex.__dict__


# ---------------------------------------------------------------- 练习 6


def test_cat_inherits_and_overrides() -> None:
    tom = Cat("Tom")
    assert tom.speak() == "meow"
    assert tom.intro() == "Tom says meow"  # intro 是从父类继承来的
    assert isinstance(tom, Animal)


def test_animal_base_behaviour() -> None:
    assert Animal("x").speak() == "..."


# ---------------------------------------------------------------- 练习 7


def test_wordcounter_accumulates() -> None:
    wc = WordCounter()
    wc.add("Apple banana")
    wc.add("apple")

    assert wc.counts == {"apple": 2, "banana": 1}


def test_wordcounter_top_and_len() -> None:
    wc = WordCounter()
    wc.add("apple banana apple cherry")

    assert len(wc) == 3
    assert wc.top(2) == [("apple", 2), ("banana", 1)]
    assert wc.top(10) == [("apple", 2), ("banana", 1), ("cherry", 1)]


def test_wordcounter_most_common() -> None:
    assert WordCounter().most_common() is None

    wc = WordCounter()
    wc.add("b b a")
    assert wc.most_common() == "b"


# ---------------------------------------------------------------- 练习 8


def test_todolist_add_returns_incrementing_id() -> None:
    todos = TodoList()
    assert todos.add("学类") == 1
    assert todos.add("写测试") == 2
    assert len(todos) == 2


def test_todolist_complete_and_pending() -> None:
    todos = TodoList()
    todos.add("a")
    todos.add("b")
    todos.add("c")

    todos.complete(2)

    assert todos.pending() == ["a", "c"]


def test_todolist_complete_missing_raises() -> None:
    todos = TodoList()
    todos.add("a")

    with pytest.raises(KeyError):
        todos.complete(99)


def test_todolist_len_counts_all() -> None:
    todos = TodoList()
    todos.add("a")
    todos.add("b")
    todos.complete(1)

    assert len(todos) == 2  # 完成的也算
