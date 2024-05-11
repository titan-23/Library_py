from array import array
from typing import Generic, List, TypeVar, Callable, Iterable, Union
from titan_pylib.data_structures.dynamic_connectivity.link_cut_tree import LinkCutTree

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
