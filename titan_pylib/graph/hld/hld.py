from typing import Any, Iterator, List, Tuple


class HLD:

    def __init__(self, G: List[List[int]], root: int):
        """``root`` を根とする木 ``G`` を HLD します。
        :math:`O(n)` です。

        Args:
          G (List[List[int]]): 木を表す隣接リストです。
          root (int): 根です。
        """
        n = len(G)
        self.n: int = n
        self.G: List[List[int]] = G
        self.size: List[int] = [1] * n
        self.par: List[int] = [-1] * n
        self.dep: List[int] = [-1] * n
        self.nodein: List[int] = [0] * n
        self.nodeout: List[int] = [0] * n
        self.head: List[int] = [0] * n
        self.hld: List[int] = [0] * n
        self._dfs(root)

    def _dfs(self, root: int) -> None:
        dep, par, size, G = self.dep, self.par, self.size, self.G
        dep[root] = 0
        stack = [root]
        while stack:
            v = stack.pop()
            if v >= 0:
                dep_nxt = dep[v] + 1
                for x in G[v]:
                    if dep[x] != -1:
                        continue
                    dep[x] = dep_nxt
                    stack.append(~x)
                    stack.append(x)
            else:
                v = ~v
                G_v, dep_v = G[v], dep[v]
                for i, x in enumerate(G_v):
                    if dep[x] < dep_v:
                        par[v] = x
                        continue
                    size[v] += size[x]
                    if size[x] > size[G_v[0]]:
                        G_v[0], G_v[i] = G_v[i], G_v[0]

        head, nodein, nodeout, hld = self.head, self.nodein, self.nodeout, self.hld
        curtime = 0
        stack = [~root, root]
        while stack:
            v = stack.pop()
            if v >= 0:
                if par[v] == -1:
                    head[v] = v
                nodein[v] = curtime
                hld[curtime] = v
                curtime += 1
                if not G[v]:
                    continue
                G_v0 = G[v][0]
                for x in reversed(G[v]):
                    if x == par[v]:
                        continue
                    head[x] = head[v] if x == G_v0 else x
                    stack.append(~x)
                    stack.append(x)
            else:
                nodeout[~v] = curtime

    def build_list(self, a: List[Any]) -> List[Any]:
        """``hld配列`` を基にインデックスを振りなおします。非破壊的です。
        :math:`O(n)` です。

        Args:
          a (List[Any]): 元の配列です。

        Returns:
          List[Any]: 振りなおし後の配列です。
        """
        return [a[e] for e in self.hld]

    def for_each_vertex_path(self, u: int, v: int) -> Iterator[Tuple[int, int]]:
        """``u-v`` パスに対応する区間のインデックスを返します。
        :math:`O(\\log{n})` です。
        """
        head, nodein, dep, par = self.head, self.nodein, self.dep, self.par
        while head[u] != head[v]:
            if dep[head[u]] < dep[head[v]]:
                u, v = v, u
            yield nodein[head[u]], nodein[u] + 1
            u = par[head[u]]
        if dep[u] < dep[v]:
            u, v = v, u
        yield nodein[v], nodein[u] + 1

    def for_each_vertex_subtree(self, v: int) -> Iterator[Tuple[int, int]]:
        """頂点 ``v`` の部分木に対応する区間のインデックスを返します。
        :math:`O(1)` です。
        """
        yield self.nodein[v], self.nodeout[v]

    def path_kth_elm(self, s: int, t: int, k: int) -> int:
        """``s`` から ``t`` に向かって ``k`` 個進んだ頂点のインデックスを返します。
        存在しないときは ``-1`` を返します。
        :math:`O(\\log{n})` です。
        """
        head, dep, par = self.head, self.dep, self.par
        lca = self.lca(s, t)
        d = dep[s] + dep[t] - 2 * dep[lca]
        if d < k:
            return -1
        if dep[s] - dep[lca] < k:
            s = t
            k = d - k
        hs = head[s]
        while dep[s] - dep[hs] < k:
            k -= dep[s] - dep[hs] + 1
            s = par[hs]
            hs = head[s]
        return self.hld[self.nodein[s] - k]

    def lca(self, u: int, v: int) -> int:
        """``u``, ``v`` の LCA を返します。
        :math:`O(\\log{n})` です。
        """
        nodein, head, par = self.nodein, self.head, self.par
        while True:
            if nodein[u] > nodein[v]:
                u, v = v, u
            if head[u] == head[v]:
                return u
            v = par[head[v]]
