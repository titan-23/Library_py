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

  def iter(self, k: int) -> Iterator[T]:
    csr = self.csr
    for i in range(self.start[k], self.start[k+1]):
      yield csr[i]

