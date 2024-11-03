from titan_pylib.data_structures.segment_tree.lazy_segment_tree import LazySegmentTree
from titan_pylib.graph.hld.hld import HLD
from typing import Union, Iterable, Callable, TypeVar, Generic

T = TypeVar("T")
F = TypeVar("F")


class HLDLazySegmentTree(Generic[T, F]):
    """遅延セグ木搭載HLDです。

    Note:
        **非可換に対応してます。**
    """

    def __init__(
        self,
        hld: HLD,
        n_or_a: Union[int, Iterable[T]],
        op: Callable[[T, T], T],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id: F,
    ) -> None:
        self.hld: HLD = hld
        a = (
            [e] * n_or_a
            if isinstance(n_or_a, int)
            else self.hld.build_list(list(n_or_a))
        )
        self.seg: LazySegmentTree[T, F] = LazySegmentTree(
            a, op, mapping, composition, e, id
        )
        self.rseg: LazySegmentTree[T, F] = LazySegmentTree(
            a[::-1], op, mapping, composition, e, id
        )
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

    def path_apply(self, u: int, v: int, f: F) -> None:
        """頂点 ``u`` から頂点 ``v`` へのパスに作用させます。
        :math:`O(\\log^2{n})` です。

        Args:
            u (int): パスの **始点** です。
            v (int): パスの **終点** です。
            f (F): 作用素です。
        """
        head, nodein, dep, par = (
            self.hld.head,
            self.hld.nodein,
            self.hld.dep,
            self.hld.par,
        )
        while head[u] != head[v]:
            if dep[head[u]] < dep[head[v]]:
                u, v = v, u
            self.seg.apply(nodein[head[u]], nodein[u] + 1, f)
            self.rseg.apply(
                self.hld.n - (nodein[u] + 1 - 1) - 1,
                self.hld.n - nodein[head[u]] - 1 + 1,
                f,
            )
            u = par[head[u]]
        if dep[u] < dep[v]:
            u, v = v, u
        self.seg.apply(nodein[v], nodein[u] + 1, f)
        self.rseg.apply(
            self.hld.n - (nodein[u] + 1 - 1) - 1, self.hld.n - nodein[v] - 1 + 1, f
        )

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
        """部分木の集約値を返します。
        :math:`O(\\log{n})` です。

        Args:
            v (int): 根とする頂点です。

        Returns:
            T: 求める集約値です。
        """
        return self.seg.prod(self.hld.nodein[v], self.hld.nodeout[v])

    def subtree_apply(self, v: int, f: F) -> None:
        """部分木に作用させます。
        :math:`O(\\log{n})` です。

        Args:
            v (int): 根とする頂点です。
            f (F): 作用素です。
        """
        self.seg.apply(self.hld.nodein[v], self.hld.nodeout[v], f)
        self.rseg.apply(
            self.hld.n - self.hld.nodeout[v] - 1 - 1,
            self.hld.n - self.hld.nodein[v] - 1 + 1,
            f,
        )
