from typing import Generic, Union, TypeVar, Callable, Iterable, Optional
from __pypy__ import newlist_hint

T = TypeVar("T")
F = TypeVar("F")


class LazySplayTree(Generic[T, F]):

    class Node:

        def __init__(self, key: T, lazy: F):
            self.key: T = key
            self.data: T = key
            self.rdata: T = key
            self.lazy: F = lazy
            self.left: Optional["LazySplayTree.Node"] = None
            self.right: Optional["LazySplayTree.Node"] = None
            self.par: Optional["LazySplayTree.Node"] = None
            self.size: int = 1
            self.rev: int = 0

    def __init__(
        self,
        n_or_a: Union[int, Iterable[T]],
        op: Callable[[T, T], T],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id: F,
        _root: Node = None,
    ):
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.e = e
        self.id = id
        self.root = _root
        if _root:
            return
        a = n_or_a
        if isinstance(a, int):
            if a > 0:
                a = [e for _ in range(a)]
        elif not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: list[T]) -> None:
        Node = self.Node
        id = self.id

        def build(l: int, r: int) -> Node:
            mid = (l + r) >> 1
            node = Node(a[mid], id)
            if l != mid:
                node.left = build(l, mid)
                node.left.par = node
            if mid + 1 != r:
                node.right = build(mid + 1, r)
                node.right.par = node
            self._update(node)
            return node

        self.root = build(0, len(a))

    def _rotate(self, node: Node) -> None:
        pnode = node.par
        gnode = pnode.par
        if gnode:
            if gnode.left is pnode:
                gnode.left = node
            else:
                gnode.right = node
        node.par = gnode
        if pnode.left is node:
            pnode.left = node.right
            if node.right:
                node.right.par = pnode
            node.right = pnode
        else:
            pnode.right = node.left
            if node.left:
                node.left.par = pnode
            node.left = pnode
        pnode.par = node
        self._update(pnode)
        self._update(node)

    def _propagate_rev(self, node: Optional[Node]) -> None:
        if not node:
            return
        node.rev ^= 1

    def _propagate_lazy(self, node: Optional[Node], f: F) -> None:
        if not node:
            return
        node.key = self.mapping(f, node.key)
        node.data = self.mapping(f, node.data)
        node.rdata = self.mapping(f, node.rdata)
        node.lazy = f if node.lazy == self.id else self.composition(f, node.lazy)

    def _propagate(self, node: Optional[Node]) -> None:
        if not node:
            return
        if node.rev:
            node.data, node.rdata = node.rdata, node.data
            node.left, node.right = node.right, node.left
            self._propagate_rev(node.left)
            self._propagate_rev(node.right)
            node.rev = 0
        if node.lazy != self.id:
            self._propagate_lazy(node.left, node.lazy)
            self._propagate_lazy(node.right, node.lazy)
            node.lazy = self.id

    def _update(self, node: Node) -> None:
        node.data = node.key
        node.rdata = node.key
        node.size = 1
        if node.left:
            node.data = self.op(node.left.data, node.data)
            node.rdata = self.op(node.rdata, node.left.rdata)
            node.size += node.left.size
        if node.right:
            node.data = self.op(node.data, node.right.data)
            node.rdata = self.op(node.right.rdata, node.rdata)
            node.size += node.right.size

    def _splay(self, node: Node) -> None:
        while node.par and node.par.par:
            pnode = node.par
            self._rotate(
                pnode if (pnode.par.left is pnode) == (pnode.left is node) else node
            )
            self._rotate(node)
        if node.par:
            self._rotate(node)

    def _get_kth_elm_splay(self, node: Optional[Node], k: int) -> None:
        if k < 0:
            k += len(self)
        while True:
            self._propagate(node)
            t = node.left.size if node.left else 0
            if t == k:
                break
            if t > k:
                node = node.left
            else:
                node = node.right
                k -= t + 1
        self._splay(node)
        return node

    def _get_left_splay(self, node: Optional[Node]) -> Optional[Node]:
        self._propagate(node)
        if not node or not node.left:
            return node
        while node.left:
            node = node.left
            self._propagate(node)
        self._splay(node)
        return node

    def _get_right_splay(self, node: Optional[Node]) -> Optional[Node]:
        self._propagate(node)
        if not node or not node.right:
            return node
        while node.right:
            node = node.right
            self._propagate(node)
        self._splay(node)
        return node

    def merge(self, other: "LazySplayTree") -> None:
        if not self.root:
            self.root = other.root
            return
        if not other.root:
            return
        self.root = self._get_right_splay(self.root)
        self.root.right = other.root
        other.root.par = self.root
        self._update(self.root)

    def split(self, k: int) -> tuple["LazySplayTree", "LazySplayTree"]:
        left, right = self._internal_split(self.root, k)
        left_splay = LazySplayTree(
            0, self.op, self.mapping, self.composition, self.e, self.id, left
        )
        right_splay = LazySplayTree(
            0, self.op, self.mapping, self.composition, self.e, self.id, right
        )
        return left_splay, right_splay

    def _internal_split(self, k: int) -> tuple[Node, Node]:
        # self.root will be broken
        if k >= len(self):
            return self.root, None
        right = self._get_kth_elm_splay(self.root, k)
        left = right.left
        if left:
            left.par = None
        right.left = None
        self._update(right)
        return left, right

    def _internal_merge(
        self, left: Optional[Node], right: Optional[Node]
    ) -> Optional[Node]:
        # need (not right) or (not right.left)
        if not right:
            return left
        assert right.left is None
        right.left = left
        if left:
            left.par = right
        self._update(right)
        return right

    def reverse(self, l: int, r: int) -> None:
        assert (
            0 <= l <= r <= len(self)
        ), f"IndexError: {self.__class__.__name__}.reverse({l}, {r}), len={len(self)}"
        left, right = self._internal_split(r)
        if l == 0:
            self._propagate_rev(left)
        else:
            left = self._get_kth_elm_splay(left, l - 1)
            self._propagate_rev(left.right)
        self.root = self._internal_merge(left, right)

    def all_reverse(self) -> None:
        self._propagate_rev(self.root)

    def apply(self, l: int, r: int, f: F) -> None:
        assert (
            0 <= l <= r <= len(self)
        ), f"IndexError: {self.__class__.__name__}.apply({l}, {r}, {f}), len={len(self)}"
        left, right = self._internal_split(r)
        if l == 0:
            self._propagate_lazy(left, f)
        else:
            left = self._get_kth_elm_splay(left, l - 1)
            self._propagate_lazy(left.right, f)
            self._update(left)
        self.root = self._internal_merge(left, right)

    def all_apply(self, f: F) -> None:
        self._propagate_lazy(self.root, f)

    def prod(self, l: int, r: int) -> T:
        assert (
            0 <= l <= r <= len(self)
        ), f"IndexError: {self.__class__.__name__}.prod({l}, {r}), len={len(self)}"
        if l == r:
            return self.e
        left, right = self._internal_split(r)
        if l == 0:
            res = left.data
        else:
            left = self._get_kth_elm_splay(left, l - 1)
            res = left.right.data
        self.root = self._internal_merge(left, right)
        return res

    def all_prod(self) -> T:
        self._propagate(self.root)
        return self.root.data if self.root else self.e

    def insert(self, k: int, key: T) -> None:
        node = self.Node(key, self.id)
        if not self.root:
            self.root = node
            return
        if k >= len(self):
            root = self._get_kth_elm_splay(self.root, len(self) - 1)
            node.left = root
        else:
            root = self._get_kth_elm_splay(self.root, k)
            if root.left:
                node.left = root.left
                root.left.par = node
                root.left = None
                self._update(root)
            node.right = root
        root.par = node
        self.root = node
        self._update(self.root)

    def append(self, key: T) -> None:
        node = self._get_right_splay(self.root)
        self.root = self.Node(key, self.id)
        self.root.left = node
        if node:
            node.par = self.root
        self._update(self.root)

    def appendleft(self, key: T) -> None:
        node = self._get_left_splay(self.root)
        self.root = self.Node(key, self.id)
        self.root.right = node
        if node:
            node.par = self.root
        self._update(self.root)

    def pop(self, k: int = -1) -> T:
        if k == -1:
            node = self._get_right_splay(self.root)
            if node.left:
                node.left.par = None
            self.root = node.left
            return node.key
        root = self._get_kth_elm_splay(self.root, k)
        res = root.key
        if root.left and root.right:
            node = self._get_right_splay(root.left)
            node.par = None
            node.right = root.right
            if node.right:
                node.right.par = node
            self._update(node)
            self.root = node
        else:
            self.root = root.right if root.right else root.left
            if self.root:
                self.root.par = None
        return res

    def popleft(self) -> T:
        node = self._get_left_splay(self.root)
        self.root = node.right
        if node.right:
            node.right.par = None
        return node.key

    def copy(self) -> "LazySplayTree":
        return LazySplayTree(
            self.tolist(), self.op, self.mapping, self.composition, self.e
        )

    def clear(self) -> None:
        self.root = None

    def tolist(self) -> list[T]:
        node = self.root
        stack, res = [], newlist_hint(len(self))
        while stack or node:
            if node:
                self._propagate(node)
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                res.append(node.key)
                node = node.right
        return res

    def __setitem__(self, k: int, key: T):
        self.root = self._get_kth_elm_splay(self.root, k)
        self.root.key = key
        self._update(self.root)

    def __getitem__(self, k: int) -> T:
        self.root = self._get_kth_elm_splay(self.root, k)
        return self.root.key

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == len(self):
            raise StopIteration
        res = self[self.__iter]
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(len(self)):
            yield self[-i - 1]

    def __len__(self):
        return self.root.size if self.root else 0

    def __str__(self):
        return str(self.tolist())

    def __bool__(self):
        return self.root is not None

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
