from typing import List, Generator, Tuple
from types import GeneratorType

class HLD():

  def antirec(func, stack=[]):
    def wrappedfunc(*args, **kwargs):
      if stack:
        return func(*args, **kwargs)
      to = func(*args, **kwargs)
      while True:
        if isinstance(to, GeneratorType):
          stack.append(to)
          to = next(to)
        else:
          stack.pop()
          if not stack:
            break
          to = stack[-1].send(to)
      return to
    return wrappedfunc

  def __init__(self, G: List[List[int]], root: int):
    n = len(G)
    self.n: int = n
    self.G: List[List[int]] = G
    self.size: List[int] = [0] * n
    self.par: List[int] = [0] * n
    self.dep: List[int] = [0] * n
    self.nodein: List[int] = [0] * n
    self.nodeout: List[int] = [0] * n
    self.head: List[int] = [0] * n
    self.hld: List[int] = [0] * n
    self.dfs1(root, -1)
    self.time: int = 0
    self.dfs2(root, -1)

  @antirec
  def dfs1(self, v: int, p: int) -> Generator:
    self.par[v] = p
    size = 1
    dep = self.dep[v]
    for i, x in enumerate(self.G[v]):
      x = self.G[v][i]
      if x == p:
        continue
      self.dep[x] = dep + 1
      yield self.dfs1(x, v)
      size += self.size[x]
      if self.size[x] > self.size[self.G[v][0]]:
        self.G[v][0], self.G[v][i] = self.G[v][i], self.G[v][0]
    self.size[v] = size
    yield

  @antirec
  def dfs2(self, v: int, p: int) -> Generator:
    if p == -1:
      self.head[v] = v
    self.nodein[v] = self.time
    self.hld[self.time] = v
    self.time += 1
    for x in self.G[v]:
      if x == p:
        continue
      self.head[x] = self.head[v] if x == self.G[v][0] else x
      yield self.dfs2(x, v)
    self.nodeout[v] = self.time
    yield

  def for_each_edge(self, u: int, v: int) -> Generator[Tuple[int, int], None, None]:
    head, nodein, dep, par = self.head, self.nodein, self.dep, self.par
    while head[u] != head[v]:
      if dep[head[u]] > dep[head[v]]:
        yield (self.n-nodein[u]-1, self.n-nodein[head[u]])  # lres
        u = par[head[u]]
      else:
        yield ((nodein[head[v]], nodein[v]+1))  # rres
        v = par[head[v]]
    if dep[u] > dep[v]:
      yield (self.n-nodein[u]-1, self.n-nodein[v])  # lres
    else:
      yield nodein[u], nodein[v]+1  # lres


class HLDQuery():

  def __init__(self, hld: HLD):
    self.hld = hld

  def build_list(self, a: List) -> List:
    return [a[e] for e in self.hld.hld]

  def path_prod(self, u: int, v: int, data, op, e):
    head, nodein, dep, par, n = self.hld.head, self.hld.nodein, self.hld.dep, self.hld.par, self.hld.n
    res = e
    while head[u] != head[v]:
      if dep[head[u]] > dep[head[v]]:
        u, v = v, u
      res = op(data.prod(nodein[head[v]], nodein[v]+1), res)
      v = par[head[v]]
    if dep[u] > dep[v]:
      u, v = v, u
    return op(res, data.prod(nodein[u], nodein[v]+1))

  def path_prod_noncommutative(self, u: int, v: int, data, rdata, op, e):
    head, nodein, dep, par, n = self.hld.head, self.hld.nodein, self.hld.dep, self.hld.par, self.hld.n
    lres, rres = e, e
    while head[u] != head[v]:
      if dep[head[u]] > dep[head[v]]:
        lres = op(lres, rdata.prod(n-nodein[u]-1, n-nodein[head[u]]))
        u = par[head[u]]
      else:
        rres = op(data.prod(nodein[head[v]], nodein[v]+1), rres)
        v = par[head[v]]
    if dep[u] > dep[v]:
      lres = op(lres, rdata.prod(n-nodein[u]-1, n-nodein[v]))
    else:
      lres = op(lres, data.prod(nodein[u], nodein[v]+1))
    return op(lres, rres)

  def path_kth_elm(self, s: int, t: int, k: int) -> int:
    head, dep, par = self.hld.head, self.hld.dep, self.hld.par
    lca = self.lca(s, t)
    d = dep[s] + dep[t] - 2*dep[lca]
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
    return self.hld.hld[self.hld.nodein[s] - k]

  def lca(self, u: int, v: int) -> int:
    nodein, head, par = self.hld.nodein, self.hld.head, self.hld.par
    while True:
      if nodein[u] > nodein[v]:
        u, v = v, u
      if head[u] == head[v]:
        return u
      v = par[head[v]]

  def get(self, k: int) -> int:
    return self.hld.nodein[k]

  def get_noncommutative(self, k: int) -> Tuple[int, int]:
    return self.hld.nodein[k], self.hld.n-self.hld.nodein[k]-1

  def subtree_prod(self, v: int) -> Tuple[int, int]:
    return self.hld.nodein[v], self.hld.nodeout[v]

