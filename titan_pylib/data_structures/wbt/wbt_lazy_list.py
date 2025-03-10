from titan_pylib.data_structures.wbt._wbt_lazy_list_node import _WBTLazyListNode
from typing import Generic, TypeVar, Optional, Iterable, Callable

T = TypeVar("T")
F = TypeVar("F")


class WBTLazyList(Generic[T, F]):

    def __init__(
        self,
        op: Callable[[T, T], T],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id_: F,
        a: Iterable[T] = [],
    ) -> None:
        self._root = None
        self._op = op
        self._mapping = mapping
        self._composition = composition
        self._e = e
        self._id = id_
        self.__build(a)

    def __build(self, a: Iterable[T]) -> None:
        def build(
            l: int, r: int, pnode: Optional[_WBTLazyListNode] = None
        ) -> _WBTLazyListNode:
            if l == r:
                return None
            mid = (l + r) // 2
            node = _WBTLazyListNode(self, a[mid], self._id)
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
    def _weight(self, node: Optional[_WBTLazyListNode]) -> int:
        return node._size + 1 if node else 1

    def _merge_with_root(
        self,
        l: Optional[_WBTLazyListNode],
        root: _WBTLazyListNode,
        r: Optional[_WBTLazyListNode],
    ) -> _WBTLazyListNode:
        if self._weight(l) * _WBTLazyListNode.DELTA < self._weight(r):
            r._propagate()
            r._left = self._merge_with_root(l, root, r._left)
            r._left._par = r
            r._par = None
            r._update()
            if self._weight(r._right) * _WBTLazyListNode.DELTA < self._weight(r._left):
                return r._balance_right()
            return r
        elif self._weight(r) * _WBTLazyListNode.DELTA < self._weight(l):
            l._propagate()
            l._right = self._merge_with_root(l._right, root, r)
            l._right._par = l
            l._par = None
            l._update()
            if self._weight(l._left) * _WBTLazyListNode.DELTA < self._weight(l._right):
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
        self, node: _WBTLazyListNode, k: int
    ) -> tuple[Optional[_WBTLazyListNode], Optional[_WBTLazyListNode]]:
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

    def find_order(self, k: int) -> "WBTLazyList[T, F]":
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

    def split(self, k: int) -> tuple["WBTLazyList", "WBTLazyList"]:
        lnode, rnode = self._split_node(self._root, k)
        l, r = (
            WBTLazyList(self._op, self._mapping, self._composition, self._e, self._id),
            WBTLazyList(self._op, self._mapping, self._composition, self._e, self._id),
        )
        l._root = lnode
        r._root = rnode
        return l, r

    def _pop_max(
        self, node: _WBTLazyListNode
    ) -> tuple[_WBTLazyListNode, _WBTLazyListNode]:
        l, tmp = self._split_node(node, node._size - 1)
        return l, tmp

    def _merge_node(self, l: _WBTLazyListNode, r: _WBTLazyListNode) -> _WBTLazyListNode:
        if l is None:
            return r
        if r is None:
            return l
        l, tmp = self._pop_max(l)
        return self._merge_with_root(l, tmp, r)

    def extend(self, other: "WBTLazyList[T, F]") -> None:
        self._root = self._merge_node(self._root, other._root)

    def insert(self, k: int, key) -> None:
        s, t = self._split_node(self._root, k)
        self._root = self._merge_with_root(s, _WBTLazyListNode(self, key, self._id), t)

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
        def dfs(node: _WBTLazyListNode) -> tuple[int, int]:
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

    def prod(self, l: int, r: int) -> T:
        def dfs(node: _WBTLazyListNode[T, F], left: int, right: int) -> T:
            if right <= l or r <= left:
                return self._e
            node._propagate()
            if l <= left and right < r:
                return node._data
            lsize = node._left._size if node._left else 0
            res = self._e
            if node._left:
                res = dfs(node._left, left, left + lsize)
            if l <= left + lsize < r:
                res = self._op(res, node._key)
            if node._right:
                res = self._op(res, dfs(node._right, left + lsize + 1, right))
            return res

        return dfs(self._root, 0, len(self))

    def apply(self, l, r, f):
        s, t = self._split_node(self._root, r)
        r, s = self._split_node(s, l)
        s._apply_lazy(f)
        self._root = self._merge_node(self._merge_node(r, s), t)

    def reverse(self, l, r):
        s, t = self._split_node(self._root, r)
        r, s = self._split_node(s, l)
        s._apply_rev()
        self._root = self._merge_node(self._merge_node(r, s), t)

    def __len__(self):
        return self._root._size if self._root else 0

    def __iter__(self):
        node = self._root
        stack: list[_WBTLazyListNode] = []
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
