from titan_pylib.data_structures.array.persistent_array import PersistentArray
from typing import Optional


class PersistentUnionFind:

    def __init__(self, n: int, _parents: Optional[PersistentArray[int]] = None) -> None:
        """``n`` 個の要素からなる ``PersistentUnionFind`` を構築します。
        :math:`O(n)` です。
        """
        self._n: int = n
        self._parents: PersistentArray[int] = (
            PersistentArray([-1] * n) if _parents is None else _parents
        )

    def _new(self, _parents: PersistentArray[int]) -> "PersistentUnionFind":
        return PersistentUnionFind(self._n, _parents)

    def copy(self) -> "PersistentUnionFind":
        """コピーします。
        :math:`O(1)` です。
        """
        return self._new(self._parents.copy())

    def root(self, x: int) -> int:
        """要素 ``x`` を含む集合の代表元を返します。
        :math:`O(\\log^2{n})` です。
        """
        _parents = self._parents
        while True:
            p = _parents.get(x)
            if p < 0:
                return x
            x = p

    def unite(self, x: int, y: int, update: bool = True) -> "PersistentUnionFind":
        """要素 ``x`` を含む集合と要素 ``y`` を含む集合を併合します。
        :math:`O(\\log^2{n})` です。

        Args:
          x (int): 集合の要素です。
          y (int): 集合の要素です。
          update (bool, optional): 併合後を新しいインスタンスにするなら ``True`` です。

        Returns:
          PersistentUnionFind: 併合後の uf です。
        """
        x = self.root(x)
        y = self.root(y)
        res_parents = self._parents.copy() if update else self._parents
        if x == y:
            return self._new(res_parents)
        px, py = res_parents.get(x), res_parents.get(y)
        if px > py:
            x, y = y, x
        res_parents = res_parents.set(x, px + py)
        res_parents = res_parents.set(y, x)
        return self._new(res_parents)

    def size(self, x: int) -> int:
        """要素 ``x`` を含む集合の要素数を返します。
        :math:`O(\\log^2{n})` です。
        """
        return -self._parents.get(self.root(x))

    def same(self, x: int, y: int) -> bool:
        """
        要素 ``x`` と ``y`` が同じ集合に属するなら ``True`` を、
        そうでないなら ``False`` を返します。
        :math:`O(\\log^2{n})` です。
        """
        return self.root(x) == self.root(y)
