# from titan_pylib.data_structures.wbt.wbt_list import WBTList
# from titan_pylib.data_structures.wbt._wbt_list_node import _WBTListNode
# from titan_pylib.data_structures.wbt._wbt_node_base import _WBTNodeBase
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

    def _rebalance(self) -> "_WBTNodeBase[T]":
        """根までを再構築する

        Returns:
            _WBTNodeBase[T]: 根ノード
        """
        node = self
        while True:
            node._update()
            wl, wr = node._weight_left(), node._weight_right()
            if wl * _WBTNodeBase.DELTA < wr:
                if (
                    node._right._weight_left()
                    >= node._right._weight_right() * _WBTNodeBase.GAMMA
                ):
                    node._right = node._right._rotate_right()
                node = node._rotate_left()
            elif wr * _WBTNodeBase.DELTA < wl:
                if (
                    node._left._weight_right()
                    >= node._left._weight_left() * _WBTNodeBase.GAMMA
                ):
                    node._left = node._left._rotate_left()
                node = node._rotate_right()
            if not node._par:
                return node
            node = node._par

    def _copy_from(self, other: "_WBTNodeBase[T]") -> None:
        self._size = other._size
        if other._left:
            other._left._par = self
        if other._right:
            other._right._par = self
        if other._par:
            if other._par._left is other:
                other._par._left = self
            else:
                other._par._right = self
        self._par = other._par
        self._left = other._left
        self._right = other._right

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

    def _min(self) -> "_WBTNodeBase[T]":
        node = self
        while node._left:
            node = node._left
        return node

    def _max(self) -> "_WBTNodeBase[T]":
        node = self
        while node._right:
            node = node._right
        return node

    def _next(self) -> Optional["_WBTNodeBase[T]"]:
        if self._right:
            return self._right._min()
        now, pre = self, None
        while now and now._right is pre:
            now, pre = now._par, now
        return now

    def _prev(self) -> Optional["_WBTNodeBase[T]"]:
        if self._left:
            return self._left._max()
        now, pre = self, None
        while now and now._left is pre:
            now, pre = now._par, now
        return now

    def __add__(self, other: int) -> Optional["_WBTNodeBase[T]"]:
        node = self
        for _ in range(other):
            node = node._next()
        return node

    def __sub__(self, other: int) -> Optional["_WBTNodeBase[T]"]:
        node = self
        for _ in range(other):
            node = node._prev()
        return node

    __iadd__ = __add__
    __isub__ = __sub__

    def __str__(self) -> str:
        # if self._left is None and self._right is None:
        #     return f"key:{self._key, self._size}\n"
        # return f"key:{self._key, self._size},\n _left:{self._left},\n _right:{self._right}\n"
        return str(self._key)

    __repr__ = __str__
from typing import Generic, TypeVar, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from titan_pylib.data_structures.wbt.wbt_list import WBTList

T = TypeVar("T")


class _WBTListNode(_WBTNodeBase, Generic[T]):

    __slots__ = (
        "_left",
        "_right",
        "_par",
        "_tree",
        "_key",
        "_rev",
    )

    def __init__(self, tree: "WBTList[T]", key: T) -> None:
        super().__init__()
        self._tree: WBTList[T] = tree
        self._key: T = key
        self._rev: int = 0
        self._left: "_WBTListNode[T]"
        self._right: "_WBTListNode[T]"
        self._par: "_WBTListNode[T]"

    def __str__(self) -> str:
        if self._left is None and self._right is None:
            return f"key:{self._key, self._size}\n"
        return f"key:{self._key, self._size},\n _left:{self._left},\n _right:{self._right}\n"

    def _check(self):
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

    def propagate_above(self) -> None:
        """これの上について、revをすべて伝播する"""
        stack: list["_WBTListNode[T]"] = []
        node = self
        while node:
            stack.append(node)
            node = node._par
        while stack:
            node = stack.pop()
            node._propagate()

    def update_above(self) -> None:
        """これの上について、updateする

        Note:
            これの上はすべて revを伝播済み
        """
        node = self
        while node:
            node._update()
            node = node._par

    def _update(self) -> None:
        self._size = 1
        if self._left:
            self._size += self._left._size
        if self._right:
            self._size += self._right._size

    def _apply_rev(self) -> None:
        self._rev ^= 1

    def _propagate(self) -> None:
        if self._rev:
            self._left, self._right = self._right, self._left
            if self._left:
                self._left._apply_rev()
            if self._right:
                self._right._apply_rev()
            self._rev = 0

    def _rotate_right(self) -> "_WBTListNode[T]":
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

    def _rotate_left(self) -> "_WBTListNode[T]":
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

    def _balance_left(self) -> "_WBTListNode[T]":
        self._right._propagate()
        if self._right._weight_left() >= self._right._weight_right() * self.GAMMA:
            self._right = self._right._rotate_right()
        return self._rotate_left()

    def _balance_right(self) -> "_WBTListNode[T]":
        self._left._propagate()
        if self._left._weight_right() >= self._left._weight_left() * self.GAMMA:
            self._left = self._left._rotate_left()
        return self._rotate_right()

    def _min(self) -> "_WBTListNode[T]":
        self.propagate_above()
        assert self._rev == 0
        node = self
        while node._left:
            node = node._left
            node._propagate()
        return node

    def _max(self) -> "_WBTListNode[T]":
        self.propagate_above()
        assert self._rev == 0
        node = self
        while node._right:
            node = node._right
            node._propagate()
        return node

    def _next(self) -> Optional["_WBTListNode[T]"]:
        self.propagate_above()
        if self._right:
            return self._right._min()
        now, pre = self, None
        while now and now._right is pre:
            now, pre = now._par, now
        return now

    def _prev(self) -> Optional["_WBTListNode[T]"]:
        self.propagate_above()
        if self._left:
            return self._left._max()
        now, pre = self, None
        while now and now._left is pre:
            now, pre = now._par, now
        return now
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
