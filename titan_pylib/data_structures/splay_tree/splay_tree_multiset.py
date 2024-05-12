from titan_pylib.my_class.supports_less_than import SupportsLessThan
import sys
from __pypy__ import newlist_hint
from typing import Iterator, Optional, Generic, Iterable, TypeVar

T = TypeVar("T", bound=SupportsLessThan)


class SplayTreeMultiset(Generic[T]):

    class Node:

        def __init__(self, key: T, val: int):
            self.key: T = key
            self.size: int = 1
            self.val: int = val
            self.valsize: int = val
            self.left: Optional["SplayTreeMultiset.Node"] = None
            self.right: Optional["SplayTreeMultiset.Node"] = None

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.size, self.val, self.valsize}\n"
            return f"key:{self.key, self.size, self.val, self.valsize},\n left:{self.left},\n right:{self.right}\n"

    def __init__(self, a: Iterable[T] = []) -> None:
        self.root: Optional["SplayTreeMultiset.Node"] = None
        if a:
            self._build(a)

    def _build(self, a: Iterable[T]) -> None:
        Node = SplayTreeMultiset.Node

        def sort(l: int, r: int) -> SplayTreeMultiset.Node:
            mid = (l + r) >> 1
            node = Node(key[mid], val[mid])
            if l != mid:
                node.left = sort(l, mid)
            if mid + 1 != r:
                node.right = sort(mid + 1, r)
            self._update(node)
            return node

        key, val = self._rle(sorted(a))
        if len(key) == 0:
            return
        self.root = sort(0, len(key))

    def _rle(self, a: list[T]) -> tuple[list[T], list[int]]:
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

    def _update(self, node: Node) -> None:
        if node.left is None:
            if node.right is None:
                node.size = 1
                node.valsize = node.val
            else:
                node.size = 1 + node.right.size
                node.valsize = node.val + node.right.valsize
        else:
            if node.right is None:
                node.size = 1 + node.left.size
                node.valsize = node.val + node.left.valsize
            else:
                node.size = 1 + node.left.size + node.right.size
                node.valsize = node.val + node.left.valsize + node.right.valsize

    def _splay(self, path: list[Node], d: int) -> Node:
        for _ in range(len(path) >> 1):
            node = path.pop()
            pnode = path.pop()
            if d & 1 == d >> 1 & 1:
                if d & 1:
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
                if d & 1:
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
            self._update(pnode)
            self._update(node)
            self._update(tmp)
            if not path:
                return tmp
            d >>= 2
            if d & 1:
                path[-1].left = tmp
            else:
                path[-1].right = tmp
        gnode = path[0]
        if d & 1:
            node = gnode.left
            gnode.left = node.right
            node.right = gnode
        else:
            node = gnode.right
            gnode.right = node.left
            node.left = gnode
        self._update(gnode)
        self._update(node)
        return node

    def _set_search_splay(self, key: T) -> None:
        node = self.root
        if node is None or node.key == key:
            return
        path = []
        d = 0
        while True:
            if node.key == key:
                break
            if key < node.key:
                if node.left is None:
                    break
                path.append(node)
                d <<= 1
                d |= 1
                node = node.left
            else:
                if node.right is None:
                    break
                path.append(node)
                d <<= 1
                node = node.right
        if path:
            self.root = self._splay(path, d)

    def _set_kth_elm_splay(self, k: int) -> None:
        if k < 0:
            k += self.__len__()
        d = 0
        node = self.root
        path = []
        while True:
            t = node.val if node.left is None else node.val + node.left.valsize
            if t - node.val <= k < t:
                if path:
                    self.root = self._splay(path, d)
                break
            elif t > k:
                path.append(node)
                d <<= 1
                d |= 1
                node = node.left
            else:
                path.append(node)
                d <<= 1
                node = node.right
                k -= t

    def _set_kth_elm_tree_splay(self, k: int) -> None:
        if k < 0:
            k += self.len_elm()
        assert 0 <= k < self.len_elm()
        d = 0
        node = self.root
        path = []
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                if path:
                    self.root = self._splay(path, d)
                return
            elif t > k:
                path.append(node)
                d <<= 1
                d |= 1
                node = node.left
            else:
                path.append(node)
                d <<= 1
                node = node.right
                k -= t + 1

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
        if self.root is None:
            self.root = SplayTreeMultiset.Node(key, val)
            return
        self._set_search_splay(key)
        if self.root.key == key:
            self.root.val += val
            self._update(self.root)
            return
        node = SplayTreeMultiset.Node(key, val)
        if key < self.root.key:
            node.left = self.root.left
            node.right = self.root
            self.root.left = None
            self._update(node.right)
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
            self._update(node.left)
        self._update(node)
        self.root = node
        return

    def discard(self, key: T, val: int = 1) -> bool:
        if self.root is None:
            return False
        self._set_search_splay(key)
        if self.root.key != key:
            return False
        if self.root.val > val:
            self.root.val -= val
            self._update(self.root)
            return True
        if self.root.left is None:
            self.root = self.root.right
        elif self.root.right is None:
            self.root = self.root.left
        else:
            node = self._get_min_splay(self.root.right)
            node.left = self.root.left
            self._update(node)
            self.root = node
        return True

    def discard_all(self, key: T) -> bool:
        return self.discard(key, self.count(key))

    def count(self, key: T) -> int:
        if self.root is None:
            return 0
        self._set_search_splay(key)
        return self.root.val if self.root.key == key else 0

    def le(self, key: T) -> Optional[T]:
        node = self.root
        if node is None:
            return None
        path = []
        d = 0
        res = None
        while True:
            if node.key == key:
                res = key
                break
            elif key < node.key:
                if node.left is None:
                    break
                path.append(node)
                d <<= 1
                d |= 1
                node = node.left
            else:
                res = node.key
                if node.right is None:
                    break
                path.append(node)
                d <<= 1
                node = node.right
        if path:
            self.root = self._splay(path, d)
        return res

    def lt(self, key: T) -> Optional[T]:
        node = self.root
        path = []
        d = 0
        res = None
        while node is not None:
            if key <= node.key:
                path.append(node)
                d <<= 1
                d |= 1
                node = node.left
            else:
                path.append(node)
                d <<= 1
                res = node.key
                node = node.right
        else:
            if path:
                path.pop()
                d >>= 1
        if path:
            self.root = self._splay(path, d)
        return res

    def ge(self, key: T) -> Optional[T]:
        node = self.root
        if node is None:
            return None
        path = []
        d = 0
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
                d <<= 1
                d |= 1
                node = node.left
            else:
                if node.right is None:
                    break
                path.append(node)
                d <<= 1
                node = node.right
        if path:
            self.root = self._splay(path, d)
        return res

    def gt(self, key: T) -> Optional[T]:
        node = self.root
        path = []
        d = 0
        res = None
        while node is not None:
            if key < node.key:
                path.append(node)
                d <<= 1
                d |= 1
                res = node.key
                node = node.left
            else:
                path.append(node)
                d <<= 1
                node = node.right
        else:
            if path:
                path.pop()
                d >>= 1
        if path:
            self.root = self._splay(path, d)
        return res

    def index(self, key: T) -> int:
        if self.root is None:
            return 0
        self._set_search_splay(key)
        res = 0 if self.root.left is None else self.root.left.valsize
        if self.root.key < key:
            res += self.root.val
        return res

    def index_right(self, key: T) -> int:
        if self.root is None:
            return 0
        self._set_search_splay(key)
        res = 0 if self.root.left is None else self.root.left.valsize
        if self.root.key <= key:
            res += self.root.val
        return res

    def index_keys(self, key: T) -> int:
        if self.root is None:
            return 0
        self._set_search_splay(key)
        res = 0 if self.root.left is None else self.root.left.size
        if self.root.key < key:
            res += 1
        return res

    def index_right_keys(self, key: T) -> int:
        if self.root is None:
            return 0
        self._set_search_splay(key)
        res = 0 if self.root.left is None else self.root.left.size
        if self.root.key <= key:
            res += 1
        return res

    def pop(self, k: int = -1) -> T:
        self._set_kth_elm_splay(k)
        res = self.root.key
        self.discard(res)
        return res

    def pop_max(self) -> T:
        return self.pop()

    def pop_min(self) -> T:
        return self.pop(0)

    def tolist(self) -> list[T]:
        a = []
        if self.root is None:
            return a
        if sys.getrecursionlimit() < self.len_elm():
            sys.setrecursionlimit(self.len_elm() + 1)

        def rec(node):
            if node.left is not None:
                rec(node.left)
            for _ in range(node.val):
                a.append(node.key)
            if node.right is not None:
                rec(node.right)

        rec(self.root)
        return a

    def tolist_items(self) -> list[tuple[T, int]]:
        a = []
        if self.root is None:
            return a
        if sys.getrecursionlimit() < self.len_elm():
            sys.setrecursionlimit(self.len_elm() + 1)

        def rec(node):
            if node.left is not None:
                rec(node.left)
            a.append((node.key, node.val))
            if node.right is not None:
                rec(node.right)

        rec(self.root)
        return a

    def get_elm(self, k: int) -> T:
        assert -self.len_elm() <= k < self.len_elm()
        self._set_kth_elm_tree_splay(k)
        return self.root.key

    def items(self) -> Iterator[tuple[T, int]]:
        for i in range(self.len_elm()):
            self._set_kth_elm_tree_splay(i)
            yield self.root.key, self.root.val

    def keys(self) -> Iterator[T]:
        for i in range(self.len_elm()):
            self._set_kth_elm_tree_splay(i)
            yield self.root.key

    def values(self) -> Iterator[int]:
        for i in range(self.len_elm()):
            self._set_kth_elm_tree_splay(i)
            yield self.root.val

    def len_elm(self) -> int:
        return 0 if self.root is None else self.root.size

    def show(self) -> None:
        print(
            "{" + ", ".join(map(lambda x: f"{x[0]}: {x[1]}", self.tolist_items())) + "}"
        )

    def clear(self) -> None:
        self.root = None

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == self.__len__():
            raise StopIteration
        res = self.__getitem__(self.__iter)
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(self.__len__()):
            yield self.__getitem__(-i - 1)

    def __contains__(self, key: T) -> bool:
        self._set_search_splay(key)
        return self.root is not None and self.root.key == key

    def __getitem__(self, k: int) -> T:
        self._set_kth_elm_splay(k)
        return self.root.key

    def __len__(self):
        return 0 if self.root is None else self.root.valsize

    def __bool__(self):
        return self.root is not None

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"SplayTreeMultiset({self.tolist()})"
