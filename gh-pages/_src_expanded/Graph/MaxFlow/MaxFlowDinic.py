# from Library_py.Graph.MaxFlow.MaxFlowDinic import MaxFlowDinic
from collections import deque
from typing import List

class MaxFlowDinic():

  def __init__(self, n: int):
    self.n: int = n
    self.G: List[List[List[int]]] = [[] for _ in range(n)]

  def add_edge(self, u: int, v: int, w: int) -> None:
    assert 0 <= u < self.n, f'Indexerror: {self.__class__.__name__}.add_edge({u}, {v})'
    assert 0 <= v < self.n, f'Indexerror: {self.__class__.__name__}.add_edge({u}, {v})'
    G_u = len(self.G[u])
    G_v = len(self.G[v])
    self.G[u].append([v, w, G_v])
    self.G[v].append([u, 0, G_u])

  def _bfs(self, s: int) -> None:
    level = [-1] * self.n
    dq = deque([s])
    level[s] = 0
    while dq:
      v = dq.popleft()
      for x, w, _ in self.G[v]:
        if w > 0 and level[x] == -1:
          level[x] = level[v] + 1
          dq.append(x)
    self.level = level

  def _dfs(self, v: int, g: int, f: int) -> int:
    if v == g:
      return f
    for i in range(self.it[v], len(self.G[v])):
      self.it[v] += 1
      x, w, rev = self.G[v][i]
      if w > 0 and self.level[v] < self.level[x]:
        fv = self._dfs(x, g, min(f, w))
        if fv > 0:
          self.G[v][i][1] -= fv
          self.G[x][rev][1] += fv
          return fv
    return 0

  def max_flow(self, s: int, g: int, INF: int=10**18) -> int:
    assert 0 <= s < self.n, f'Indexerror: {self.__class__.__class__}.max_flow(), {s=}'
    assert 0 <= g < self.n, f'Indexerror: {self.__class__.__class__}.max_flow(), {g=}'
    ans = 0
    while True:
      self._bfs(s)
      if self.level[g] < 0:
        break
      self.it = [0] * self.n
      while True:
        f = self._dfs(s, g, INF)
        if f == 0:
          break
        ans += f
    return ans


