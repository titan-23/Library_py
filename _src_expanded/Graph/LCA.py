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

  def __init__(self, _G: List[List[int]], _root: int):
    _n = len(_G)
    bit = _n.bit_length() + 1
    msk = (1 << bit) - 1
    path = [-1] * (2*_n-1)
    depth = [-1] * (2*_n-1)
    nodeid = [-1] * _n
    todo = [(_root, -1<<bit)]
    nowt = -1
    while todo:
      v, pd = todo.pop()
      nowt += 1
      d = pd & msk
      if v >= 0:
        p = pd >> bit
        nodeid[v] = nowt
        path[nowt] = v
        depth[nowt] = d
        for x in _G[v]:
          if x != p:
            todo.append((~v, (p<<bit)+d))
            todo.append((x, (v<<bit)+d+1))
      else:
        path[nowt] = ~v
        depth[nowt] = d
    self._n = _n
    self._path = path
    self._nodeid = nodeid
    self._depth = depth
    self._msk = msk
    a = [(d<<bit)+i for i, d in enumerate(depth)]
    self._st: SparseTableRmQ[int] = SparseTableRmQ(a, e=max(a))

  def lca(self, x: int, y: int) -> int:
    l, r = self._nodeid[x], self._nodeid[y]
    if l > r:
      l, r = r, l
    return self._path[self._st.prod(l, r+1)&self._msk]

  def lca_mul(self, a: List[int]) -> int:
    l = self._n
    r = -l
    for e in a:
      e = self._nodeid[e]
      if l > e: l = e
      if r < e: r = e
    return self._path[self._st.prod(l, r+1)]

  def dist(self, x: int, y: int) -> int:
    # assert all costs are 1.
    return self._depth[self._nodeid[x]] + self._depth[self._nodeid[y]] - 2*self._depth[self._nodeid[self.lca(x, y)]]


