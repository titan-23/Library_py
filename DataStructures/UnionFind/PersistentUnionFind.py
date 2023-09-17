from Library_py.DataStructures.Array.PersistentArray import PersistentArray

class PersistentUnionFind():

  def __init__(self, n: int, init_t: int=0, max_t: int=-1):
    self._n: int = n
    self._parents: PersistentArray[int] = PersistentArray([-1]*n, init_t=init_t, max_t=max_t)

  def root(self, x: int, t: int) -> int:
    stack = []
    while True:
      p = self._parents.get(x, t)
      if p < 0:
        break
      stack.append(x)
      x = p
    while stack:
      v = stack.pop()
      self._parents.set(v, x, t, t)
    return x

  def unite(self, x: int, y: int, pre_t: int, new_t: int) -> bool:
    x = self.root(x, pre_t)
    y = self.root(y, pre_t)
    if x == y:
      self._parents.copy(pre_t, new_t)
      return False
    px, py = self._parents.get(x, pre_t), self._parents.get(y, pre_t)
    if px > py:
      x, y = y, x
    self._parents.set(x, px + py, pre_t, new_t)
    self._parents.set(y, x, pre_t, new_t)
    return True

  def size(self, x: int, t: int) -> int:
    return -self._parents.get(self.root(x, t), t)

  def same(self, x: int, y: int, t: int) -> bool:
    return self.root(x, t) == self.root(y, t)

