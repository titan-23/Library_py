# from titan_pylib.data_structures.dynamic_connectivity.lazy_link_cut_tree import LazyLinkCutTree
from array import array
from typing import Generic, List, TypeVar, Callable, Iterable, Union
# from titan_pylib.data_structures.dynamic_connectivity.link_cut_tree import LinkCutTree
from array import array


class LinkCutTree:
    """LinkCutTree です。"""

    # - link / cut / merge / split
    # - root / same
    # - lca / path_length / path_kth_elm
    # など

    def __init__(self, n: int) -> None:
        self.n = n
        self.arr: array[int] = array("I", [self.n, self.n, self.n, 0] * (self.n + 1))
        # node.left  : arr[node<<2|0]
        # node.right : arr[node<<2|1]
        # node.par   : arr[node<<2|2]
        # node.rev   : arr[node<<2|3]
        self.size: array[int] = array("I", [1] * (self.n + 1))
        self.size[-1] = 0
        self.group_cnt = self.n

    def _is_root(self, node: int) -> bool:
        return (self.arr[node << 2 | 2] == self.n) or not (
            self.arr[self.arr[node << 2 | 2] << 2] == node
            or self.arr[self.arr[node << 2 | 2] << 2 | 1] == node
        )

    def _propagate(self, node: int) -> None:
        if node == self.n:
            return
        arr = self.arr
        if arr[node << 2 | 3]:
            arr[node << 2 | 3] = 0
            ln, rn = arr[node << 2], arr[node << 2 | 1]
            arr[node << 2] = rn
            arr[node << 2 | 1] = ln
            arr[ln << 2 | 3] ^= 1
            arr[rn << 2 | 3] ^= 1

    def _update(self, node: int) -> None:
        if node == self.n:
            return
        ln, rn = self.arr[node << 2], self.arr[node << 2 | 1]
        self._propagate(ln)
        self._propagate(rn)
        self.size[node] = 1 + self.size[ln] + self.size[rn]

    def _update_triple(self, x: int, y: int, z: int) -> None:
        self._propagate(self.arr[x << 2])
        self._propagate(self.arr[x << 2 | 1])
        self._propagate(self.arr[y << 2])
        self._propagate(self.arr[y << 2 | 1])
        self.size[z] = self.size[x]
        self.size[x] = 1 + self.size[self.arr[x << 2]] + self.size[self.arr[x << 2 | 1]]
        self.size[y] = 1 + self.size[self.arr[y << 2]] + self.size[self.arr[y << 2 | 1]]

    def _update_double(self, x: int, y: int) -> None:
        self._propagate(self.arr[x << 2])
        self._propagate(self.arr[x << 2 | 1])
        self.size[y] = self.size[x]
        self.size[x] = 1 + self.size[self.arr[x << 2]] + self.size[self.arr[x << 2 | 1]]

    def _splay(self, node: int) -> None:
        # splayを抜けた後、nodeは遅延伝播済みにするようにする
        # (splay後のnodeのleft,rightにアクセスしやすいと非常にラクなはず)
        if node == self.n:
            return
        _propagate, _is_root, _update_triple = (
            self._propagate,
            self._is_root,
            self._update_triple,
        )
        _propagate(node)
        if _is_root(node):
            return
        arr = self.arr
        pnode = arr[node << 2 | 2]
        while not _is_root(pnode):
            gnode = arr[pnode << 2 | 2]
            _propagate(gnode)
            _propagate(pnode)
            _propagate(node)
            f = arr[pnode << 2] == node
            g = (arr[gnode << 2 | f] == pnode) ^ (arr[pnode << 2 | f] == node)
            nnode = (node if g else pnode) << 2 | f ^ g
            arr[pnode << 2 | f ^ 1] = arr[node << 2 | f]
            arr[gnode << 2 | f ^ g ^ 1] = arr[nnode]
            arr[node << 2 | f] = pnode
            arr[nnode] = gnode
            arr[node << 2 | 2] = arr[gnode << 2 | 2]
            arr[gnode << 2 | 2] = nnode >> 2
            arr[arr[pnode << 2 | f ^ 1] << 2 | 2] = pnode
            arr[arr[gnode << 2 | f ^ g ^ 1] << 2 | 2] = gnode
            arr[pnode << 2 | 2] = node
            _update_triple(gnode, pnode, node)
            pnode = arr[node << 2 | 2]
            if arr[pnode << 2] == gnode:
                arr[pnode << 2] = node
            elif arr[pnode << 2 | 1] == gnode:
                arr[pnode << 2 | 1] = node
            else:
                return
        _propagate(pnode)
        _propagate(node)
        f = arr[pnode << 2] == node
        arr[pnode << 2 | f ^ 1] = arr[node << 2 | f]
        arr[node << 2 | f] = pnode
        arr[arr[pnode << 2 | f ^ 1] << 2 | 2] = pnode
        arr[node << 2 | 2] = arr[pnode << 2 | 2]
        arr[pnode << 2 | 2] = node
        self._update_double(pnode, node)

    def expose(self, v: int) -> int:
        """``v`` が属する木において、その木を管理しているsplay木の根から ``v`` までのパスを作ります。
        償却 :math:`O(\\log{n})` です。
        """
        arr, n, _splay, _update = self.arr, self.n, self._splay, self._update
        pre = v
        while arr[v << 2 | 2] != n:
            _splay(v)
            arr[v << 2 | 1] = n
            _update(v)
            if arr[v << 2 | 2] == n:
                break
            pre = arr[v << 2 | 2]
            _splay(pre)
            arr[pre << 2 | 1] = v
            _update(pre)
        arr[v << 2 | 1] = n
        _update(v)
        return pre

    def lca(self, u: int, v: int, root: int) -> int:
        """``root`` を根としたときの、 ``u``, ``v`` の LCA を返します。
        償却 :math:`O(\\log{n})` です。
        """
        self.evert(root)
        self.expose(u)
        return self.expose(v)

    def link(self, c: int, p: int) -> None:
        """辺 ``(c -> p)`` を追加します。
        償却 :math:`O(\\log{n})` です。

        制約:
          ``c`` は元の木の根でなければならないです。
        """
        assert not self.same(c, p)
        self.expose(c)
        self.expose(p)
        self.arr[c << 2 | 2] = p
        self.arr[p << 2 | 1] = c
        self._update(p)
        self.group_cnt -= 1

    def cut(self, c: int) -> None:
        """辺 ``{c -> cの親}`` を削除します。
        償却 :math:`O(\\log{n})` です。

        制約:
          ``c`` は元の木の根であってはいけないです。
        """
        arr = self.arr
        self.expose(c)
        assert arr[c << 2] != self.n
        arr[arr[c << 2] << 2 | 2] = self.n
        arr[c << 2] = self.n
        self._update(c)
        self.group_cnt += 1

    def group_count(self) -> int:
        """連結成分数を返します。
        :math:`O(1)` です。
        """
        return self.group_cnt

    def root(self, v: int) -> int:
        """``v`` が属する木の根を返します。
        償却 :math:`O(\\log{n})` です。
        """
        self.expose(v)
        arr, n = self.arr, self.n
        while arr[v << 2] != n:
            v = arr[v << 2]
            self._propagate(v)
        self._splay(v)
        return v

    def same(self, u: int, v: int) -> bool:
        """連結判定です。
        償却 :math:`O(\\log{n})` です。

        Returns:
          bool: ``u``, ``v`` が同じ連結成分であれば ``True`` を、そうでなければ ``False`` を返します。
        """
        return self.root(u) == self.root(v)

    def evert(self, v: int) -> None:
        """``v`` を根にします。
        償却 :math:`O(\\log{n})` です。
        """
        self.expose(v)
        self.arr[v << 2 | 3] ^= 1
        self._propagate(v)

    def merge(self, u: int, v: int) -> bool:
        """``u``, ``v`` が同じ連結成分なら ``False`` を返します。
        そうでなければ辺 ``{u -> v}`` を追加して ``True`` を返します。
        償却 :math:`O(\\log{n})` です。
        """
        if self.same(u, v):
            return False
        self.evert(u)
        self.expose(v)
        self.arr[u << 2 | 2] = v
        self.arr[v << 2 | 1] = u
        self._update(v)
        self.group_cnt -= 1
        return True

    def split(self, u: int, v: int) -> bool:
        """辺 ``{u -> v}`` があれば削除し ``True`` を返します。
        そうでなければ何もせず ``False`` を返します。
        償却 :math:`O(\\log{n})` です。
        """
        self.evert(u)
        self.cut(v)
        return True

    def path_length(self, u: int, v: int) -> int:
        """``u`` から ``v`` へのパスに含まれる頂点の数を返します。
        存在しないときは ``-1`` を返します。
        償却 :math:`O(\\log{n})` です。
        """
        if not self.same(u, v):
            return -1
        self.evert(u)
        self.expose(v)
        return self.size[v]

    def path_kth_elm(self, s: int, t: int, k: int) -> int:
        """``u`` から ``v`` へ ``k`` 個進んだ頂点を返します。
        存在しないときは ``-1`` を返します。
        償却 :math:`O(\\log{n})` です。
        """
        self.evert(s)
        self.expose(t)
        if self.size[t] <= k:
            return -1
        size, arr = self.size, self.arr
        while True:
            self._propagate(t)
            s = size[arr[t << 2]]
            if s == k:
                self._splay(t)
                return t
            t = arr[t << 2 | (s < k)]
            if s < k:
                k -= s + 1

    def __str__(self):
        return f"{self.__class__.__name__}"

    __repr__ = __str__

T = TypeVar("T")
F = TypeVar("F")


class LazyLinkCutTree(LinkCutTree, Generic[T, F]):
    """LazyLinkCutTree です。"""

    # パスクエリ全部載せ
    # - link / cut / merge / split
    # - prod / apply / getitem / setitem
    # - root / same
    # - lca / path_length / path_kth_elm
    # など

    # opがいらないならupdateを即returnするように変更したり、
    # 可換opならupdateを短縮したりなど

    def __init__(
        self,
        n_or_a: Union[int, Iterable[T]],
        op: Callable[[T, T], T],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id: F,
    ) -> None:
        """
        各引数は遅延セグ木のアレです。よしなに。

        Args:
          op (Callable[[T, T], T]): 非可換でも構いません。
        """
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.e = e
        self.id = id
        self.key: List[T] = [e] * (n_or_a) if isinstance(n_or_a, int) else list(n_or_a)
        self.n = len(self.key)
        self.key.append(e)
        self.data: List[T] = [x for x in self.key for _ in range(2)]
        self.lazy: List[F] = [id] * (self.n + 1)
        self.arr: array[int] = array("I", [self.n, self.n, self.n, 0] * (self.n + 1))
        # node.left  : arr[node<<2|0]
        # node.right : arr[node<<2|1]
        # node.par   : arr[node<<2|2]
        # node.rev   : arr[node<<2|3]
        self.size: array[int] = array("I", [1] * (self.n + 1))
        self.size[-1] = 0
        self.group_cnt = self.n

    def _propagate_lazy(self, node: int, f: F) -> None:
        if node == self.n:
            return
        self.key[node] = self.mapping(f, self.key[node])
        self.data[node << 1] = self.mapping(f, self.data[node << 1])
        self.data[node << 1 | 1] = self.mapping(f, self.data[node << 1 | 1])
        self.lazy[node] = (
            f if self.lazy[node] == self.id else self.composition(f, self.lazy[node])
        )

    def _propagate(self, node: int) -> None:
        if node == self.n:
            return
        arr = self.arr
        if arr[node << 2 | 3]:
            self.data[node << 1], self.data[node << 1 | 1] = (
                self.data[node << 1 | 1],
                self.data[node << 1],
            )
            arr[node << 2 | 3] = 0
            ln, rn = arr[node << 2], arr[node << 2 | 1]
            arr[node << 2] = rn
            arr[node << 2 | 1] = ln
            arr[ln << 2 | 3] ^= 1
            arr[rn << 2 | 3] ^= 1
        if self.lazy[node] == self.id:
            return
        self._propagate_lazy(self.arr[node << 2], self.lazy[node])
        self._propagate_lazy(self.arr[node << 2 | 1], self.lazy[node])
        self.lazy[node] = self.id

    def _update(self, node: int) -> None:
        if node == self.n:
            return
        ln, rn = self.arr[node << 2], self.arr[node << 2 | 1]
        self._propagate(ln)
        self._propagate(rn)
        self.data[node << 1] = self.op(
            self.op(self.data[ln << 1], self.key[node]), self.data[rn << 1]
        )
        self.data[node << 1 | 1] = self.op(
            self.op(self.data[rn << 1 | 1], self.key[node]), self.data[ln << 1 | 1]
        )
        self.size[node] = 1 + self.size[ln] + self.size[rn]

    def _update_triple(self, x: int, y: int, z: int) -> None:
        data, key, arr, size = self.data, self.key, self.arr, self.size
        lx, rx = arr[x << 2], arr[x << 2 | 1]
        ly, ry = arr[y << 2], arr[y << 2 | 1]
        self._propagate(lx)
        self._propagate(rx)
        self._propagate(ly)
        self._propagate(ry)
        data[z << 1] = data[x << 1]
        data[x << 1] = self.op(self.op(data[lx << 1], key[x]), data[rx << 1])
        data[y << 1] = self.op(self.op(data[ly << 1], key[y]), data[ry << 1])
        data[z << 1 | 1] = data[x << 1 | 1]
        data[x << 1 | 1] = self.op(
            self.op(data[rx << 1 | 1], key[x]), data[lx << 1 | 1]
        )
        data[y << 1 | 1] = self.op(
            self.op(data[ry << 1 | 1], key[y]), data[ly << 1 | 1]
        )
        size[z] = size[x]
        size[x] = 1 + size[lx] + size[rx]
        size[y] = 1 + size[ly] + size[ry]

    def _update_double(self, x: int, y: int) -> None:
        data, key, arr, size = self.data, self.key, self.arr, self.size
        lx, rx = arr[x << 2], arr[x << 2 | 1]
        self._propagate(lx)
        self._propagate(rx)
        data[y << 1] = data[x << 1]
        data[x << 1] = self.op(self.op(data[lx << 1], key[x]), data[rx << 1])
        data[y << 1 | 1] = data[x << 1 | 1]
        data[x << 1 | 1] = self.op(
            self.op(data[rx << 1 | 1], key[x]), data[lx << 1 | 1]
        )
        size[y] = size[x]
        size[x] = 1 + size[lx] + size[rx]

    def path_prod(self, u: int, v: int) -> T:
        """``u`` から ``v`` へのパスの総積を返します。
        償却 :math:`O(\\log{n})` です。
        """
        self.evert(u)
        self.expose(v)
        return self.data[v << 1]

    def path_apply(self, u: int, v: int, f: F) -> None:
        """``u`` から ``v`` へのパスに ``f`` を作用させます。
        償却 :math:`O(\\log{n})` です。
        """
        self.evert(u)
        self.expose(v)
        self._propagate_lazy(v, f)

    def __setitem__(self, k: int, v: T):
        """頂点 ``k`` の値を ``v`` に更新します。
        償却 :math:`O(\\log{n})` です。
        """
        self._splay(k)
        self.key[k] = v
        self._update(k)

    def __getitem__(self, k: int) -> T:
        """頂点 ``k`` の値を返します。
        償却 :math:`O(\\log{n})` です。
        """
        self._splay(k)
        return self.key[k]

    def __str__(self):
        return str([self[i] for i in range(self.n)])

    __repr__ = __str__
