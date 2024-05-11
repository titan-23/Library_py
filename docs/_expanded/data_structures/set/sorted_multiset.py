# from titan_pylib.data_structures.set.sorted_multiset import SortedMultiset
# https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, List, Tuple, TypeVar, Optional

T = TypeVar("T")


class SortedMultiset(Generic[T]):

    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def _build(self, a=None) -> None:
        if a is None:
            a = list(self)
        size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [
            a[size * i // bucket_size : size * (i + 1) // bucket_size]
            for i in range(bucket_size)
        ]

    def __init__(self, a: Iterable[T] = []) -> None:
        a = list(a)
        self.size = len(a)
        if not all(a[i] <= a[i + 1] for i in range(self.size - 1)):
            a.sort()
        self._build(a)

    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i:
                yield j

    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i):
                yield j

    def __eq__(self, other):
        return list(self) == list(other)

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "SortedMultiset" + str(self.a)

    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"

    def _position(self, x: T) -> Tuple[List[T], int]:
        for a in self.a:
            if x <= a[-1]:
                break
        return (a, bisect_left(a, x))

    def __contains__(self, x: T) -> bool:
        if self.size == 0:
            return False
        a, i = self._position(x)
        return i != len(a) and a[i] == x

    def count(self, x: T) -> int:
        return self.index_right(x) - self.index(x)

    def add(self, x: T) -> None:
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return
        a, i = self._position(x)
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()

    def _pop(self, a: List[T], i: int) -> T:
        ans = a.pop(i)
        self.size -= 1
        if not a:
            self._build()
        return ans

    def discard(self, x: T) -> bool:
        if self.size == 0:
            return False
        a, i = self._position(x)
        if i == len(a) or a[i] != x:
            return False
        self._pop(a, i)
        return True

    def lt(self, x: T) -> Optional[T]:
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x: T) -> Optional[T]:
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x: T) -> Optional[T]:
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x: T) -> Optional[T]:
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, i: int) -> T:
        if i < 0:
            for a in reversed(self.a):
                i += len(a)
                if i >= 0:
                    return a[i]
        else:
            for a in self.a:
                if i < len(a):
                    return a[i]
                i -= len(a)
        raise IndexError

    def pop(self, i: int = -1) -> T:
        if i < 0:
            for a in reversed(self.a):
                i += len(a)
                if i >= 0:
                    return self._pop(a, i)
        else:
            for a in self.a:
                if i < len(a):
                    return self._pop(a, i)
                i -= len(a)
        raise IndexError

    def index(self, x: T) -> int:
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans
