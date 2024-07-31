from titan_pylib.graph.flow.max_flow_dinic import MaxFlowDinic


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
