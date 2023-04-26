from typing import Generic, TypeVar, Iterable, Sequence
T = TypeVar('T')

class SparseTableRmQ(Generic[T]):

  def __init__(self, a: Iterable[T], e: T=float('inf')):
    if not isinstance(a, Sequence):
      a = list(a)
    self.size = len(a)
    log = self.size.bit_length()-1
    self.data = [a] + [None] * log
    for i in range(log):
      pre = self.data[i]
      l = 1 << i
      self.data[i+1] = [pre[j] if pre[j] < pre[j+l] else pre[j+l] for j in range(len(pre)-l)]
    self.e = e

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.size
    if l == r: return self.e
    u = (r-l).bit_length()-1
    return self.data[u][l] if self.data[u][l] < self.data[u][r-(1<<u)] else self.data[u][r-(1<<u)]

  def __getitem__(self, k: int) -> T:
    assert 0 <= k < self.size
    return self.data[0][k]

  def __str__(self):
    return str(self.data[0])

  def __repr__(self):
    return f'SparseTableRmQ({self.data[0]}, {self.e})'

