from titan_pylib.my_class.ordered_set_interface import OrderedSetInterface
from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.data_structures.bst_base.bst_set_node_base import BSTSetNodeBase
import math
from typing import Final, Iterator, TypeVar, Generic, Iterable, Optional
from __pypy__ import newlist_hint

T = TypeVar("T", bound=SupportsLessThan)


class ScapegoatTreeSet(OrderedSetInterface, Generic[T]):

    ALPHA: Final[float] = 0.75
    BETA: Final[float] = math.log2(1 / ALPHA)

    class Node:

        def __init__(self, key: T):
            self.key: T = key
            self.left: Optional["ScapegoatTreeSet.Node"] = None
            self.right: Optional["ScapegoatTreeSet.Node"] = None
            self.size: int = 1

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.size}\n"
            return (
                f"key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n"
            )

    def __init__(self, a: Iterable[T] = []):
        self.root: Optional["ScapegoatTreeSet.Node"] = None
        if not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: list[T]) -> None:
        Node = ScapegoatTreeSet.Node

        def rec(l: int, r: int) -> ScapegoatTreeSet.Node:
            mid = (l + r) >> 1
            node = Node(a[mid])
            if l != mid:
                node.left = rec(l, mid)
                node.size += node.left.size
            if mid + 1 != r:
                node.right = rec(mid + 1, r)
                node.size += node.right.size
            return node

        a = BSTSetNodeBase[T, ScapegoatTreeSet.Node].sort_unique(a)
        self.root = rec(0, len(a))

    def _rebuild(self, node: Node) -> Node:
        def rec(l: int, r: int) -> "ScapegoatTreeSet.Node":
            mid = (l + r) >> 1
            node = a[mid]
            node.size = 1
            if l != mid:
                node.left = rec(l, mid)
                node.size += node.left.size
            else:
                node.left = None
            if mid + 1 != r:
                node.right = rec(mid + 1, r)
                node.size += node.right.size
            else:
                node.right = None
            return node

        a = newlist_hint(node.size)
        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                a.append(node)
                node = node.right
        return rec(0, len(a))

    def add(self, key: T) -> bool:
        Node = ScapegoatTreeSet.Node
        node = self.root
        if node is None:
            self.root = Node(key)
            return True
        path = []
        while node:
            path.append(node)
            if key == node.key:
                return False
            node = node.left if key < node.key else node.right
        if key < path[-1].key:
            path[-1].left = Node(key)
        else:
            path[-1].right = Node(key)
        if len(path) * ScapegoatTreeSet.BETA > math.log(self.root.size):
            node_size = 1
            while path:
                pnode = path.pop()
                pnode_size = pnode.size + 1
                if ScapegoatTreeSet.ALPHA * pnode_size < node_size:
                    break
                node_size = pnode_size
            new_node = self._rebuild(pnode)
            if not path:
                self.root = new_node
                return True
            if new_node.key < path[-1].key:
                path[-1].left = new_node
            else:
                path[-1].right = new_node
        for p in path:
            p.size += 1
        return True

    def discard(self, key: T) -> bool:
        d = 1
        node = self.root
        path = []
        while node is not None:
            if key == node.key:
                break
            path.append(node)
            d = key < node.key
            node = node.left if d else node.right
        else:
            return False
        if node.left is not None and node.right is not None:
            path.append(node)
            lmax = node.left
            d = 1 if lmax.right is None else 0
            while lmax.right is not None:
                path.append(lmax)
                lmax = lmax.right
            node.key = lmax.key
            node = lmax
        cnode = node.right if node.left is None else node.left
        if path:
            if d == 1:
                path[-1].left = cnode
            else:
                path[-1].right = cnode
        else:
            self.root = cnode
        for p in path:
            p.size -= 1
        return True

    def remove(self, key: T) -> None:
        if self.discard(key):
            return
        raise KeyError

    def le(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].le(self.root, key)

    def lt(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].lt(self.root, key)

    def ge(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].ge(self.root, key)

    def gt(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].gt(self.root, key)

    def index(self, key: T) -> int:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].index(self.root, key)

    def index_right(self, key: T) -> int:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].index_right(self.root, key)

    def pop(self, k: int = -1) -> T:
        if k < 0:
            k += len(self)
        d = 1
        node = self.root
        path = []
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                break
            path.append(node)
            if t < k:
                node = node.right
                k -= t + 1
                d = 0
            elif t > k:
                d = 1
                node = node.left
        res = node.key
        if node.left is not None and node.right is not None:
            path.append(node)
            lmax = node.left
            d = 1 if lmax.right is None else 0
            while lmax.right is not None:
                path.append(lmax)
                lmax = lmax.right
            node.key = lmax.key
            node = lmax
        cnode = node.right if node.left is None else node.left
        if path:
            if d == 1:
                path[-1].left = cnode
            else:
                path[-1].right = cnode
        else:
            self.root = cnode
        for p in path:
            p.size -= 1
        return res

    def pop_min(self) -> T:
        return self.pop(0)

    def pop_max(self) -> T:
        return self.pop(-1)

    def clear(self) -> None:
        self.root = None

    def tolist(self) -> list[T]:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].tolist(self.root, len(self))

    def get_min(self) -> T:
        return self[0]

    def get_max(self) -> T:
        return self[-1]

    def __contains__(self, key: T):
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def __getitem__(self, k: int) -> T:
        return BSTSetNodeBase[T, ScapegoatTreeSet.Node].kth_elm(self.root, k, len(self))

    def __iter__(self) -> Iterator[T]:
        self.__iter = 0
        return self

    def __next__(self) -> T:
        if self.__iter == self.__len__():
            raise StopIteration
        res = self[self.__iter]
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(self.__len__()):
            yield self[-i - 1]

    def __len__(self):
        return 0 if self.root is None else self.root.size

    def __bool__(self):
        return self.root is not None

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
