# from Library_py.DataStructures.DynamicConnectivity.OfflineDynamicConnectivity import OfflineDynamicConnectivity
from typing import List, Callable, Tuple
from collections import defaultdict

class OfflineDynamicConnectivity():

  class UndoableUnionFind():

    def __init__(self, n: int):
      self._n: int = n
      self._parents: List[int] = [-1] * n
      self._all_sum: List[int] = [0] * n
      self._one_sum: List[int] = [0] * n
      self._history: List[Tuple[int, int, int]] = []
      self._group_count: int = n

    def undo(self) -> None:
      assert self._history, 'UndoableUnionFind.undo() with non history'
      y, py, all_sum_y = self._history.pop()
      x, px, all_sum_x = self._history.pop()
      if y == -1:
        return
      self._group_count += 1
      self._parents[y] = py
      self._parents[x] = px
      s = (self._all_sum[x] - all_sum_y - all_sum_x) // (-py-px) * (-py)
      self._all_sum[y] += s
      self._all_sum[x] -= all_sum_y + s
      self._one_sum[x] -= self._one_sum[y]

    def root(self, x: int) -> int:
      while self._parents[x] >= 0:
        x = self._parents[x]
      return x

    def unite(self, x: int, y: int) -> bool:
      x = self.root(x)
      y = self.root(y)
      if x == y:
        self._history.append((-1, -1, -1))
        self._history.append((-1, -1, -1))
        return False
      if self._parents[x] > self._parents[y]:
        x, y = y, x
      self._group_count -= 1
      self._history.append((x, self._parents[x], self._all_sum[x]))
      self._history.append((y, self._parents[y], self._all_sum[y]))
      self._all_sum[x] += self._all_sum[y]
      self._one_sum[x] += self._one_sum[y]
      self._parents[x] += self._parents[y]
      self._parents[y] = x
      return True

    def size(self, x: int) -> int:
      return -self._parents[self.root(x)]

    def same(self, x: int, y: int) -> bool:
      return self.root(x) == self.root(y)

    def add_point(self, x: int, v: int) -> None:
      while x >= 0:
        self._one_sum[x] += v
        x = self._parents[x]

    def add_group(self, x: int, v: int) -> None:
      x = self.root(x)
      self._all_sum[x] += v * self.size(x)

    def group_count(self) -> int:
      return self._group_count

    def group_sum(self, x: int) -> int:
      x = self.root(x)
      return self._one_sum[x] + self._all_sum[x]

    def all_group_members(self) -> defaultdict:
      group_members = defaultdict(list)
      for member in range(self._n):
        group_members[self.root(member)].append(member)
      return group_members

    def __str__(self):
      return '<offline-dc.uf> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'

  def __init__(self, n: int):
    self._n = n
    self._bit = n.bit_length() + 1
    self._msk = (1 << self._bit) - 1
    self._query_count = 0
    self._edge = defaultdict(list)
    self.uf = OfflineDynamicConnectivity.UndoableUnionFind(n)

  def add_edge(self, u: int, v: int) -> None:
    assert 0 <= u < self._n and 0 <= v < self._n
    if u > v:
      u, v = v, u
    self._edge[u<<self._bit|v].append(self._query_count<<1)
    self._query_count += 1

  def delete_edge(self, u: int, v: int) -> None:
    assert 0 <= u < self._n and 0 <= v < self._n
    if u > v:
      u, v = v, u
    self._edge[u<<self._bit|v].append(self._query_count<<1|1)
    self._query_count += 1

  def add_none(self) -> None:
    self._query_count += 1

  def init_edge(self, E: List[Tuple[int, int]]) -> None:
    bit, edge = self._bit, self._edge
    for u, v in E:
      assert 0 <= u < self._n and 0 <= v < self._n
      if u > v:
        u, v = v, u
      edge[u<<bit|v].append(0)
    self._query_count += 1

  def run(self, out: Callable[[int], None]) -> None:
    # O(qlogqlogn)
    uf, bit, msk, q = self.uf, self._bit, self._msk, self._query_count
    log = (q - 1).bit_length()
    size = 1 << log
    data = [[] for _ in range(size<<1)]
    size2 = size * 2
    for k, v in self._edge.items():
      LR = []
      i = 0
      cnt = 0
      while i < len(v):
        if v[i] & 1 == 0:
          cnt += 1
        if cnt > 0:
          LR.append(v[i]>>1)
          i += 1
          while i < len(v) and cnt > 0:
            if v[i] & 1 == 0:
              cnt += 1
            else:
              assert cnt >= 0, 'Edge Error: minus edge.'
              cnt -= 1
              if cnt == 0:
                LR.append(v[i]>>1)
            i += 1
          i -= 1
        i += 1
      if cnt > 0:
        LR.append(q)
      LR.reverse()
      while LR:
        l = LR.pop() + size
        r = LR.pop() + size
        while l < r:
          if l & 1:
            data[l].append(k)
            l += 1
          if r & 1:
            data[r^1].append(k)
          l >>= 1
          r >>= 1
    todo = [1]
    while todo:
      v = todo.pop()
      if v >= 0:
        for uv in data[v]:
          uf.unite(uv>>bit, uv&msk)
        todo.append(~v)
        if v<<1|1 < size2:
          todo.append(v<<1|1)
          todo.append(v<<1)
        elif v - size < q:
          out(v-size)
      else:
        for _ in data[~v]:
          uf.undo()

  def __repr__(self):
    return f'OfflineDynamicConnectivity({self._n})'


