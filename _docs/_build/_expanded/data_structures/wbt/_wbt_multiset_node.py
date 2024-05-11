# from titan_pylib.data_structures.wbt._wbt_multiset_node import _WBTMultisetNode
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
from typing import TypeVar, Optional

T = TypeVar("T")


class _WBTMultisetNode(_WBTNodeBase[T]):

    __slots__ = "_key", "_count", "_count_size", "_size", "_par", "_left", "_right"

    def __init__(self, key: T, count: int) -> None:
        super().__init__()
        self._key: T = key
        self._count: int = count
        self._count_size: int = count
        self._par: Optional[_WBTMultisetNode[T]]
        self._left: Optional[_WBTMultisetNode[T]]
        self._right: Optional[_WBTMultisetNode[T]]

    @property
    def key(self) -> T:
        return self._key

    @property
    def count(self) -> T:
        return self._count

    def _update(self) -> None:
        super()._update()
        self._count_size = (
            self._count
            + (self._left._count_size if self._left else 0)
            + (self._right._count_size if self._right else 0)
        )

    def _rotate_right(self) -> "_WBTMultisetNode[T]":
        u = self._left
        u._size = self._size
        u._count_size = self._count_size
        self._size -= u._left._size + 1 if u._left else 1
        self._count_size -= u._left._count_size + u._count if u._left else u._count
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

    def _rotate_left(self) -> "_WBTMultisetNode[T]":
        u = self._right
        u._size = self._size
        u._count_size = self._count_size
        self._size -= u._right._size + 1 if u._right else 1
        self._count_size -= u._right._count_size + u._count if u._right else u._count
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

    def _copy_from(self, other: "_WBTMultisetNode[T]") -> None:
        super()._copy_from(other)
        self._count = other._count
        self._count_size = other._count_size
