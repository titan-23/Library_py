from Library_py.DataStructures.AVLTree.AVLTreeSet2 import AVLTreeSet2
import enum
from enum import Enum
from typing import Optional, List, Tuple
import random

class RandomTreeType(Enum):

  random = enum.auto()
  path = enum.auto()
  star = enum.auto()


class RandomTree():

  def __init__(self, n: int, seed: Optional[int]=None):
    self.n = n
    random.seed(seed)

  def build(self, typ: RandomTreeType=RandomTreeType.random) -> List[Tuple[int, int]]:
    if typ == RandomTreeType.random:
      return self._build_random()
    if typ == RandomTreeType.path:
      return self._build_path()
    if typ == RandomTreeType.star:
      return self._build_star()
    raise ValueError(typ)

  def _build_star(self) -> List[Tuple[int, int]]:
    center = random.randrange(0, self.n)
    edge = []
    for i in range(self.n):
      if i == center:
        continue
      if random.random() < 0.5:
        edge.append((center, i))
      else:
        edge.append((i, center))
    random.shuffle(edge)
    return edge

  def _build_path(self) -> List[Tuple[int, int]]:
    p = list(range(self.n))
    random.shuffle(p)
    edges = [(p[i], p[i+1]) for i in range(self.n-1)]
    random.shuffle(edges)
    return edges

  def _build_random(self) -> List[Tuple[int, int]]:
    edges = []
    D = [1] * self.n
    A = [0] * (self.n-2)
    for i in range(self.n-2):
      v = random.randrange(0, self.n)
      D[v] += 1
      A[i] = v
    avl: AVLTreeSet2[Tuple[int, int]] = AVLTreeSet2((D[i], i) for i in range(self.n))
    for a in A:
      d, v = avl.pop_min()
      assert d == 1
      edges.append((v, a))
      D[v] -= 1
      avl.remove((D[a], a))
      D[a] -= 1
      if D[a] >= 1:
        avl.add((D[a], a))
    u = D.index(1)
    D[u] -= 1
    v = D.index(1)
    D[v] -= 1
    edges.append((u, v))
    random.shuffle(edges)
    return edges

