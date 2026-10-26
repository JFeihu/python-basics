"""Day 5：类与对象（120 分钟，今天量比前几天大，可以拆成两次做）

为什么类重要：第 3 周你要读的 FastAPI 代码，几乎全是类——
`class TodoCreate(BaseModel)`、`class User(Base)`、`class Settings(BaseSettings)`。
看不懂类，那些代码就只是一堆看不懂的括号。

今天 8 题，分三组：
- 基础（1~4）：__init__ / self / 方法 / 实例属性 / 魔术方法 / dataclass
- 概念（5~6）：类属性 vs 实例属性、继承与方法重写
- 综合（7~8）：用类封装状态（这才是"什么时候该用类"）

怎么用：读 test_day05.py → 实现 → uv run pytest test_day05.py -q -x
"""

from dataclasses import dataclass

# ================================================================ 第一组：基础


class Counter:
    """练习 1：最简单的类——实例属性 + 方法。

    要求：
    - 创建时 count 为 0；
    - add(n=1)：把 count 加上 n，并**返回加完后的值**；
    - reset()：把 count 归零。
    """

    def __init__(self) -> None:
        # 这题把 __init__ 给你写好了，看它怎么用 self
        self.count = 0

    def add(self, n: int = 1) -> int:
        self.count += n
        return self.count

    def reset(self) -> None:
        self.count = 0


class Point:
    """练习 2：魔术方法——让对象"像内置类型一样"好用。

    要求：
    - __init__(x, y)：保存到 self.x / self.y；
    - __repr__：返回 "Point(1, 2)" 这种字符串（注意逗号后面有空格）；
    - __eq__：两个 Point 的 x、y 都相同就相等；和别的类型比较返回 False（不要报错）；
    - move(dx, dy)：原地修改坐标，没有返回值。

    提示：__eq__ 里先 isinstance(other, Point) 判断类型，不同类型直接 return False。
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        # 实例对象本身并不是一个类型，它只是类产生出来的对象，所以这里的第二个参数不能传入 self
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


class BankAccount:
    """练习 3：封装——对象自己保证数据合法，外部改不坏。

    要求：
    - __init__(balance=0)：balance 存到 self.balance；如果传负数，抛 ValueError；
    - deposit(amount)：amount <= 0 抛 ValueError；否则加钱，**返回新余额**；
    - withdraw(amount)：amount <= 0 抛 ValueError；余额不足抛 ValueError("余额不足")；
      否则扣钱，返回新余额。

    提示：raise ValueError("金额必须大于 0") —— 异常消息写清楚，调试时能救命。
    """

    def __init__(self, balance: float = 0) -> None:
        if balance < 0:
            raise ValueError("金额必须大于 0")
        else:
            self.balance = balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("金额必须大于 0")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("金额必须大于 0")
        elif amount > self.balance:
            raise ValueError("余额不足")
        else:
            self.balance -= amount
            return self.balance


@dataclass
class Item:
    """练习 4：dataclass——自动生成 __init__ / __repr__ / __eq__。

    上面三行就是全部字段声明，等价于手写 __init__ 保存三个属性 + __repr__ + __eq__。
    你只需要加一个方法 total()，返回 price * qty。
    """

    name: str
    price: float
    qty: int = 1

    def total(self) -> float:
        return self.price * self.qty


# ================================================================ 第二组：概念


class Dog:
    """练习 5：类属性 vs 实例属性。

    species 写在类里、不在 __init__ 里 → 它是**类属性**，所有 Dog 共享一份。
    name 在 __init__ 里用 self.name 赋值 → 是**实例属性**，每条狗各一份。

    要求：
    - __init__(name)：保存 self.name；
    - describe()：返回 "rex is a Canis familiaris"（用 self.name 和类属性拼）。

    想一个问题：如果在 __init__ 里写 self.species = "..."，会发生什么？
    会在实例对象中创建一个专属的实例属性，且只能通过 实例.species 调用
    而类属性就要通过 类名.类属性 调用二者互不干扰
    """

    species = "Canis familiaris"

    def __init__(self, name: str) -> None:
        self.name = name

    def describe(self) -> str:
        return f"{self.name} is a {Dog.species}"


class Animal:
    """练习 6 的父类，已经写好，不用改。"""

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."

    def intro(self) -> str:
        return f"{self.name} says {self.speak()}"


class Cat(Animal):
    """练习 6：继承 + 方法重写。

    要求：只重写 speak()，返回 "meow"。

    观察点：你没有重写 __init__ 和 intro，但它们已经能用了——
    因为 Cat 继承了 Animal 的全部方法，只需要改掉不一样的那一个。
    这就是"重写（override）"。
    """

    def speak(self) -> str:
        return "meow"


# ================================================================ 第三组：综合


class WordCounter:
    """练习 7：什么时候该用类——当你要"记住状态"的时候。

    你已经用函数写过 word_count（Day 2）：一次调用、一次结果、不记状态。
    现在要"持续累加"：add("apple banana") 再 add("apple")，结果要合并。
    这就需要对象把数据存在自己身上。

    要求：
    - __init__：self.counts = {}（单词 → 次数）；
    - add(text)：按空白分词、转小写、累加到 self.counts（多次调用要累加，不是覆盖）；
    - top(n)：返回 [(单词, 次数), ...]，次数降序、同次数按字母升序（复用 Day 2 的规则）；
    - __len__：返回不同单词的个数；
    - most_common()：返回次数最多的那个单词；一个词都没有时返回 None。
    """

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def add(self, text: str) -> None:
        words = text.lower().split()
        for item in words:
            self.counts[item] = self.counts.get(item, 0) + 1

    def top(self, n: int) -> list[tuple[str, int]]:

        return sorted(self.counts.items(), key=lambda x: (-x[1], x[0]))[:n]

    def __len__(self) -> int:
        return len(self.counts)

    def most_common(self) -> str | None:
        if self.counts == {}:
            return None
        else:
            return self.top(1)[0][0]


class TodoList:
    """练习 8：综合——一个带状态的小列表（和第 3 周的 Todo 接口同构）。

    要求：
    - __init__：self._todos = []，每个元素是 {"id": int, "title": str, "done": bool}；
    - add(title)：追加一条，id 从 1 开始递增，返回新 id；
    - complete(todo_id)：把对应任务标记 done=True；找不到就 raise KeyError；
    - pending()：返回所有**未完成**任务的 title 列表（保持添加顺序）；
    - __len__：任务总数（完成的也算）。
    """

    def __init__(self) -> None:
        self._todos: list[dict] = []

    def add(self, title: str) -> int:
        todo_id = len(self._todos) + 1
        self._todos.append({"id": len(self) + 1, "title": title, "done": False})
        return todo_id

    def complete(self, todo_id: int) -> None:
        # try:
        #     self._todos[todo_id - 1]["done"] = True
        # except:
        #     raise KeyError
        for todo in self._todos:
            if todo["id"] == todo_id:
                todo["done"] = True
                return
        raise KeyError(f"没有 id={todo_id} 的任务")

    def pending(self) -> list[str]:
        res = []
        for dic in self._todos:
            if not dic["done"]:
                res.append(dic["title"])
        return res

    def __len__(self) -> int:
        return len(self._todos)
