from typing import Union, Callable, TypeVar, Generic, Iterable

T = TypeVar("T")
F = TypeVar("F")


class DualCommutativeSegmentTree(Generic[T, F]):
    """作用が可換な双対セグ木です。"""

    def __init__(
        self,
        n_or_a: Union[int, Iterable[T]],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id: F,
    ) -> None:
        self.mapping: Callable[[F, T], T] = mapping
        self.composition: Callable[[F, F], F] = composition
        self.e: T = e
        self.id: F = id
        self.data: list[T] = [e] * n_or_a if isinstance(n_or_a, int) else list(n_or_a)
        self.n: int = len(self.data)
        self.log: int = (self.n - 1).bit_length()
        self.size: int = 1 << self.log
        self.lazy: list[F] = [id] * self.size

    def _all_apply(self, k: int, f: F) -> None:
        if k < self.size:
            self.lazy[k] = self.composition(f, self.lazy[k])
            return
        k -= self.size
        if k < self.n:
            self.data[k] = self.mapping(f, self.data[k])

    def _propagate(self, k: int) -> None:
        self._all_apply(k << 1, self.lazy[k])
        self._all_apply(k << 1 | 1, self.lazy[k])
        self.lazy[k] = self.id

    def apply_point(self, k: int, f: F) -> None:
        """``k`` 番目の値に ``f`` を作用させます。
        :math:`O(1)` です。

        Args:
            k (int): _description_
            f (F): _description_
        """
        assert (
            0 <= k < self.n
        ), f"IndexError: {self.__class__.__name__}.apply_point({k}, {f}), n={self.n}"
        self.data[k] = self.mapping(f, self.data[k])

    def apply(self, l: int, r: int, f: F) -> None:
        """区間 ``[l, r)`` に ``f`` を作用させます。
        :math:`O(\\log{n})` です。

        Args:
            l (int): _description_
            r (int): _description_
            f (F): _description_
        """
        assert (
            0 <= l <= r <= self.n
        ), f"IndexError: {self.__class__.__name__}.apply({l}, {r}, {f}), n={self.n}"
        if l == r:
            return
        if f == self.id:
            return
        l += self.size
        r += self.size
        data, lazy = self.data, self.lazy
        if (l - self.size) & 1:
            data[l - self.size] = self.mapping(f, data[l - self.size])
            l += 1
        if (r - self.size) & 1:
            data[(r - self.size) ^ 1] = self.mapping(f, data[(r - self.size) ^ 1])
            r ^= 1
        l >>= 1
        r >>= 1
        while l < r:
            if l & 1:
                lazy[l] = self.composition(f, lazy[l])
                l += 1
            if r & 1:
                r ^= 1
                lazy[r] = self.composition(f, lazy[r])
            l >>= 1
            r >>= 1

    def all_apply(self, f: F) -> None:
        """区間 ``[0, n)`` に ``f`` を作用させます。
        :math:`O(1)` です。
        """
        self.lazy[1] = self.composition(f, self.lazy[1])

    def all_propagate(self) -> None:
        for i in range(self.size):
            self._propagate(i)

    def tolist(self) -> list[T]:
        self.all_propagate()
        return self.data[:]

    def __getitem__(self, k: int) -> T:
        """``k`` 番目の値を取得します。
        :math:`O(\\log{n})` です。
        """
        assert (
            -self.n <= k < self.n
        ), f"IndexError: {self.__class__.__name__}[{k}], n={self.n}"
        if k < 0:
            k += self.n
        lazy = self.lazy
        k += self.size
        lazy_f = self.id
        for i in range(self.log, 0, -1):
            lazy_f = self.composition(lazy_f, lazy[k >> i])
        return self.mapping(lazy_f, self.data[k - self.size])

    def __setitem__(self, k: int, v: T) -> None:
        assert (
            -self.n <= k < self.n
        ), f"IndexError: {self.__class__.__name__}[{k}] = {v}, n={self.n}"
        if k < 0:
            k += self.n
        k += self.size
        for i in range(self.log, 0, -1):
            self._propagate(k >> i)
        self.data[k - self.size] = v

    def __str__(self):
        return str([self[i] for i in range(self.n)])

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
