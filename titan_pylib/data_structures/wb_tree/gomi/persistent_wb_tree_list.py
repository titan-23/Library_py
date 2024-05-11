from math import sqrt
from typing import Generic, Iterable, Optional, TypeVar, Callable, List, Tuple, Final

T = TypeVar("T")


class PersistentWBTreeList(Generic[T]):

    ALPHA: Final[float] = 1 - sqrt(2) / 2
    BETA: Final[float] = (1 - 2 * ALPHA) / (1 - ALPHA)

    class Node:

        def __init__(self, key: T):
            self.key: T = key
            self.left: Optional[PersistentWBTreeList.Node] = None
            self.right: Optional[PersistentWBTreeList.Node] = None
            self.size: int = 1

        def copy(self) -> "PersistentWBTreeList.Node":
            node = PersistentWBTreeList.Node(self.key)
            node.left = self.left
            node.right = self.right
            node.size = self.size
            return node

        def balance(self) -> float:
            return ((self.left.size if self.left else 0) + 1) / (self.size + 1)

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key={self.key}, size={self.size}\n"
            return f"key={self.key}, size={self.size},\n left:{self.left},\n right:{self.right}\n"

        __repr__ = __str__

    def __init__(self, a: Iterable[T], _root: Optional[Node] = None) -> None:
        self.root: Optional[PersistentWBTreeList.Node] = _root
        a = list(a)
        if a:
            self._build(list(a))

    def _build(self, a: List[T]) -> None:
        Node = PersistentWBTreeList.Node

        def build(l: int, r: int) -> Node:
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
            else:
                node.size = 1 + node.right.size
        else:
            if node.right is None:
                node.size = 1 + node.left.size
            else:
                node.size = 1 + node.left.size + node.right.size

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
                r = self._balance_right(r)
                return r
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

    def merge(self, other: "PersistentWBTreeList") -> "PersistentWBTreeList":
        root = self._merge_node(self.root, other.root)
        return self._new(root)

    def _pop_right(self, node: Node) -> Tuple[Node, Node]:
        path = []
        node = node.copy()
        mx = node
        while node.right is not None:
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
    ) -> Tuple[Optional[Node], Optional[Node]]:
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

    def split(self, k: int) -> Tuple["PersistentWBTreeList", "PersistentWBTreeList"]:
        l, r = self._split_node(self.root, k)
        return self._new(l), self._new(r)

    def _new(
        self, root: Optional["PersistentWBTreeList.Node"]
    ) -> "PersistentWBTreeList":
        return PersistentWBTreeList([], root)

    def insert(self, k: int, key: T) -> "PersistentWBTreeList":
        s, t = self._split_node(self.root, k)
        root = self._merge_with_root(s, PersistentWBTreeList.Node(key), t)
        return self._new(root)

    def pop(self, k: int) -> Tuple["PersistentWBTreeList", T]:
        s, t = self._split_node(self.root, k + 1)
        assert s
        s, tmp = self._pop_right(s)
        root = self._merge_node(s, t)
        return self._new(root), tmp.key

    def set(self, k: int, v: T) -> "PersistentWBTreeList":
        if k < 0:
            k += len(self)
        node = self.root.copy()
        root = node
        pnode = None
        d = 0
        while True:
            assert node
            t = 0 if node.left is None else node.left.size
            if t == k:
                node = node.copy()
                node.key = v
                if d:
                    pnode.left = node
                else:
                    pnode.right = node
                return self._new(root)
            pnode = node
            if t < k:
                k -= t + 1
                node = node.right.copy()
                d = 0
            else:
                d = 1
                node = node.left.copy()
            if d:
                pnode.left = node
            else:
                pnode.right = node

    def copy(self) -> "PersistentWBTreeList":
        root = self.root.copy() if self.root else None
        return self._new(root)

    def tolist(self) -> List[T]:
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

    def __getitem__(self, k: int) -> T:
        if k < 0:
            k += len(self)
        node = self.root
        while True:
            assert node
            t = 0 if node.left is None else node.left.size
            if t == k:
                return node.key
            elif t < k:
                k -= t + 1
                node = node.right
            else:
                node = node.left

    def __len__(self):
        return 0 if self.root is None else self.root.size

    def __str__(self):
        return "[" + ", ".join(map(str, self.tolist())) + "]"

    def __repr__(self):
        return f"PersistentWBTreeList({self})"
