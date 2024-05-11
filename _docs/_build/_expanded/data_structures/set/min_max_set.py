# from titan_pylib.data_structures.set.min_max_set import MinMaxSet
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
# from titan_pylib.data_structures.heap.double_ended_heap import DoubleEndedHeap
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Generic, Iterable, TypeVar, List

T = TypeVar("T", bound=SupportsLessThan)


class DoubleEndedHeap(Generic[T]):
    """
    - [両端優先度付きキューのInterval-Heap実装](https://natsugiri.hatenablog.com/entry/2016/10/10/035445)
    - [Double-ended priority queue(wikipedia)](https://en.wikipedia.org/wiki/Double-ended_priority_queue)
    """

    def __init__(self, a: Iterable[T] = []) -> None:
        """構築します。
        :math:`O(n)` です。

        Args:
          a (Iterable[T], optional): 構築元の配列です。
        """
        self._data = list(a)
        self._heapify()

    def _heapify(self) -> None:
        n = len(self._data)
        for i in range(n - 1, -1, -1):
            if i & 1 and self._data[i - 1] < self._data[i]:
                self._data[i - 1], self._data[i] = self._data[i], self._data[i - 1]
            k = self._down(i)
            self._up(k, i)

    def add(self, key: T) -> None:
        """``key`` を1つ追加します。
        :math:`O(\\log{n})` です。
        """
        self._data.append(key)
        self._up(len(self._data) - 1)

    def pop_min(self) -> T:
        """最小の要素を削除して返します。
        :math:`O(\\log{n})` です。
        """
        if len(self._data) < 3:
            res = self._data.pop()
        else:
            self._data[1], self._data[-1] = self._data[-1], self._data[1]
            res = self._data.pop()
            k = self._down(1)
            self._up(k)
        return res

    def pop_max(self) -> T:
        """最大の要素を削除して返します。
        :math:`O(\\log{n})` です。
        """
        if len(self._data) < 2:
            res = self._data.pop()
        else:
            self._data[0], self._data[-1] = self._data[-1], self._data[0]
            res = self._data.pop()
            self._up(self._down(0))
        return res

    def get_min(self) -> T:
        """最小の要素を返します。
        :math:`O(1)` です。
        """
        return self._data[0] if len(self._data) < 2 else self._data[1]

    def get_max(self) -> T:
        """最大の要素を返します。
        :math:`O(1)` です。
        """
        return self._data[0]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return len(self._data) > 0

    def _parent(self, k: int) -> int:
        return ((k >> 1) - 1) & ~1

    def _down(self, k: int) -> int:
        n = len(self._data)
        if k & 1:
            while k << 1 | 1 < n:
                c = 2 * k + 3
                if n <= c or self._data[c - 2] < self._data[c]:
                    c -= 2
                if c < n and self._data[c] < self._data[k]:
                    self._data[k], self._data[c] = self._data[c], self._data[k]
                    k = c
                else:
                    break
        else:
            while 2 * k + 2 < n:
                c = 2 * k + 4
                if n <= c or self._data[c] < self._data[c - 2]:
                    c -= 2
                if c < n and self._data[k] < self._data[c]:
                    self._data[k], self._data[c] = self._data[c], self._data[k]
                    k = c
                else:
                    break
        return k

    def _up(self, k: int, root: int = 1) -> int:
        if (k | 1) < len(self._data) and self._data[k & ~1] < self._data[k | 1]:
            self._data[k & ~1], self._data[k | 1] = (
                self._data[k | 1],
                self._data[k & ~1],
            )
            k ^= 1
        while root < k:
            p = self._parent(k)
            if not self._data[p] < self._data[k]:
                break
            self._data[p], self._data[k] = self._data[k], self._data[p]
            k = p
        while root < k:
            p = self._parent(k) | 1
            if not self._data[k] < self._data[p]:
                break
            self._data[p], self._data[k] = self._data[k], self._data[p]
            k = p
        return k

    def tolist(self) -> List[T]:
        return sorted(self._data)

    def __str__(self) -> str:
        return str(self.tolist())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"
from typing import Generic, Iterable, TypeVar, List

T = TypeVar("T", bound=SupportsLessThan)


class MinMaxSet(Generic[T]):

    def __init__(self, a: Iterable[T] = []):
        a = set(a)
        self.data = a
        self.heap = DoubleEndedHeap(a)

    def add(self, key: T) -> bool:
        if key not in self.data:
            self.heap.add(key)
            self.data.add(key)
            return True
        return False

    def discard(self, key: T) -> bool:
        if key in self.data:
            self.data.discard(key)
            return True
        return False

    def pop_min(self) -> T:
        while True:
            v = self.heap.pop_min()
            if v in self.data:
                self.data.discard(v)
                return v

    def pop_max(self) -> T:
        while True:
            v = self.heap.pop_max()
            if v in self.data:
                self.data.discard(v)
                return v

    def get_min(self) -> T:
        while True:
            v = self.heap.get_min()
            if v in self.data:
                return v
            else:
                self.heap.pop_min()

    def get_max(self) -> T:
        while True:
            v = self.heap.get_max()
            if v in self.data:
                return v
            else:
                self.heap.pop_max()

    def tolist(self) -> List[T]:
        return sorted(self.data)

    def __contains__(self, key: T):
        return key in self.data

    def __getitem__(self, k: int):  # 末尾と先頭のみ
        if k == -1 or k == len(self.data) - 1:
            return self.get_max()
        elif k == 0:
            return self.get_min()
        raise IndexError

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "{" + ", ".join(map(str, sorted(self.data))) + "}"

    def __repr__(self):
        return f"MinMaxSet({self})"
