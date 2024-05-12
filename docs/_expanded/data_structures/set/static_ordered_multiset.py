# from titan_pylib.data_structures.set.static_ordered_multiset import StaticOrderedMultiset
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
from typing import Iterable, Optional, TypeVar, Generic
from bisect import bisect_right, bisect_left
from collections import Counter

T = TypeVar("T", bound=SupportsLessThan)


class StaticOrderedMultiset(Generic[T]):

    def __init__(self, a: Iterable = [T]):
        self.l: list[T] = sorted(a)
        self.s: Counter[T] = Counter(self.l)
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

    def count(self, x: T) -> int:
        return self.s[x]

    def len_elm(self) -> int:
        return len(self.s)

    def __getitem__(self, k: int) -> T:
        return self.l[k]

    def __contains__(self, x: T):
        return x in self.s

    def __len__(self):
        return self.n

    def __str__(self):
        return "{" + ", ".join(map(str, self.l)) + "}"

    def __repr__(self):
        return "StaticOrderedMultiset([" + ", ".join(map(str, self.l)) + "])"
