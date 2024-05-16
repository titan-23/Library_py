from typing import Union, Sequence
from array import array


class BigInt:

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
        self.a = array("B", (int(a[i]) for i in range(len(a) - 1, start - 1, -1)))
        self.n = len(self.a)

    @classmethod
    def _gen(cls, a: array, sgn: bool):
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

    @staticmethod
    def _add(b1: "BigInt", b2: "BigInt") -> array:
        if b1.n > b2.n:
            b1, b2 = b2, b1
        a = array("B")
        carry = 0
        for i in range(b1.n):
            x = b1.a[i] + b2.a[i] + carry
            carry = 1 if x >= 10 else 0
            a.append(x % 10)
        for i in range(b1.n, b2.n):
            x = b2.a[i] + carry
            carry = 1 if x >= 10 else 0
            a.append(x % 10)
        if carry:
            a.append(carry)
        return a

    @staticmethod
    def _sub(b1: "BigInt", b2: "BigInt") -> tuple[array, bool]:
        sgn = True
        if b1._abs_lt(b2):
            b1, b2 = b2, b1
            sgn = False
        a = array("B")
        kurisagari = False
        for i in range(b2.n):
            val = b1.a[i] - kurisagari
            if val < b2.a[i]:
                kurisagari = True
                a.append(val + 10 - b2.a[i])
            else:
                kurisagari = False
                a.append(val - b2.a[i])
        for i in range(b2.n, b1.n):
            val = b1.a[i] - kurisagari
            if val < 0:
                kurisagari = True
                a.append(val + 10)
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
            res *= 10
            res += self.a[i]
        if not self.sgn:
            res = -res
        return res

    def __abs__(self) -> "BigInt":
        return self._gen(self.a[:], True)

    def __str__(self):
        return ("" if self.sgn else "-") + "".join(map(str, self.a))[::-1]

    __repr__ = __str__
