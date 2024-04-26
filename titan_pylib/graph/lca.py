from titan_pylib.data_structures.sparse_table.sparse_table_RmQ import SparseTableRmQ
from typing import List

class LCA():
  """LCA を定数倍良く求めます。

  :math:`< O(NlogN), O(1) >`
  https://github.com/cheran-senthil/PyRival/blob/master/pyrival/graphs/lca.py
  """

  def __init__(self, G: List[List[int]], root: int) -> None:
    """根が ``root`` の重み無し隣接リスト ``G`` で表されるグラフに対して LCA を求めます。
    時間・空間 :math:`O(n\\log{n})` です。

    Args:
      G (List[List[int]]): 隣接リストです。
      root (int): 根です。
    """
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
    """頂点 ``u`` と頂点 ``v`` の LCA を返します。
    :math:`O(1)` です。
    """
    if u == v:
      return u
    l, r = self._nodein[u], self._nodein[v]
    if l > r:
      l, r = r, l
    return self._path[self._st.prod(l, r)]

  def lca_mul(self, a: List[int]) -> int:
    """頂点集合 ``a`` の LCA を返します。"""
    if all(a[i] == a[i+1] for i in range(len(a)-1)):
      return a[0]
    l = self._n+1
    r = -l
    for e in a:
      e = self._nodein[e]
      if l > e: l = e
      if r < e: r = e
    return self._path[self._st.prod(l, r)]

