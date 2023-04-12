from typing import List, Set
from collections import defaultdict

class UnionFindMembers():

  def __init__(self, n: int) -> None:
    '''Build a new UnionFind. / O(N)'''
    self._n = n
    self._group_count = n
    self._group = [[i] for i in range(n)]

  def unite(self, x: int, y: int) -> bool:
    '''Untie x and y. / O(logN)'''
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

  def size(self, x: int) -> int:
    '''Return xが属する集合の要素数. / O(1)'''
    return len(self._group[x])

  def same(self, x: int, y: int) -> bool:
    '''Return True if 'same' else False. / O(1)'''
    return self._group[x] is self._group[y]

  def members(self, x: int) -> List[int]:
    '''Return set(the members of x). / O(1)'''
    return self._group[x]

  def group_count(self) -> int:
    '''Return the number of groups. / O(1)'''
    return self._group_count

