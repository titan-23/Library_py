from typing import List, Tuple
from collections import defaultdict

class UndoableUnionFind():

  def __init__(self, n: int):
    self._n: int = n
    self._parents: List[int] = [-1] * n
    self._history: List[Tuple[int, int]] = []

  def undo(self) -> None:
    assert self._history, f'UndoableUnionFind.undo() with non history'
    y, py = self._history.pop()
    x, px = self._history.pop()
    if y == -1:
      return
    self._parents[y] = py
    self._parents[x] = px

  def root(self, x: int) -> int:
    '''Return root of x. / O(logN)'''
    while self._parents[x] >= 0:
      x = self._parents[x]
    return x

  def unite(self, x: int, y: int) -> bool:
    '''Untie x and y. / O(logN)'''
    x = self.root(x)
    y = self.root(y)
    if x == y:
      self._history.append((-1, -1))
      self._history.append((-1, -1))
      return False
    if self._parents[x] > self._parents[y]:
      x, y = y, x
    self._history.append((x, self._parents[x]))
    self._history.append((y, self._parents[y]))
    self._parents[x] += self._parents[y]
    self._parents[y] = x
    return True

  def size(self, x: int) -> int:
    '''Return xが属する集合の要素数. / O(logN)'''
    return -self._parents[self.root(x)]

  def same(self, x: int, y: int) -> bool:
    '''Return True if 'same' else False. / O(logN)'''
    return self.root(x) == self.root(y)

  def all_roots(self) -> List[int]:
    '''Return all roots. / O(N)'''
    return [i for i, x in enumerate(self._parents) if x < 0]

  def all_group_members(self) -> defaultdict:
    '''Return all_group_members. / O(NlogN)'''
    group_members = defaultdict(list)
    for member in range(self._n):
      group_members[self.root(member)].append(member)
    return group_members

  def clear(self) -> None:
    '''Clear. / O(N)'''
    for i in range(self._n):
      self._parents[i] = -1

  def __str__(self) -> str:
    return '<UndoableUnionFind> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'


