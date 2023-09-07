from ..DataStructures.SparseTable.SparseTableRmQ import SparseTableRmQ
from typing import List
from __pypy__ import newlist_hint

class LCA():

  def __init__(self, _G: List[List[int]], _root: int):
    _n = len(_G)
    bit = _n.bit_length() + 1
    msk = (1 << bit) - 1
    path = [-1] * (2*_n-1)
    depth = [-1] * (2*_n-1)
    nodeid = [-1] * _n
    todo = newlist_hint(2*_n)
    todo.append((_root, -1<<bit))
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
    self._st = SparseTableRmQ(a, e=max(a))

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

