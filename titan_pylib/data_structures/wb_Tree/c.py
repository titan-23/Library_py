import sys
from typing import Generic, List, Union, TypeVar, Tuple, Callable, Iterable, Optional
from __pypy__ import newlist_hint

T = TypeVar("T")
F = TypeVar("F")


class LazySplayTree(Generic[T, F]):

    class Node:

        def __init__(self, key: T, lazy: F):
            self.key: T = key
            self.data: T = key
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
        self.root = _root
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.e = e
        self.id = id
        a = n_or_a
        if isinstance(a, int):
            if a > 0:
                a = [e for _ in range(a)]
        elif not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: List[T]) -> None:
        Node = LazySplayTree.Node
        id = self.id

        def sort(l: int, r: int) -> Node:
            mid = (l + r) >> 1
            node = Node(a[mid], id)
            if l != mid:
                node.left = sort(l, mid)
                node.left.par = node
            if mid + 1 != r:
                node.right = sort(mid + 1, r)
                node.right.par = node
            self._update(node)
            return node

        self.root = sort(0, len(a))

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
            pnode.par = node
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
        node.lazy = node.lazy if f == self.id else self.composition(f, node.lazy)

    def _propagate(self, node: Optional[Node]) -> None:
        if not node:
            return
        if node.rev:
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
        node.size = 1
        if node.left:
            node.data = self.op(node.left.data, node.data)
            node.size += node.left.size
        if node.right:
            node.data = self.op(node.data, node.right.data)
            node.size += node.right.size

    def _splay(self, node: Node) -> None:
        while node.par and node.par.par:
            pnode = node.par
            gnode = pnode.par
            if (gnode.left is pnode) == (pnode.left is node):
                self._rotate(pnode)
                self._rotate(node)
            else:
                self._rotate(node)
                self._rotate(node)
        if not node.par:
            return
        self._rotate(node)
        return node

    def _get_kth_elm_splay(self, node: Optional[Node], k: int) -> None:
        if k < 0:
            k += len(self)
        while True:
            self._propagate(node)
            t = 0 if node.left is None else node.left.size
            if t == k:
                break
            if t > k:
                node = node.left
            else:
                node = node.right
                k -= t + 1
        self._splay(node)
        return node

    def _get_left_splay(self, node: Node) -> Node:
        self._propagate(node)
        if not node or node.left:
            return node
        while node.left:
            node = node.left
            self._propagate(node)
        self._splay(node)
        return node

    def _get_max_splay(self, node: Node) -> Node:
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
        self.root = self._get_max_splay(self.root)
        self.root.right = other.root
        other.root.par = self.root
        self._update(self.root)

    def split(self, k: int) -> Tuple["LazySplayTree", "LazySplayTree"]:
        left, right = self._internal_split(self.root, k)
        return left, right

    def _internal_split(self, k: int) -> Tuple[Node, Node]:
        if k >= len(self):
            return self.root, None
        right = self._get_kth_elm_splay(self.root, k)
        left = right.left
        if left:
            left.par = None
        right.left = None
        self._update(right)
        self.root = None
        return left, right

    def reverse(self, l: int, r: int) -> None:
        assert (
            0 <= l <= r <= len(self)
        ), f"IndexError: LazySplayTree.reverse({l}, {r}), len={len(self)}"
        left, right = self._internal_split(r)
        if l == 0:
            self._propagate_rev(left)
        else:
            left = self._get_kth_elm_splay(left, l - 1)
            self._propagate_rev(left.right)
        if right is None:
            right = left
        else:
            right.left = left
            left.par = right
            self._update(right)
        self.root = right

    def all_reverse(self) -> None:
        self._propagate_rev(self.root)

    def apply(self, l: int, r: int, f: F) -> None:
        if l >= r:
            return
        left, right = self._internal_split(r)
        if l == 0:
            self._propagate_lazy(left, f)
        else:
            left = self._get_kth_elm_splay(left, l - 1)
            self._propagate_lazy(left.right, f)
            self._update(left)
        if right is None:
            right = left
        else:
            right.left = left
            left.par = right
            self._update(right)
        self.root = right

    def all_apply(self, f: F) -> None:
        self._propagate_lazy(self.root, f)

    def prod(self, l: int, r: int) -> T:
        if l >= r:
            return self.e
        left, right = self._internal_split(r)
        if l == 0:
            res = left.data
        else:
            left = self._get_kth_elm_splay(left, l - 1)
            res = left.right.data
        if right is None:
            right = left
        else:
            right.left = left
            left.par = right
            self._update(right)
        self.root = right
        return res

    def all_prod(self) -> T:
        return self.e if self.root is None else self.root.data

    def insert(self, k: int, key: T) -> None:
        node = LazySplayTree.Node(key, self.id)
        if not self.root:
            self.root = node
            return
        if k >= len(self):
            self.root = self._get_kth_elm_splay(self.root, len(self) - 1)
            node.left = self.root
            self.root.par = node
            self.root = node
        else:
            self.root = self._get_kth_elm_splay(self.root, k)
            if self.root.left:
                node.left = self.root.left
                self.root.left.par = node
                self.root.left = None
                self._update(self.root)
            node.right = self.root
            self.root.par = node
            self.root = node
        self._update(self.root)

    def append(self, key: T) -> None:
        node = self._get_max_splay(self.root)
        self.root = self.Node(key, self.id)
        self.root.left = node
        if node:
            node.par = self.root
        self._update(self.root)

    def appendleft(self, key: T) -> None:
        node = self._get_left_splay(self.root)
        self.root = self.Node(key, self.id)
        self.root.right = node
        self._update(self.root)

    def pop(self, k: int = -1) -> T:
        if k == -1:
            node = self._get_max_splay(self.root)
            node.left.par = None
            self.root = node.left
            return node.key
        self.root = self._get_kth_elm_splay(self.root, k)
        res = self.root.key
        if not self.root.left:
            self.root = self.root.right
            if self.root:
                self.root.par = None
        elif not self.root.right:
            self.root = self.root.left
            if self.root:
                self.root.par = None
        else:
            node = self._get_max_splay(self.root.left)
            node.par = None
            node.right = self.root.right
            if node.right:
                node.right.par = node
            self.root = node
            self._update(self.root)
        return res

    def popleft(self) -> T:
        node = self._get_left_splay(self.root)
        self._propagate(node)
        self.root = node.right
        if node:
            node.par = None
        return node.key

    def rotate(self, x: int) -> None:
        n = len(self)
        x %= n
        l, self = self.split(n - x)
        self.merge(l)

    def copy(self) -> "LazySplayTree":
        return LazySplayTree(
            self.tolist(), self.op, self.mapping, self.composition, self.e
        )

    def clear(self) -> None:
        self.root = None

    def tolist(self) -> List[T]:
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
        return 0 if self.root is None else self.root.size

    def __str__(self):
        return str(self.tolist())

    def __bool__(self):
        return self.root is not None

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"


import sys

# from Library_py.IO.FastO import FastO
import os
from __pypy__.builders import StringBuilder


class FastO:

    sb = StringBuilder()

    @classmethod
    def write(cls, *args, sep: str = " ", end: str = "\n", flush: bool = False) -> None:
        append = cls.sb.append
        for i in range(len(args) - 1):
            append(str(args[i]))
            append(sep)
        if args:
            append(str(args[-1]))
        append(end)
        if flush:
            cls.flush()

    @classmethod
    def flush(cls) -> None:
        os.write(1, cls.sb.build().encode())
        cls.sb = StringBuilder()


write, flush = FastO.write, FastO.flush
input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

mod = 998244353


def op(s, t):
    s1, s2 = s >> 30, s & msk
    t1, t2 = t >> 30, t & msk
    c1 = (s1 + t1) % mod
    c2 = (s2 + t2) % mod
    return (c1 << 30) + c2


def mapping(f, s):
    f1, f2 = f >> 30, f & msk
    s1, s2 = s >> 30, s & msk
    return (((s1 * f1 + s2 * f2) % mod) << 30) + s2


def composition(f, g):
    f1, f2 = f >> 30, f & msk
    g1, g2 = g >> 30, g & msk
    z1 = (f1 * g1) % mod
    z2 = (f1 * g2 + f2) % mod
    return (z1 << 30) + z2


e = 0
id = 1 << 30

msk = (1 << 30) - 1
n, q = map(int, input().split())
A = list(map(int, input().split()))
V = [a << 30 | 1 for a in A]

s = LazySplayTree(V, op, mapping, composition, e, id)

for i in range(q):
    qu = tuple(map(int, input().split()))
    if qu[0] == 0:
        s.insert(qu[1], qu[2] << 30 | 1)
    elif qu[0] == 1:
        s.pop(qu[1])
    elif qu[0] == 2:
        s.reverse(qu[1], qu[2])
    elif qu[0] == 3:
        s.apply(qu[1], qu[2], (qu[3] << 30) | qu[4])
    else:
        write(s.prod(qu[1], qu[2]) >> 30)
flush()
