# from titan_pylib.data_structures.treap.treap_multiset import TreapMultiset
# from titan_pylib.my_class.ordered_multiset_interface import OrderedMultisetInterface
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic, List

T = TypeVar("T", bound=SupportsLessThan)


class OrderedMultisetInterface(ABC, Generic[T]):

    @abstractmethod
    def __init__(self, a: Iterable[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, key: T, cnt: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def discard(self, key: T, cnt: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def discard_all(self, key: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count(self, key: T) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove(self, key: T, cnt: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def le(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def lt(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def ge(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def gt(self, key: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_max(self) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_min(self) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def pop_max(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def pop_min(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def tolist(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator:
        raise NotImplementedError

    @abstractmethod
    def __next__(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, key: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
# from titan_pylib.data_structures.bst_base.bst_multiset_node_base import (
#     BSTMultisetNodeBase,
# )
from __pypy__ import newlist_hint
from typing import List, Tuple, TypeVar, Generic, Optional

T = TypeVar("T")
Node = TypeVar("Node")
# protcolで、key,val,left,right を規定


class BSTMultisetNodeBase(Generic[T, Node]):

    @staticmethod
    def count(node, key: T) -> int:
        while node is not None:
            if node.key == key:
                return node.val
            node = node.left if key < node.key else node.right
        return 0

    @staticmethod
    def get_min(node: Node) -> Optional[T]:
        if not node:
            return None
        while node.left:
            node = node.left
        return node.key

    @staticmethod
    def get_max(node: Node) -> Optional[T]:
        if not node:
            return None
        while node.right:
            node = node.right
        return node.key

    @staticmethod
    def contains(node: Node, key: T) -> bool:
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    @staticmethod
    def tolist(node: Node, _len: int = 0) -> List[T]:
        stack = []
        a = newlist_hint(_len)
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                for _ in range(node.val):
                    a.append(node.key)
                node = node.right
        return a

    @staticmethod
    def tolist_items(node: Node, _len: int = 0) -> List[Tuple[T, int]]:
        stack = newlist_hint(_len)
        a = newlist_hint(_len)
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                a.append((node.key, node.val))
                node = node.right
        return a

    @staticmethod
    def _rle(a: List[T]) -> Tuple[List[T], List[int]]:
        keys, vals = newlist_hint(len(a)), newlist_hint(len(a))
        keys.append(a[0])
        vals.append(1)
        for i, elm in enumerate(a):
            if i == 0:
                continue
            if elm == keys[-1]:
                vals[-1] += 1
                continue
            keys.append(elm)
            vals.append(1)
        return keys, vals

    @staticmethod
    def le(node: Node, key: T) -> Optional[T]:
        res = None
        while node is not None:
            if key == node.key:
                res = key
                break
            if key < node.key:
                node = node.left
            else:
                res = node.key
                node = node.right
        return res

    @staticmethod
    def lt(node: Node, key: T) -> Optional[T]:
        res = None
        while node is not None:
            if key <= node.key:
                node = node.left
            else:
                res = node.key
                node = node.right
        return res

    @staticmethod
    def ge(node: Node, key: T) -> Optional[T]:
        res = None
        while node is not None:
            if key == node.key:
                res = key
                break
            if key < node.key:
                res = node.key
                node = node.left
            else:
                node = node.right
        return res

    @staticmethod
    def gt(node: Node, key: T) -> Optional[T]:
        res = None
        while node is not None:
            if key < node.key:
                res = node.key
                node = node.left
            else:
                node = node.right
        return res

    @staticmethod
    def index(node: Node, key: T) -> int:
        k = 0
        while node:
            if key == node.key:
                if node.left:
                    k += node.left.valsize
                break
            if key < node.key:
                node = node.left
            else:
                k += node.val if node.left is None else node.left.valsize + node.val
                node = node.right
        return k

    @staticmethod
    def index_right(node: Node, key: T) -> int:
        k = 0
        while node:
            if key == node.key:
                k += node.val if node.left is None else node.left.valsize + node.val
                break
            if key < node.key:
                node = node.left
            else:
                k += node.val if node.left is None else node.left.valsize + node.val
                node = node.right
        return k
from typing import Generic, Iterable, TypeVar, Tuple, List, Optional, Sequence

T = TypeVar("T", bound=SupportsLessThan)


class TreapMultiset(OrderedMultisetInterface, Generic[T]):

    class Random:

        _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

        @classmethod
        def random(cls) -> int:
            t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
            cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
            cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
            return cls._w

    class Node:

        def __init__(self, key: T, val: int = 1, priority: int = -1):
            self.key: T = key
            self.val: int = val
            self.left: Optional["TreapMultiset.Node"] = None
            self.right: Optional["TreapMultiset.Node"] = None
            self.priority: int = (
                TreapMultiset.Random.random() if priority == -1 else priority
            )

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.priority}\n"
            return f"key:{self.key, self.priority},\n left:{self.left},\n right:{self.right}\n"

    def __init__(self, a: Iterable[T] = []):
        self.root: Optional["TreapMultiset.Node"] = None
        self._len: int = 0
        self._len_elm: int = 0
        if not isinstance(a, Sequence):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: Iterable[T]) -> None:
        Node = TreapMultiset.Node

        def sort(l: int, r: int) -> Node:
            mid = (l + r) >> 1
            node = Node(key[mid], val[mid], rand[mid])
            if l != mid:
                node.left = sort(l, mid)
            if mid + 1 != r:
                node.right = sort(mid + 1, r)
            return node

        a = sorted(a)
        key, val = BSTMultisetNodeBase[T, TreapMultiset.Node]._rle(a)
        self._len = len(a)
        self._len_elm = len(key)
        rand = sorted(TreapMultiset.Random.random() for _ in range(self._len_elm))
        self.root = sort(0, len(key))

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

    def add(self, key: T, val: int = 1) -> None:
        self._len += val
        if self.root is None:
            self.root = TreapMultiset.Node(key, val)
            self._len_elm += 1
            return
        node = self.root
        path = []
        di = 0
        while node is not None:
            if key == node.key:
                node.val += val
                return
            path.append(node)
            if key < node.key:
                di <<= 1
                di |= 1
                node = node.left
            else:
                di <<= 1
                node = node.right
        self._len_elm += 1
        if di & 1:
            path[-1].left = TreapMultiset.Node(key, val)
        else:
            path[-1].right = TreapMultiset.Node(key, val)
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
            if new_node is not None:
                if path:
                    if di & 1:
                        path[-1].left = new_node
                    else:
                        path[-1].right = new_node
                else:
                    self.root = new_node
        self._len += 1

    def discard(self, key: T, val: int = 1) -> bool:
        node = self.root
        pnode = None
        while node is not None:
            if key == node.key:
                break
            pnode = node
            node = node.left if key < node.key else node.right
        else:
            return False
        self._len -= min(val, node.val)
        if node.val > val:
            node.val -= val
            return True
        self._len_elm -= 1
        while node.left is not None and node.right is not None:
            if node.left.priority < node.right.priority:
                if pnode is None:
                    pnode = self._rotate_L(node)
                    self.root = pnode
                    continue
                new_node = self._rotate_L(node)
                if node.key < pnode.key:
                    pnode.left = new_node
                else:
                    pnode.right = new_node
            else:
                if pnode is None:
                    pnode = self._rotate_R(node)
                    self.root = pnode
                    continue
                new_node = self._rotate_R(node)
                if node.key < pnode.key:
                    pnode.left = new_node
                else:
                    pnode.right = new_node
            pnode = new_node
        if pnode is None:
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

    def discard_all(self, key: T) -> bool:
        return self.discard(key, self.count(key))

    def remove(self, key: T, val: int = 1) -> None:
        if self.discard(key, val):
            return
        raise KeyError(key)

    def count(self, key: T) -> int:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].count(self.root)

    def le(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].le(self.root, key)

    def lt(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].lt(self.root, key)

    def ge(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].ge(self.root, key)

    def gt(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].gt(self.root, key)

    def len_elm(self) -> int:
        return self._len_elm

    def show(self) -> None:
        print(
            "{" + ", ".join(map(lambda x: f"{x[0]}: {x[1]}", self.tolist_items())) + "}"
        )

    def tolist(self) -> List[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].tolist(self.root, len(self))

    def tolist_items(self) -> List[Tuple[T, int]]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].tolist_items(
            self.root, self._len_elm
        )

    def get_min(self) -> Optional[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node][
            T, TreapMultiset.Node
        ].get_min(self.root)

    def get_max(self) -> Optional[T]:
        return BSTMultisetNodeBase[T, TreapMultiset.Node].get_max(self.root)

    def pop_min(self) -> T:
        assert self
        self._len -= 1
        node = self.root
        pnode = None
        while node.left is not None:
            pnode = node
            node = node.left
        if node.val > 1:
            node.val -= 1
            return node.key
        self._len_elm -= 1
        res = node.key
        if pnode is None:
            self.root = self.root.right
        else:
            pnode.left = node.right
        return res

    def pop_max(self) -> T:
        assert self, "IndexError"
        self._len -= 1
        node = self.root
        pnode = None
        while node.right is not None:
            pnode = node
            node = node.right
        if node.val > 1:
            node.val -= 1
            return node.key
        self._len_elm -= 1
        res = node.key
        if pnode is None:
            self.root = self.root.left
        else:
            pnode.right = node.left
        return res

    def clear(self) -> None:
        self.root = None

    def __iter__(self):
        self._it = self.get_min()
        self._cnt = 1
        return self

    def __next__(self):
        if self._it is None:
            raise StopIteration
        res = self._it
        if self._cnt == self.count(self._it):
            self._it = self.gt(self._it)
            self._cnt = 1
        else:
            self._cnt += 1
        return res

    def __contains__(self, key: T):
        return BSTMultisetNodeBase[T, TreapMultiset.Node].contains(self.root, key)

    def __bool__(self):
        return self.root is not None

    def __len__(self):
        return self._len

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"TreapMultiset({self.tolist()})"
