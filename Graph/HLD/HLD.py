from typing import Any, List, Generator, Tuple
from types import GeneratorType

class HLD():

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

  @staticmethod
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

  def path_kth_elm(self, s: int, t: int, k: int) -> int:
    head, dep, par = self.head, self.dep, self.par
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
    return self.hld[self.nodein[s] - k]

  def lca(self, u: int, v: int) -> int:
    nodein, head, par = self.nodein, self.head, self.par
    while True:
      if nodein[u] > nodein[v]:
        u, v = v, u
      if head[u] == head[v]:
        return u
      v = par[head[v]]

  def build_list(self, a: List[Any]) -> List[Any]:
    return [a[e] for e in self.hld]

  def for_each_vertex(self, u: int, v: int) -> Generator[Tuple[int, int], None, None]:
    head, nodein, dep, par = self.head, self.nodein, self.dep, self.par
    while head[u] != head[v]:
      if dep[head[u]] < dep[head[v]]:
        u, v = v, u
      yield nodein[head[u]], nodein[u]+1
      u = par[head[u]]
    if dep[u] < dep[v]:
      u, v = v, u
    yield nodein[v], nodein[u]+1

