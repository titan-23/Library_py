# from titan_pylib.data_structures.union_find.undoable_union_find import UndoableUnionFind
from collections import defaultdict


class UndoableUnionFind:

    def __init__(self, n: int) -> None:
        """``n`` 個の要素からなる ``UndoableUnionFind`` を構築します。
        :math:`O(n)` です。
        """
        self._n: int = n
        self._parents: list[int] = [-1] * n
        self._group_count: int = n
        self._history: list[tuple[int, int]] = []

    def root(self, x: int) -> int:
        """要素 ``x`` を含む集合の代表元を返します。
        :math:`O(\\log{n})` です。
        """
        while self._parents[x] >= 0:
            x = self._parents[x]
        return x

    def unite(self, x: int, y: int) -> bool:
        """要素 ``x`` を含む集合と要素 ``y`` を含む集合を併合します。
        :math:`O(\\log{n})` です。

        Returns:
          bool: もともと同じ集合であれば ``False``、そうでなければ ``True`` を返します。
        """
        x = self.root(x)
        y = self.root(y)
        if x == y:
            self._history.append((-1, -1))
            return False
        if self._parents[x] > self._parents[y]:
            x, y = y, x
        self._group_count -= 1
        self._history.append((x, self._parents[x]))
        self._history.append((y, self._parents[y]))
        self._parents[x] += self._parents[y]
        self._parents[y] = x
        return True

    def undo(self) -> None:
        """直前の ``unite`` クエリを戻します。
        :math:`O(\\log{n})` です。
        """
        assert (
            self._history
        ), f"Error: {self.__class__.__name__}.undo() with non history."
        y, py = self._history.pop()
        if y == -1:
            return
        self._group_count += 1
        x, px = self._history.pop()
        self._parents[y] = py
        self._parents[x] = px

    def size(self, x: int) -> int:
        """要素 ``x`` を含む集合の要素数を返します。
        :math:`O(\\log{n})` です。
        """
        return -self._parents[self.root(x)]

    def same(self, x: int, y: int) -> bool:
        """
        要素 ``x`` と ``y`` が同じ集合に属するなら ``True`` を、
        そうでないなら ``False`` を返します。
        :math:`O(\\log{n})` です。
        """
        return self.root(x) == self.root(y)

    def all_roots(self) -> list[int]:
        """全ての集合の代表元からなるリストを返します。
        :math:`O(n)` です。

        Returns:
            list[int]: 昇順であることが保証されます。
        """
        return [i for i, x in enumerate(self._parents) if x < 0]

    def all_group_members(self) -> defaultdict:
        """
        `key` に代表元、 `value` に `key` を代表元とする集合のリストをもつ `defaultdict` を返します。
        :math:`O(n\\log{n})` です。
        """
        group_members = defaultdict(list)
        for member in range(self._n):
            group_members[self.root(member)].append(member)
        return group_members

    def group_count(self) -> int:
        """集合の総数を返します。
        :math:`O(1)` です。
        """
        return self._group_count

    def clear(self) -> None:
        """集合の連結状態をなくします(初期状態に戻します)。
        :math:`O(n)` です。
        """
        for i in range(self._n):
            self._parents[i] = -1

    def __str__(self) -> str:
        """よしなにします。

        :math:`O(n\\log{n})` です。
        """
        return (
            f"<{self.__class__.__name__}> [\n"
            + "\n".join(f"  {k}: {v}" for k, v in self.all_group_members().items())
            + "\n]"
        )
