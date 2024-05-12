from math import sqrt
from typing import (
    Generic,
    Iterable,
    Optional,
    TypeVar,
    Callable,
    Final,
)

T = TypeVar("T")


class PersistentWBTree(Generic[T]):

    ALPHA: Final[float] = 1 - sqrt(2) / 2
    BETA: Final[float] = (1 - 2 * ALPHA) / (1 - ALPHA)

    class Node:

        def __init__(self, key: T) -> None:
            self.key: T = key
            self.data: T = key
            self.left: Optional[PersistentWBTree.Node] = None
            self.right: Optional[PersistentWBTree.Node] = None
            self.size: int = 1

        def copy(self) -> "PersistentWBTree.Node":
            node = PersistentWBTree.Node(self.key)
            node.data = self.data
            node.left = self.left
            node.right = self.right
            node.size = self.size
            return node

        def balance(self) -> float:
            return ((self.left.size if self.left else 0) + 1) / (self.size + 1)

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key={self.key}, size={self.size}, data={self.data}\n"
            return f"key={self.key}, size={self.size}, data={self.data},\n left:{self.left},\n right:{self.right}\n"

        __repr__ = __str__

    def __init__(
        self,
        a: Iterable[T],
        op: Callable[[T, T], T],
        e: T,
        _root: Optional[Node] = None,
    ) -> None:
        self.root: Optional[PersistentWBTree.Node] = _root
        self.op: Callable[[T, T], T] = op
        self.e: T = e
        a = list(a)
        if a:
            self._build(a)

    def _build(self, a: list[T]) -> None:
        Node = PersistentWBTree.Node

        def build(l: int, r: int) -> PersistentWBTree.Node:
            mid = (l + r) >> 1
            node = Node(a[mid])
            if l != mid:
                node.left = build(l, mid)
            if mid + 1 != r:
                node.right = build(mid + 1, r)
            self._update(node)
            return node

        self.root = build(0, len(a))

    def _update(self, node: Node) -> None:
        if node.left is None:
            if node.right is None:
                node.size = 1
                node.data = node.key
            else:
                node.size = 1 + node.right.size
                node.data = self.op(node.key, node.right.data)
        else:
            if node.right is None:
                node.size = 1 + node.left.size
                node.data = self.op(node.left.data, node.key)
            else:
                node.size = 1 + node.left.size + node.right.size
                node.data = self.op(self.op(node.left.data, node.key), node.right.data)

    def _rotate_right(self, node: Node) -> Node:
        assert node.left
        u = node.left.copy()
        node.left = u.right
        u.right = node
        self._update(node)
        self._update(u)
        return u

    def _rotate_left(self, node: Node) -> Node:
        assert node.right
        u = node.right.copy()
        node.right = u.left
        u.left = node
        self._update(node)
        self._update(u)
        return u

    def _balance_left(self, node: Node) -> Node:
        assert node.right
        node.right = node.right.copy()
        u = node.right
        if u.balance() >= self.BETA:
            assert u.left
            node.right = self._rotate_right(u)
        u = self._rotate_left(node)
        return u

    def _balance_right(self, node: Node) -> Node:
        assert node.left
        node.left = node.left.copy()
        u = node.left
        if u.balance() <= 1 - self.BETA:
            assert u.right
            node.left = self._rotate_left(u)
        u = self._rotate_right(node)
        return u

    def _merge_with_root(
        self, l: Optional[Node], root: Node, r: Optional[Node]
    ) -> Node:
        ls = l.size if l else 0
        rs = r.size if r else 0
        diff = (ls + 1) / (ls + rs + 1 + 1)
        if diff > 1 - self.ALPHA:
            assert l
            l = l.copy()
            l.right = self._merge_with_root(l.right, root, r)
            self._update(l)
            if not (self.ALPHA <= l.balance() <= 1 - self.ALPHA):
                return self._balance_left(l)
            return l
        if diff < self.ALPHA:
            assert r
            r = r.copy()
            r.left = self._merge_with_root(l, root, r.left)
            self._update(r)
            if not (self.ALPHA <= r.balance() <= 1 - self.ALPHA):
                return self._balance_right(r)
            return r
        root = root.copy()
        root.left = l
        root.right = r
        self._update(root)
        return root

    def _merge_node(self, l: Optional[Node], r: Optional[Node]) -> Optional[Node]:
        if l is None and r is None:
            return None
        if l is None:
            assert r
            return r.copy()
        if r is None:
            return l.copy()
        l = l.copy()
        r = r.copy()
        l, root = self._pop_right(l)
        return self._merge_with_root(l, root, r)

    def merge(self, other: "PersistentWBTree") -> "PersistentWBTree":
        root = self._merge_node(self.root, other.root)
        return self._new(root)

    def _pop_right(self, node: Node) -> tuple[Node, Node]:
        path = []
        node = node.copy()
        mx = node
        while node.right:
            path.append(node)
            node = node.right.copy()
            mx = node
        path.append(node.left.copy() if node.left else None)
        for _ in range(len(path) - 1):
            node = path.pop()
            if node is None:
                path[-1].right = None
                self._update(path[-1])
                continue
            b = node.balance()
            if self.ALPHA <= b <= 1 - self.ALPHA:
                path[-1].right = node
            elif b > 1 - self.ALPHA:
                path[-1].right = self._balance_right(node)
            else:
                path[-1].right = self._balance_left(node)
            self._update(path[-1])
        if path[0] is not None:
            b = path[0].balance()
            if b > 1 - self.ALPHA:
                path[0] = self._balance_right(path[0])
            elif b < self.ALPHA:
                path[0] = self._balance_left(path[0])
        mx.left = None
        self._update(mx)
        return path[0], mx

    def _split_node(
        self, node: Optional[Node], k: int
    ) -> tuple[Optional[Node], Optional[Node]]:
        if node is None:
            return None, None
        tmp = k if node.left is None else k - node.left.size
        l, r = None, None
        if tmp == 0:
            return node.left, self._merge_with_root(None, node, node.right)
        elif tmp < 0:
            l, r = self._split_node(node.left, k)
            return l, self._merge_with_root(r, node, node.right)
        else:
            l, r = self._split_node(node.right, tmp - 1)
            return self._merge_with_root(node.left, node, l), r

    def split(self, k: int) -> tuple["PersistentWBTree[T]", "PersistentWBTree[T]"]:
        l, r = self._split_node(self.root, k)
        return self._new(l), self._new(r)

    def _new(self, root: Optional["Node"]) -> "PersistentWBTree[T]":
        return PersistentWBTree([], self.op, self.e, root)

    def prod(self, l: int, r) -> T:
        if l >= r or (not self.root):
            return self.e

        def dfs(node: PersistentWBTree.Node, left: int, right: int) -> T:
            if right <= l or r <= left:
                return self.e
            if l <= left and right < r:
                return node.data
            lsize = node.left.size if node.left else 0
            res = self.e
            if node.left:
                res = dfs(node.left, left, left + lsize)
            if l <= left + lsize < r:
                res = self.op(res, node.key)
            if node.right:
                res = self.op(res, dfs(node.right, left + lsize + 1, right))
            return res

        return dfs(self.root, 0, len(self))

    def insert(self, k: int, key: T) -> "PersistentWBTree[T]":
        s, t = self._split_node(self.root, k)
        root = self._merge_with_root(s, PersistentWBTree.Node(key, self.id), t)
        return self._new(root)

    def pop(self, k: int) -> tuple["PersistentWBTree[T]", T]:
        s, t = self._split_node(self.root, k + 1)
        assert s
        s, tmp = self._pop_right(s)
        root = self._merge_node(s, t)
        return self._new(root), tmp.key

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
        return a

    def copy(self) -> "PersistentWBTree":
        root = self.root.copy() if self.root else None
        return self._new(root)

    def set(self, k: int, v: T) -> "PersistentWBTree":
        if k < 0:
            k += len(self)
        node = self.root.copy()
        root = node
        pnode = None
        d = 0
        path = [node]
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                node = node.copy()
                node.key = v
                path.append(node)
                if pnode:
                    if d:
                        pnode.left = node
                    else:
                        pnode.right = node
                else:
                    root = node
                while path:
                    self._update(path.pop())
                return self._new(root)
            pnode = node
            if t < k:
                k -= t + 1
                d = 0
                node = node.right.copy()
                pnode.right = node
            else:
                d = 1
                node = node.left.copy()
                pnode.left = node
            path.append(node)

    def __getitem__(self, k: int) -> T:
        if k < 0:
            k += len(self)
        node = self.root
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                return node.key
            if t < k:
                k -= t + 1
                node = node.right
            else:
                node = node.left

    def __len__(self):
        return 0 if self.root is None else self.root.size

    def __str__(self):
        return str(self.tolist())

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
