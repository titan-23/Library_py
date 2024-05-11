from titan_pylib.data_structures.wb_tree.wbt_node_base import _WBTNodeBase
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
