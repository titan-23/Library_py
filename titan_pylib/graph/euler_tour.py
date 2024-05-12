from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
from titan_pylib.data_structures.segment_tree.segment_tree_RmQ import SegmentTreeRmQ


class EulerTour:

    def __init__(
        self, G: list[list[tuple[int, int]]], root: int, vertexcost: list[int] = []
    ) -> None:
        n = len(G)
        if not vertexcost:
            vertexcost = [0] * n

        path = [0] * (2 * n)
        vcost1 = [0] * (2 * n)  # for vertex subtree
        vcost2 = [0] * (2 * n)  # for vertex path
        ecost1 = [0] * (2 * n)  # for edge subtree
        ecost2 = [0] * (2 * n)  # for edge path
        nodein = [0] * n
        nodeout = [0] * n
        depth = [-1] * n

        curtime = -1
        depth[root] = 0
        stack: list[tuple[int, int]] = [(~root, 0), (root, 0)]
        while stack:
            curtime += 1
            v, ec = stack.pop()
            if v >= 0:
                nodein[v] = curtime
                path[curtime] = v
                ecost1[curtime] = ec
                ecost2[curtime] = ec
                vcost1[curtime] = vertexcost[v]
                vcost2[curtime] = vertexcost[v]
                if len(G[v]) == 1:
                    nodeout[v] = curtime + 1
                for x, c in G[v]:
                    if depth[x] != -1:
                        continue
                    depth[x] = depth[v] + 1
                    stack.append((~v, c))
                    stack.append((x, c))
            else:
                v = ~v
                path[curtime] = v
                ecost1[curtime] = 0
                ecost2[curtime] = -ec
                vcost1[curtime] = 0
                vcost2[curtime] = -vertexcost[v]
                nodeout[v] = curtime

        # ---------------------- #

        self._n = n
        self._depth = depth
        self._nodein = nodein
        self._nodeout = nodeout
        self._vertexcost = vertexcost
        self._path = path

        self._vcost_subtree = FenwickTree(vcost1)
        self._vcost_path = FenwickTree(vcost2)
        self._ecost_subtree = FenwickTree(ecost1)
        self._ecost_path = FenwickTree(ecost2)

        bit = len(path).bit_length()
        self.msk = (1 << bit) - 1
        a: list[int] = [(depth[v] << bit) + i for i, v in enumerate(path)]
        self._st: SegmentTreeRmQ[int] = SegmentTreeRmQ(a, e=max(a))

    def lca(self, u: int, v: int) -> int:
        if u == v:
            return u
        l = min(self._nodein[u], self._nodein[v])
        r = max(self._nodeout[u], self._nodeout[v])
        ind = self._st.prod(l, r) & self.msk
        return self._path[ind]

    def lca_mul(self, a: list[int]) -> int:
        l, r = self._n + 1, -self._n - 1
        for e in a:
            l = min(l, self._nodein[e])
            r = max(r, self._nodeout[e])
        ind = self._st.prod(l, r) & self.msk
        return self._path[ind]

    def subtree_vcost(self, v: int) -> int:
        l = self._nodein[v]
        r = self._nodeout[v]
        return self._vcost_subtree.prod(l, r)

    def subtree_ecost(self, v: int) -> int:
        l = self._nodein[v]
        r = self._nodeout[v]
        return self._ecost_subtree.prod(l + 1, r)

    def _path_vcost(self, v: int) -> int:
        """頂点 v を含む"""
        return self._vcost_path.pref(self._nodein[v] + 1)

    def _path_ecost(self, v: int) -> int:
        """根から頂点 v までの辺"""
        return self._ecost_path.pref(self._nodein[v] + 1)

    def path_vcost(self, u: int, v: int) -> int:
        a = self.lca(u, v)
        return (
            self._path_vcost(u)
            + self._path_vcost(v)
            - 2 * self._path_vcost(a)
            + self._vertexcost[a]
        )

    def path_ecost(self, u: int, v: int) -> int:
        return (
            self._path_ecost(u)
            + self._path_ecost(v)
            - 2 * self._path_ecost(self.lca(u, v))
        )

    def add_vertex(self, v: int, w: int) -> None:
        """Add w to vertex x. / O(logN)"""
        l = self._nodein[v]
        r = self._nodeout[v]
        self._vcost_subtree.add(l, w)
        self._vcost_path.add(l, w)
        self._vcost_path.add(r, -w)
        self._vertexcost[v] += w

    def set_vertex(self, v: int, w: int) -> None:
        """Set w to vertex v. / O(logN)"""
        self.add_vertex(v, w - self._vertexcost[v])

    def add_edge(self, u: int, v: int, w: int) -> None:
        """Add w to edge([u - v]). / O(logN)"""
        if self._depth[u] < self._depth[v]:
            u, v = v, u
        l = self._nodein[u]
        r = self._nodeout[u]
        self._ecost_subtree.add(l, w)
        self._ecost_subtree.add(r + 1, -w)
        self._ecost_path.add(l, w)
        self._ecost_path.add(r + 1, -w)

    def set_edge(self, u: int, v: int, w: int) -> None:
        """Set w to edge([u - v]). / O(logN)"""
        self.add_edge(u, v, w - self.path_ecost(u, v))
