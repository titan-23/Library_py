# from titan_pylib.graph.flow.bipartite_max_matching import BipartiteMaxMatching
# from titan_pylib.graph.flow.max_flow_dinic import MaxFlowDinic
from collections import deque
# from titan_pylib.others.antirec import antirec
from types import GeneratorType

# ref: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
# ref: https://twitter.com/onakasuita_py/status/1731535542305907041


def antirec(func):
    stack = []

    def wrappedfunc(*args, **kwargs):
        if stack:
            return func(*args, **kwargs)
        to = func(*args, **kwargs)
        while True:
            if isinstance(to, GeneratorType):
                stack.append(to)
                to = next(to)
            else:
                stack.pop()
                if not stack:
                    break
                to = stack[-1].send(to)
        return to

    return wrappedfunc


def antirec_cache(func):
    stack = []
    memo = {}
    args_list = []

    def wrappedfunc(*args):
        args_list.append(args)
        if stack:
            return func(*args)
        to = func(*args)
        while True:
            if args_list[-1] in memo:
                res = memo[args_list.pop()]
                if not stack:
                    return res
                to = stack[-1].send(res)
                continue
            if isinstance(to, GeneratorType):
                stack.append(to)
                to = next(to)
            else:
                memo[args_list.pop()] = to
                stack.pop()
                if not stack:
                    break
                to = stack[-1].send(to)
        return to

    return wrappedfunc


class MaxFlowDinic:
    """mf.G[v]:= [x, cap, ind, flow]"""

    def __init__(self, n: int):
        self.n: int = n
        self.G: list[list[list[int]]] = [[] for _ in range(n)]
        self.level = [-1] * n

    def add_edge(self, u: int, v: int, w: int) -> None:
        assert (
            0 <= u < self.n
        ), f"Indexerror: {self.__class__.__name__}.add_edge({u}, {v})"
        assert (
            0 <= v < self.n
        ), f"Indexerror: {self.__class__.__name__}.add_edge({u}, {v})"
        G_u = len(self.G[u])
        G_v = len(self.G[v])
        self.G[u].append([v, w, G_v, 0])
        self.G[v].append([u, 0, G_u, 0])

    def _bfs(self, s: int) -> None:
        level = self.level
        for i in range(len(level)):
            level[i] = -1
        dq = deque([s])
        level[s] = 0
        while dq:
            v = dq.popleft()
            for x, w, _, _ in self.G[v]:
                if w > 0 and level[x] == -1:
                    level[x] = level[v] + 1
                    dq.append(x)
        self.level = level

    @antirec
    def _dfs(self, v: int, g: int, f: int):
        if v == g:
            yield f
        else:
            for i in range(self.it[v], len(self.G[v])):
                self.it[v] += 1
                x, w, rev, _ = self.G[v][i]
                if w > 0 and self.level[v] < self.level[x]:
                    fv = yield self._dfs(x, g, min(f, w))
                    if fv > 0:
                        self.G[v][i][3] += f
                        self.G[x][rev][3] -= f
                        self.G[v][i][1] -= fv
                        self.G[x][rev][1] += fv
                        yield fv
                        break
            else:
                yield 0

    def max_flow(self, s: int, g: int, INF: int = 10**18) -> int:
        """:math:`O(V^2 E)`"""
        assert (
            0 <= s < self.n
        ), f"Indexerror: {self.__class__.__class__}.max_flow(), {s=}"
        assert (
            0 <= g < self.n
        ), f"Indexerror: {self.__class__.__class__}.max_flow(), {g=}"
        ans = 0
        while True:
            self._bfs(s)
            if self.level[g] < 0:
                break
            self.it = [0] * self.n
            while True:
                f = self._dfs(s, g, INF)
                if f == 0:
                    break
                ans += f
        return ans


class BipartiteMaxMatching:

    def __init__(self, n: int, m: int) -> None:
        """二部グラフの最大マッチングを求めるグラフを初期化します。

        Args:
            n (int): 左側の頂点数です。
            m (int): 右側の頂点数です。
        """
        self.n = n
        self.m = m
        self.s = n + m
        self.t = n + m + 1
        self.mf = MaxFlowDinic(n + m + 2)
        for i in range(n):
            self.mf.add_edge(self.s, i, 1)
        for i in range(m):
            self.mf.add_edge(n + i, self.t, 1)

    def add_edge(self, l: int, r: int) -> None:
        """左側の頂点 ``l`` と右側の頂点 ``r`` に辺を貼ります。

        Args:
            l (int):
            r (int):
        """
        assert 0 <= l < self.n
        assert 0 <= r < self.m
        self.mf.add_edge(l, self.n + r, 1)

    def max_matching(self) -> tuple[int, list[tuple[int, int]]]:
        """最大マッチングを求め、マッチングの個数と使用する辺を返します。
        :math:`O(E \sqrt{V})` です。

        Returns:
            tuple[int, list[tuple[int, int]]]:
        """
        ans = self.mf.max_flow(self.s, self.t)
        K = []
        for a in range(self.n):
            for b, _, _, f in self.mf.G[a]:
                if self.n <= b < self.n + self.t and f > 0:
                    K.append((a, b - self.n))
        return ans, K
