from typing import Set, List
from collections import defaultdict

class UnionFindHeavy():

  def __init__(self, n: int) -> None:
    self._n: int = n
    self._group_numbers: int = n
    self._parents: List[int] = [-1] * n  # defaultdict(lambda: -1)
    # self._roots = set(range(n))
    self._edges: List[int] = [0] * n
    self._G: List[List[int]] = [[] for _ in range(n)]

  def root(self, x: int) -> int:
    assert 0 <= x < self._n, f'{self.__class__.__name__}.root(x) IndexError, x={x}'
    a = x
    while self._parents[a] >= 0:
      a = self._parents[a]
    # return a  # not compressing path.
    while self._parents[x] >= 0:
      y = x
      x = self._parents[x]
      self._parents[y] = a
    return a

  def unite(self, x: int, y: int) -> bool:
    assert 0 <= x < self._n and 0 <= y < self._n, \
        f'IndexError: {self.__class__.__name__}.unite({x}, {y})'
    x = self.root(x)
    y = self.root(y)
    self._edges[x] += 1
    self._edges[y] += 1
    if x == y: return False
    self._G[x].append(y)
    self._G[y].append(x)
    self._group_numbers -= 1
    if self._parents[x] > self._parents[y]:
      x, y = y, x
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    # self._roots.discard(y)
    return True

  def get_edges(self, x: int) -> int:
    return self._edges[self.root(x)]

  # x -> y
  def unite_right(self, x: int, y: int) -> int:
    assert 0 <= x < self._n and 0 <= y < self._n, \
        f'IndexError: {self.__class__.__name__}.unite_right(x: int, y: int), x={x}, y={y}'
    x = self.root(x)
    y = self.root(y)
    if x == y: return x
    self._G[x].append(y)
    self._G[y].append(x)
    self._group_numbers -= 1
    self._parents[y] += self._parents[x]
    self._parents[x] = y
    # self._roots.discard(y)
    return y

  # x <- y
  def unite_left(self, x: int, y: int) -> int:
    assert 0 <= x < self._n and 0 <= y < self._n, \
        f'IndexError: {self.__class__.__name__}.unite_left(x: int, y: int), x={x}, y={y}'
    x = self.root(x)
    y = self.root(y)
    if x == y: return x
    self._G[x].append(y)
    self._G[y].append(x)
    self._group_numbers -= 1
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    # self._roots.discard(y)
    return x

  def size(self, x: int) -> int:
    assert 0 <= x < self._n, \
        f'IndexError: {self.__class__.__name__}.size(x: int), x={x}'
    return -self._parents[self.root(x)]

  def same(self, x: int, y: int) -> bool:
    assert 0 <= x < self._n and 0 <= y < self._n, \
        f'IndexError: {self.__class__.__name__}.same(x: int, y: int), x={x}, y={y}'
    return self.root(x) == self.root(y)

  def members(self, x: int) -> Set[int]:
    assert 0 <= x < self._n, \
        f'IndexError: {self.__class__.__name__}.members(x: int), x={x}'
    seen = set([x])
    todo = [x]
    while todo:
      v = todo.pop()
      for x in self._G[v]:
        if x in seen: continue
        todo.append(x)
        seen.add(x)
    return seen

  def all_roots(self) -> List[int]:
    '''Return all roots. / O(1)'''
    # return self._roots
    return [i for i, x in enumerate(self._parents) if x < 0]

  def group_count(self) -> int:
    return self._group_numbers

  def all_group_members(self) -> defaultdict:
    group_members = defaultdict(list)
    for member in range(self._n):
      group_members[self.root(member)].append(member)
    return group_members

  def clear(self) -> None:
    self._group_numbers = self._n
    for i in range(self._n):
      self._parents[i] = -1
      self._G[i].clear()

  def __str__(self) -> str:
    return f'<{self.__class__.__name__}> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'

