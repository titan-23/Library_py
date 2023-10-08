from typing import Iterable, List, TypeVar, Generic
T = TypeVar('T')

class PartialPersistentArray(Generic[T]):

  def __init__(self, a: Iterable[T]):
    self.a: List[List[T]] = [[e] for e in a]
    self.t: List[List[int]] = [[0] for _ in range(len(self.a))]
    self.last_time: int = 0

  def set(self, k: int, v: T, t: int) -> None:
    assert t >= self.last_time
    assert t > self.t[k][-1]
    self.a[k].append(v)
    self.t[k].append(t)
    self.last_time = t

  def get(self, k: int, t: int=-1) -> T:
    if t == -1 or t >= self.t[k][-1]:
      return self.a[k][-1]
    tk = self.t[k]
    ok, ng = 0, len(tk)
    while ng - ok > 1:
      mid = (ok + ng) // 2
      if tk[mid] <= t:
        ok = mid
      else:
        ng = mid
    return self.a[k][ok]

  def tolist(self, t: int) -> List[T]:
    return [self.get(i, t) for i in range(len(self))]

  def show(self, t: int) -> None:
    print(f'Time: {t}', end='')
    print([self.get(i, t) for i in range(len(self))])

  def show_all(self) -> None:
    for i in range(self.last_time):
      self.show(i)

  def __len__(self):
    return len(self.a)


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


