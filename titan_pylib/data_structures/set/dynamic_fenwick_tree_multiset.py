from titan_pylib.data_structures.set.dynamic_fenwick_tree_set import (
    DynamicFenwickTreeSet,
)
from typing import Iterable


class DynamicFenwickTreeMultiset(DynamicFenwickTreeSet):

    def __init__(self, n: int, a: Iterable[int] = []) -> None:
        super().__init__(n, a)

    def add(self, key: int, val: int = 1) -> None:
        self._len += val
        if key in self._cnt:
            self._cnt[key] += val
        else:
            self._cnt[key] = val
        self._fw.add(key, val)

    def discard(self, key: int, val: int = 1) -> bool:
        if key not in self._cnt:
            return False
        cnt = self._cnt[key]
        if val >= cnt:
            self._len -= cnt
            del self._cnt[key]
            self._fw.add(key, -cnt)
        else:
            self._len -= val
            self._cnt[key] -= val
            self._fw.add(key, -val)
        return True

    def discard_all(self, key: int) -> bool:
        return self.discard(key, val=self.count(key))

    def count(self, key: int) -> int:
        return self._cnt[key]

    def items(self) -> Iterable[tuple[int, int]]:
        _iter = 0
        while _iter < self._len:
            res = self.__getitem__(_iter)
            cnt = self.count(res)
            _iter += cnt
            yield res, cnt

    def show(self) -> None:
        print("{" + ", ".join(f"{i[0]}: {i[1]}" for i in self.items()) + "}")

    def __repr__(self):
        return f"DynamicFenwickTreeMultiset({self})"
