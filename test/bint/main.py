from typing import Union, Sequence


class BigInt:

    _KETA = 18
    _BAI10 = 10**_KETA

    def __init__(
        self, a: Union[Sequence[int], int, str], _internal: bool = False
    ) -> None:
        if _internal:
            self.a = a
            self.n = len(a)
            return
        self.sgn = True
        if isinstance(a, int):
            a = str(a)
        if a and a[0] == "-":
            self.sgn = False
        start = 1 if a and (a[0] == "-" or a[0] == "+") else 0
        arr = []
        for i in range(len(a) - 1, start - 1, -self._KETA):
            val = 0
            for j in range(max(start, i - self._KETA + 1), i + 1):
                val *= 10
                val += int(a[j])
            arr.append(val)
        self.a = arr
        self.n = len(self.a)

    @classmethod
    def _gen(cls, a: list[int], sgn: bool):
        res = cls(a, True)
        res.sgn = sgn
        if res.n == 0:
            res.sgn = True
        return res

    def __eq__(self, other: "BigInt") -> bool:
        return self.sgn == other.sgn and self.a == other.a

    def __ge__(self, other: "BigInt") -> bool:
        return self == other or other < self

    def __gt__(self, other: "BigInt") -> bool:
        return other < self

    def __le__(self, other: "BigInt") -> bool:
        return self == other or self < other

    def __lt__(self, other: "BigInt") -> bool:
        if self.sgn and (not other.sgn):
            return False
        if (not self.sgn) and other.sgn:
            return True
        if self.sgn:
            # both +
            if self.n == other.n:
                for i in range(self.n - 1, -1, -1):
                    if self.a[i] < other.a[i]:
                        return True
                    if self.a[i] > other.a[i]:
                        return False
                return False  # same
            return self.n < other.n
        else:
            # both -
            if self.n == other.n:
                for i in range(self.n - 1, -1, -1):
                    if self.a[i] > other.a[i]:
                        return True
                    if self.a[i] < other.a[i]:
                        return False
                return False  # same
            return self.n > other.n

    def _abs_lt(self, other: "BigInt") -> bool:
        if self.n == other.n:
            for i in range(self.n - 1, -1, -1):
                if self.a[i] == other.a[i]:
                    continue
                return self.a[i] < other.a[i]
            return False  # same
        return self.n < other.n

    @classmethod
    def _add(cls, b1: "BigInt", b2: "BigInt") -> list[int]:
        if b1.n < b2.n:
            b1, b2 = b2, b1
        a = []
        carry = 0
        for i in range(b1.n):
            x = b1.a[i] + carry
            if i < b2.n:
                x += b2.a[i]
            if x >= cls._BAI10:
                carry = 1
                x -= cls._BAI10
            else:
                carry = 0
            a.append(x)
        if carry:
            a.append(carry)
        return a

    @classmethod
    def _sub(cls, b1: "BigInt", b2: "BigInt") -> tuple[list[int], bool]:
        sgn = True
        if b1._abs_lt(b2):
            b1, b2 = b2, b1
            sgn = False
        a = []
        kurisagari = False
        for i in range(b1.n):
            val = b1.a[i] - kurisagari
            if i < b2.n:
                val -= b2.a[i]
            if val < 0:
                kurisagari = True
                val += cls._BAI10
            else:
                kurisagari = False
            a.append(val)
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        return a, sgn

    def __add__(self, other: "BigInt") -> "BigInt":
        sgn = True
        if self.sgn and other.sgn:
            a = self._add(self, other)
            sgn = True
        elif (not self.sgn) and (not other.sgn):
            a = self._add(self, other)
            sgn = False
        else:
            if self.sgn:
                a, sgn = self._sub(self, other)
            else:
                a, sgn = self._sub(other, self)
        return self._gen(a, sgn)

    def __int__(self) -> int:
        res = 0
        for i in range(self.n - 1, -1, -1):
            res *= self._BAI10
            res += self.a[i]
        if not self.sgn:
            res = -res
        return res

    def __abs__(self) -> "BigInt":
        return self._gen(self.a[:], True)

    def __str__(self):
        return ("" if self.sgn else "-") + "".join(
            map(
                lambda x: str(x[1]).zfill(0 if x[0] == 0 else self._KETA),
                enumerate(reversed(self.a)),
            )
        )

    __repr__ = __str__


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
