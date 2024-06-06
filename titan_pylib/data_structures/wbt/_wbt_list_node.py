from titan_pylib.data_structures.wbt._wbt_node_base import _WBTNodeBase
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
