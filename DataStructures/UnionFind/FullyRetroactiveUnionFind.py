from Library_py.DataStructures.DynamicConnectivity.LinkCutTree import LinkCutTree

class FullyRetroactiveUnionFind():

  def __init__(self, n: int, m: int):
    m += 1
    self.n = n
    self.edge = [None] * m
    self.node_pool = set(range(n, n+m))
    self.lct = LinkCutTree(n+m, op=lambda s, t: s if s > t else t, e=-1)

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

