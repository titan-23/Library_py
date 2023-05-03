from typing import Generic, TypeVar, Iterable, Sequence
from math import log2
T = TypeVar('T')

class RmQ(Generic[T]):

  def __init__(self, a: Iterable[int]):
    self.a = list(a)
    self.n = len(self.a)
    self._build()
  
  def _build(self):
    a = self.a
    n = self.n

    # sparse table
    ln = int(log2(n)) + 1
    B = [min(a[i*ln:(i+1)*ln]) for i in range(n//ln)]
    size = len(B)
    log = size.bit_length() - 1
    self.bucket = [B] + [[]] * log
    for i in range(log):
      pre = self.bucket[i]
      l = 1 << i
      self.bucket[i+1] = [pre[j] if pre[j] < pre[j+l] else pre[j+l] for j in range(len(pre)-l)]
    
    # bit



  def _prod_bucket(self, l: int, r: int) -> T:
    u = (r-l).bit_length()-1
    return self.bucket[u][l] if self.bucket[u][l] < self.bucket[u][r-(1<<u)] else self.bucket[u][r-(1<<u)]

  def prod(l, r):
    




a = RmQ([1, 2, 3, 4])


