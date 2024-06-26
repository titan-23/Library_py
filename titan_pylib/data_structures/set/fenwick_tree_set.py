from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
from typing import Iterable, TypeVar, Generic, Union, Optional

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
        self._to_zaatsu: dict[T, int] = (
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
