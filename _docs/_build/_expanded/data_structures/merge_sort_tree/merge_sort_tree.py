# from titan_pylib.data_structures.merge_sort_tree.merge_sort_tree import MergeSortTree
from typing import Generic, Iterable, TypeVar, Callable, Iterator

T = TypeVar("T")
D = TypeVar("D")


class MergeSortTree(Generic[T, D]):

    def __init__(self, a: Iterable[T], func: Callable[[list[T]], D]) -> None:
        a = list(a)
        self._n = len(a)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log
        _data: list[list[T]] = [[]] * (self._size << 1)
        _data[self._size : self._size + self._n] = [[e] for e in a]
        for i in range(self._size - 1, 0, -1):
            _data[i] = self._merge(_data[i << 1], _data[i << 1 | 1])
        self._data = _data
        self._func_data: list[D] = [func(v) for v in self._data]

    def _merge(self, left: list[T], right: list[T]) -> list[T]:
        i, j, l, r = 0, 0, len(left), len(right)
        res = []
        while i < l and j < r:
            if left[i] < right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1
        for i in range(i, l):
            res.append(left[i])
        for j in range(j, r):
            res.append(right[j])
        return res

    def prod_iter(self, l: int, r: int) -> Iterator[tuple[list[T], D]]:
        """区間 ``[l, r)`` における、セグ木の各区間のソート済み配列とそれに ``func`` を適用したものを投げます。
        :math:`O(\\log{n})` です。

        Yields:
          Iterator[tuple[list[T], D]]: (ソート済み配列、func(ソート済み配列)) です。
        """
        assert (
            0 <= l <= r <= self._n
        ), f"IndexError: {self.__class__.__name__}.prod_iter({l}, {r})"
        _data, _func_data = self._data, self._func_data
        l += self._size
        r += self._size
        while l < r:
            if l & 1:
                yield _data[l], _func_data[l]
                l += 1
            if r & 1:
                r -= 1
                yield _data[r], _func_data[r]
            l >>= 1
            r >>= 1
