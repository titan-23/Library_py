from titan_pylib.data_structures.heap.max_heap import MaxHeap
from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import TypeVar, Generic, Iterable
T = TypeVar('T', bound=SupportsLessThan)

class DeletableMaxHeap(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    """削除可能Maxヒープです。
    要素の 追加/削除/最大値取得 が効率よく行えます。
    """
    self.hq: MaxHeap[T] = MaxHeap(a)
    self.rem_hq: MaxHeap[T] = MaxHeap()
    self._len: int = len(self.hq)

  def push(self, key: T) -> None:
    """``key`` を追加します。
    :math:`O(\\log{n})` です。
    """
    self._len += 1
    if self.rem_hq and self.rem_hq.get_max() == key:
      self.rem_hq.pop_max()
      return
    self.hq.push(key)

  def remove(self, key: T) -> None:
    """``key`` を削除します。
    :math:`O(\\log{n})` です。
    """
    assert self._len > 0
    self._len -= 1
    if self.hq.get_max() == key:
      self.hq.pop_max()
    else:
      self.rem_hq.push(key)

  def _delete(self) -> None:
    while self.rem_hq and self.rem_hq.get_max() == self.hq.get_max():
      self.hq.pop_max()
      self.rem_hq.pop_max()

  def get_max(self) -> T:
    """最大の要素を返します。
    :math:`O(\\log{n})` です。
    """
    assert self._len > 0
    self._delete()
    return self.hq.get_max()

  def pop_max(self) -> T:
    """最大の要素を削除して返します。
    :math:`O(\\log{n})` です。
    """
    assert self._len > 0
    self._len -= 1
    self._delete()
    return self.hq.pop_max()

  def __len__(self) -> int:
    return self._len
