from typing import List
from collections import defaultdict

class UnionFind():

  def __init__(self, n: int) -> None:
    '''Build a new UnionFind. / O(N)'''
    self._n = n
    self._group_numbers = n
    self._parents = [-1] * n

  def root(self, x: int) -> int:
    '''Return root of x, compressing path. / O(α(N))'''
    a = x
    while self._parents[a] >= 0:
      a = self._parents[a]
    while self._parents[x] >= 0:
      y = x
      x = self._parents[x]
      self._parents[y] = a
    return a

  def unite(self, x: int, y: int) -> bool:
    '''Untie x and y. / O(α(N))'''
    x = self.root(x)
    y = self.root(y)
    if x == y: return False
    self._group_numbers -= 1
    if self._parents[x] > self._parents[y]:
      x, y = y, x
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    return True

  def unite_right(self, x: int, y: int) -> int:
    # x -> y
    x = self.root(x)
    y = self.root(y)
    if x == y: return x
    self._group_numbers -= 1
    self._parents[y] += self._parents[x]
    self._parents[x] = y
    return y

  def unite_left(self, x: int, y: int) -> int:
    # x <- y
    x = self.root(x)
    y = self.root(y)
    if x == y: return x
    self._group_numbers -= 1
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    return x

  def size(self, x: int) -> int:
    '''Return xが属する集合の要素数. / O(α(N))'''
    return -self._parents[self.root(x)]

  def same(self, x: int, y: int) -> bool:
    '''Return True if 'same' else False. / O(α(N))'''
    return self.root(x) == self.root(y)

  def members(self, x: int) -> List[int]:
    '''Return set(the members of x). / O(size(x))'''
    x = self.root(x)
    return [i for i in range(self._n) if self.root(i) == x]

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

  def __str__(self) -> str:
    return '<UnionFind> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'

