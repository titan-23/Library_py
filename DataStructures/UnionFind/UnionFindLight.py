from typing import List
from collections import defaultdict

class UnionFindLight:

  '''Build a new UnionFindLight. / O(N)'''
  def __init__(self, n: int) -> None:
    self._n = n
    self._group_numbers = n
    self._parents = [-1] * n

  '''Return root of x, compressing path. / O(α(N))'''
  def root(self, x: int) -> int:
    a = x
    while self._parents[a] >= 0:
      a = self._parents[a]
    while self._parents[x] >= 0:
      y = x
      x = self._parents[x]
      self._parents[y] = a
    return a

  '''Untie x and y. / O(α(N))'''
  def unite(self, x: int, y: int) -> bool:
    x = self.root(x)
    y = self.root(y)
    if x == y: return False
    self._group_numbers -= 1
    if self._parents[x] > self._parents[y]:
      x, y = y, x
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    return True

  # x -> y
  def unite_right(self, x: int, y: int) -> int:
    x = self.root(x)
    y = self.root(y)
    if x == y: return x
    self._group_numbers -= 1
    self._parents[y] += self._parents[x]
    self._parents[x] = y
    return y

  # x <- y
  def unite_left(self, x: int, y: int) -> int:
    x = self.root(x)
    y = self.root(y)
    if x == y: return x
    self._group_numbers -= 1
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    return x

  '''Return xが属する集合の要素数. / O(α(N))'''
  def size(self, x: int) -> int:
    return -self._parents[self.root(x)]

  '''Return True if 'same' else False. / O(α(N))'''
  def same(self, x: int, y: int) -> bool:
    return self.root(x) == self.root(y)

  '''Return set(the members of x). / O(size(x))'''
  def members(self, x: int) -> List[int]:
    x = self.root(x)
    return [i for i in range(self._n) if self.root(i) == x]

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

  def __str__(self) -> str:
    return '<UnionFindLight> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'

