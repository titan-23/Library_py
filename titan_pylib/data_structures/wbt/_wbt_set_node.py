from titan_pylib.data_structures.wbt._wbt_node_base import _WBTNodeBase
from typing import TypeVar, Optional

T = TypeVar("T")


class _WBTSetNode(_WBTNodeBase[T]):

    __slots__ = "_key", "_size", "_par", "_left", "_right"

    def __init__(self, key: T) -> None:
        super().__init__()
        self._key: T = key
        self._par: Optional[_WBTSetNode[T]]
        self._left: Optional[_WBTSetNode[T]]
        self._right: Optional[_WBTSetNode[T]]

    @property
    def key(self) -> T:
        return self._key
