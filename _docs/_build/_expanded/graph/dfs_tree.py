# 展開に失敗しました
from titan_pylib.others.antirec import antirec


class DFSTree:

    def __init__(self, G: list[list[int]]) -> None:
        self.n = len(G)
        self.G = G
        self.order = [-1] * self.n
        self.low = [self.n] * self.n
        self.par = [-1] * self.n
        self.dfs_forest = [[] for _ in range(self.n)]
        self._calc_lowlink()

    def _calc_lowlink(self) -> None:
        t = 0
        order, low, par, dfs_forest = self.order, self.low, self.par, self.dfs_forest
        G = self.G

        @antirec
        def dfs(v: int, p: int = -1):
            nonlocal t
            par[v] = p
            order[v] = t
            low[v] = t
            t += 1
            seen_p = False
            for x in G[v]:
                if x == p and not seen_p:
                    seen_p = True
                    continue
                if order[x] == -1:
                    dfs_forest[v].append(x)
                    dfs_forest[x].append(v)
                    yield dfs(x, v)
                    low[v] = min(low[v], low[x])
                else:
                    low[v] = min(low[v], order[x])
            yield

        for v in range(self.n):
            if order[v] == -1:
                dfs(v)

    def get_bridge(self) -> list[tuple[int, int]]:
        order, low, par, dfs_forest = self.order, self.low, self.par, self.dfs_forest
        bridge = []
        for v in range(self.n):
            if par[v] != -1:
                continue
            todo = [v]
            while todo:
                v = todo.pop()
                for x in dfs_forest[v]:
                    if x == par[v]:
                        continue
                    if order[v] < low[x]:
                        bridge.append((min(v, x), max(v, x)))
                    todo.append(x)
        return bridge

    def get_two_edge_connected_components(self):
        """二辺連結成分分解"""
        order, low, par, dfs_forest = self.order, self.low, self.par, self.dfs_forest
        ids = [-1] * self.n
        E = []
        idx = 0
        for v in range(self.n):
            if par[v] != -1:
                continue
            ids[v] = idx
            todo = [v]
            while todo:
                v = todo.pop()
                for x in dfs_forest[v]:
                    if x == par[v]:
                        continue
                    if order[v] < low[x]:
                        idx += 1
                        ids[x] = idx
                        E.append((ids[v], idx))
                    else:
                        ids[x] = ids[v]
                    todo.append(x)
            idx += 1
        gropus = [[] for _ in range(idx)]
        F = [[] for _ in range(idx)]
        for v in range(self.n):
            gropus[ids[v]].append(v)
        for u, v in E:
            F[u].append(v)
            F[v].append(u)
        return ids, gropus, F
