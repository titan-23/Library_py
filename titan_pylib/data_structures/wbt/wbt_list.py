from titan_pylib.data_structures.wbt._wbt_list_node import _WBTListNode
from typing import Generic, TypeVar, Optional, Iterable, Callable

T = TypeVar("T")


class WBTList(Generic[T]):
    # insert / pop / pop_max

    def __init__(
        self,
        a: Iterable[T] = [],
    ) -> None:
        self._root = None
        self.__build(a)

    def __build(self, a: Iterable[T]) -> None:
        def build(l: int, r: int, pnode: Optional[_WBTListNode] = None) -> _WBTListNode:
            if l == r:
                return None
            mid = (l + r) // 2
            node = _WBTListNode(self, a[mid])
            node._left = build(l, mid, node)
            node._right = build(mid + 1, r, node)
            node._par = pnode
            node._update()
            return node

        if not isinstance(a, list):
            a = list(a)
        if not a:
            return
        self._root = build(0, len(a))

    @classmethod
    def _weight(self, node: Optional[_WBTListNode]) -> int:
        return node._size + 1 if node else 1

    def _merge_with_root(
        self,
        l: Optional[_WBTListNode],
        root: _WBTListNode,
        r: Optional[_WBTListNode],
    ) -> _WBTListNode:
        if self._weight(l) * _WBTListNode.DELTA < self._weight(r):
            r._propagate()
            r._left = self._merge_with_root(l, root, r._left)
            r._left._par = r
            r._par = None
            r._update()
            if self._weight(r._right) * _WBTListNode.DELTA < self._weight(r._left):
                return r._balance_right()
            return r
        elif self._weight(r) * _WBTListNode.DELTA < self._weight(l):
            l._propagate()
            l._right = self._merge_with_root(l._right, root, r)
            l._right._par = l
            l._par = None
            l._update()
            if self._weight(l._left) * _WBTListNode.DELTA < self._weight(l._right):
                return l._balance_left()
            return l
        else:
            root._left = l
            root._right = r
            if l:
                l._par = root
            if r:
                r._par = root
            root._update()
            return root

    def _split_node(
        self, node: _WBTListNode, k: int
    ) -> tuple[Optional[_WBTListNode], Optional[_WBTListNode]]:
        if not node:
            return None, None
        node._propagate()
        par = node._par
        u = k if node._left is None else k - node._left._size
        s, t = None, None
        if u == 0:
            s = node._left
            t = self._merge_with_root(None, node, node._right)
        elif u < 0:
            s, t = self._split_node(node._left, k)
            t = self._merge_with_root(t, node, node._right)
        else:
            s, t = self._split_node(node._right, u - 1)
            s = self._merge_with_root(node._left, node, s)
        if s:
            s._par = par
        if t:
            t._par = par
        return s, t

    def find_order(self, k: int) -> "WBTList[T]":
        if k < 0:
            k += len(self)
        node = self._root
        while True:
            node._propagate()
            t = node._left._size if node._left else 0
            if t == k:
                return node
            if t < k:
                k -= t + 1
                node = node._right
            else:
                node = node._left

    def split(self, k: int) -> tuple["WBTList", "WBTList"]:
        lnode, rnode = self._split_node(self._root, k)
        l, r = WBTList(), WBTList()
        l._root = lnode
        r._root = rnode
        return l, r

    def _pop_max(self, node: _WBTListNode) -> tuple[_WBTListNode, _WBTListNode]:
        l, tmp = self._split_node(node, node._size - 1)
        return l, tmp

    def _merge_node(self, l: _WBTListNode, r: _WBTListNode) -> _WBTListNode:
        if l is None:
            return r
        if r is None:
            return l
        l, tmp = self._pop_max(l)
        return self._merge_with_root(l, tmp, r)

    def extend(self, other: "WBTList[T]") -> None:
        self._root = self._merge_node(self._root, other._root)

    def insert(self, k: int, key) -> None:
        s, t = self._split_node(self._root, k)
        self._root = self._merge_with_root(s, _WBTListNode(self, key), t)

    def pop(self, k: int):
        s, t = self._split_node(self._root, k + 1)
        s, tmp = self._pop_max(s)
        self._root = self._merge_node(s, t)
        return tmp._key

    def _check(self, verbose: bool = False) -> None:
        """作業用デバック関数
        size,key,balanceをチェックして、正しければ高さを表示する
        """
        if self._root is None:
            if verbose:
                print("ok. 0 (empty)")
            return

        # _size, height
        def dfs(node: _WBTListNode) -> tuple[int, int]:
            h = 0
            s = 1
            if node._left:
                assert node._left._par is node
                ls, lh = dfs(node._left)
                s += ls
                h = max(h, lh)
            if node._right:
                assert node._right._par is node
                rs, rh = dfs(node._right)
                s += rs
                h = max(h, rh)
            assert node._size == s
            node._balance_check()
            return s, h + 1

        assert self._root._par is None
        _, h = dfs(self._root)
        if verbose:
            print(f"ok. {h}")

    def reverse(self, l, r):
        s, t = self._split_node(self._root, r)
        r, s = self._split_node(s, l)
        s._apply_rev()
        self._root = self._merge_node(self._merge_node(r, s), t)

    def __len__(self):
        return self._root._size if self._root else 0

    def __iter__(self):
        node = self._root
        stack: list[_WBTListNode] = []
        while stack or node:
            if node:
                node._propagate()
                stack.append(node)
                node = node._left
            else:
                node = stack.pop()
                yield node._key
                node = node._right

    def __str__(self):
        return str(list(self))
