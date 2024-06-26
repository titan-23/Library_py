from titan_pylib.my_class.ordered_set_interface import OrderedSetInterface
from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.data_structures.bst_base.bst_set_node_base import BSTSetNodeBase
from typing import Generic, Iterable, TypeVar, Optional

T = TypeVar("T", bound=SupportsLessThan)


class TreapSet(OrderedSetInterface, Generic[T]):
    """treap です。

    乱数を使用して平衡を保っています。Hackされることなんてあるんですかね。今のところ集合と多重集合しかないです。
    """

    class Random:

        _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

        @classmethod
        def random(cls) -> int:
            t = (cls._x ^ ((cls._x << 11) & 0xFFFFFFFF)) & 0xFFFFFFFF
            cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
            cls._w = (cls._w ^ (cls._w >> 19)) ^ (
                t ^ ((t >> 8)) & 0xFFFFFFFF
            ) & 0xFFFFFFFF
            return cls._w

    class Node:

        def __init__(self, key: T, priority: int = -1):
            self.key: T = key
            self.left: Optional["TreapSet.Node"] = None
            self.right: Optional["TreapSet.Node"] = None
            self.priority: int = (
                TreapSet.Random.random() if priority == -1 else priority
            )

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.priority}\n"
            return f"key:{self.key, self.priority},\n left:{self.left},\n right:{self.right}\n"

    def __init__(self, a: Iterable[T] = []):
        self.root: Optional["TreapSet.Node"] = None
        self._len: int = 0
        if not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: list[T]) -> None:
        Node = TreapSet.Node

        def rec(l: int, r: int) -> TreapSet.Node:
            mid = (l + r) >> 1
            node = Node(a[mid], rand[mid])
            if l != mid:
                node.left = rec(l, mid)
            if mid + 1 != r:
                node.right = rec(mid + 1, r)
            return node

        a = BSTSetNodeBase[T, TreapSet.Node].sort_unique(a)
        self._len = len(a)
        rand = sorted(TreapSet.Random.random() for _ in range(self._len))
        self.root = rec(0, self._len)

    def _rotate_L(self, node: Node) -> Node:
        u = node.left
        node.left = u.right
        u.right = node
        return u

    def _rotate_R(self, node: Node) -> Node:
        u = node.right
        node.right = u.left
        u.left = node
        return u

    def add(self, key: T) -> bool:
        if not self.root:
            self.root = TreapSet.Node(key)
            self._len = 1
            return True
        node = self.root
        path = []
        di = 0
        while node:
            if key == node.key:
                return False
            path.append(node)
            if key < node.key:
                di <<= 1
                di |= 1
                node = node.left
            else:
                di <<= 1
                node = node.right
        if di & 1:
            path[-1].left = TreapSet.Node(key)
        else:
            path[-1].right = TreapSet.Node(key)
        while path:
            new_node = None
            node = path.pop()
            if di & 1:
                if node.left.priority < node.priority:
                    new_node = self._rotate_L(node)
            else:
                if node.right.priority < node.priority:
                    new_node = self._rotate_R(node)
            di >>= 1
            if new_node:
                if path:
                    if di & 1:
                        path[-1].left = new_node
                    else:
                        path[-1].right = new_node
                else:
                    self.root = new_node
        self._len += 1
        return True

    def discard(self, key: T) -> bool:
        node = self.root
        pnode = None
        while node:
            if key == node.key:
                break
            pnode = node
            node = node.left if key < node.key else node.right
        else:
            return False
        self._len -= 1
        while node.left and node.right:
            if node.left.priority < node.right.priority:
                if not pnode:
                    pnode = self._rotate_L(node)
                    self.root = pnode
                    continue
                new_node = self._rotate_L(node)
                if node.key < pnode.key:
                    pnode.left = new_node
                else:
                    pnode.right = new_node
            else:
                if not pnode:
                    pnode = self._rotate_R(node)
                    self.root = pnode
                    continue
                new_node = self._rotate_R(node)
                if node.key < pnode.key:
                    pnode.left = new_node
                else:
                    pnode.right = new_node
            pnode = new_node
        if not pnode:
            if node.left is None:
                self.root = node.right
            else:
                self.root = node.left
            return True
        if node.left is None:
            if node.key < pnode.key:
                pnode.left = node.right
            else:
                pnode.right = node.right
        else:
            if node.key < pnode.key:
                pnode.left = node.left
            else:
                pnode.right = node.left
        return True

    def remove(self, key: T) -> None:
        if self.discard(key):
            return
        raise KeyError(key)

    def le(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, TreapSet.Node].le(self.root, key)

    def lt(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, TreapSet.Node].lt(self.root, key)

    def ge(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, TreapSet.Node].ge(self.root, key)

    def gt(self, key: T) -> Optional[T]:
        return BSTSetNodeBase[T, TreapSet.Node].gt(self.root, key)

    def get_min(self) -> Optional[T]:
        return BSTSetNodeBase[T, TreapSet.Node].get_min(self.root)

    def get_max(self) -> Optional[T]:
        return BSTSetNodeBase[T, TreapSet.Node].get_max(self.root)

    def pop_min(self) -> T:
        assert self.root, f"IndexError: pop_min() from Empty {self.__class__.__name__}."
        node = self.root
        pnode = None
        while node.left:
            pnode = node
            node = node.left
        self._len -= 1
        res = node.key
        if not pnode:
            self.root = self.root.right
        else:
            pnode.left = node.right
        return res

    def pop_max(self) -> T:
        assert self.root, f"IndexError: pop_max() from Empty {self.__class__.__name__}."
        node = self.root
        pnode = None
        while node.right:
            pnode = node
            node = node.right
        self._len -= 1
        res = node.key
        if not pnode:
            self.root = self.root.left
        else:
            pnode.right = node.left
        return res

    def clear(self) -> None:
        self.root = None

    def tolist(self) -> list[T]:
        return BSTSetNodeBase[T, TreapSet.Node].tolist(self.root)

    def __iter__(self):
        self._it = self.get_min()
        return self

    def __next__(self):
        if self._it is None:
            raise StopIteration
        res = self._it
        self._it = self.gt(self._it)
        return res

    def __contains__(self, key: T):
        return BSTSetNodeBase[T, TreapSet.Node].contains(self.root, key)

    def __len__(self):
        return self._len

    def __bool__(self):
        return self._len > 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tolist()})"
