from typing import List, Set
from collections import defaultdict

class UnionFindMembers:

  '''Build a new UnionFind. / O(N)'''
  def __init__(self, n: int) -> None:
    self._n = n
    self._group_count = n
    self._group = [[i] for i in range(n)]

  '''Untie x and y. / O(logN)'''
  def unite(self, x: int, y: int) -> bool:
    x = self._group[x]
    y = self._group[y]
    if x is y: return False
    self._group_count -= 1
    if len(x) > len(y):
      x, y = y, x
    for i in x:
      y.append(i)
      self._group[i] = y
    return True

  '''Return xが属する集合の要素数. / O(1)'''
  def size(self, x: int) -> int:
    return len(self._group[x])

  '''Return True if 'same' else False. / O(1)'''
  def same(self, x: int, y: int) -> bool:
    return self._group[x] is self._group[y]

  '''Return set(the members of x). / O(1)'''
  def members(self, x: int) -> List[int]:
    return self._group[x]

  '''Return the number of groups. / O(1)'''
  def group_count(self) -> int:
    return self._group_count


