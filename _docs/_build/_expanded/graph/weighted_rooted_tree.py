# from titan_pylib.graph.weighted_rooted_tree import WeightedRootedTree
class WeightedRootedTree:

    def __init__(
        self,
        _G: list[list[tuple[int, int]]],
        _root: int,
        cp: bool = False,
        lca: bool = False,
    ):
        self._n = len(_G)
        self._G = _G
        self._root = _root
        self._height = -1
        self._toposo = []
        self._dist = []
        self._descendant_num = []
        self._child = []
        self._child_num = []
        self._parents = []
        self._diameter = (-1, -1, -1)
        self._bipartite_graph = []
        self._cp = cp
        self._lca = lca
        self._rank = []
        K = 1
        while 1 << K < self._n:
            K += 1
        self._K = K
        self._doubling = [[-1] * self._n for _ in range(self._K)]
        self._calc_dist_toposo()
        if cp:
            self._calc_child_parents()
        if lca:
            self._calc_doubling()

    def __str__(self):
        self._calc_child_parents()
        ret = ["<WeightedRootedTree> ["]
        ret.extend(
            [
                f"  dist:{str(d).zfill(2)} - v:{str(i).zfill(2)} - p:{str(self._parents[i]).zfill(2)} - child:{sorted(self._child[i])}"
                for i, d in sorted(enumerate(self._dist), key=lambda x: x[1])
            ]
        )
        ret.append("]")
        return "\n".join(ret)

    def _calc_dist_toposo(self) -> None:
        """Calc dist and toposo. / O(N)"""
        # initメソッドで直接実行
        _G, _root = self._G, self._root
        _dist = [-1] * self._n
        _rank = [-1] * self._n
        _dist[_root] = 0
        _rank[_root] = 0
        _toposo = []
        _toposo.append(_root)
        todo = [_root]
        while todo:
            v = todo.pop()
            d = _dist[v]
            r = _rank[v]
            for x, c in _G[v]:
                if _dist[x] != -1:
                    continue
                _dist[x] = d + c
                _rank[x] = r + 1
                todo.append(x)
                _toposo.append(x)
        self._dist = _dist
        self._rank = _rank
        self._toposo = _toposo

    def _calc_child_parents(self) -> None:
        """Calc child and parents. / O(N)"""
        if self._child and self._child_num and self._parents:
            return
        _G, _rank = self._G, self._rank
        _child_num = [0] * self._n
        _child = [[] for _ in range(self._n)]
        _parents = [-1] * self._n
        for v in self._toposo[::-1]:
            for x, _ in _G[v]:
                if _rank[x] < _rank[v]:
                    _parents[v] = x
                    continue
                _child[v].append(x)
                _child_num[v] += 1
        self._child_num = _child_num
        self._child = _child
        self._parents = _parents

    def get_dists(self) -> list[int]:
        """Return dist from root. / O(N)"""
        return self._dist

    def get_toposo(self) -> list[int]:
        """Return toposo. / O(N)"""
        return self._toposo

    def get_height(self) -> int:
        """Return height. / O(N)"""
        if self._height > -1:
            return self._height
        self._height = max(self._dist)
        return self._height

    def get_descendant_num(self) -> list[int]:
        """Return descendant_num. / O(N)"""
        if self._descendant_num:
            return self._descendant_num
        _G, _dist = self._G, self._dist
        _descendant_num = [1] * self._n
        for v in self._toposo[::-1]:
            for x, _ in _G[v]:
                if _dist[x] < _dist[v]:
                    continue
                _descendant_num[v] += _descendant_num[x]
        for i in range(self._n):
            _descendant_num[i] -= 1
        self._descendant_num = _descendant_num
        return self._descendant_num

    def get_child(self) -> list[list[int]]:
        """Return child / O(N)"""
        if self._child:
            return self._child
        self._calc_child_parents()
        return self._child

    def get_child_num(self) -> list[int]:
        """Return child_num. / O(N)"""
        if self._child_num:
            return self._child_num
        self._calc_child_parents()
        return self._child_num

    def get_parents(self) -> list[int]:
        """Return parents. / O(N)"""
        if self._parents:
            return self._parents
        self._calc_child_parents()
        return self._parents

    def get_diameter(self) -> tuple[int, int, int]:
        """Return diameter of tree. (diameter, start, stop) / O(N)"""
        if self._diameter[0] > -1:
            return self._diameter
        s = self._dist.index(self.get_height())
        todo = [s]
        ndist = [-1] * self._n
        ndist[s] = 0
        while todo:
            v = todo.pop()
            d = ndist[v]
            for x, c in self._G[v]:
                if ndist[x] != -1:
                    continue
                ndist[x] = d + c
                todo.append(x)
        diameter = max(ndist)
        t = ndist.index(diameter)
        self._diameter = (diameter, s, t)
        return self._diameter

    def get_bipartite_graph(self) -> list[int]:
        """Return [1 if root else 0]. / O(N)"""
        if self._bipartite_graph:
            return self._bipartite_graph
        self._bipartite_graph = [-1] * self._n
        _bipartite_graph = self._bipartite_graph
        _bipartite_graph[self._root] = 1
        todo = [self._root]
        while todo:
            v = todo.pop()
            nc = 0 if _bipartite_graph[v] else 1
            for x, _ in self._G[v]:
                if _bipartite_graph[x] != -1:
                    continue
                _bipartite_graph[x] = nc
                todo.append(x)
        return _bipartite_graph

    def _calc_doubling(self) -> None:
        "Calc doubling if self._lca. / O(NlogN)"
        if not self._parents:
            self._calc_child_parents()
        for i in range(self._n):
            self._doubling[0][i] = self._parents[i]
        for k in range(self._K - 1):
            for v in range(self._n):
                if self._doubling[k][v] < 0:
                    self._doubling[k + 1][v] = -1
                else:
                    self._doubling[k + 1][v] = self._doubling[k][self._doubling[k][v]]

    def get_lca(self, u: int, v: int) -> int:
        """Return LCA of (u, v). / O(logN)"""
        assert self._lca, f"{self.__class__.__name__}.get_lca(), `lca` must be True"
        _doubling, _rank = self._doubling, self._rank
        if _rank[u] < _rank[v]:
            u, v = v, u
        _r = _rank[u] - _rank[v]
        for k in range(self._K):
            if _r >> k & 1:
                u = _doubling[k][u]
        if u == v:
            return u
        for k in range(self._K - 1, -1, -1):
            if _doubling[k][u] != _doubling[k][v]:
                u = _doubling[k][u]
                v = _doubling[k][v]
        return _doubling[0][u]

    def get_dist(self, u: int, v: int) -> int:
        """Return dist(u - v). / O(logN)"""
        return self._dist[u] + self._dist[v] - 2 * self._dist[self.get_lca(u, v)]

    def is_on_path(self, u: int, v: int, a: int) -> bool:
        """Return True if (a is on path(u - v)) else False. / O(logN)"""
        raise NotImplementedError
        return self.get_dist(u, a) + self.get_dist(a, v) == self.get_dist(
            u, v
        )  # rank??

    def get_path(self, u: int, v: int) -> list[int]:
        """Return path (u -> v). / O(logN + |path|)"""
        assert self._lca, f"{self.__class__.__name__}, `lca` must be True"
        if u == v:
            return [u]
        self.get_parents()

        def get_path_lca(u: int, v: int) -> list[int]:
            path = []
            while u != v:
                u = self._parents[u]
                if u == v:
                    break
                path.append(u)
            return path

        lca = self.get_lca(u, v)
        path = [u]
        path.extend(get_path_lca(u, lca))
        if u != lca and v != lca:
            path.append(lca)
        path.extend(get_path_lca(v, lca)[::-1])
        path.append(v)
        return path

    def dfs_in_out(self) -> tuple[list[int], list[int]]:
        curtime = -1
        todo = [~self._root, self._root]
        intime = [-1] * self._n
        outtime = [-1] * self._n
        seen = [False] * self._n
        seen[self._root] = True
        while todo:
            curtime += 1
            v = todo.pop()
            if v >= 0:
                intime[v] = curtime
                for x, _ in self._G[v]:
                    if not seen[x]:
                        todo.append(~x)
                        todo.append(x)
                        seen[x] = True
            else:
                outtime[~v] = curtime
        return intime, outtime
