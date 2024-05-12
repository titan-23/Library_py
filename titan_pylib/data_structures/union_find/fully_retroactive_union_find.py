from titan_pylib.data_structures.dynamic_connectivity.link_cut_tree import LinkCutTree


class FullyRetroactiveUnionFind:

    def __init__(self, n: int, m: int) -> None:
        """頂点数 ``n`` 、クエリ列の長さ ``m`` の ``FullyRetroactiveUnionFind`` を作ります。

        ここで、クエリは `unite` のみです。

        :math:`O(n+m)` です。

        Args:
          n (int): 頂点数です。
          m (int): クエリ列の長さです。
        """
        m += 1
        self.n: int = n
        self.edge: list[tuple[int, int, int]] = [()] * m
        self.node_pool: set[int] = set(range(n, n + m))
        self.lct: LinkCutTree[int, None] = LinkCutTree(
            n + m,
            op=lambda s, t: s if s > t else t,
            mapping=lambda f, s: -1,
            composition=lambda f, g: None,
            e=-1,
            id=None,
        )

    def unite(self, u: int, v: int, t: int) -> None:
        """時刻 ``t`` のクエリを ``unite(u, v)`` にします。

        償却 :math:`O(\\log{(n+m)})` です。

        Args:
          u (int): 集合の要素です。
          v (int): 集合の要素です。
          t (int): 時刻です。

        Note:
          ``disconnect`` を使用する場合、 ``u``, ``v`` が連結されていてはいけません。
        """
        node = self.node_pool.pop()
        self.edge[t] = (u, v, node)
        self.lct[node] = t
        self.lct.merge(u, node)
        self.lct.merge(node, v)

    def disconnect(self, t: int) -> None:
        """時刻 ``t`` の連結クエリをなくして、そのクエリの2頂点を非連結にします。

        償却 :math:`O(\\log{(n+m)})` です。

        Args:
          t (int): 時刻です。

        Note:
          時刻 ``t`` のクエリは連結クエリでないといけません。
        """
        assert self.edge[t] is not None
        u, v, node = self.edge[t]
        self.node_pool.add(node)
        self.edge[t] = None
        self.lct.split(u, node)
        self.lct.split(node, v)

    def same(self, u: int, v: int, t: int) -> bool:
        """時刻 ``t`` で ``u``, ``v`` の連結判定をします。

        償却 :math:`O(\\log{(n+m)})` です。

        Args:
          u (int): 集合の要素です。
          v (int): 集合の要素です。
          t (int): 時刻です。

        Returns:
          bool:
        """
        if not self.lct.same(u, v):
            return False
        return self.lct.path_prod(u, v) <= t
