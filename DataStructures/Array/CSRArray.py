from typing import Generic, TypeVar, List, Iterator
from itertools import chain
T = TypeVar('T')

class CSRArray(Generic[T]):

  def __init__(self, a: List[List[T]]) -> None:
    n = len(a)
    start = list(map(len, a))
    start.insert(0, 0)
    for i in range(n):
      start[i+1] += start[i]
    self.csr = list(chain(*a))
    self.start = start

  def set(self, i: int, j: int, val: int) -> None:
    self.csr[self.start[i]+j] = val

  def iter(self, k: int, start: int=0) -> Iterator[T]:
    csr = self.csr
    for i in range(self.start[k]+start, self.start[k+1]):
      yield csr[i]

