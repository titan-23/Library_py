from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Iterable, TypeVar, Generic, Optional
from bisect import bisect_right, bisect_left

T = TypeVar("T", bound=SupportsLessThan)


class StaticOrderedSet(Generic[T]):

    def __init__(self, a: Iterable = [T]):
        self.s: set[T] = set(a)
        self.l: list[T] = sorted(self.s)
        self.n: int = len(self.l)

    def ge(self, x: T) -> Optional[T]:
        i = bisect_left(self.l, x)
        return self.l[i] if i < self.n else None

    def gt(self, x: T) -> Optional[T]:
        i = bisect_right(self.l, x)
        return self.l[i] if i < self.n else None

    def le(self, x: T) -> Optional[T]:
        i = bisect_right(self.l, x) - 1
        return self.l[i] if i >= 0 else None

    def lt(self, x: T) -> Optional[T]:
        i = bisect_left(self.l, x) - 1
        return self.l[i] if i >= 0 else None

    def index(self, x: T) -> int:
        return bisect_left(self.l, x)

    def index_right(self, x: T) -> int:
        return bisect_right(self.l, x)

    def neighbor(self, x: T) -> Optional[int]:
        le = self.le(x)
        ge = self.ge(x)
        if le is None:
            return ge
        if ge is None:
            return le
        return le if x - le < ge - x else ge

    def __getitem__(self, k: int) -> T:
        return self.l[k]

    def __contains__(self, x: T):
        return x in self.s

    def __len__(self):
        return self.n

    def __str__(self):
        return "{" + ", ".join(map(str, self.l)) + "}"

    def __repr__(self):
        return f"StaticOrderedSet({self})"
