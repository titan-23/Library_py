from typing import List, Set, Optional
from collections import defaultdict

class WeightedUnionFind():

  def __init__(self, n: int) -> None:
    self._n = n
    self._group_numbers = n
    self._parents = [-1]
    self._weight = [0]
    self._G = [[] for _ in range(n)]

  def root(self, x: int) -> int:
    '''Return root of x, compressing path. / O(α(N))'''
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

  def unite(self, x: int, y: int, w: int) -> int:
    '''Untie x and y, weight[y] = weight[x] + w. / O(α(N))'''
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

  def size(self, x: int) -> int:
    '''Return xが属する集合の要素数. / O(α(N))'''
    return -self._parents[self.root(x)]

  def same(self, x: int, y: int) -> bool:
    '''Return True if 'same' else False. / O(α(N))'''
    return self.root(x) == self.root(y)

  def members(self, x: int) -> Set[int]:
    '''Return set(the members of x). / O(size(x))'''
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

  def all_roots(self) -> List[int]:
    '''Return all roots. / O(N)'''
    return [i for i, x in enumerate(self._parents) if x < 0]

  def group_count(self) -> int:
    '''Return the number of groups. / O(1)'''
    return self._group_numbers

  def all_group_members(self) -> defaultdict:
    '''Return all_group_members. / O(Nα(N))'''
    group_members = defaultdict(list)
    for member in range(self._n):
      group_members[self.root(member)].append(member)
    return group_members

  def clear(self) -> None:
    '''Clear. / O(N)'''
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

