from titan_pylib.data_structures.heap.min_heap import MinHeap
from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import TypeVar, Generic, Iterable
T = TypeVar('T', bound=SupportsLessThan)

class DeletableMinHeap(Generic[T]):

  def __init__(self, a: Iterable[T]) -> None:
    self.hq: MinHeap[T] = MinHeap(a)
    self.rem_hq: MinHeap[T] = MinHeap()
    self._len: int = len(self.hq)

  def push(self, key: T) -> None:
    self._len += 1
    if self.rem_hq and self.rem_hq.get_min() == key:
      self.rem_hq.pop_min()
      return
    self.hq.push(key)

  def remove(self, key: T) -> None:
    assert self._len > 0
    self._len -= 1
    self.rem_hq.push(key)

  def _delete(self) -> None:
    while self.rem_hq and self.rem_hq.get_min() == self.hq.get_min():
      self.hq.pop_min()
      self.rem_hq.pop_min()

  def get_min(self) -> T:
    assert self._len > 0
    self._delete()
    return self.hq.get_min()

  def pop_min(self) -> T:
    assert self._len > 0
    self._len -= 1
    self._delete()
    return self.hq.pop_min()

  def __len__(self):
    return self._len
