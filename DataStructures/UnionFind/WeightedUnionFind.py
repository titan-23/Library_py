from typing import List, Set, Union, Optional
from collections import defaultdict

class WeightedUnionFind:

  def __init__(self, n: int) -> None:
    self._n = n
    self._group_numbers = n
    self._parents = [-1]
    self._weight = [0]
    self._G = [[] for _ in range(n)]

  '''Return root of x, compressing path. / O(α(N))'''
  def root(self, x: int) -> int:
    path = [x]
    while self._parents[x] >= 0:
      x = self._parents[x]
      path.append(x)
    a = path.pop()
    while path:
      x = path.pop()
      self._weight[x] += self._weight[self._parents[x]]
      self._parents[x] = a
    return a

  '''Untie x and y, weight[y] = weight[x] + w. / O(α(N))'''
  def unite(self, x: int, y: int, w: int) -> int:
    rx = self.root(x)
    ry = self.root(y)
    w += self._weight[x] - self._weight[y]
    if rx == ry:
      return rx
    self._G[rx].append(ry)
    self._G[ry].append(rx)
    self._group_numbers -= 1
    if self._parents[rx] > self._parents[ry]:
      rx, ry = ry, rx
      w = -w
    self._parents[rx] += self._parents[ry]
    self._parents[ry] = rx
    self._weight[ry] = w
    return rx

  '''Return xが属する集合の要素数. / O(α(N))'''
  def size(self, x: int) -> int:
    return -self._parents[self.root(x)]

  '''Return True if 'same' else False. / O(α(N))'''
  def same(self, x: int, y: int) -> bool:
    return self.root(x) == self.root(y)

  '''Return set(the members of x). / O(size(x))'''
  def members(self, x: int) -> Set[int]:
    seen = set([x])
    todo = [x]
    while todo:
      v = todo.pop()
      for vv in self._G[v]:
        if vv in seen:
          continue
        todo.append(vv)
        seen.add(vv)
    return seen

  '''Return all roots. / O(N)'''
  def all_roots(self) -> List[int]:
    return [i for i, x in enumerate(self._parents) if x < 0]

  '''Return the number of groups. / O(1)'''
  def group_count(self) -> int:
    return self._group_numbers

  '''Return all_group_members. / O(Nα(N))'''
  def all_group_members(self) -> defaultdict:
    group_members = defaultdict(list)
    for member in range(self._n):
      group_members[self.root(member)].append(member)
    return group_members

  '''Clear. / O(N)'''
  def clear(self) -> None:
    self._group_numbers = self._n
    for i in range(self._n):
      self._parents[i] = -1
      self._G[i].clear()

  '''weight[y] - weight[x] / O(α(N))'''
  def diff(self, x: int, y: int) -> Optional[int]:
    if not self.same(x, y):
      return None
    return self._weight[y] - self._weight[x]

  def __str__(self) -> str:
    return '<WeightedUnionFind> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'

