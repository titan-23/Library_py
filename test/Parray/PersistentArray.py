from typing import Iterable, TypeVar, Generic, Optional

T = TypeVar("T")


class PersistentArray(Generic[T]):

    class Node:

        # __slots__ = ('key', 'left', 'right')

        def __init__(self, key: T):
            self.key: T = key
            self.left: Optional[PersistentArray.Node] = None
            self.right: Optional[PersistentArray.Node] = None

        def copy(self) -> "PersistentArray.Node":
            node = PersistentArray.Node(self.key)
            node.left = self.left
            node.right = self.right
            return node

    def __init__(
        self, a: Iterable[T] = [], _root: Optional["PersistentArray.Node"] = None
    ):
        self.root = self._build(a) if _root is None else _root

    def _build(self, a: Iterable[T]) -> Optional["PersistentArray.Node"]:
        pool = [PersistentArray.Node(e) for e in a]
        if not pool:
            return None
        n = len(pool)
        for i in range(1, n + 1):
            if 2 * i - 1 < n:
                pool[i - 1].left = pool[2 * i - 1]
            if 2 * i < n:
                pool[i - 1].right = pool[2 * i]
        return pool[0]

    def _new(self, root: Optional["PersistentArray.Node"]) -> "PersistentArray[T]":
        return PersistentArray(_root=root)

    def set(self, k: int, v: T) -> "PersistentArray[T]":
        node = self.root
        if node is None:
            return self._new(None)
        new_node = node.copy()
        res = self._new(new_node)
        k += 1
        b = k.bit_length()
        for i in range(b - 2, -1, -1):
            if k >> i & 1:
                node = node.right
                new_node.right = node.copy()
                new_node = new_node.right
            else:
                node = node.left
                new_node.left = node.copy()
                new_node = new_node.left
        new_node.key = v
        return res

    def get(self, k: int) -> T:
        node = self.root
        k += 1
        b = k.bit_length()
        for i in range(b - 2, -1, -1):
            if k >> i & 1:
                node = node.right
            else:
                node = node.left
        return node.key

    __getitem__ = get

    def copy(self) -> "PersistentArray[T]":
        return self._new(None if self.root is None else self.root.copy())

    def tolist(self) -> list[T]:
        node = self.root
        q = [node]
        a: list[T] = []
        if not node:
            return a
        for node in q:
            a.append(node.key)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return a

    def __str__(self):
        return str(self)

    def __repr__(self):
        return f"PersistentArray({self})"
