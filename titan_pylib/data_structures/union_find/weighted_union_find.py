from typing import Optional
from collections import defaultdict


class WeightedUnionFind:

    def __init__(self, n: int):
        self._n: int = n
        self._group_numbers: int = n
        self._parents: list[int] = [-1] * n
        self._weight: list[int] = [0] * n

    def root(self, x: int) -> int:
        path = [x]
        while self._parents[x] >= 0:
            x = self._parents[x]
            path.append(x)
        a = path.pop()
        while path:
            x = path.pop()
            self._weight[x] += self._weight[self._parents[x]]
            self._parents[x] = a
        return a

    def unite(self, x: int, y: int, w: int) -> Optional[int]:
        """Untie x and y, weight[y] = weight[x] + w. / O(α(N))"""
        rx = self.root(x)
        ry = self.root(y)
        if rx == ry:
            return rx if self.diff(x, y) == w else None
        w += self._weight[x] - self._weight[y]
        self._group_numbers -= 1
        if self._parents[rx] > self._parents[ry]:
            rx, ry = ry, rx
            w = -w
        self._parents[rx] += self._parents[ry]
        self._parents[ry] = rx
        self._weight[ry] = w
        return rx

    def size(self, x: int) -> int:
        return -self._parents[self.root(x)]

    def same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)

    def members(self, x: int) -> list[int]:
        x = self.root(x)
        return [i for i in range(self._n) if self.root(i) == x]

    def all_roots(self) -> list[int]:
        return [i for i, x in enumerate(self._parents) if x < 0]

    def group_count(self) -> int:
        return self._group_numbers

    def all_group_members(self) -> defaultdict:
        group_members = defaultdict(list)
        for member in range(self._n):
            group_members[self.root(member)].append(member)
        return group_members

    def clear(self) -> None:
        self._group_numbers = self._n
        for i in range(self._n):
            # self._G[i].clear()
            self._parents[i] = -1

    def diff(self, x: int, y: int) -> Optional[int]:
        """weight[y] - weight[x]"""
        if not self.same(x, y):
            return None
        return self._weight[y] - self._weight[x]

    def __str__(self) -> str:
        return (
            "<WeightedUnionFind> [\n"
            + "\n".join(f"  {k}: {v}" for k, v in self.all_group_members().items())
            + "\n]"
        )
