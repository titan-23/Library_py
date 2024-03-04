# from titan_pylib.data_structures.heap.radix_heap import RadixHeap
from typing import Generic, Tuple, TypeVar, List
T = TypeVar('T')

class RadixHeap(Generic[T]):

  def __init__(self, u: int):
    self.u = u
    self.log = u.bit_length()
    self.lim = (1 << self.log) - 1
    self.last = 0
    self._len = 0
    self.data: List[List[Tuple[int, T]]] = [[] for _ in range(self.log)]

  def push(self, key: int, val: T) -> None:
    assert key <= self.lim
    self._len += 1
    self.data[(key ^ self.last).bit_length()].append((key, val))

  def pop_min(self) -> Tuple[int, T]:
    self._len -= 1
    data = self.data
    if data[0]:
      return data[0].pop()
    for d in data:
      if not d: continue
      last = min(d)[0]
      for elm in d:
        data[(elm[0] ^ last).bit_length()].append(elm)
      d.clear()
      self.last = last
      break
    return data[0].pop()

  def __len__(self):
    return self._len

  def __bool__(self):
    return self._len > 0

  def __str__(self):
    a = []
    for d in self.data:
      a.extend(d)
    return str(a)

