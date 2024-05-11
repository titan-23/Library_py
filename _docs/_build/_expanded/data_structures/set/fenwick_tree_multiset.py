# from titan_pylib.data_structures.set.fenwick_tree_multiset import FenwickTreeMultiset
# from titan_pylib.data_structures.set.fenwick_tree_set import FenwickTreeSet
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
# from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
from typing import List, Union, Iterable, Optional


class FenwickTree:
    """FenwickTreeです。"""

    def __init__(self, n_or_a: Union[Iterable[int], int]):
        """構築します。
        :math:`O(n)` です。

        Args:
          n_or_a (Union[Iterable[int], int]): `n_or_a` が `int` のとき、初期値 `0` 、長さ `n` で構築します。
                                              `n_or_a` が `Iterable` のとき、初期値 `a` で構築します。
        """
        if isinstance(n_or_a, int):
            self._size = n_or_a
            self._tree = [0] * (self._size + 1)
        else:
            a = n_or_a if isinstance(n_or_a, list) else list(n_or_a)
            _size = len(a)
            _tree = [0] + a
            for i in range(1, _size):
                if i + (i & -i) <= _size:
                    _tree[i + (i & -i)] += _tree[i]
            self._size = _size
            self._tree = _tree
        self._s = 1 << (self._size - 1).bit_length()

    def pref(self, r: int) -> int:
        """区間 ``[0, r)`` の総和を返します。
        :math:`O(\\log{n})` です。
        """
        assert (
            0 <= r <= self._size
        ), f"IndexError: {self.__class__.__name__}.pref({r}), n={self._size}"
        ret, _tree = 0, self._tree
        while r > 0:
            ret += _tree[r]
            r &= r - 1
        return ret

    def suff(self, l: int) -> int:
        """区間 ``[l, n)`` の総和を返します。
        :math:`O(\\log{n})` です。
        """
        assert (
            0 <= l < self._size
        ), f"IndexError: {self.__class__.__name__}.suff({l}), n={self._size}"
        return self.pref(self._size) - self.pref(l)

    def sum(self, l: int, r: int) -> int:
        """区間 ``[l, r)`` の総和を返します。
        :math:`O(\\log{n})` です。
        """
        assert (
            0 <= l <= r <= self._size
        ), f"IndexError: {self.__class__.__name__}.sum({l}, {r}), n={self._size}"
        _tree = self._tree
        res = 0
        while r > l:
            res += _tree[r]
            r &= r - 1
        while l > r:
            res -= _tree[l]
            l &= l - 1
        return res

    prod = sum

    def __getitem__(self, k: int) -> int:
        """位置 ``k`` の要素を返します。
        :math:`O(\\log{n})` です。
        """
        assert (
            -self._size <= k < self._size
        ), f"IndexError: {self.__class__.__name__}[{k}], n={self._size}"
        if k < 0:
            k += self._size
        return self.sum(k, k + 1)

    def add(self, k: int, x: int) -> None:
        """``k`` 番目の値に ``x`` を加えます。
        :math:`O(\\log{n})` です。
        """
        assert (
            0 <= k < self._size
        ), f"IndexError: {self.__class__.__name__}.add({k}, {x}), n={self._size}"
        k += 1
        _tree = self._tree
        while k <= self._size:
            _tree[k] += x
            k += k & -k

    def __setitem__(self, k: int, x: int):
        """``k`` 番目の値を ``x`` に更新します。
        :math:`O(\\log{n})` です。
        """
        assert (
            -self._size <= k < self._size
        ), f"IndexError: {self.__class__.__name__}[{k}] = {x}, n={self._size}"
        if k < 0:
            k += self._size
        pre = self[k]
        self.add(k, x - pre)

    def bisect_left(self, w: int) -> Optional[int]:
        i, s, _size, _tree = 0, self._s, self._size, self._tree
        while s:
            if i + s <= _size and _tree[i + s] < w:
                w -= _tree[i + s]
                i += s
            s >>= 1
        return i if w else None

    def bisect_right(self, w: int) -> int:
        i, s, _size, _tree = 0, self._s, self._size, self._tree
        while s:
            if i + s <= _size and _tree[i + s] <= w:
                w -= _tree[i + s]
                i += s
            s >>= 1
        return i

    def _pop(self, k: int) -> int:
        assert k >= 0
        i, acc, s, _size, _tree = 0, 0, self._s, self._size, self._tree
        while s:
            if i + s <= _size:
                if acc + _tree[i + s] <= k:
                    acc += _tree[i + s]
                    i += s
                else:
                    _tree[i + s] -= 1
            s >>= 1
        return i

    def tolist(self) -> List[int]:
        """リストにして返します。
        :math:`O(n)` です。
        """
        sub = [self.pref(i) for i in range(self._size + 1)]
        return [sub[i + 1] - sub[i] for i in range(self._size)]

    @staticmethod
    def get_inversion_num(a: List[int], compress: bool = False) -> int:
        inv = 0
        if compress:
            a_ = sorted(set(a))
            z = {e: i for i, e in enumerate(a_)}
            fw = FenwickTree(len(a_))
            for i, e in enumerate(a):
                inv += i - fw.pref(z[e])
                fw.add(z[e], 1)
        else:
            fw = FenwickTree(len(a))
            for i, e in enumerate(a):
                inv += i - fw.pref(e)
                fw.add(e, 1)
        return inv

    def __str__(self):
        return str(self.tolist())

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
from typing import Dict, Iterable, TypeVar, Generic, Union, Optional

T = TypeVar("T", bound=SupportsLessThan)


class FenwickTreeSet(Generic[T]):

    def __init__(
        self,
        _used: Union[int, Iterable[T]],
        _a: Iterable[T] = [],
        compress=True,
        _multi=False,
    ) -> None:
        self._len = 0
        if isinstance(_used, int):
            self._to_origin = list(range(_used))
        elif isinstance(_used, set):
            self._to_origin = sorted(_used)
        else:
            self._to_origin = sorted(set(_used))
        self._to_zaatsu: Dict[T, int] = (
            {key: i for i, key in enumerate(self._to_origin)}
            if compress
            else self._to_origin
        )
        self._size = len(self._to_origin)
        self._cnt = [0] * self._size
        _a = list(_a)
        if _a:
            a_ = [0] * self._size
            if _multi:
                self._len = len(_a)
                for v in _a:
                    i = self._to_zaatsu[v]
                    a_[i] += 1
                    self._cnt[i] += 1
            else:
                for v in _a:
                    i = self._to_zaatsu[v]
                    if self._cnt[i] == 0:
                        self._len += 1
                        a_[i] = 1
                        self._cnt[i] = 1
            self._fw = FenwickTree(a_)
        else:
            self._fw = FenwickTree(self._size)

    def add(self, key: T) -> bool:
        i = self._to_zaatsu[key]
        if self._cnt[i]:
            return False
        self._len += 1
        self._cnt[i] = 1
        self._fw.add(i, 1)
        return True

    def remove(self, key: T) -> None:
        if not self.discard(key):
            raise KeyError(key)

    def discard(self, key: T) -> bool:
        i = self._to_zaatsu[key]
        if self._cnt[i]:
            self._len -= 1
            self._cnt[i] = 0
            self._fw.add(i, -1)
            return True
        return False

    def le(self, key: T) -> Optional[T]:
        i = self._to_zaatsu[key]
        if self._cnt[i]:
            return key
        pref = self._fw.pref(i) - 1
        return None if pref < 0 else self._to_origin[self._fw.bisect_right(pref)]

    def lt(self, key: T) -> Optional[T]:
        pref = self._fw.pref(self._to_zaatsu[key]) - 1
        return None if pref < 0 else self._to_origin[self._fw.bisect_right(pref)]

    def ge(self, key: T) -> Optional[T]:
        i = self._to_zaatsu[key]
        if self._cnt[i]:
            return key
        pref = self._fw.pref(i + 1)
        return (
            None if pref >= self._len else self._to_origin[self._fw.bisect_right(pref)]
        )

    def gt(self, key: T) -> Optional[T]:
        pref = self._fw.pref(self._to_zaatsu[key] + 1)
        return (
            None if pref >= self._len else self._to_origin[self._fw.bisect_right(pref)]
        )

    def index(self, key: T) -> int:
        return self._fw.pref(self._to_zaatsu[key])

    def index_right(self, key: T) -> int:
        return self._fw.pref(self._to_zaatsu[key] + 1)

    def pop(self, k: int = -1) -> T:
        assert (
            -self._len <= k < self._len
        ), f"IndexError: FenwickTreeSet.pop({k}), Index out of range."
        if k < 0:
            k += self._len
        self._len -= 1
        x = self._fw._pop(k)
        self._cnt[x] = 0
        return self._to_origin[x]

    def pop_min(self) -> T:
        assert (
            self._len > 0
        ), f"IndexError: pop_min() from empty {self.__class__.__name__}."
        return self.pop(0)

    def pop_max(self) -> T:
        assert (
            self._len > 0
        ), f"IndexError: pop_max() from empty {self.__class__.__name__}."
        return self.pop(-1)

    def get_min(self) -> Optional[T]:
        if not self:
            return
        return self[0]

    def get_max(self) -> Optional[T]:
        if not self:
            return
        return self[-1]

    def __getitem__(self, k):
        assert (
            -self._len <= k < self._len
        ), f"IndexError: FenwickTreeSet[{k}], Index out of range."
        if k < 0:
            k += self._len
        return self._to_origin[self._fw.bisect_right(k)]

    def __iter__(self):
        self._iter = 0
        return self

    def __next__(self):
        if self._iter == self._len:
            raise StopIteration
        res = self._to_origin[self._fw.bisect_right(self._iter)]
        self._iter += 1
        return res

    def __reversed__(self):
        _to_origin = self._to_origin
        for i in range(self._len):
            yield _to_origin[self._fw.bisect_right(self._len - i - 1)]

    def __len__(self):
        return self._len

    def __contains__(self, key: T):
        return self._cnt[self._to_zaatsu[key]] > 0

    def __bool__(self):
        return self._len > 0

    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
from typing import Iterable, TypeVar, Generic, Union, Tuple

T = TypeVar("T")


class FenwickTreeMultiset(FenwickTreeSet, Generic[T]):

    def __init__(
        self, used: Union[int, Iterable[T]], a: Iterable[T] = [], compress: bool = True
    ) -> None:
        """
        Args:
          used (Union[int, Iterable[T]]): 使用する要素の集合
          a (Iterable[T], optional): 初期集合
          compress (bool, optional): 座圧するかどうか( ``True`` : する)
        """
        super().__init__(used, a, compress=compress, _multi=True)

    def add(self, key: T, num: int = 1) -> None:
        if num <= 0:
            return
        i = self._to_zaatsu[key]
        self._len += num
        self._cnt[i] += num
        self._fw.add(i, num)

    def remove(self, key: T, num: int = 1) -> None:
        if not self.discard(key, num):
            raise KeyError(key)

    def discard(self, key: T, num: int = 1) -> bool:
        i = self._to_zaatsu[key]
        num = min(num, self._cnt[i])
        if num <= 0:
            return False
        self._len -= num
        self._cnt[i] -= num
        self._fw.add(i, -num)
        return True

    def discard_all(self, key: T) -> bool:
        return self.discard(key, num=self.count(key))

    def count(self, key: T) -> int:
        return self._cnt[self._to_zaatsu[key]]

    def pop(self, k: int = -1) -> T:
        assert (
            -self._len <= k < self._len
        ), f"IndexError: {self.__class__.__name__}.pop({k}), len={self._len}"
        x = self[k]
        self.discard(x)
        return x

    def pop_min(self) -> T:
        assert (
            self._len > 0
        ), f"IndexError: pop_min() from empty {self.__class__.__name__}."
        return self.pop(0)

    def pop_max(self) -> T:
        assert (
            self._len > 0
        ), f"IndexError: pop_max() from empty {self.__class__.__name__}."
        return self.pop(-1)

    def items(self) -> Iterable[Tuple[T, int]]:
        _iter = 0
        while _iter < self._len:
            res = self._to_origin[self._bisect_right(_iter)]
            cnt = self.count(res)
            _iter += cnt
            yield res, cnt

    def show(self) -> None:
        print("{" + ", ".join(f"{i[0]}: {i[1]}" for i in self.items()) + "}")
