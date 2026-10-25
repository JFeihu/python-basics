"""Day 4：文件读写与异常处理（70~100 分钟）

前面三天，数据都在内存里——程序一结束就没了。
今天我教你两件事：

1. **把数据存进文件、再从文件读回来**（`with open(...)`）
2. **程序出错时不崩**（`try / except`）

这两件事在真实项目里无处不在：读配置、写日志、导入 Excel、导出报表、调第三方接口。

⚠️ Windows 上的大坑：`open()` 不写 `encoding="utf-8"` 时，默认用系统编码（中文 Windows 是 GBK），
   写中文再读回来就可能乱码。**今天所有 open 都必须带 encoding="utf-8"**。

怎么用：读 test_day04.py → 实现下面 4 个函数 → uv run pytest test_day04.py -q -x
"""

from pathlib import Path

# ---------------------------------------------------------------- 练习 1


def safe_int(text: str, default: int = 0) -> int:
    """把字符串转成整数；转不了就返回 default，绝不抛异常。

    safe_int("42")        ->  42
    safe_int("  7  ")     ->  7         （int 会自动忽略首尾空白）
    safe_int("abc")       ->  0
    safe_int("3.5")       ->  0         （int("3.5") 会报错）
    safe_int("abc", -1)   ->  -1

    提示：try 里写 return int(text)，except ValueError 里写 return default。
          只捕获 ValueError，不要写 except:（那会把键盘中断都吞掉）。
    """
    raise NotImplementedError("TODO: 实现 safe_int")


# ---------------------------------------------------------------- 练习 2


def read_lines(path: Path) -> list[str]:
    """读文件，返回所有非空行（去掉每行末尾的换行符）。

    - 空行（只有空白字符的行）要跳过；
    - 每行末尾的 \n 和 \r\n 都要去掉；
    - 必须用 encoding="utf-8" 打开，否则中文会乱码；
    - 文件不存在时**不要捕获异常**，让它抛 FileNotFoundError（让调用方决定怎么办）。

    提示：with path.open(encoding="utf-8") as f:
              for line in f:
                  line = line.strip()      # strip 会同时去掉空白和换行
                  if line:
                      result.append(line)
    """
    raise NotImplementedError("TODO: 实现 read_lines")


# ---------------------------------------------------------------- 练习 3


def count_words_in_file(path: Path) -> dict[str, int]:
    """统计文件里每个单词出现的次数（转小写）。

    文件内容：
        Apple banana
        apple
    返回：{"apple": 2, "banana": 1}

    提示：这题就是「读文件 + Day 2 的 word_count」的组合。
          可以 import day02 里的 word_count 来复用，也可以自己再写一遍。
          先 read_lines 拿到所有行，再用 " ".join(lines) 拼成一段文本。
    """
    raise NotImplementedError("TODO: 实现 count_words_in_file")


# ---------------------------------------------------------------- 练习 4


def write_report(path: Path, counts: dict[str, int]) -> int:
    """把统计结果写成文本文件，每行格式 "单词: 次数"，按次数从多到少排列。

    counts = {"apple": 2, "banana": 1}
    文件内容：
        apple: 2
        banana: 1

    要求：
    - 用 encoding="utf-8" 写（否则中文写进去就坏了）；
    - 每个词一行，按次数降序；次数相同按单词升序；
    - 文件末尾保留一个换行；
    - 返回写入的行数。

    提示：写文件用 path.open("w", encoding="utf-8")，同样放在 with 里。
          排序可以直接用 Day 2 的 top_n(counts, len(counts))。
          写完记得 return 行数（len(counts)）。
    """
    raise NotImplementedError("TODO: 实现 write_report")
