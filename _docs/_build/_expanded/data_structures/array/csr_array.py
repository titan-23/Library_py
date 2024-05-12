# from titan_pylib.data_structures.array.csr_array import CSRArray
from typing import Generic, TypeVar, Iterator
from itertools import chain

T = TypeVar("T")


class CSRArray(Generic[T]):
    """CSR形式の配列です"""

    def __init__(self, a: list[list[T]]) -> None:
        """2次元配列 ``a`` を CSR 形式にします。

        Args:
          a (list[list[T]]): 変換する2次元配列です。
        """
        n = len(a)
        start = list(map(len, a))
        start.insert(0, 0)
        for i in range(n):
            start[i + 1] += start[i]
        self.csr: list[T] = list(chain(*a))
        self.start: list[int] = start

    def set(self, i: int, j: int, val: T) -> None:
        """インデックスを指定して値を更新します。

        Args:
          i (int): 行のインデックスです。
          j (int): 列のインデックスです。
          val (T): a[i][j] 要素を更新する値です。
        """
        self.csr[self.start[i] + j] = val

    def iter(self, i: int, j: int = 0) -> Iterator[T]:
        """行を指定してイテレートします。

        Args:
          i (int): 行のインデックスです。
          j (int, optional): 列のインデックスです。デフォルトは ``0`` です。
        """
        csr = self.csr
        for ij in range(self.start[i] + j, self.start[i + 1]):
            yield csr[ij]
