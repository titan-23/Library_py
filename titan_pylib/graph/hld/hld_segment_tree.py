from titan_pylib.data_structures.segment_tree.segment_tree import SegmentTree
from titan_pylib.graph.hld.hld import HLD
from typing import Union, Iterable, Callable, TypeVar, Generic

T = TypeVar("T")


class HLDSegmentTree(Generic[T]):
    """セグ木搭載HLDです。

    Note:
        **非可換に対応していません。**
    """

    def __init__(
        self, hld: HLD, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T
    ) -> None:
        self.hld: HLD = hld
        n_or_a = (
            n_or_a if isinstance(n_or_a, int) else self.hld.build_list(list(n_or_a))
        )
        self.seg: SegmentTree[T] = SegmentTree(n_or_a, op, e)
        self.op: Callable[[T, T], T] = op
        self.e: T = e

    def path_prod(self, u: int, v: int) -> T:
        """頂点 ``u`` から頂点 ``v`` へのパスの集約値を返します。
        :math:`O(\\log^2{n})` です。

        Note:
            **非可換に対応していません。**

        Args:
            u (int): パスの端点です。
            v (int): パスの端点です。

        Returns:
            T: 求める集約値です。
        """
        head, nodein, dep, par = (
            self.hld.head,
            self.hld.nodein,
            self.hld.dep,
            self.hld.par,
        )
        res = self.e
        while head[u] != head[v]:
            if dep[head[u]] < dep[head[v]]:
                u, v = v, u
            res = self.op(res, self.seg.prod(nodein[head[u]], nodein[u] + 1))
            u = par[head[u]]
        if dep[u] < dep[v]:
            u, v = v, u
        return self.op(res, self.seg.prod(nodein[v], nodein[u] + 1))

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

    __getitem__ = get
    __setitem__ = set

    def subtree_prod(self, v: int) -> T:
        """部分木の集約値を返します。
        :math:`O(\\log{n})` です。

        Args:
            v (int): 根とする頂点です。

        Returns:
            T: 求める集約値です。
        """
        return self.seg.prod(self.hld.nodein[v], self.hld.nodeout[v])
