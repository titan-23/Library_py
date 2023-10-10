from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Generic, TypeVar, Iterable, Sequence
T = TypeVar('T', bound=SupportsLessThan)

class SparseTableRmQ(Generic[T]):

  def __init__(self, a: Iterable[T], e: T):
    if not isinstance(a, Sequence):
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

  def __init__(self, G: List[List[int]], root: int):
    _n = len(G)
    bit = _n.bit_length() + 1
    msk = (1 << bit) - 1
    path = [-1] * (2*_n)
    depth = [-1] * _n
    nodein = [-1] * _n
    curtime = -1
    depth[root] = 0
    stack = [~root, root]
    while stack:
      curtime += 1
      v = stack.pop()
      if v >= 0:
        nodein[v] = curtime
        path[curtime] = v
        for x in G[v]:
          if depth[x] != -1:
            continue
          depth[x] = depth[v] + 1
          stack.append(~v)
          stack.append(x)
      else:
        path[curtime] = ~v
    self._n = _n
    self._path = path
    self._nodein = nodein
    self._depth = depth
    self._msk = msk
    a: List[int] = [(depth[v]<<bit)+i for i, v in enumerate(path)]
    self._st: SparseTableRmQ = SparseTableRmQ(a, e=max(a))

  def lca(self, u: int, v: int) -> int:
    l, r = self._nodein[u], self._nodein[v]
    if l > r:
      l, r = r, l
    return self._path[self._st.prod(l, r+1)&self._msk]

  def lca_mul(self, a: List[int]) -> int:
    l = self._n
    r = -l
    for e in a:
      e = self._nodein[e]
      if l > e: l = e
      if r < e: r = e
    return self._path[self._st.prod(l, r+1)&self._msk]

  def dist(self, u: int, v: int) -> int:
    # assert all costs are 1.
    return self._depth[self._nodein[u]] + self._depth[self._nodein[v]] - 2*self._depth[self._nodein[self.lca(u, v)]]


