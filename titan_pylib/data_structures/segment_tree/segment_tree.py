from titan_pylib.data_structures.segment_tree.segment_tree_interface import (
    SegmentTreeInterface,
)
from typing import Generic, Iterable, TypeVar, Callable, Union

T = TypeVar("T")


class SegmentTree(SegmentTreeInterface, Generic[T]):
    """セグ木です。非再帰です。"""

    def __init__(
        self, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T
    ) -> None:
        """``SegmentTree`` を構築します。
        :math:`O(n)` です。

        Args:
            n_or_a (Union[int, Iterable[T]]): ``n: int`` のとき、 ``e`` を初期値として長さ ``n`` の ``SegmentTree`` を構築します。
                                              ``a: Iterable[T]`` のとき、 ``a`` から ``SegmentTree`` を構築します。
            op (Callable[[T, T], T]): 2項演算の関数です。
            e (T): 単位元です。
        """
        self._op = op
        self._e = e
        if isinstance(n_or_a, int):
            self._n = n_or_a
            self._log = (self._n - 1).bit_length()
            self._size = 1 << self._log
            self._data = [e] * (self._size << 1)
        else:
            n_or_a = list(n_or_a)
            self._n = len(n_or_a)
            self._log = (self._n - 1).bit_length()
            self._size = 1 << self._log
            _data = [e] * (self._size << 1)
            _data[self._size : self._size + self._n] = n_or_a
            for i in range(self._size - 1, 0, -1):
                _data[i] = op(_data[i << 1], _data[i << 1 | 1])
            self._data = _data

    def set(self, k: int, v: T) -> None:
        """一点更新です。
        :math:`O(\\log{n})` です。

        Args:
            k (int): 更新するインデックスです。
            v (T): 更新する値です。

        制約:
            :math:`-n \\leq n \\leq k < n`
        """
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.set({k}, {v}), n={self._n}"
        if k < 0:
            k += self._n
        k += self._size
        self._data[k] = v
        for _ in range(self._log):
            k >>= 1
            self._data[k] = self._op(self._data[k << 1], self._data[k << 1 | 1])

    def get(self, k: int) -> T:
        """一点取得です。
        :math:`O(1)` です。

        Args:
            k (int): インデックスです。

        制約:
            :math:`-n \\leq n \\leq k < n`
        """
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.get({k}), n={self._n}"
        if k < 0:
            k += self._n
        return self._data[k + self._size]

    def prod(self, l: int, r: int) -> T:
        """区間 ``[l, r)`` の総積を返します。
        :math:`O(\\log{n})` です。

        Args:
            l (int): インデックスです。
            r (int): インデックスです。

        制約:
            :math:`0 \\leq l \\leq r \\leq n`
        """
        assert (
            0 <= l <= r <= self._n
        ), f"IndexError: {self.__class__.__name__}.prod({l}, {r})"
        l += self._size
        r += self._size
        lres = self._e
        rres = self._e
        while l < r:
            if l & 1:
                lres = self._op(lres, self._data[l])
                l += 1
            if r & 1:
                rres = self._op(self._data[r ^ 1], rres)
            l >>= 1
            r >>= 1
        return self._op(lres, rres)

    def all_prod(self) -> T:
        """区間 ``[0, n)`` の総積を返します。
        :math:`O(1)` です。
        """
        return self._data[1]

    def max_right(self, l: int, f: Callable[[T], bool]) -> int:
        """Find the largest index R s.t. f([l, R)) == True. / O(\\log{n})"""
        assert (
            0 <= l <= self._n
        ), f"IndexError: {self.__class__.__name__}.max_right({l}, f) index out of range"
        # assert f(self._e), \
        #     f'{self.__class__.__name__}.max_right({l}, f), f({self._e}) must be true.'
        if l == self._n:
            return self._n
        l += self._size
        s = self._e
        while True:
            while l & 1 == 0:
                l >>= 1
            if not f(self._op(s, self._data[l])):
                while l < self._size:
                    l <<= 1
                    if f(self._op(s, self._data[l])):
                        s = self._op(s, self._data[l])
                        l |= 1
                return l - self._size
            s = self._op(s, self._data[l])
            l += 1
            if l & -l == l:
                break
        return self._n

    def min_left(self, r: int, f: Callable[[T], bool]) -> int:
        """Find the smallest index L s.t. f([L, r)) == True. / O(\\log{n})"""
        assert (
            0 <= r <= self._n
        ), f"IndexError: {self.__class__.__name__}.min_left({r}, f) index out of range"
        # assert f(self._e), \
        #     f'{self.__class__.__name__}.min_left({r}, f), f({self._e}) must be true.'
        if r == 0:
            return 0
        r += self._size
        s = self._e
        while True:
            r -= 1
            while r > 1 and r & 1:
                r >>= 1
            if not f(self._op(self._data[r], s)):
                while r < self._size:
                    r = r << 1 | 1
                    if f(self._op(self._data[r], s)):
                        s = self._op(self._data[r], s)
                        r ^= 1
                return r + 1 - self._size
            s = self._op(self._data[r], s)
            if r & -r == r:
                break
        return 0

    def tolist(self) -> list[T]:
        """リストにして返します。
        :math:`O(n)` です。
        """
        return [self.get(i) for i in range(self._n)]

    def show(self) -> None:
        """デバッグ用のメソッドです。"""
        print(
            f"<{self.__class__.__name__}> [\n"
            + "\n".join(
                [
                    "  "
                    + " ".join(
                        map(str, [self._data[(1 << i) + j] for j in range(1 << i)])
                    )
                    for i in range(self._log + 1)
                ]
            )
            + "\n]"
        )

    def __getitem__(self, k: int) -> T:
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.__getitem__({k}), n={self._n}"
        return self.get(k)

    def __setitem__(self, k: int, v: T):
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.__setitem__{k}, {v}), n={self._n}"
        self.set(k, v)

    def __len__(self) -> int:
        return self._n

    def __str__(self) -> str:
        return str(self.tolist())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"
