from typing import Generic, Iterable, TypeVar, Callable, Union, List, Generator
from types import GeneratorType
T = TypeVar('T')

class HLD(Generic[T]):

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

  def __init__(self, n_or_a: Union[int, Iterable[T]], G: List[List[int]], op: Callable[[T, T], T], e: T):
    n = len(G)
    self.n = n
    self.G = G
    self.e = e
    self.op = op
    self.size = [0] * n
    self.par = [0] * n
    self.dep = [0] * n
    self.nodein = [0] * n
    self.nodeout = [0] * n
    self.head = [0] * n
    self.hld = [0] * n
    self.dfs1(0, -1)
    self.time = 0
    self.dfs2(0, -1)
    if isinstance(n_or_a, int):
      self.data = SegmentTree(n_or_a, op, e)
      self.rdata = SegmentTree(n_or_a, op, e)
    else:
      n_or_a = list(n_or_a)
      a = [n_or_a[e] for e in self.hld]
      self.data = SegmentTree(a, op, e)
      self.rdata = SegmentTree(a[::-1], op, e)

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

  def path_prod(self, u: int, v: int) -> T:
    head, nodein, dep, par = self.head, self.nodein, self.dep, self.par
    data_prod, rdata_prod = self.data.prod, self.rdata.prod
    lres, rres = self.e, self.e
    while head[u] != head[v]:
      if dep[head[u]] > dep[head[v]]:
        lres = self.op(lres, rdata_prod(self.n-nodein[u]-1, self.n-nodein[head[u]]))
        u = par[head[u]]
      else:
        rres = self.op(data_prod(nodein[head[v]], nodein[v]+1), rres)
        v = par[head[v]]
    if dep[u] > dep[v]:
      lres = self.op(lres, rdata_prod(self.n-nodein[u]-1, self.n-nodein[v]))
    else:
      lres = self.op(lres, data_prod(nodein[u], nodein[v]+1))
    return self.op(lres, rres)

  def subtree_prod(self, u: int) -> T:
    return self.data.prod(self.nodein[u], self.nodeout[u])

  def lca(self, u: int, v: int) -> int:
    nodein, head, par = self.nodein, self.head, self.par
    while True:
      if nodein[u] > nodein[v]:
        u, v = v, u
      if head[u] == head[v]:
        return u
      v = par[head[v]]

  def get(self, k: int) -> T:
    return self.data[self.nodein[k]]

  def set(self, k: int, v: T) -> None:
    self.data[self.nodein[k]] = v
    self.rdata[self.n-self.nodein[k]-1] = v


def op(s, t):
  return

e = None

