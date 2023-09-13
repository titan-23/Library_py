from ..Array.PartialPersistentArray import PartialPersistentArray

class PartialPersistentUnionFind():

  def __init__(self, n: int):
    self._n: int = n
    self._parents: PartialPersistentArray[int] = PartialPersistentArray([-1] * n)
    self._last_time: int = 0

  def root(self, x: int, t: int=-1) -> int:
    assert t == -1 or t <= self._last_time
    while True:
      p = self._parents.get(x, t)
      if p < 0:
        return x
      x = p

  def unite(self, x: int, y: int, t: int) -> bool:
    assert t == -1 or t >= self._last_time
    self._last_time = t
    x = self.root(x, t)
    y = self.root(y, t)
    if x == y:
      return False
    if self._parents.get(x, t) > self._parents.get(y, t):
      x, y = y, x
    self._parents.set(x, self._parents.get(x, t) + self._parents.get(y, t), t)
    self._parents.set(y, x, t)
    return True

  def size(self, x: int, t: int=-1) -> int:
    assert t == -1 or t <= self._last_time
    return -self._parents.get(self.root(x, t), t)

  def same(self, x: int, y: int, t: int=-1) -> bool:
    assert t == -1 or t <= self._last_time
    return self.root(x, t) == self.root(y, t)

