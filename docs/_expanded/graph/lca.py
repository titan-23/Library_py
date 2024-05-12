# from titan_pylib.graph.lca import LCA
# from titan_pylib.data_structures.sparse_table.sparse_table_RmQ import SparseTableRmQ
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
from typing import Generic, TypeVar, Iterable

T = TypeVar("T", bound=SupportsLessThan)


class SparseTableRmQ(Generic[T]):
    """
    2項演算を :math:`\\min` にしたものです。
    """

    def __init__(self, a: Iterable[T], e: T):
        if not isinstance(a, list):
            a = list(a)
        self.size = len(a)
        log = self.size.bit_length() - 1
        data = [a] + [[]] * log
        for i in range(log):
            pre = data[i]
            l = 1 << i
            data[i + 1] = [
                pre[j] if pre[j] < pre[j + l] else pre[j + l]
                for j in range(len(pre) - l)
            ]
        self.data = data
        self.e = e

    def prod(self, l: int, r: int) -> T:
        assert 0 <= l <= r <= self.size
        if l == r:
            return self.e
        u = (r - l).bit_length() - 1
        return (
            self.data[u][l]
            if self.data[u][l] < self.data[u][r - (1 << u)]
            else self.data[u][r - (1 << u)]
        )

    def __getitem__(self, k: int) -> T:
        assert 0 <= k < self.size
        return self.data[0][k]

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.data[0])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data[0]}, {self.e})"


class LCA:
    """LCA を定数倍良く求めます。

    :math:`< O(NlogN), O(1) >`
    https://github.com/cheran-senthil/PyRival/blob/master/pyrival/graphs/lca.py
    """

    def __init__(self, G: list[list[int]], root: int) -> None:
        """根が ``root`` の重み無し隣接リスト ``G`` で表されるグラフに対して LCA を求めます。
        時間・空間 :math:`O(n\\log{n})` です。

        Args:
          G (list[list[int]]): 隣接リストです。
          root (int): 根です。
        """
        _n = len(G)
        path = [-1] * _n
        nodein = [-1] * _n
        par = [-1] * _n
        curtime = -1
        stack = [root]
        while stack:
            v = stack.pop()
            path[curtime] = par[v]
            curtime += 1
            nodein[v] = curtime
            for x in G[v]:
                if nodein[x] != -1:
                    continue
                par[x] = v
                stack.append(x)
        self._n = _n
        self._path = path
        self._nodein = nodein
        self._st: SparseTableRmQ[int] = SparseTableRmQ((nodein[v] for v in path), e=_n)

    def lca(self, u: int, v: int) -> int:
        """頂点 ``u`` と頂点 ``v`` の LCA を返します。
        :math:`O(1)` です。
        """
        if u == v:
            return u
        l, r = self._nodein[u], self._nodein[v]
        if l > r:
            l, r = r, l
        return self._path[self._st.prod(l, r)]

    def lca_mul(self, a: list[int]) -> int:
        """頂点集合 ``a`` の LCA を返します。"""
        if all(a[i] == a[i + 1] for i in range(len(a) - 1)):
            return a[0]
        l = self._n + 1
        r = -l
        for e in a:
            e = self._nodein[e]
            if l > e:
                l = e
            if r < e:
                r = e
        return self._path[self._st.prod(l, r)]
