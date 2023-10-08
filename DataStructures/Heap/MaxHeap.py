from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import TypeVar, Generic, Iterable
T = TypeVar('T', bound=SupportsLessThan)

class MaxHeap(Generic[T]):

  def __init__(self, a: Iterable[T]=[]):
    self.a = list(a)
    self._heapify()

  def _heapify(self) -> None:
    for i in range(len(self.a)-1, -1, -1):
      self._down(i)

  def _down(self, i: int) -> None:
    a = self.a
    n = len(a)
    while i*2+1 < n:
      u, v = i*2+1, i*2+2
      if v < n and a[u] < a[v]:
        u = v
      if a[i] < a[u]:
        a[i], a[u] = a[u], a[i]
        i = u
      else:
        break

  def _up(self, i: int) -> None:
    a = self.a
    while i > 0:
      p = (i-1) >> 1
      if a[i] > a[p]:
        a[i], a[p] = a[p], a[i]
        i = p
      else:
        break

  def get_max(self) -> T:
    return self.a[0]

  def pop_max(self) -> T:
    res = self.a[0]
    self.a[0] = self.a[-1]
    self.a.pop()
    self._down(0)
    return res

  def push(self, key: T) -> None:
    self.a.append(key)
    self._up(len(self.a)-1)

  def pushpop_max(self, key: T) -> T:
    if self.a[0] < key or self.a[0] == key:
      return key
    res = self.a[0]
    self.a[0] = key
    self._down(0)
    return res

  def replace_max(self, key: T) -> T:
    res = self.a[0]
    self.a[0] = key
    self._down(0)
    return res

  def __getitem__(self, k: int) -> T:
    assert k == 0
    return self.a[0]

  def __len__(self):
    return len(self.a)
  
  def __str__(self):
    return str(self.a)

  def __repr__(self):
    return f'MaxHeap({self})'

