import sys
from typing import Generic, List, TypeVar, Tuple, Callable, Iterable, Any, Optional, Union
T = TypeVar('T')
F = TypeVar('F')

class Node:

  def __init__(self, index: int, key: Any):
    self.index = index
    self.key = key
    self.data = key
    self.rdata = key
    self.lazy = None
    self.par = None
    self.left = None
    self.right = None
    self.size = 1
    self.rev = 0

  def _is_root(self):
    return (self.par is None) or not (self.par.left is self or self.par.right is self)

  def __str__(self):
    if self.left is None and self.right is None:
      return f'(index,par,key,data):{self.index, (self.par.index if self.par else None), self.key, self.node, self._is_root()}, rev={self.rev}\n'
    return f'(index,par,key,data):{self.index, (self.par.index if self.par else None), self.key, self.node, self._is_root()}, rev={self.rev},\n left:{self.left},\n right:{self.right}\n'


class LinkCutTree(Generic[T, F]):

  def __init__(self, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T]=lambda x, y: None, mapping: Callable[[F, T], T]=lambda x, y: None, composition: Callable[[F, F], F]=lambda x, y: None, e: T=None):
    self.node = [Node(i, e) for i in range(n_or_a)] if isinstance(n_or_a, int) else [Node(i, e) for i in n_or_a]
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e

  def _propagate(self, node: Node) -> None:
    if node is None: return
    if node.rev:
      node.data, node.rdata = node.rdata, node.data
      node.left, node.right = node.right, node.left
      if node.left is not None:
        node.left.rev ^= 1
        self._propagate(node.left)
      if node.right is not None:
        node.right.rev ^= 1
        self._propagate(node.right)
      node.rev = 0
    if node.lazy is not None:
      lazy = node.lazy
      if node.left is not None:
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.rdata = self.mapping(lazy, node.left.rdata)
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.lazy = lazy if node.left.lazy is None else self.composition(lazy, node.left.lazy)
      if node.right is not None:
        node.right.data = self.mapping(lazy, node.right.data)
        node.right.rdata = self.mapping(lazy, node.right.rdata)
        node.right.key = self.mapping(lazy, node.right.key)
        node.right.lazy = lazy if node.right.lazy is None else self.composition(lazy, node.right.lazy)
      node.lazy = None

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
        node.data = node.key
        node.rdata = node.key
      else:
        node.size = 1 + node.right.size
        node.data = self.op(node.key, node.right.data)
        node.rdata = self.op(node.right.rdata, node.key)
    else:
      if node.right is None:
        node.size = 1 + node.left.size
        node.data = self.op(node.left.data, node.key)
        node.rdata = self.op(node.key, node.left.rdata)
      else:
        node.size = 1 + node.left.size + node.right.size
        node.data = self.op(self.op(node.left.data, node.key), node.right.data)
        node.rdata = self.op(self.op(node.right.rdata, node.key), node.left.rdata)

  def _update_triple(self, x: Node, y: Node, z: Node) -> None:
    z.size = x.size
    z.data = x.data
    z.rdata = x.rdata
    lx, rx = x.left, x.right
    if lx is None:
      if rx is None:
        x.data = x.key
        x.rdata = x.key
        x.size = 1
      else:
        x.data = self.op(x.key, rx.data)
        x.rdata = self.op(rx.rdata, x.key)
        x.size = 1 + rx.size
    else:
      if rx is None:
        x.data = self.op(lx.data, x.key)
        x.rdata = self.op(x.key, lx.rdata)
        x.size = 1 + lx.size
      else:
        x.data = self.op(self.op(lx.data, x.key), rx.data)
        x.rdata = self.op(self.op(rx.rdata, x.key), lx.rdata)
        x.size = 1 + lx.size + rx.size
    ly, ry = y.left, y.right
    if ly is None:
      if ry is None:
        y.data = y.key
        y.rdata = y.key
        y.size = 1
      else:
        y.data = self.op(y.key, ry.data)
        y.rdata = self.op(ry.rdata, y.key)
        y.size = 1 + ry.size
    else:
      if ry is None:
        y.data = self.op(ly.data, y.key)
        y.rdata = self.op(y.key, ly.rdata)
        y.size = 1 + ly.size
      else:
        y.data = self.op(self.op(ly.data, y.key), ry.data)
        y.rdata = self.op(self.op(ry.rdata, y.key), ly.rdata)
        y.size = 1 + ly.size + ry.size

  def _splay(self, node: Node) -> None:
    if node is None or node._is_root():
      self._propagate(node)
      return
    self._propagate(node)
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
    assert not self.same(c, p)
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
    assert node.left is not None
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
    node = self.node[v]
    node.key = self.mapping(f, node.key)
    node.data = self.mapping(f, node.data)
    node.rdata = self.mapping(f, node.rdata)
    node.lazy = f if node.lazy is None else self.composition(f, node.lazy)

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
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

  def __str__(self):
    seen = [False] * len(self.node)
    return 'LinkCutTree'

  def __repr__(self):
    return f'LinkCutTree()'


def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

import sys
input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

n, q = map(int, input().split())

if n > 50000 or q > 50000:
  assert False

lct = LinkCutTree(n, op=lambda x, y: x + y, mapping=lambda x, y: None, composition=lambda x, y: None, e=0)
A = list(map(int, input().split()))
for i, a in enumerate(A):
  lct[i] = a
for _ in range(n-1):
  u, v = map(int, input().split())
  lct.merge(u, v)

for _ in range(q):
  t, *qu = map(int, input().split())
  if t == 0:
    u, v, w, x = qu
    lct.split(u, v)
    lct.merge(w, x)
  elif t == 1:
    p, x = qu
    lct[p] += x
  else:
    u, v = qu
    print(lct.prod(u, v))
