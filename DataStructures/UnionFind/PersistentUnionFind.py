from Library_py.DataStructures.Array.PersistentArray import PersistentArray
from typing import Optional

class PersistentUnionFind():

  def __init__(self, n: int, _parents: Optional[PersistentArray[int]]=None):
    self._n: int = n
    self._parents: PersistentArray[int] = PersistentArray([-1] * n) if _parents is None else _parents

  def _new(self, _parents: PersistentArray[int]) -> 'PersistentUnionFind':
    return PersistentUnionFind(self._n, _parents)

  def copy(self) -> 'PersistentUnionFind':
    return self._new(self._parents.copy())

  def root(self, x: int) -> int:
    stack = []
    _parents = self._parents
    while True:
      p = _parents.get(x)
      if p < 0:
        break
      stack.append(x)
      x = p
    while stack:
      v = stack.pop()
      _parents = _parents.set(v, x)
    self._parents = _parents
    return x

  def unite(self, x: int, y: int, update: bool=False) -> 'PersistentUnionFind':
    x = self.root(x)
    y = self.root(y)
    res_parents = self._parents.copy() if update else self._parents
    if x == y:
      return self._new(res_parents)
    px, py = res_parents.get(x), res_parents.get(y)
    if px > py:
      x, y = y, x
    res_parents = res_parents.set(x, px + py)
    res_parents = res_parents.set(y, x)
    return self._new(res_parents)

  def size(self, x: int) -> int:
    return -self._parents.get(self.root(x))

  def same(self, x: int, y: int) -> bool:
    return self.root(x) == self.root(y)

