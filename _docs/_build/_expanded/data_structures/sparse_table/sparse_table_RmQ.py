# from titan_pylib.data_structures.sparse_table.sparse_table_RmQ import SparseTableRmQ
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Generic, TypeVar, Iterable
T = TypeVar('T', bound=SupportsLessThan)

class SparseTableRmQ(Generic[T]):
  """
  2項演算を :math:`\\min` にしたものです。
  """

  def __init__(self, a: Iterable[T], e: T):
    if not isinstance(a, list):
      a = list(a)
    self.size = len(a)
    log = self.size.bit_length()-1
    data = [a] + [[]] * log
    for i in range(log):
      pre = data[i]
      l = 1 << i
      data[i+1] = [pre[j] if pre[j] < pre[j+l] else pre[j+l] for j in range(len(pre)-l)]
    self.data = data
    self.e = e

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.size
    if l == r: return self.e
    u = (r-l).bit_length()-1
    return self.data[u][l] if self.data[u][l] < self.data[u][r-(1<<u)] else self.data[u][r-(1<<u)]

  def __getitem__(self, k: int) -> T:
    assert 0 <= k < self.size
    return self.data[0][k]

  def __len__(self):
    return self.size

  def __str__(self):
    return str(self.data[0])

  def __repr__(self):
    return f'{self.__class__.__name__}({self.data[0]}, {self.e})'


