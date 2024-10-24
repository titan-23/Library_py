# from titan_pylib.data_structures.heap.Randomized_meldable_heap import RandomizedMeldableHeap
from typing import TypeVar, Generic, Iterable, Optional

T = TypeVar("T")


class RandomizedMeldableHeap(Generic[T]):
    """併合可能ヒープです。

    [Randomized Meldable Heap](https://trap.jp/post/1050/), traP
    """

    _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

    class Node:

        def __init__(self, key: T) -> None:
            self.key = key
            self.left = None
            self.right = None

    def __init__(self, a: Iterable[T] = []):
        self.root = None
        self.size = 0
        self._build(a)

    def _build(self, a: Iterable[T]) -> None:
        a = sorted(a)
        if not a:
            return
        n = len(a)
        pool = [self.Node(e) for e in a]
        for i in range(len(a)):
            if i * 2 + 1 < n:
                pool[i].left = pool[i * 2 + 1]
            if i * 2 + 2 < n:
                pool[i].right = pool[i * 2 + 2]
        self.root = pool[0]

    @classmethod
    def _randbit(cls) -> int:
        t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
        cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
        cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
        return cls._w & 1

    @classmethod
    def _meld(cls, x: Optional[Node], y: Optional[Node]) -> Optional[Node]:
        if x is None:
            return y
        if y is None:
            return x
        if x.key > y.key:
            x, y = y, x
        if cls._randbit():
            x.left = cls._meld(x.left, y)
        else:
            x.right = cls._meld(x.right, y)
        return x

    @classmethod
    def meld(
        cls, x: "RandomizedMeldableHeap", y: "RandomizedMeldableHeap"
    ) -> "RandomizedMeldableHeap":
        new_heap = RandomizedMeldableHeap()
        new_heap.size = x.size + y.size
        new_heap.root = cls._meld(x.root, y.root)
        return new_heap

    def push(self, key: T) -> None:
        node = RandomizedMeldableHeap.Node(key)
        self.root = self._meld(self.root, node)
        self.size += 1

    def pop_min(self) -> T:
        res = self.root.key
        self.root = self._meld(self.root.left, self.root.right)
        return res

    def get_min(self) -> T:
        return self.root.key

    def tolist(self) -> list[T]:
        node = self.root
        stack = []
        a = []
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                a.append(node.key)
                node = node.right
        a.sort()
        return a

    def __bool__(self):
        return self.root is not None

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.tolist())

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
