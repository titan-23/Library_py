# from titan_pylib.graph.hld.hld_lazy_segment_tree import HLDLazySegmentTree
# from titan_pylib.data_structures.segment_tree.lazy_segment_tree import LazySegmentTree
from typing import Union, Callable, List, TypeVar, Generic, Iterable

T = TypeVar("T")
F = TypeVar("F")


class LazySegmentTree(Generic[T, F]):
    """遅延セグ木です。"""

    def __init__(
        self,
        n_or_a: Union[int, Iterable[T]],
        op: Callable[[T, T], T],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id: F,
    ) -> None:
        self.op: Callable[[T, T], T] = op
        self.mapping: Callable[[F, T], T] = mapping
        self.composition: Callable[[F, F], F] = composition
        self.e: T = e
        self.id: F = id
        if isinstance(n_or_a, int):
            self.n = n_or_a
            self.log = (self.n - 1).bit_length()
            self.size = 1 << self.log
            self.data = [e] * (self.size << 1)
        else:
            a = list(n_or_a)
            self.n = len(a)
            self.log = (self.n - 1).bit_length()
            self.size = 1 << self.log
            data = [e] * (self.size << 1)
            data[self.size : self.size + self.n] = a
            for i in range(self.size - 1, 0, -1):
                data[i] = op(data[i << 1], data[i << 1 | 1])
            self.data = data
        self.lazy = [id] * self.size

    def _update(self, k: int) -> None:
        self.data[k] = self.op(self.data[k << 1], self.data[k << 1 | 1])

    def _all_apply(self, k: int, f: F) -> None:
        self.data[k] = self.mapping(f, self.data[k])
        if k >= self.size:
            return
        self.lazy[k] = self.composition(f, self.lazy[k])

    def _propagate(self, k: int) -> None:
        if self.lazy[k] == self.id:
            return
        self._all_apply(k << 1, self.lazy[k])
        self._all_apply(k << 1 | 1, self.lazy[k])
        self.lazy[k] = self.id

    def apply_point(self, k: int, f: F) -> None:
        k += self.size
        for i in range(self.log, 0, -1):
            self._propagate(k >> i)
        self.data[k] = self.mapping(f, self.data[k])
        for i in range(1, self.log + 1):
            self._update(k >> i)

    def _upper_propagate(self, l: int, r: int) -> None:
        for i in range(self.log, 0, -1):
            if l >> i << i != l:
                self._propagate(l >> i)
            if (r >> i << i != r) and (l >> i != (r - 1) >> i or l >> i << i == l):
                self._propagate((r - 1) >> i)

    def apply(self, l: int, r: int, f: F) -> None:
        assert (
            0 <= l <= r <= self.n
        ), f"IndexError: {self.__class__.__name__}.apply({l}, {r}, {f}), n={self.n}"
        if l == r:
            return
        if f == self.id:
            return
        l += self.size
        r += self.size
        self._upper_propagate(l, r)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._all_apply(l, f)
                l += 1
            if r & 1:
                self._all_apply(r ^ 1, f)
            l >>= 1
            r >>= 1
        ll, rr = l2, r2 - 1
        for i in range(1, self.log + 1):
            ll >>= 1
            rr >>= 1
            if ll << i != l2:
                self._update(ll)
            if (ll << i == l2 or ll != rr) and (r2 >> i << i != r2):
                self._update(rr)

    def all_apply(self, f: F) -> None:
        self.lazy[1] = self.composition(f, self.lazy[1])

    def prod(self, l: int, r: int) -> T:
        assert (
            0 <= l <= r <= self.n
        ), f"IndexError: {self.__class__.__name__}.prod({l}, {r}), n={self.n}"
        if l == r:
            return self.e
        l += self.size
        r += self.size
        self._upper_propagate(l, r)
        lres = self.e
        rres = self.e
        while l < r:
            if l & 1:
                lres = self.op(lres, self.data[l])
                l += 1
            if r & 1:
                rres = self.op(self.data[r ^ 1], rres)
            l >>= 1
            r >>= 1
        return self.op(lres, rres)

    def all_prod(self) -> T:
        return self.data[1]

    def all_propagate(self) -> None:
        for i in range(self.size):
            self._propagate(i)

    def tolist(self) -> List[T]:
        self.all_propagate()
        return self.data[self.size : self.size + self.n]

    def max_right(self, l, f) -> int:
        assert 0 <= l <= self.n
        assert f(self.e)
        if l == self.size:
            return self.n
        l += self.size
        for i in range(self.log, 0, -1):
            self._propagate(l >> i)
        s = self.e
        while True:
            while l & 1 == 0:
                l >>= 1
            if not f(self.op(s, self.data[l])):
                while l < self.size:
                    self._propagate(l)
                    l <<= 1
                    if f(self.op(s, self.data[l])):
                        s = self.op(s, self.data[l])
                        l |= 1
                return l - self.size
            s = self.op(s, self.data[l])
            l += 1
            if l & -l == l:
                break
        return self.n

    def min_left(self, r: int, f) -> int:
        assert 0 <= r <= self.n
        assert f(self.e)
        if r == 0:
            return 0
        r += self.size
        for i in range(self.log, 0, -1):
            self._propagate((r - 1) >> i)
        s = self.e
        while True:
            r -= 1
            while r > 1 and r & 1:
                r >>= 1
            if not f(self.op(self.data[r], s)):
                while r < self.size:
                    self._propagate(r)
                    r = r << 1 | 1
                    if f(self.op(self.data[r], s)):
                        s = self.op(self.data[r], s)
                        r ^= 1
                return r + 1 - self.size
            s = self.op(self.data[r], s)
            if r & -r == r:
                break
        return 0

    def __getitem__(self, k: int) -> T:
        assert (
            -self.n <= k < self.n
        ), f"IndexError: {self.__class__.__name__}[{k}], n={self.n}"
        if k < 0:
            k += self.n
        k += self.size
        for i in range(self.log, 0, -1):
            self._propagate(k >> i)
        return self.data[k]

    def __setitem__(self, k: int, v: T):
        assert (
            -self.n <= k < self.n
        ), f"IndexError: {self.__class__.__name__}[{k}] = {v}, n={self.n}"
        if k < 0:
            k += self.n
        k += self.size
        for i in range(self.log, 0, -1):
            self._propagate(k >> i)
        self.data[k] = v
        for i in range(1, self.log + 1):
            self._update(k >> i)

    def __str__(self) -> str:
        return str(self.tolist())

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
# from titan_pylib.graph.hld.hld import HLD
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
        self.rseg: LazySegmentTree[T, F] = LazySegmentTree(a[::-1], op, e)
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
            u = par[head[u]]
        if dep[u] < dep[v]:
            u, v = v, u
        self.seg.apply(nodein[v], nodein[u] + 1, f)

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
