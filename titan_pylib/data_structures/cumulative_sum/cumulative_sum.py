from typing import Iterable


class CumulativeSum:
    """1次元累積和です。"""

    def __init__(self, a: Iterable[int], e: int = 0):
        """
        :math:`O(n)` です。

        Args:
          a (Iterable[int]): ``CumulativeSum`` を構築する配列です。
          e (int): 単位元です。デフォルトは ``0`` です。
        """
        a = list(a)
        n = len(a)
        acc = [e] * (n + 1)
        for i in range(n):
            acc[i + 1] = acc[i] + a[i]
        self.n = n
        self.acc = acc
        self.a = a

    def pref(self, r: int) -> int:
        """区間 ``[0, r)`` の演算結果を返します。
        :math:`O(1)` です。

        Args:
          r (int): インデックスです。
        """
        assert (
            0 <= r <= self.n
        ), f"IndexError: {self.__class__.__name__}.pref({r}), n={self.n}"
        return self.acc[r]

    def all_sum(self) -> int:
        """区間 `[0, n)` の演算結果を返します。
        :math:`O(1)` です。

        Args:
          l (int): インデックスです。
          r (int): インデックスです。
        """
        return self.acc[-1]

    def sum(self, l: int, r: int) -> int:
        """区間 `[l, r)` の演算結果を返します。
        :math:`O(1)` です。

        Args:
          l (int): インデックスです。
          r (int): インデックスです。
        """
        assert (
            0 <= l <= r <= self.n
        ), f"IndexError: {self.__class__.__name__}.sum({l}, {r}), n={self.n}"
        return self.acc[r] - self.acc[l]

    prod = sum
    all_prod = all_sum

    def __getitem__(self, k: int) -> int:
        assert (
            -self.n <= k < self.n
        ), f"IndexError: {self.__class__.__name__}[{k}], n={self.n}"
        return self.a[k]

    def __len__(self):
        return len(self.a)

    def __str__(self):
        return str(self.acc)

    __repr__ = __str__
