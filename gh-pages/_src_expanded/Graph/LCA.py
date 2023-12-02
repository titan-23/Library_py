# from Library_py.Graph.LCA import LCA
# from Library_py.DataStructures.SparseTable.SparseTableRmQ import SparseTableRmQ
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Generic, TypeVar, Iterable
T = TypeVar('T', bound=SupportsLessThan)

class SparseTableRmQ(Generic[T]):

  def __init__(self, a: Iterable[T], e: T):
    if not isinstance(a, list):
      a = list(a)
    self.size = len(a)
    log = self.size.bit_length()-1
    self.data = [a] + [[]] * log
    for i in range(log):
      pre = self.data[i]
      l = 1 << i
      self.data[i+1] = [pre[j] if pre[j] < pre[j+l] else pre[j+l] for j in range(len(pre)-l)]
    self.e = e

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.size
    if l == r: return self.e
    u = (r-l).bit_length()-1
    return self.data[u][l] if self.data[u][l] < self.data[u][r-(1<<u)] else self.data[u][r-(1<<u)]

  def __getitem__(self, k: int) -> T:
    assert 0 <= k < self.size
    return self.data[0][k]

  def __len__(self):
    return self.size

  def __str__(self):
    return str(self.data[0])

  def __repr__(self):
    return f'SparseTableRmQ({self.data[0]}, {self.e})'

from typing import List

class LCA():

  # < O(NlogN), O(1) >
  # https://github.com/cheran-senthil/PyRival/blob/master/pyrival/graphs/lca.py

  def __init__(self, G: List[List[int]], root: int) -> None:
    _n = len(G)
    path = [-1] * _n
    nodein = [-1] * _n
    par = [-1] * _n
    curtime = -1
    stack = [root]
    while stack:
      v = stack.pop()
      path[curtime] = par[v]
      curtime += 1
      nodein[v] = curtime
      for x in G[v]:
        if nodein[x] != -1:
          continue
        par[x] = v
        stack.append(x)
    self._n = _n
    self._path = path
    self._nodein = nodein
    self._st: SparseTableRmQ[int] = SparseTableRmQ((nodein[v] for v in path), e=_n)

  def lca(self, u: int, v: int) -> int:
    if u == v:
      return u
    l, r = self._nodein[u], self._nodein[v]
    if l > r:
      l, r = r, l
    return self._path[self._st.prod(l, r)]

  def lca_mul(self, a: List[int]) -> int:
    if all(a[i] == a[i+1] for i in range(len(a)-1)):
      return a[0]
    l = self._n+1
    r = -l
    for e in a:
      e = self._nodein[e]
      if l > e: l = e
      if r < e: r = e
    return self._path[self._st.prod(l, r)]


