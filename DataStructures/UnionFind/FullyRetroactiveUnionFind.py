from Library_py.DataStructures.DynamicConnectivity.LinkCutTree import LinkCutTree
from typing import List, Tuple, Set

class FullyRetroactiveUnionFind():

  def __init__(self, n: int, m: int):
    m += 1
    self.n: int = n
    self.edge: List[Tuple[int, int, int]] = [()] * m
    self.node_pool: Set[int] = set(range(n, n+m))
    self.lct: LinkCutTree[int, None] = LinkCutTree(n+m,
                                                   op=lambda s, t: s if s > t else t,
                                                   mapping=lambda f, s: -1,
                                                   composition=lambda f, g: None,
                                                   e=-1,
                                                   id=None)

  def unite(self, u: int, v: int, t: int) -> None:
    node = self.node_pool.pop()
    self.edge[t] = (u, v, node)
    self.lct[node] = t
    self.lct.merge(u, node)
    self.lct.merge(node, v)

  def disconnect(self, t: int) -> None:
    assert self.edge[t] is not None
    u, v, node = self.edge[t]
    self.node_pool.add(node)
    self.edge[t] = None
    self.lct.split(u, node)
    self.lct.split(node, v)

  def same(self, u: int, v: int, t: int) -> bool:
    if not self.lct.same(u, v):
      return False
    return self.lct.path_prod(u, v) <= t

