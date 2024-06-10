# from titan_pylib.graph.perfect_binary_tree import PerfectBinaryTree
class PerfectBinaryTree:
    """1-indexedの完全二分木クラス"""

    def __init__(self) -> None:
        pass

    def par(self, u: int) -> int:
        """親を返す"""
        return (u >> 1) if u > 1 else -1

    def child_left(self, u: int) -> int:
        """左の子を返す"""
        return u << 1

    def child_right(self, u: int) -> int:
        """右の子を返す"""
        return u << 1 | 1

    def children(self, u: int) -> tuple[int, int]:
        """左右の子をタプルで返す"""
        return (self.child_left(u), self.child_right(u))

    def sibling(self, u: int) -> int:
        """兄弟を返す"""
        return u ^ 1

    def dep(self, u: int) -> int:
        """深さを返す / :math:`O(1)`"""
        return u.bit_length()

    def la(self, u: int, k: int) -> int:
        """``k``個上の祖先を返す
        k == 0 のとき、u自身を返す
        """
        return u >> k

    def lca(self, u: int, v: int) -> int:
        """lcaを返す"""
        if self.dep(u) > self.dep(v):
            u, v = v, u
        v = self.la(v, self.dep(v) - self.dep(u))
        return u >> (u ^ v).bit_length()
    
    def dist(self, u: int, v: int) -> int:
        """距離を返す"""
        return self.dep(u) + self.dep(v) - 2*self.dep(self.lca(u, v))

    def get_path(self, u: int, v: int) -> list[int]:
        """uからvへのパスをリストで返す"""
        def get(x):
            a = []
            while x != lca:
                a.append(x)
                x = self.par(x)
            return a

        lca = self.lca(u, v)
        return get(u) + [lca] + get(v)[::-1]
