from typing import Optional, Iterable


class SegkiSet:

    # 0以上u未満の整数が載る集合
    # セグ木的な構造、各Nodeはその子孫のOR値を保持(ORではなくSUMならBITと同じ感じ)
    #
    # 空間: O(u)
    # add, discard, predecessor, successor: O(logu)
    # contains, len: O(1)
    # iteration: (nlogu)
    # kth element: O(klogu)

    def __init__(self, u: int, a: Iterable[int] = []):
        self.log = (u - 1).bit_length()
        self.size = 1 << self.log
        self.u = u
        self.data = bytearray(self.size << 1)
        self.len = 0
        for _a in a:
            self.add(_a)

    def add(self, k: int) -> bool:
        k += self.size
        if self.data[k]:
            return False
        self.len += 1
        self.data[k] = 1
        while k > 1:
            k >>= 1
            if self.data[k]:
                break
            self.data[k] = 1
        return True

    def discard(self, k: int) -> bool:
        k += self.size
        if self.data[k] == 0:
            return False
        self.len -= 1
        self.data[k] = 0
        while k > 1:
            if k & 1:
                if self.data[k - 1]:
                    break
            else:
                if self.data[k + 1]:
                    break
            k >>= 1
            self.data[k] = 0
        return True

    def get_min(self) -> Optional[int]:
        if self.data[1] == 0:
            return None
        k = 1
        while k < self.size:
            k <<= 1
            if self.data[k] == 0:
                k |= 1
        return k - self.size

    def get_max(self) -> Optional[int]:
        if self.data[1] == 0:
            return None
        k = 1
        while k < self.size:
            k <<= 1
            if self.data[k | 1]:
                k |= 1
        return k - self.size

    """Find the largest element < key, or None if it doesn't exist. / O(logN)"""

    def lt(self, k: int) -> Optional[int]:
        if self.data[1] == 0:
            return None
        x = k
        k += self.size
        while k > 1:
            if k & 1 and self.data[k - 1]:
                k >>= 1
                break
            k >>= 1
        k <<= 1
        if self.data[k] == 0:
            return None
        while k < self.size:
            k <<= 1
            if self.data[k | 1]:
                k |= 1
        k -= self.size
        return k if k < x else None

    """Find the smallest element > key, or None if it doesn't exist. / O(logN)"""

    def gt(self, k: int) -> Optional[int]:
        if self.data[1] == 0:
            return None
        x = k
        k += self.size
        while k > 1:
            if k & 1 == 0 and self.data[k + 1]:
                k >>= 1
                break
            k >>= 1
        k = k << 1 | 1
        while k < self.size:
            k <<= 1
            if self.data[k] == 0:
                k |= 1
        k -= self.size
        return k if k > x and k < self.u else None

    def le(self, k: int) -> Optional[int]:
        if self.data[k + self.size]:
            return k
        return self.lt(k)

    def ge(self, k: int) -> Optional[int]:
        if self.data[k + self.size]:
            return k
        return self.gt(k)

    def debug(self):
        print(
            "\n".join(
                " ".join(map(str, (self.data[(1 << i) + j] for j in range(1 << i))))
                for i in range(self.log + 1)
            )
        )

    def __contains__(self, k: int):
        return self.data[k + self.size] == 1

    def __getitem__(self, k: int):  # kは先頭か末尾にすることを推奨
        # O(klogu)
        if k < 0:
            k += self.len
        if k == 0:
            return self.get_min()
        if k == self.len - 1:
            return self.get_max()
        if k < self.len >> 1:
            key = self.get_min()
            for _ in range(k):
                key = self.gt(key)
        else:
            key = self.get_max()
            for _ in range(self.len - k - 1):
                key = self.lt(key)
        return key

    def __len__(self):
        return self.len

    def __iter__(self):
        key = self.get_min()
        while key is not None:
            yield key
            key = self.gt(key)

    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"
