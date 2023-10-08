from Library_py.DataStructures.SparseTable.SparseTableRmQ import SparseTableRmQ
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
    return self._path[self._st.prod(l, r+1)]

  def dist(self, u: int, v: int) -> int:
    # assert all costs are 1.
    return self._depth[self._nodein[u]] + self._depth[self._nodein[v]] - 2*self._depth[self._nodein[self.lca(u, v)]]

