from typing import Generic, TypeVar, Callable, Iterable, Optional, Union
T = TypeVar('T')
F = TypeVar('F')

class LinkCutTree(Generic[T, F]):

  class Node():

    def __init__(self, index: int, key: T, lazy: F) -> None:
      self.index = index
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
      return (self.par is None) or not (self.par.left is self or self.par.right is self)

    def __str__(self):
      if self.left is None and self.right is None:
        return f'(index,par,key,data):{self.index, (self.par.index if self.par else None), self.key, self.node, self._is_root()}, rev={self.rev}\n'
      return f'(index,par,key,data):{self.index, (self.par.index if self.par else None), self.key, self.node, self._is_root()}, rev={self.rev},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T]=lambda x, y: None,
               mapping: Callable[[F, T], T]=lambda x, y: None,
               composition: Callable[[F, F], F]=lambda x, y: None,
               e: T=None,
               id: F=None,
               ) -> None:
    self.node = [LinkCutTree.Node(i, e, id) for i in range(n_or_a)] if isinstance(n_or_a, int) else [LinkCutTree.Node(i, e, id) for i in n_or_a]
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id = id

  def _propagate_f(self, node: Node, f: F) -> None:
    node.data = self.mapping(f, node.data)
    node.rdata = self.mapping(f, node.rdata)
    node.key = self.mapping(f, node.key)
    node.lazy = f if node.lazy == self.id else self.composition(f, node.lazy)

  def _propagate(self, node: Node) -> None:
    if node is None: return
    if node.rev:
      node.data, node.rdata = node.rdata, node.data
      node.left, node.right = node.right, node.left
      if node.left:
        node.left.rev ^= 1
      if node.right:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy:
      if node.left:
        self._propagate_f(node.left, node.lazy)
      if node.right:
        self._propagate_f(node.right, node.lazy)
      node.lazy = self.id

  def _update(self, node: Node) -> None:
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
      node.rdata = self.op(node.right.right, node.data)
      node.size += node.right.size

  def _update_triple(self, x: Node, y: Node, z: Node) -> None:
    self._update(x)
    self._update(y)
    self._update(z)

  def _rotate_right(self, node: Node) -> None:
    u = node.left
    node.left = u.right
    u.right = node

  def _rotate_left(self, node: Node) -> None:
    u = node.right
    node.right = u.left
    u.left = node

  def _splay(self, node: Node) -> None:
    self._propagate(node)
    if node is None or node._is_root():
      return
    while node.par.par is not None:
      pnode = node.par
      if pnode._is_root(): break
      gnode = pnode.par
      self._propagate(gnode)
      self._propagate(pnode)
      self._propagate(node)
      node.par = gnode.par
      if (gnode.left is pnode) == (pnode.left is node):
        if pnode.left is node:
          tmp1 = node.right
          pnode.left = tmp1
          node.right = pnode
          tmp2 = pnode.right
          gnode.left = tmp2
          pnode.right = gnode
        else:
          tmp1 = node.left
          pnode.right = tmp1
          node.left = pnode
          tmp2 = pnode.left
          gnode.right = tmp2
          pnode.left = gnode
        if tmp1:
          tmp1.par = pnode
        if tmp2:
          tmp2.par = gnode
        pnode.par = node
        gnode.par = pnode
      else:
        if pnode.left is node:
          tmp1 = node.right
          pnode.left = tmp1
          node.right = pnode
          tmp2 = node.left
          gnode.right = tmp2
          node.left = gnode
        else:
          tmp1 = node.left
          pnode.right = tmp1
          node.left = pnode
          tmp2 = node.right
          gnode.left = tmp2
          node.right = gnode
        if tmp1:
          tmp1.par = pnode
        if tmp2:
          tmp2.par = gnode
        pnode.par = node
        gnode.par = node
      self._update_triple(gnode, pnode, node)
      if node.par is None:
        self._propagate(node)
        return
      if node.par.left is gnode:
        node.par.left = node
      elif node.par.right is gnode:
        node.par.right = node
      self._update(node.par)
      if node._is_root():
        self._propagate(node)
        return
    if node._is_root():
      self._propagate(node)
      return
    pnode = node.par
    self._propagate(pnode)
    self._propagate(node)
    if pnode.left is node:
      pnode.left = node.right
      if pnode.left:
        pnode.left.par = pnode
      node.right = pnode
    else:
      pnode.right = node.left
      if pnode.right:
        pnode.right.par = pnode
      node.left = pnode
    node.par = pnode.par
    pnode.par = node
    self._update(pnode)
    self._update(node)

  def expose(self, v: int) -> None:
    node = self.node[v]
    while True:
      self._splay(node)
      node.right = None
      self._update(node)
      if node.par is None:
        break
      self._splay(node.par)
      node.par.right = node
      self._update(node.par)
    self._splay(node)
    node.right = None
    self._update(node)

  def link(self, c: int, p: int) -> None:
    self.expose(c)
    self.expose(p)
    self.node[c].par = self.node[p]
    self.node[p].right = self.node[c]
    self._update(self.node[p])

  def cut(self, c: int) -> None:
    # cとc.parの間の辺を削除
    # cut後、頂点cを根とする木が新たに産まれる
    self.expose(c)
    node = self.node[c]
    node.left.par = None
    node.left = None
    self._update(node)

  def root(self, v: int) -> Node:
    self.expose(v)
    node = self.node[v]
    self._propagate(node)
    while node.left is not None:
      node = node.left
      self._propagate(node)
    self._splay(node)
    return node

  def same(self, u: int, v: int) -> bool:
    return self.root(u) is self.root(v)

  def toggle(self, v: int) -> None:
    self.node[v].rev ^= 1
    self._propagate(self.node[v])

  def evert(self, v: int) -> None:
    # vが属する木の根をvにする
    # evert後、vは遅延伝播済み
    # vの遅延素子は無い
    self.expose(v)
    self.toggle(v)

  def prod(self, u: int, v: int) -> T:
    self.evert(u)
    self.expose(v)
    return self.node[v].data

  def apply(self, u: int, v: int, f: F) -> None:
    self.evert(u)
    self.expose(v)
    self._propagate_f(self.node[v], f)

  def merge(self, u: int, v: int) -> bool:
    if self.same(u, v): return False
    self.evert(u)
    self.link(u, v)
    return True

  def group_count(self) -> int:
    return sum(1 for e in self.node if e.par is None)

  def show(self) -> None:
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

  def path_kth_elm(self, s: int, t: int, k: int) -> Optional[int]:
    self.evert(s)
    self.expose(t)
    node = self.node[t]
    if node.size <= k:
      return None
    while True:
      self._propagate(node)
      t = 0 if node.left is None else node.left.size
      if t == k:
        self._splay(node)
        return node.index
      if t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

  def __str__(self):
    return 'LinkCutTree'

  def __repr__(self):
    return 'LinkCutTree'

