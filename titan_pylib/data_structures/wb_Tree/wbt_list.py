from typing import Generic, TypeVar, Optional, Final

T = TypeVar("T")


class _WBTNodeBase(Generic[T]):
    """WBTノードのベースクラス
    size, par, left, rightをもつ
    """

    __slots__ = "_size", "_par", "_left", "_right"
    DELTA: Final[int] = 3
    GAMMA: Final[int] = 2

    def __init__(self) -> None:
        self._size: int = 1
        self._par: Optional[_WBTNodeBase[T]] = None
        self._left: Optional[_WBTNodeBase[T]] = None
        self._right: Optional[_WBTNodeBase[T]] = None

    def _weight_left(self) -> int:
        return self._left._size + 1 if self._left else 1

    def _weight_right(self) -> int:
        return self._right._size + 1 if self._right else 1

    def _update(self) -> None:
        self._size = (
            1
            + (self._left._size if self._left else 0)
            + (self._right._size if self._right else 0)
        )

    def _rotate_right(self) -> "_WBTNodeBase[T]":
        u = self._left
        u._size = self._size
        self._size -= u._left._size + 1 if u._left else 1
        u._par = self._par
        self._left = u._right
        if u._right:
            u._right._par = self
        u._right = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        return u

    def _rotate_left(self) -> "_WBTNodeBase[T]":
        u = self._right
        u._size = self._size
        self._size -= u._right._size + 1 if u._right else 1
        u._par = self._par
        self._right = u._left
        if u._left:
            u._left._par = self
        u._left = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        return u

    def _balance_check(self) -> None:
        if not self._weight_left() * _WBTNodeBase.DELTA >= self._weight_right():
            print(self._weight_left(), self._weight_right(), flush=True)
            print(self)
            assert False, f"self._weight_left() * DELTA >= self._weight_right()"
        if not self._weight_right() * _WBTNodeBase.DELTA >= self._weight_left():
            print(self._weight_left(), self._weight_right(), flush=True)
            print(self)
            assert False, f"self._weight_right() * DELTA >= self._weight_left()"


from typing import Generic, TypeVar, Optional, Iterable, Callable

T = TypeVar("T")
F = TypeVar("F")


class _WBTListNode(_WBTNodeBase, Generic[T, F]):

    __slots__ = (
        "_left",
        "_right",
        "_par",
        "_tree",
        "_key",
        "_lazy",
        "_data",
        "_rdata",
        "_rev",
    )

    def __init__(self, tree: "WBTList[T, F]", key: T, lazy: F) -> None:
        super().__init__()
        self._tree = tree
        self._key: T = key
        self._data: T = key
        self._rdata: T = key
        self._lazy: F = lazy
        self._rev: int = 0

        self._left: "_WBTListNode[T]"
        self._right: "_WBTListNode[T]"
        self._par: "_WBTListNode[T]"

    def __str__(self) -> str:
        if self._left is None and self._right is None:
            return f"key:{self._key, self._size}\n"
        return f"key:{self._key, self._size},\n _left:{self._left},\n _right:{self._right}\n"

    def check(self):
        def dfs(node: "_WBTListNode"):
            s = 1
            if node._left:
                assert node._left._par is node
                s += node._left._size
                dfs(node._left)
            if node._right:
                assert node._right._par is node
                s += node._right._size
                dfs(node._right)
            assert s == node._size

        dfs(self)
        # print("check ok.")

    def _update(self) -> None:
        self._size = 1
        self._data = self._key
        self._rdata = self._key
        if self._left:
            self._size += self._left._size
            self._data = self._tree._op(self._left._data, self._data)
            self._rdata = self._tree._op(self._rdata, self._left._rdata)
        if self._right:
            self._size += self._right._size
            self._data = self._tree._op(self._data, self._right._data)
            self._rdata = self._tree._op(self._right._rdata, self._rdata)

    def _apply_rev(self) -> None:
        self._rev ^= 1

    def _apply_lazy(self, f: F) -> None:
        self._key = self._tree._mapping(f, self._key)
        self._data = self._tree._mapping(f, self._data)
        self._rdata = self._tree._mapping(f, self._rdata)
        self._lazy = self._tree._composition(f, self._lazy)

    def _propagate(self) -> None:
        if self._rev:
            self._data, self._rdata = self._rdata, self._data
            self._left, self._right = self._right, self._left
            if self._left:
                self._left._apply_rev()
            if self._right:
                self._right._apply_rev()
            self._rev = 0
        if self._lazy != self._tree._id:
            if self._left:
                self._left._apply_lazy(self._lazy)
            if self._right:
                self._right._apply_lazy(self._lazy)
            self._lazy = self._tree._id

    def __rotate_right(self) -> "_WBTListNode[T, F]":
        u = self._left
        u._propagate()
        u._par = self._par
        self._left = u._right
        if u._right:
            u._right._par = self
        u._right = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        self._update()
        u._update()
        return u

    def __rotate_left(self) -> "_WBTListNode[T, F]":
        u = self._right
        u._propagate()
        u._par = self._par
        self._right = u._left
        if u._left:
            u._left._par = self
        u._left = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        self._update()
        u._update()
        return u

    def _balance_left(self) -> "_WBTListNode[T, F]":
        self._right._propagate()
        if (
            self._right._weight_left()
            >= self._right._weight_right() * _WBTNodeBase.GAMMA
        ):
            self._right = self._right.__rotate_right()
        return self.__rotate_left()

    def _balance_right(self) -> "_WBTListNode[T, F]":
        self._left._propagate()
        if self._left._weight_right() >= self._left._weight_left() * _WBTNodeBase.GAMMA:
            self._left = self._left.__rotate_left()
        return self.__rotate_right()


class WBTList(Generic[T, F]):
    # insert / pop / pop_max

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

    def __build(self, a):

        def build(l: int, r: int, pnode: Optional[_WBTListNode] = None) -> _WBTListNode:
            if l == r:
                return None
            mid = (l + r) // 2
            node = _WBTListNode(self, a[mid], self._id)
            node._left = build(l, mid, node)
            node._right = build(mid + 1, r, node)
            node._par = pnode
            node._update()
            return node

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
        # if s:
        #     s._par = None
        # if t:
        #     t._par = None
        return s, t

    def split(self, k: int) -> tuple["WBTList", "WBTList"]:
        lnode, rnode = self._split_node(self._root, k)
        l, r = (
            WBTList(self._op, self._mapping, self._composition, self._e, self._id),
            WBTList(self._op, self._mapping, self._composition, self._e, self._id),
        )
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

    def extend(self, other: "WBTList[T, F]") -> None:
        self._root = self._merge_node(self._root, other._root)

    def insert(self, k: int, key) -> None:
        s, t = self._split_node(self._root, k)
        self._root = self._merge_with_root(s, _WBTListNode(self, key, self._id), t)

    def pop(self, k: int):
        s, t = self._split_node(self._root, k + 1)
        s, tmp = self._pop_max(s)
        self._root = self._merge_node(s, t)
        return tmp._key

    def tolist(self) -> list:
        node = self._root
        stack: list[_WBTListNode] = []
        a = []
        while stack or node:
            if node:
                node._propagate()
                stack.append(node)
                node = node._left
            else:
                node = stack.pop()
                a.append(node._key)
                node = node._right
        return a

    def _check(self, verbose: bool = False) -> None:
        """作業用デバック関数
        size,key,balanceをチェックして、正しければ高さを表示する
        """
        if self._root is None:
            if verbose:
                debug("ok. 0 (empty)")
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

        _, h = dfs(self._root)
        if verbose:
            debug(f"ok. {h}")

    def prod(self, l: int, r: int) -> T:
        def dfs(node: _WBTListNode, left: int, right: int) -> T:
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


def debug(*args):
    pass


import sys
import os
import io


class FastO:
    """標準出力高速化ライブラリです。"""

    _output = io.StringIO()

    @classmethod
    def write(cls, *args, sep: str = " ", end: str = "\n", flush: bool = False) -> None:
        """標準出力します。次の ``FastO.flush()`` が起きると print します。"""
        wr = cls._output.write
        for i in range(len(args) - 1):
            wr(str(args[i]))
            wr(sep)
        if args:
            wr(str(args[-1]))
        wr(end)
        if flush:
            cls.flush()

    @classmethod
    def flush(cls) -> None:
        """``flush`` します。これを実行しないと ``write`` した内容が表示されないので忘れないでください。"""
        os.write(1, cls._output.getvalue().encode())
        cls._output.close()


write, flush = FastO.write, FastO.flush
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


def dynamic_sequence():
    input = lambda: sys.stdin.buffer.readline().rstrip()
    n, q = map(int, input().split())
    A = list(map(int, input().split()))
    V = [a << 30 | 1 for a in A]

    s = WBTList(op, mapping, composition, e, id, V)

    for i in range(q):
        com, *qu = map(int, input().split())
        if com == 0:
            i, x = qu
            s.insert(i, x << 30 | 1)
        elif com == 1:
            i = qu[0]
            s.pop(i)
        elif com == 2:
            l, r = qu
            s.reverse(l, r)
        elif com == 3:
            l, r, b, c = qu
            s.apply(l, r, (b << 30) | c)
        else:
            l, r = qu
            write(s.prod(l, r) >> 30)
    flush()


def LR_insertion():
    input = lambda: sys.stdin.readline().rstrip()
    n = int(input())
    s = input()
    wbt = WBTList(op, mapping, composition, e, id, [0])
    indx = 0
    for i, c in enumerate(s, 1):
        if c == "L":
            wbt.insert(indx, i)
        else:
            indx += 1
            wbt.insert(indx, i)
    write(" ".join(map(str, wbt.tolist())))
    flush()


dynamic_sequence()
# LR_insertion()
