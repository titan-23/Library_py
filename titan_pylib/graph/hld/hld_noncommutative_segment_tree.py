from titan_pylib.data_structures.segment_tree.segment_tree import SegmentTree
from titan_pylib.graph.hld.hld import HLD
from typing import Union, Iterable, Callable, TypeVar, Generic

T = TypeVar("T")


class HLDNoncommutativeSegmentTree(Generic[T]):
    """セグ木搭載HLDです。

    Note:
        **非可換に対応してます。**
    """

    def __init__(
        self, hld: HLD, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T
    ):
        self.hld: HLD = hld
        a = (
            [e] * n_or_a
            if isinstance(n_or_a, int)
            else self.hld.build_list(list(n_or_a))
        )
        self.seg: SegmentTree[T] = SegmentTree(a, op, e)
        self.rseg: SegmentTree[T] = SegmentTree(a[::-1], op, e)
        self.op: Callable[[T, T], T] = op
        self.e: T = e

    def path_prod(self, u: int, v: int) -> T:
        """頂点 ``u`` から頂点 ``v`` へのパスの集約値を返します。
        :math:`O(\\log^2{n})` です。

        Args:
            u (int): パスの **始点** です。
            v (int): パスの **終点** です。

        Returns:
            T: 求める集約値です。
        """
        head, nodein, dep, par, n = (
            self.hld.head,
            self.hld.nodein,
            self.hld.dep,
            self.hld.par,
            self.hld.n,
        )
        lres, rres = self.e, self.e
        seg, rseg = self.seg, self.rseg
        while head[u] != head[v]:
            if dep[head[u]] > dep[head[v]]:
                lres = self.op(lres, rseg.prod(n - nodein[u] - 1, n - nodein[head[u]]))
                u = par[head[u]]
            else:
                rres = self.op(seg.prod(nodein[head[v]], nodein[v] + 1), rres)
                v = par[head[v]]
        if dep[u] > dep[v]:
            lres = self.op(lres, rseg.prod(n - nodein[u] - 1, n - nodein[v]))
        else:
            lres = self.op(lres, seg.prod(nodein[u], nodein[v] + 1))
        return self.op(lres, rres)

    def get(self, k: int) -> T:
        """頂点の値を返します。
        :math:`O(\\log{n})` です。

        Args:
            k (int): 頂点のインデックスです。

        Returns:
            T: 頂点の値です。
        """
        return self.seg[self.hld.nodein[k]]

    def set(self, k: int, v: T) -> None:
        """頂点の値を更新します。
        :math:`O(\\log{n})` です。

        Args:
            k (int): 頂点のインデックスです。
            v (T): 更新する値です。
        """
        self.seg[self.hld.nodein[k]] = v
        self.rseg[self.hld.n - self.hld.nodein[k] - 1] = v

    __getitem__ = get
    __setitem__ = set

    def subtree_prod(self, v: int) -> T:
        return self.seg.prod(self.hld.nodein[v], self.hld.nodeout[v])
