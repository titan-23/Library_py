# from Library_py.DataStructures.Array.CSRArray import CSRArray
from typing import Generic, TypeVar, List
from itertools import chain
T = TypeVar('T')

class CSRArray(Generic[T]):

  def __init__(self, a: List[List[T]]) -> None:
    n = len(a)
    self.csr = list(chain(*a))
    start = [len(e) for e in a]
    start.insert(0, 0)
    for i in range(n):
      start[i+1] += start[i]

  def iter_k(self, k: int):
    csr = self.csr
    for i in range(self.start[k], self.start[k+1]):
      yield csr[i]


