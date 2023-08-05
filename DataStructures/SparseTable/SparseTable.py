from typing import Generic, TypeVar, Iterable, Callable, Sequence
T = TypeVar('T')

class SparseTable(Generic[T]):

  def __init__(self, a: Iterable[T], op: Callable[[T, T], T], e: T=None):
    if not isinstance(a, Sequence):
      a = list(a)
    self.size = len(a)
    log = self.size.bit_length()-1
    self.data = [a] + [[]] * log
    for i in range(log):
      pre = self.data[i]
      l = 1 << i
      self.data[i+1] = [op(pre[j], pre[j+l]) for j in range(len(pre)-l)]
    self.op = op
    self.e = e

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: SparseTable.prod({l}, {r}), len={self.size}'
    if l == r: return self.e
    u = (r-l).bit_length()-1
    return self.op(self.data[u][l], self.data[u][r-(1<<u)])

  def __getitem__(self, k: int) -> T:
    assert 0 <= k < self.size, \
        f'IndexError: SparseTable.__getitem__({k}), len={self.size}'
    return self.data[0][k]

  def __len__(self):
    return self.size

  def __str__(self):
    return str(self.data[0])

  def __repr__(self):
    return f'SparseTable({self}, {self.op}, {self.e})'

