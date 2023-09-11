from Library_py.DataStructures.SegmentTree.LazySegmentTree import LazySegmentTree
from Library_py.Graph.HLD.HLD import HLD
from typing import Union, Iterable, Callable, TypeVar, Generic
T = TypeVar('T')
F = TypeVar('F')

class HLDLazySegmentTree(Generic[T, F]):

  def __init__(self, hld: HLD, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], mapping: Callable[[F, T], T], composition: Callable[[F, F], F], e: T, id: F):
    self.hld: HLD = hld
    n_or_a = n_or_a if isinstance(n_or_a, int) else self.hld.build_list(list(n_or_a))
    self.seg: LazySegmentTree[T, F] = LazySegmentTree(n_or_a, op, mapping, composition, e, id)
    self.op: Callable[[T, T], T] = op
    self.e: T = e

  def path_prod(self, u: int, v: int) -> T:
    head, nodein, dep, par = self.hld.head, self.hld.nodein, self.hld.dep, self.hld.par
    res = self.e
    while head[u] != head[v]:
      if dep[head[u]] < dep[head[v]]:
        u, v = v, u
      res = self.op(res, self.seg.prod(nodein[head[u]], nodein[u]+1))
      u = par[head[u]]
    if dep[u] < dep[v]:
      u, v = v, u
    return self.op(res, self.seg.prod(nodein[v], nodein[u]+1))

  def path_apply(self, u: int, v: int, f: F) -> None:
    head, nodein, dep, par = self.hld.head, self.hld.nodein, self.hld.dep, self.hld.par
    res = self.e
    while head[u] != head[v]:
      if dep[head[u]] < dep[head[v]]:
        u, v = v, u
      self.seg.apply(nodein[head[u]], nodein[u]+1, f)
      u = par[head[u]]
    if dep[u] < dep[v]:
      u, v = v, u
    self.seg.apply(nodein[v], nodein[u]+1, f)

  def get(self, k: int) -> T:
    return self.seg[self.hld.nodein[k]]

  def set(self, k: int, v: T) -> None:
    self.seg[self.hld.nodein[k]] = v

  __getitem__ = get
  __setitem__ = set

  def subtree_prod(self, v: int) -> T:
    return self.seg.prod(self.hld.nodein[v], self.hld.nodeout[v])

  def subtree_apply(self, v: int, f: F) -> None:
    self.seg.apply(self.hld.nodein[v], self.hld.nodeout[v], f)

