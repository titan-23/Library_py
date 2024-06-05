from titan_pylib.math.big_int import BigInt
import random

random.seed(0)


def test_big_int():
    t = 10**5
    MAX = 10**20
    for _ in range(t):
        a = random.randint(-MAX, MAX)
        b = random.randint(-MAX, MAX)
        x = a + b
        y = BigInt(a) + BigInt(b)
        if str(x) != str(y):
            print("error: ", x, y)
            print(f"{a=}, {b=}")
            assert False
    exit(0)


# test_big_int()

import sys

# from titan_pylib.io.fast_o import FastO
import os
import io


class FastO:
    """標準出力高速化ライブラリです。"""

    _output = io.StringIO()

    @classmethod
    def write(cls, *args, sep: str = " ", end: str = "\n", flush: bool = False) -> None:
        """標準出力します。次の ``FastO.flush()`` が起きると print します。"""
        wr = cls._output.write
        for i in range(len(args) - 1):
            wr(str(args[i]))
            wr(sep)
        if args:
            wr(str(args[-1]))
        wr(end)
        if flush:
            cls.flush()

    @classmethod
    def flush(cls) -> None:
        """``flush`` します。これを実行しないと ``write`` した内容が表示されないので忘れないでください。"""
        os.write(1, cls._output.getvalue().encode())
        cls._output.close()


write, flush = FastO.write, FastO.flush
input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

t = int(input())
for _ in range(t):
    a, b = map(lambda x: BigInt(x), input().split())
    write(a + b)
flush()
