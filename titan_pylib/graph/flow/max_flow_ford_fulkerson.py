import sys


class MaxFlowFordFulkerson:

    def __init__(self, n: int):
        self.n: int = n
        self.m: int = 0
        self.G: list[list[list[int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, w: int) -> None:
        assert (
            0 <= u < self.n
        ), f"Indexerror: {self.__class__.__name__}.add_edge({u}, {v})"
        assert (
            0 <= v < self.n
        ), f"Indexerror: {self.__class__.__name__}.add_edge({u}, {v})"
        G_u = len(self.G[u])
        G_v = len(self.G[v])
        self.G[u].append([v, w, G_v])
        self.G[v].append([u, 0, G_u])
        self.m += 2

    def _dfs(self, v: int, g: int, f: int, used: list[int]) -> int:
        if v == g:
            return f
        used[v] = 1
        for i, (x, w, l) in enumerate(self.G[v]):
            if used[x]:
                continue
            if w == 0:
                continue
            fv = self._dfs(x, g, min(f, w), used)
            if fv > 0:
                self.G[v][i][1] -= fv
                self.G[x][l][1] += fv
                return fv
        return 0

    def max_flow(self, s: int, g: int, INF: int = 10**18) -> int:
        """:math:`O(F|E|)"""
        assert (
            0 <= s < self.n
        ), f"Indexerror: {self.__class__.__class__}.max_flow(), {s=}"
        assert (
            0 <= g < self.n
        ), f"Indexerror: {self.__class__.__class__}.max_flow(), {g=}"
        lim_rec = sys.getrecursionlimit()
        if lim_rec < self.m:
            sys.setrecursionlimit(self.m + 1)
        ans = 0
        while True:
            used = [0] * self.n
            f = self._dfs(s, g, INF, used)
            if f == 0:
                break
            ans += f
        return ans
