from array import array
from typing import Optional

WORD = 62


def bit_length64(x: int) -> int:
    return x.bit_length() if x < 4294967296 else (x >> 32).bit_length() + 32
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    x |= x >> 32
    x = x - ((x >> 1) & 0x5555555555555555)
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0F
    x += x >> 8
    x += x >> 16
    x += x >> 32
    return x & 0x0000007F


class MyWordsizeTreeSet:

    def __init__(self, u: int):
        self.u = u
        data = []
        len_ = 0
        while u:
            u //= WORD
            print(u + 1)
            data.append([0] * (u + 1))
        self.data: list[array[int]] = data
        self.len: int = len_
        self.len_data: int = len(data)

    def add(self, x: int) -> bool:
        assert (
            0 <= x < self.u
        ), f"ValueError: {self.__class__.__name__}.add({x}), u={self.u}"
        if self.data[0][x // WORD] >> (x % WORD) & 1:
            return False
        self.len += 1
        for a in self.data:
            a[x // WORD] |= 1 << (x % WORD)
            x //= WORD
        return True

    def discard(self, x: int) -> bool:
        assert (
            0 <= x < self.u
        ), f"ValueError: {self.__class__.__name__}.discard({x}), u={self.u}"
        if self.data[0][x // WORD] >> (x % WORD) & 1 == 0:
            return False
        self.len -= 1
        for a in self.data:
            a[x // WORD] &= ~(1 << (x % WORD))
            x //= WORD
            if a[x]:
                break
        return True

    def ge(self, x: int) -> Optional[int]:
        if x >= self.u:
            return
        assert (
            0 <= x < self.u
        ), f"ValueError: {self.__class__.__name__}.ge({x}), u={self.u}"
        data = self.data
        d = 0
        while True:
            if d >= self.len_data or x // WORD >= len(data[d]):
                return None
            m = data[d][x // WORD] & ((~0) << (x % WORD))
            if m == 0:
                d += 1
                x = (x // WORD) + 1
            else:
                x = (x // WORD * WORD) + bit_length64(m & -m) - 1
                if d == 0:
                    break
                x *= WORD
                d -= 1
        return x

    def le(self, x: int) -> Optional[int]:
        assert (
            0 <= x < self.u
        ), f"ValueError: {self.__class__.__name__}.le({x}), u={self.u}"
        data = self.data
        d = 0
        while True:
            if x < 0 or d >= self.len_data:
                return None
            m = data[d][x // WORD] & ~((~1) << (x % WORD))
            if m == 0:
                d += 1
                x = (x // WORD) - 1
            else:
                x = (x // WORD * WORD) + bit_length64(m) - 1
                if d == 0:
                    break
                x *= WORD
                x += WORD - 1
                d -= 1
        return x

    def tolist(self) -> list[int]:
        return [x for x in self]

    def __len__(self):
        return self.len

    def __contains__(self, x: int):
        assert (
            0 <= x < self.u
        ), f"ValueError: {x} in {self.__class__.__name__}, u={self.u}"
        return self.data[0][x // WORD] >> (x % WORD) & 1 == 1

    def __iter__(self):
        self._val = self.ge(0)
        return self

    def __next__(self):
        if self._val is None:
            raise StopIteration
        pre = self._val
        self._val = self.ge(pre + 1)
        return pre

    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"
