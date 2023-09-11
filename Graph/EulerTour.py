from ..DataStructures.FenwickTree.FenwickTree import FenwickTree
from ..DataStructures.SparseTable.SparseTableRmQ import SparseTableRmQ
from typing import List
from __pypy__ import newlist_hint

class EulerTour():

  def __init__(self, G: List[List[List[int]]], root: int, vertexcost: List[int]=[]) -> None:
    n = len(G)
    if not vertexcost:
      vertexcost = [0] * n

    path = newlist_hint(2*n)
    pathdepth = newlist_hint(2*n)

    vcost1 = newlist_hint(2*n+1)
    vcost2 = newlist_hint(2*n+1)
    ecost1 = newlist_hint(2*n+1)
    ecost2 = newlist_hint(2*n+1)

    nodein = [-1] * n
    nodeout = [-1] * n

    curtime = -1
    depth = [-1] * n
    depth[root] = 0
    todo = []
    todo.append((root, 0, 0, vertexcost[root]))
    while todo:
      curtime += 1
      cn, cd, ec, vc = todo.pop()
      if cn >= 0:
        if nodein[cn] == -1:
          nodein[cn] = curtime
        depth[cn] = cd
        pathdepth.append(cd)
        path.append(cn)
        ecost1.append(ec)
        ecost2.append(ec)
        vcost1.append(vc)
        vcost2.append(vc)
        if len(G[cn]) == 1:
          nodeout[cn] = curtime + 1
        for nn, nv in G[cn]:
          if depth[nn] != -1:
            continue
          todo.append((~cn, cd, nv, -vertexcost[nn]))
          todo.append((nn, cd+1, nv, vertexcost[nn]))
      else:
        cn = ~cn
        if nodein[cn] == -1:
          nodein[cn] = curtime
        path.append(cn)
        ecost1.append(0)
        ecost2.append(-ec)
        vcost1.append(0)
        vcost2.append(vc)
        pathdepth.append(cd)
        nodeout[cn] = curtime + 1

    path.append(-1)
    pathdepth.append(-1)
    vcost1.append(0)
    vcost1.append(0)
    vcost2.append(-vertexcost[root])
    vcost2.append(-vertexcost[root])
    ecost1.append(0)
    ecost1.append(0)
    ecost2.append(0)
    ecost2.append(0)

    # ---------------------- #

    self._n = n
    self._depth = depth
    self._nodein = nodein
    self._nodeout = nodeout
    self._vertexcost = vertexcost
    self._path = path

    self._vcost1 = FenwickTree(vcost1)
    self._vcost2 = FenwickTree(vcost2)
    self._ecost1 = FenwickTree(ecost1)
    self._ecost2 = FenwickTree(ecost2)

    bit = len(pathdepth).bit_length()
    self.msk = (1 << bit) - 1
    a: List[int] = [(d<<bit)+i for i, d in enumerate(pathdepth)]
    self._st = SparseTableRmQ(a, e=max(a))

  def get_lca(self, x: int, y: int) -> int:
    if x == y: return x
    l = min(self._nodein[x], self._nodein[y])
    r = max(self._nodeout[x], self._nodeout[y])
    ind = self._st.prod(l, r) & self.msk
    return self._path[ind]

  def lca_mul(self, a: List[int]) -> int:
    l, r = self._n+1, -self._n-1
    for e in a:
      l = min(l, self._nodein[e])
      r = max(r, self._nodeout[e])
    ind = self._st.prod(l, r) & self.msk
    return self._path[ind]

  def get_subtree_vcost(self, x: int) -> int:
    l = self._nodein[x]
    r = self._nodeout[x]
    return self._vcost1.sum(l, r)

  def get_subtree_ecost(self, x: int) -> int:
    l = self._nodein[x]
    r = self._nodeout[x]
    return self._ecost1.sum(l+1, r)

  def get_path_vcost1(self, x: int) -> int:
    '''頂点xを含む'''
    return self._vcost2.pref(self._nodein[x]+1)

  def get_path_ecost1(self, x: int) -> int:
    '''根から頂点xまでの辺'''
    return self._ecost2.pref(self._nodein[x]+1)

  def get_path_vcost2(self, x: int, y: int) -> int:
    a = self.get_lca(x, y)
    return self.get_path_vcost1(x) + self.get_path_vcost1(y) - 2 * self.get_path_vcost1(a) + self._vertexcost[a]

  def get_path_ecost2(self, x: int, y: int) -> int:
    return self.get_path_ecost1(x) + self.get_path_ecost1(y) - 2 * self.get_path_ecost1(self.get_lca(x, y))

  def add_vertex(self, x: int, w: int) -> None:
    '''Add w to vertex x. / O(logN)'''
    l = self._nodein[x]
    r = self._nodeout[x]
    self._vcost1.add(l, w)
    self._vcost2.add(l, w)
    self._vcost2.add(r+1, -w)
    self._vertexcost[x] += w

  def set_vertex(self, x: int, w: int) -> None:
    '''Set w to vertex x. / O(logN)'''
    self.add_vertex(x, self.get_path_vcost2(x, x))

  def add_edge(self, u: int, v: int, w: int) -> None:
    '''Add w to edge([u - v]). / O(logN)'''
    if self._depth[u] < self._depth[v]:
      u, v = v, u
    l = self._nodein[u]
    r = self._nodeout[u]
    self._ecost1.add(l, w)
    self._ecost1.add(r+1, -w)
    self._ecost2.add(l, w)
    self._ecost2.add(r+1, -w)

  def set_edge(self, u: int, v: int, w: int) -> None:
    '''Set w to edge([u - v]). / O(logN)'''
    self.add_edge(u, v, w - self.get_path_ecost2(u, v))

