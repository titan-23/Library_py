# from titan_pylib.data_structures.fenwick_tree.fenwick_tree_abst import FenwickTreeAbst
from typing import List, Union, Iterable, TypeVar, Generic, Callable

T = TypeVar("T")


class FenwickTreeAbst(Generic[T]):
    """和や逆元をこちらで定義できます。"""

    def __init__(
        self,
        n_or_a: Union[Iterable[T], T],
        op: Callable[[T, T], T],
        inv: Callable[[T], T],
        e: T,
    ) -> None:
        if isinstance(n_or_a, int):
            self._size = n_or_a
            self._tree = [e] * (self._size + 1)
        else:
            a = n_or_a if isinstance(n_or_a, list) else list(n_or_a)
            self._size = len(a)
            self._tree = [e] + a
            for i in range(1, self._size):
                if i + (i & -i) <= self._size:
                    self._tree[i + (i & -i)] = op(
                        self._tree[i + (i & -i)], self._tree[i]
                    )
        self.op = op
        self.inv = inv
        self.e = e
        self._s = 1 << (self._size - 1).bit_length()

    def pref(self, r: int) -> T:
        assert (
            0 <= r <= self._size
        ), f"IndexError: {self.__class__.__name__}.pref({r}), n={self._size}"
        ret = self.e
        while r > 0:
            ret = self.op(ret, self._tree[r])
            r -= r & -r
        return ret

    def suff(self, l: int) -> T:
        assert (
            0 <= l < self._size
        ), f"IndexError: {self.__class__.__name__}.suff({l}), n={self._size}"
        return self.op(self.pref(self._size), self.inv(self.pref(l)))

    def sum(self, l: int, r: int) -> T:
        assert (
            0 <= l <= r <= self._size
        ), f"IndexError: {self.__class__.__name__}.sum({l}, {r}), n={self._size}"
        _tree = self._tree
        res = self.e
        while r > l:
            res = self.op(res, _tree[r])
            r &= r - 1
        while l > r:
            res += self.inv(_tree[l])
            l &= l - 1
        return res

    prod = sum

    def __getitem__(self, k: int) -> T:
        assert (
            -self._size <= k < self._size
        ), f"IndexError: {self.__class__.__name__}.__getitem__({k}), n={self._size}"
        if k < 0:
            k += self._size
        return self.op(self.pref(k + 1), self.inv(self.pref(k)))

    def add(self, k: int, x: T) -> None:
        assert (
            0 <= k < self._size
        ), f"IndexError: {self.__class__.__name__}.add({k}, {x}), n={self._size}"
        k += 1
        while k <= self._size:
            self._tree[k] = self.op(self._tree[k], x)
            k += k & -k

    def __setitem__(self, k: int, x: T):
        assert (
            -self._size <= k < self._size
        ), f"IndexError: {self.__class__.__name__}.__setitem__({k}, {x}), n={self._size}"
        if k < 0:
            k += self._size
        pre = self.__getitem__(k)
        self.add(k, self.op(x, self.inv(pre)))

    def tolist(self) -> List[T]:
        sub = [self.pref(i) for i in range(self._size + 1)]
        return [self.op(sub[i + 1], self.inv(sub[i])) for i in range(self._size)]

    def __str__(self):
        return str(self.tolist())

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
