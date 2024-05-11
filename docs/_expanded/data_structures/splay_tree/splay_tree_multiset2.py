# from titan_pylib.data_structures.splay_tree.splay_tree_multiset2 import SplayTreeMultiset2
import sys
from __pypy__ import newlist_hint
from typing import Generic, Iterable, List, TypeVar, Tuple, Optional

T = TypeVar("T")


class SplayTreeMultiset2(Generic[T]):

    class Node:

        def __init__(self, key: T, val: int):
            self.key = key
            self.val = val
            self.left = None
            self.right = None

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.val}\n"
            return (
                f"key:{self.key, self.val},\n left:{self.left},\n right:{self.right}\n"
            )

    def __init__(self, a: Iterable[T] = []):
        self.node = None
        self._len = 0
        self._len_elm = 0
        if not (hasattr(a, "__getitem__") and hasattr(a, "__len__")):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: Iterable[T]) -> None:
        Node = SplayTreeMultiset2.Node

        def sort(l: int, r: int) -> Node:
            mid = (l + r) >> 1
            node = Node(key[mid], val[mid])
            if l != mid:
                node.left = sort(l, mid)
            if mid + 1 != r:
                node.right = sort(mid + 1, r)
            return node

        a = sorted(a)
        self._len = len(a)
        key, val = self._rle(sorted(a))
        self._len_elm = len(key)
        self.node = sort(0, len(key))

    def _rle(self, a: List[T]) -> Tuple[List[T], List[int]]:
        x = newlist_hint(len(a))
        y = newlist_hint(len(a))
        x.append(a[0])
        y.append(1)
        for i, e in enumerate(a):
            if i == 0:
                continue
            if e == x[-1]:
                y[-1] += 1
                continue
            x.append(e)
            y.append(1)
        return x, y

    def _splay(self, path: List[Node], di: int) -> Node:
        for _ in range(len(path) >> 1):
            node = path.pop()
            pnode = path.pop()
            if di & 1 == di >> 1 & 1:
                if di & 1 == 1:
                    tmp = node.left
                    node.left = tmp.right
                    tmp.right = node
                    pnode.left = node.right
                    node.right = pnode
                else:
                    tmp = node.right
                    node.right = tmp.left
                    tmp.left = node
                    pnode.right = node.left
                    node.left = pnode
            else:
                if di & 1 == 1:
                    tmp = node.left
                    node.left = tmp.right
                    pnode.right = tmp.left
                    tmp.right = node
                    tmp.left = pnode
                else:
                    tmp = node.right
                    node.right = tmp.left
                    pnode.left = tmp.right
                    tmp.left = node
                    tmp.right = pnode
            if not path:
                return tmp
            di >>= 2
            if di & 1 == 1:
                path[-1].left = tmp
            else:
                path[-1].right = tmp
        gnode = path[0]
        if di & 1 == 1:
            node = gnode.left
            gnode.left = node.right
            node.right = gnode
        else:
            node = gnode.right
            gnode.right = node.left
            node.left = gnode
        return node

    def _set_search_splay(self, key: T) -> None:
        node = self.node
        if node is None or node.key == key:
            return
        path = []
        di = 0
        while True:
            if node.key == key:
                break
            elif key < node.key:
                if node.left is None:
                    break
                path.append(node)
                di <<= 1
                di |= 1
                node = node.left
            else:
                if node.right is None:
                    break
                path.append(node)
                di <<= 1
                node = node.right
        if path:
            self.node = self._splay(path, di)

    def _get_min_splay(self, node: Node) -> Node:
        if node is None or node.left is None:
            return node
        path = []
        while node.left is not None:
            path.append(node)
            node = node.left
        return self._splay(path, (1 << len(path)) - 1)

    def _get_max_splay(self, node: Node) -> Node:
        if node is None or node.right is None:
            return node
        path = []
        while node.right is not None:
            path.append(node)
            node = node.right
        return self._splay(path, 0)

    def add(self, key: T, val: int = 1) -> None:
        self._len += val
        if self.node is None:
            self._len_elm += 1
            self.node = SplayTreeMultiset2.Node(key, val)
            return
        self._set_search_splay(key)
        if self.node.key == key:
            self.node.val += val
            return
        self._len_elm += 1
        node = SplayTreeMultiset2.Node(key, val)
        if key < self.node.key:
            node.left = self.node.left
            node.right = self.node
            self.node.left = None
        else:
            node.left = self.node
            node.right = self.node.right
            self.node.right = None
        self.node = node
        return

    def discard(self, key: T, val: int = 1) -> bool:
        if self.node is None:
            return False
        self._set_search_splay(key)
        if self.node.key != key:
            return False
        if self.node.val > val:
            self.node.val -= val
            self._len -= val
            return True
        self._len -= self.node.val
        self._len_elm -= 1
        if self.node.left is None:
            self.node = self.node.right
        elif self.node.right is None:
            self.node = self.node.left
        else:
            node = self._get_min_splay(self.node.right)
            node.left = self.node.left
            self.node = node
        return True

    def discard_all(self, key: T) -> bool:
        return self.discar(key, self.count(key))

    def count(self, key: T) -> int:
        if self.node is None:
            return 0
        self._set_search_splay(key)
        return self.node.val if self.node.key == key else 0

    def le(self, key: T) -> Optional[T]:
        node = self.node
        if node is None:
            return None
        path = []
        di = 0
        res = None
        while True:
            if node.key == key:
                res = key
                break
            elif key < node.key:
                if node.left is None:
                    break
                path.append(node)
                di <<= 1
                di |= 1
                node = node.left
            else:
                res = node.key
                if node.right is None:
                    break
                path.append(node)
                di <<= 1
                node = node.right
        if path:
            self.node = self._splay(path, di)
        return res

    def lt(self, key: T) -> Optional[T]:
        node = self.node
        if node is None:
            return None
        path = []
        di = 0
        res = None
        while True:
            if key <= node.key:
                if node.left is None:
                    break
                path.append(node)
                di <<= 1
                di |= 1
                node = node.left
            else:
                res = node.key
                if node.right is None:
                    break
                path.append(node)
                di <<= 1
                node = node.right
        if path:
            self.node = self._splay(path, di)
        return res

    def ge(self, key: T) -> Optional[T]:
        node = self.node
        if node is None:
            return None
        path = []
        di = 0
        res = None
        while True:
            if node.key == key:
                res = node.key
                break
            elif key < node.key:
                res = node.key
                if node.left is None:
                    break
                path.append(node)
                di <<= 1
                di |= 1
                node = node.left
            else:
                if node.right is None:
                    break
                path.append(node)
                di <<= 1
                node = node.right
        if path:
            self.node = self._splay(path, di)
        return res

    def gt(self, key: T) -> Optional[T]:
        node = self.node
        if node is None:
            return None
        path = []
        di = 0
        res = None
        while True:
            if key < node.key:
                res = node.key
                if node.left is None:
                    break
                path.append(node)
                di <<= 1
                di |= 1
                node = node.left
            else:
                if node.right is None:
                    break
                path.append(node)
                di <<= 1
                node = node.right
        if path:
            self.node = self._splay(path, di)
        return res

    def pop_max(self) -> T:
        self.node = self._get_max_splay(self.node)
        res = self.node.key
        self.discard(res)
        return res

    def pop_min(self) -> T:
        self.node = self._get_min_splay(self.node)
        res = self.node.key
        self.discard(res)
        return res

    def get_min(self) -> Optional[T]:
        if self.node is None:
            return
        self.node = self._get_min_splay(self.node)
        return self.node.key

    def get_max(self) -> Optional[T]:
        if self.node is None:
            return
        self.node = self._get_max_splay(self.node)
        return self.node.key

    def tolist(self) -> List[T]:
        a = []
        if self.node is None:
            return a
        if sys.getrecursionlimit() < self.len_elm():
            sys.setrecursionlimit(self.len_elm() + 1)

        def rec(node):
            if node.left is not None:
                rec(node.left)
            a.extend([node.key] * node.val)
            if node.right is not None:
                rec(node.right)

        rec(self.node)
        return a

    def tolist_items(self) -> List[Tuple[T, int]]:
        a = []
        if self.node is None:
            return a
        if sys.getrecursionlimit() < self._len_elm():
            sys.setrecursionlimit(self._len_elm() + 1)

        def rec(node):
            if node.left is not None:
                rec(node.left)
            a.append((node.key, node.val))
            if node.right is not None:
                rec(node.right)

        rec(self.node)
        return a

    def len_elm(self) -> int:
        return self._len_elm

    def clear(self) -> None:
        self.node = None

    def __getitem__(self, k):  # 先s頭と末尾しか対応していない
        if k == -1 or k == self._len - 1:
            return self.get_max()
        elif k == 0:
            return self.get_min()
        raise IndexError

    def __contains__(self, key: T) -> bool:
        self._set_search_splay(key)
        return self.node is not None and self.node.key == key

    def __len__(self):
        return self._len

    def __bool__(self):
        return self.node is not None

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"SplayTreeMultiset2({self.tolist})"
