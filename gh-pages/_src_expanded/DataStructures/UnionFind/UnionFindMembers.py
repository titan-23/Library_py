# from Library_py.DataStructures.UnionFind.UnionFindMembers import UnionFindMembers
from typing import List

class UnionFindMembers():

  def __init__(self, n: int) -> None:
    '''Build a new UnionFind. / O(N)'''
    self._n: int = n
    self._group_count: int = n
    self._group: List[List[int]] = [[i] for i in range(n)]

  def unite(self, x: int, y: int) -> bool:
    '''Untie x and y. / O(logN)'''
    u = self._group[x]
    v = self._group[y]
    if u is v: return False
    self._group_count -= 1
    if len(u) > len(v):
      u, v = v, u
    for i in u:
      v.append(i)
      self._group[i] = v
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


