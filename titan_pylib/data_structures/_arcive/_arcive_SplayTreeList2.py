# 2023.4.8
# 移植
# 理由: Lazyのほうで良くないか

import sys
from array import array
from typing import Generic, TypeVar, Iterable

T = TypeVar("T")


class SplayTreeList(Generic[T]):

    key = [None]
    size = array("I", [0])
    left = array("I", [0])
    right = array("I", [0])
    rev = array("i", [0])
    end = 1

    @classmethod
    def reserve(cls, n: int) -> None:
        cls.key += [None] * n
        cls.size += array("I", [1] * n)
        cls.left += array("I", [0] * n)
        cls.right += array("I", [0] * n)
        cls.rev += array("i", [0] * n)

    def __init__(self, a: Iterable[T] = [], node: int = 0):
        self.node = node
        if a:
            self._build(a)

    def _build(self, a: list[T]) -> None:
        def sort(l: int, r: int) -> int:
            mid = (l + r) >> 1
            if l != mid:
                SplayTreeList.left[mid] = sort(l, mid)
            if mid + 1 != r:
                SplayTreeList.right[mid] = sort(mid + 1, r)
            self._update(mid)
            return mid

        n = len(a)
        key = SplayTreeList.key
        end = SplayTreeList.end
        SplayTreeList.end += n
        SplayTreeList.reserve(n)
        key[end : end + n] = a
        self.node = sort(end, n + end)

    def _propagate(self, node: int) -> None:
        if SplayTreeList.rev[node]:
            SplayTreeList.left[node], SplayTreeList.right[node] = (
                SplayTreeList.right[node],
                SplayTreeList.left[node],
            )
            lnode, rnode = SplayTreeList.left[node], SplayTreeList.right[node]
            if lnode != 0:
                SplayTreeList.rev[lnode] ^= 1
            if rnode != 0:
                SplayTreeList.rev[rnode] ^= 1
            SplayTreeList.rev[node] = 0

    def _update(self, node: int) -> None:
        SplayTreeList.size[node] = (
            1
            + SplayTreeList.size[SplayTreeList.left[node]]
            + SplayTreeList.size[SplayTreeList.right[node]]
        )

    def _splay(self, path: list[int], di: int) -> int:
        left, right, size = SplayTreeList.left, SplayTreeList.right, SplayTreeList.size
        while len(path) > 1:
            node = path.pop()
            pnode = path.pop()
            if di & 1:
                tmp = left[node]
                left[node] = right[tmp]
                if di >> 1 & 1:
                    right[tmp] = node
                    left[pnode] = right[node]
                    right[node] = pnode
                else:
                    right[pnode] = left[tmp]
                    right[tmp] = node
                    left[tmp] = pnode
            else:
                tmp = right[node]
                right[node] = left[tmp]
                if di >> 1 & 1:
                    left[pnode] = right[tmp]
                    left[tmp] = node
                    right[tmp] = pnode
                else:
                    left[tmp] = node
                    right[pnode] = left[node]
                    left[node] = pnode
            size[tmp] = size[pnode]
            size[pnode] = 1 + size[left[pnode]] + size[right[pnode]]
            size[node] = 1 + size[left[node]] + size[right[node]]
            if not path:
                return tmp
            di >>= 2
            if di & 1:
                left[path[-1]] = tmp
            else:
                right[path[-1]] = tmp
        gnode = path[0]
        if di & 1:
            node = left[gnode]
            left[gnode] = right[node]
            right[node] = gnode
        else:
            node = right[gnode]
            right[gnode] = left[node]
            left[node] = gnode
        size[gnode] = 1 + size[left[gnode]] + size[right[gnode]]
        size[node] = 1 + size[left[node]] + size[right[node]]
        return node

    def _set_kth_elm_splay(self, k: int) -> None:
        size = SplayTreeList.size
        node = self.node
        if k < 0:
            k += size[node]
        left, right = SplayTreeList.left, SplayTreeList.right
        di = 0
        path = []
        while True:
            self._propagate(node)
            t = size[left[node]]
            if t == k:
                if path:
                    self.node = self._splay(path, di)
                return
            elif t > k:
                path.append(node)
                di <<= 1
                di |= 1
                node = left[node]
            else:
                path.append(node)
                di <<= 1
                node = right[node]
                k -= t + 1

    def _get_min_splay(self, node: int) -> int:
        if node == 0:
            return 0
        self._propagate(node)
        left = SplayTreeList.left
        if left[node] == 0:
            return node
        path = []
        while left[node] != 0:
            path.append(node)
            node = left[node]
            self._propagate(node)
        return self._splay(path, (1 << len(path)) - 1)

    def _get_max_splay(self, node: int) -> int:
        if node == 0:
            return 0
        self._propagate(node)
        right = SplayTreeList.right
        if right[node] == 0:
            return node
        path = []
        while right[node] != 0:
            path.append(node)
            node = right[node]
            self._propagate(node)
        return self._splay(path, 0)

    def merge(self, other: "SplayTreeList") -> None:
        if self.node == 0:
            self.node = other.node
            return
        if other.node == 0:
            return
        self.node = self._get_max_splay(self.node)
        SplayTreeList.right[self.node] = other.node
        self._update(self.node)

    def split(self, k: int) -> tuple["SplayTreeList", "SplayTreeList"]:
        if k >= SplayTreeList.size[self.node]:
            return self, SplayTreeList()
        self._set_kth_elm_splay(k)
        left = SplayTreeList(node=SplayTreeList.left[self.node])
        SplayTreeList.left[self.node], right = 0, self
        self._update(right.node)
        return left, right

    def reverse(self, l: int, r: int) -> None:
        if l >= r:
            return
        left, right = self.split(r)
        if l == 0:
            SplayTreeList.rev[left.node] ^= 1
        else:
            left._set_kth_elm_splay(l - 1)
            SplayTreeList.rev[SplayTreeList.right[left.node]] ^= 1
        if right.node == 0:
            right.node = left.node
        else:
            SplayTreeList.left[right.node] = left.node
            self._update(right.node)
        self.node = right.node

    def all_reverse(self) -> None:
        SplayTreeList.rev[self.node] ^= 1

    def _make_node(self, key: T) -> int:
        # classmethodにすべきかも
        end = SplayTreeList.end
        if end >= len(SplayTreeList.key):
            SplayTreeList.key.append(key)
            SplayTreeList.size.append(1)
            SplayTreeList.left.append(0)
            SplayTreeList.right.append(0)
            SplayTreeList.rev.append(0)
        else:
            SplayTreeList.key[end] = key
        SplayTreeList.end += 1
        return end

    def insert(self, k: int, key: T) -> None:
        node = self._make_node(key)
        if self.node == 0:
            self.node = node
            return
        if k >= SplayTreeList.size[self.node]:
            self._set_kth_elm_splay(SplayTreeList.size[self.node] - 1)
            SplayTreeList.left[node] = self.node
            self.node = node
        else:
            self._set_kth_elm_splay(k)
            if SplayTreeList.left[self.node] != 0:
                SplayTreeList.left[node] = SplayTreeList.left[self.node]
                SplayTreeList.left[self.node] = 0
                self._update(self.node)
            SplayTreeList.right[node] = self.node
            self.node = node
        self._update(self.node)

    def append(self, key: T) -> None:
        node = self._get_max_splay(self.node)
        self.node = self._make_node(key)
        SplayTreeList.left[self.node] = node
        self._update(self.node)

    def appendleft(self, key: T) -> None:
        node = self._get_min_splay(self.node)
        self.node = self._make_node(key)
        SplayTreeList.right[self.node] = node
        self._update(self.node)

    def pop(self, k: int = -1) -> T:
        if k == -1:
            node = self._get_max_splay(self.node)
            self._propagate(node)
            self.node = SplayTreeList.left[node]
            return SplayTreeList.key[node]
        self._set_kth_elm_splay(k)
        res = SplayTreeList.key[self.node]
        if SplayTreeList.left[self.node] == 0:
            self.node = SplayTreeList.right[self.node]
        elif SplayTreeList.right[self.node] == 0:
            self.node = SplayTreeList.left[self.node]
        else:
            node = self._get_max_splay(SplayTreeList.left[self.node])
            SplayTreeList.right[node] = SplayTreeList.right[self.node]
            self.node = node
            self._update(self.node)
        return res

    def popleft(self) -> T:
        node = self._get_min_splay(self.node)
        self._propagate(node)
        self.node = SplayTreeList.right[node]
        return SplayTreeList.key[node]

    # 「末尾をを削除し先頭に挿入」をx回
    def rotate(self, x: int) -> None:
        n = SplayTreeList.size[self.node]
        x %= n
        l, self = self.split(n - x)
        self.merge(l)

    def tolist(self) -> list[T]:
        a = []
        if self.node == 0:
            return a
        if sys.getrecursionlimit() < SplayTreeList.size[self.node] * 2:
            sys.setrecursionlimit(SplayTreeList.size[self.node] * 2)
        left, right, key = SplayTreeList.left, SplayTreeList.right, SplayTreeList.key

        def rec(node: int) -> None:
            self._propagate(node)
            if left[node] != 0:
                rec(left[node])
            a.append(key[node])
            if right[node] != 0:
                rec(right[node])

        rec(self.node)
        return a

    def clear(self) -> None:
        self.node = 0

    def __setitem__(self, k: int, key: T):
        self._set_kth_elm_splay(k)
        SplayTreeList.key[self.node] = key
        self._update(self.node)

    def __getitem__(self, k: int) -> T:
        if k < 0 or k >= SplayTreeList.size[self.node]:
            raise IndexError
        self._set_kth_elm_splay(k)
        return SplayTreeList.key[self.node]

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == SplayTreeList.size[self.node]:
            raise StopIteration
        res = self.__getitem__(self.__iter)
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(SplayTreeList.size[self.node]):
            yield self.__getitem__(-i - 1)

    def __len__(self):
        return SplayTreeList.size[self.node]

    def __str__(self):
        return "[" + ", ".join(map(str, self.tolist())) + "]"

    def __bool__(self):
        return self.node != 0

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
