from typing import Generic, TypeVar, Iterable, Callable

T = TypeVar("T")


class SparseTable(Generic[T]):
    """``SparseTable`` です。

    静的であることに注意してください。
    """

    def __init__(self, a: Iterable[T], op: Callable[[T, T], T], e: T = None):
        """
        :math:`O(n\\log{n})` です。

        Args:
          a (Iterable[T]): ``SparseTable`` を構築する配列です。
          op (Callable[[T, T], T]): 2項演算の関数です。
          e (T, optional): 単位元です。
        """
        if not isinstance(a, list):
            a = list(a)
        self.size = len(a)
        log = self.size.bit_length() - 1
        data = [a] + [[]] * log
        for i in range(log):
            pre = data[i]
            l = 1 << i
            data[i + 1] = [op(pre[j], pre[j + l]) for j in range(len(pre) - l)]
        self.data = data
        self.op = op
        self.e = e

    def prod(self, l: int, r: int) -> T:
        """区間 ``[l, r)`` の総積を返します。

        :math:`O(\\log{n})` です。

        Args:
          l (int): インデックスです。
          r (int): インデックスです。
        """
        assert (
            0 <= l <= r <= self.size
        ), f"IndexError: {self.__class__.__name__}.prod({l}, {r}), len={self.size}"
        if l == r:
            return self.e
        u = (r - l).bit_length() - 1
        return self.op(self.data[u][l], self.data[u][r - (1 << u)])

    def __getitem__(self, k: int) -> T:
        assert (
            0 <= k < self.size
        ), f"IndexError: {self.__class__.__name__}[{k}], len={self.size}"
        return self.data[0][k]

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.data[0])

    def __repr__(self):
        return f"{self.__class__.__name__}({self}, {self.op}, {self.e})"
