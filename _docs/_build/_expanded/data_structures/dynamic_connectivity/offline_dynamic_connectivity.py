# from titan_pylib.data_structures.dynamic_connectivity.offline_dynamic_connectivity import OfflineDynamicConnectivity
from typing import List, Callable, Tuple
from collections import defaultdict

class OfflineDynamicConnectivity():
  """OfflineDynamicConnectivity

  参考:
    [ちょっと変わったセグメント木の使い方(ei1333の日記)](https://ei1333.hateblo.jp/entry/2017/12/14/000000)

  Note:
    内部では辺を ``dict`` で管理しています。メモリに注意です。
  """

  class UndoableUnionFind():
    """内部で管理される `UndoableUnionFind` です。
    """

    def __init__(self, n: int):
      self._n: int = n
      self._parents: List[int] = [-1] * n
      self._all_sum: List[int] = [0] * n
      self._one_sum: List[int] = [0] * n
      self._history: List[Tuple[int, int, int]] = []
      self._group_count: int = n

    def _undo(self) -> None:
      assert self._history, 'UndoableUnionFind._undo() with non history'
      y, py, all_sum_y = self._history.pop()
      if y == -1:
        return
      x, px, all_sum_x = self._history.pop()
      self._group_count += 1
      self._parents[y] = py
      self._parents[x] = px
      s = (self._all_sum[x] - all_sum_y - all_sum_x) // (-py-px) * (-py)
      self._all_sum[y] += s
      self._all_sum[x] -= all_sum_y + s
      self._one_sum[x] -= self._one_sum[y]

    def root(self, x: int) -> int:
      """要素 ``x`` を含む集合の代表元を返します。
      :math:`O(\\log{n})` です。
      """
      while self._parents[x] >= 0:
        x = self._parents[x]
      return x

    def unite(self, x: int, y: int) -> bool:
      """要素 ``x`` を含む集合と要素 ``y`` を含む集合を併合します。
      :math:`O(\\log{n})` です。

      Returns:
        bool: もともと同じ集合であれば ``False``、そうでなければ ``True`` を返します。
      """
      x = self.root(x)
      y = self.root(y)
      if x == y:
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
      """要素 ``x`` を含む集合の要素数を返します。
      :math:`O(\\log{n})` です。
      """
      return -self._parents[self.root(x)]

    def same(self, x: int, y: int) -> bool:
      """
      要素 ``x`` と ``y`` が同じ集合に属するなら ``True`` を、
      そうでないなら ``False`` を返します。
      :math:`O(\\log{n})` です。
      """
      return self.root(x) == self.root(y)

    def add_point(self, x: int, v: int) -> None:
      """頂点 ``x`` に値 ``v`` を加算します。
      :math:`O(\\log{n})` です。
      """
      while x >= 0:
        self._one_sum[x] += v
        x = self._parents[x]

    def add_group(self, x: int, v: int) -> None:
      """頂点 ``x`` を含む連結成分の要素それぞれに ``v`` を加算します。
      :math:`O(\\log{n})` です。
      """
      x = self.root(x)
      self._all_sum[x] += v * self.size(x)

    def group_count(self) -> int:
      """集合の総数を返します。
      :math:`O(1)` です。
      """
      return self._group_count

    def group_sum(self, x: int) -> int:
      """``x`` を要素に含む集合の総和を求めます。
      :math:`O(n\\log{n})` です。
      """
      x = self.root(x)
      return self._one_sum[x] + self._all_sum[x]

    def all_group_members(self) -> defaultdict:
      """``key`` に代表元、 ``value`` に ``key`` を代表元とする集合のリストをもつ ``defaultdict`` を返します。
      :math:`O(n\\log{n})` です。
      """
      group_members = defaultdict(list)
      for member in range(self._n):
        group_members[self.root(member)].append(member)
      return group_members

    def __str__(self):
      return '<offline-dc.uf> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'

  def __init__(self, n: int) -> None:
    """初期状態を頂点数 ``n`` の無向グラフとします。
    :math:`O(n)` です。

    Args:
      n (int): 頂点数です。
    """
    self._n = n
    self._query_count = 0
    self._bit = n.bit_length() + 1
    self._msk = (1 << self._bit) - 1
    self._start = defaultdict(lambda: [0, 0])
    self._edge_data = []
    self.uf = OfflineDynamicConnectivity.UndoableUnionFind(n)

  def add_edge(self, u: int, v: int) -> None:
    """辺 ``{u, v}`` を追加します。
    :math:`O(1)` です。
    """
    assert 0 <= u < self._n and 0 <= v < self._n
    if u > v:
      u, v = v, u
    edge = u<<self._bit|v
    if self._start[edge][0] == 0:
      self._start[edge][1] = self._query_count
    self._start[edge][0] += 1

  def delete_edge(self, u: int, v: int) -> None:
    """辺 ``{u, v}`` を削除します。
    :math:`O(1)` です。
    """
    assert 0 <= u < self._n and 0 <= v < self._n
    if u > v:
      u, v = v, u
    edge = u<<self._bit|v
    if self._start[edge][0] == 1:
      self._edge_data.append((self._start[edge][1], self._query_count, edge))
    self._start[edge][0] -= 1

  def next_query(self) -> None:
    """クエリカウントを 1 進めます。
    :math:`O(1)` です。
    """
    self._query_count += 1

  def run(self, out: Callable[[int], None]) -> None:
    """実行します。
    :math:`O(q \\log{q} \\log{n})` です。

    Args:
      out (Callable[[int], None]): クエリ番号 ``k`` を引数にとります。
    """
    # O(qlogqlogn)
    uf, bit, msk, q = self.uf, self._bit, self._msk, self._query_count
    log = (q - 1).bit_length()
    size = 1 << log
    size2 = size * 2
    data = [[] for _ in range(size<<1)]

    def add(l, r, edge):
      l += size
      r += size
      while l < r:
        if l & 1:
          data[l].append(edge)
          l += 1
        if r & 1:
          data[r^1].append(edge)
        l >>= 1
        r >>= 1

    for edge, p in self._start.items():
      if p[0] != 0:
        add(p[1], self._query_count, edge)
    for l, r, edge in self._edge_data:
      add(l, r, edge)

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
          uf._undo()

  def __repr__(self):
    return f'OfflineDynamicConnectivity({self._n})'

