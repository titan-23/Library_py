from typing import Generic, TypeVar, Callable, Iterable, Optional, Union

T = TypeVar("T")
F = TypeVar("F")


class LinkCutTree(Generic[T, F]):

    class Node:

        def __init__(self, index: int, key: T, lazy: F) -> None:
            self.index: int = index
            self.key: T = key
            self.data: T = key
            self.rdata: T = key
            self.lazy: F = lazy
            self.par: Optional[LinkCutTree.Node] = None
            self.left: Optional[LinkCutTree.Node] = None
            self.right: Optional[LinkCutTree.Node] = None
            self.size: int = 1
            self.rev: int = 0

        def _is_root(self) -> bool:
            return (not self.par) or not (
                self.par.left is self or self.par.right is self
            )

        def __str__(self):
            if self.left is None and self.right is None:
                return f"(index,par,key,data):{self.index, (self.par.index if self.par else None), self.key, self.data, self._is_root()}, rev={self.rev}\n"
            return f"(index,par,key,data):{self.index, (self.par.index if self.par else None), self.key, self.data, self._is_root()}, rev={self.rev},\n left:{self.left},\n right:{self.right}\n"

    def __init__(
        self,
        n_or_a: Union[int, Iterable[T]],
        op: Callable[[T, T], T],
        mapping: Callable[[F, T], T],
        composition: Callable[[F, F], F],
        e: T,
        id: F,
    ) -> None:
        self.node = (
            [LinkCutTree.Node(i, e, id) for i in range(n_or_a)]
            if isinstance(n_or_a, int)
            else [LinkCutTree.Node(i, a, id) for i, a in enumerate(n_or_a)]
        )
        self.op = op
        self.mapping = mapping
        self.composition = composition
        self.e = e
        self.id = id
        self.n: int = len(self.node)
        self._group_count: int = self.n

    def _apply_rev(self, node: Optional[Node]) -> None:
        if not node:
            return
        node.rev ^= 1

    def _apply_f(self, node: Optional[Node], f: F) -> None:
        if not node:
            return
        node.key = self.mapping(f, node.key)
        node.data = self.mapping(f, node.data)
        node.rdata = self.mapping(f, node.rdata)
        node.lazy = f if node.lazy == self.id else self.composition(f, node.lazy)

    def _propagate(self, node: Optional[Node]) -> None:
        if not node:
            return
        if node.rev:
            node.data, node.rdata = node.rdata, node.data
            node.left, node.right = node.right, node.left
            self._apply_rev(node.left)
            self._apply_rev(node.right)
            node.rev = 0
        if node.lazy != self.id:
            self._apply_f(node.left, node.lazy)
            self._apply_f(node.right, node.lazy)
            node.lazy = self.id

    def _update(self, node: Optional[Node]) -> None:
        if not node:
            return
        self._propagate(node.left)
        self._propagate(node.right)
        node.data = node.key
        node.rdata = node.key
        node.size = 1
        if node.left:
            node.data = self.op(node.left.data, node.data)
            node.rdata = self.op(node.rdata, node.left.rdata)
            node.size += node.left.size
        if node.right:
            node.data = self.op(node.data, node.right.data)
            node.rdata = self.op(node.right.rdata, node.rdata)
            node.size += node.right.size

    def _rotate(self, node: Node) -> None:
        pnode = node.par
        gnode = pnode.par
        self._propagate(pnode)
        self._propagate(node)
        if gnode:
            if gnode.left is pnode:
                gnode.left = node
            elif gnode.right is pnode:
                gnode.right = node
        node.par = gnode
        if pnode.left is node:
            pnode.left = node.right
            if node.right:
                node.right.par = pnode
            node.right = pnode
        else:
            pnode.right = node.left
            if node.left:
                node.left.par = pnode
            node.left = pnode
        pnode.par = node
        self._update(pnode)
        self._update(node)

    def _splay(self, node: Node) -> None:
        while (not node._is_root()) and (not node.par._is_root()):
            self._rotate(
                node.par
                if (node.par.par.left is node.par) == (node.par.left is node)
                else node
            )
            self._rotate(node)
        if not node._is_root():
            self._rotate(node)
        self._propagate(node)  # splay を抜けた後は伝播済みにする

    def expose(self, v: int) -> int:
        node = self.node[v]
        pre = node
        while node.par:
            self._splay(node)
            node.right = None
            self._update(node)
            if not node.par:
                break
            pre = node.par
            self._splay(node.par)
            node.par.right = node
            self._update(node.par)
        node.right = None
        self._update(node)
        return pre

    def lca(self, u: int, v: int, root: int = -1) -> int:
        if root != -1:
            self.evert(root)
        self.expose(u)
        return self.expose(v)

    def link(self, c: int, p: int) -> None:
        self._group_count -= 1
        self.expose(c)
        self.expose(p)
        self.node[c].par = self.node[p]
        self.node[p].right = self.node[c]
        self._update(self.node[p])

    def cut(self, c: int) -> None:
        # cとc.parの間の辺を削除
        # cut後、頂点cを根とする木が新たに産まれる
        self._group_count += 1
        self.expose(c)
        node = self.node[c]
        node.left.par = None
        node.left = None
        self._update(node)

    def root(self, v: int) -> int:
        self.expose(v)
        node = self.node[v]
        self._propagate(node)
        while node.left:
            node = node.left
            self._propagate(node)
        self._splay(node)
        return node.index

    def same(self, u: int, v: int) -> bool:
        return self.root(u) == self.root(v)

    def evert(self, v: int) -> None:
        # vが属する木の根をvにする
        # evert後、vは遅延伝播済み
        # vの遅延素子は無い
        self.expose(v)
        self._apply_rev(self.node[v])
        self._propagate(self.node[v])

    def path_prod(self, u: int, v: int) -> T:
        self.evert(u)
        self.expose(v)
        return self.node[v].data

    def path_apply(self, u: int, v: int, f: F) -> None:
        self.evert(u)
        self.expose(v)
        self._apply_f(self.node[v], f)
        self._propagate(self.node[v])

    def merge(self, u: int, v: int) -> bool:
        if self.same(u, v):
            return False
        self.evert(u)
        self.link(u, v)
        return True

    def group_count(self) -> int:
        return sum(1 for e in self.node if e.par is None)

    def show(self) -> None:
        print("# show")
        for e in self.node:
            print(e)

    def __setitem__(self, k: int, v: T):
        node = self.node[k]
        self._splay(node)
        node.key = v
        self._update(node)

    def __getitem__(self, k: int) -> T:
        self._splay(self.node[k])
        return self.node[k].key

    def split(self, u: int, v: int):
        assert self.same(u, v)
        self.evert(u)
        self.cut(v)

    def path_length(self, u: int, v: int) -> int:
        self.evert(u)
        self.expose(v)
        return self.node[v].size

    def path_kth_elm(self, s: int, t: int, k: int) -> Optional[int]:
        self.evert(s)
        self.expose(t)
        node = self.node[t]
        if node.size <= k:
            return -1
        while True:
            self._propagate(node)
            t = node.left.size if node.left else 0
            if t == k:
                self._splay(node)
                return node.index
            if t > k:
                node = node.left
            else:
                node = node.right
                k -= t + 1

    def __str__(self):
        return str([self[i] for i in range(self.n)])

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
