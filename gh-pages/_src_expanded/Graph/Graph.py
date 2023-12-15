# from Library_py.Graph.Graph import Graph
# from Library_py.DataStructures.Array.CSRArray import CSRArray
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

  def iter(self, k: int) -> Iterator[T]:
    csr = self.csr
    for i in range(self.start[k], self.start[k+1]):
      yield csr[i]


class Graph():

  def __init__(self, n: int) -> None:
    self.G = [[] for _ in range(n)]
  
  def add_edge(self, u: int, v: int) -> None:
    self.G[u].append(v)
  
  def build_csr(self) -> None:
    self.csr = CSRArray(self.G)



