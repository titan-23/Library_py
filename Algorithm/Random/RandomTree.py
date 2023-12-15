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

  @classmethod
  def build(cls, n: int, typ: RandomTreeType=RandomTreeType.random, seed: Optional[int]=None) -> List[Tuple[int, int]]:
    random.seed(seed)
    if typ == RandomTreeType.random:
      return cls._build_random(n)
    if typ == RandomTreeType.path:
      return cls._build_path(n)
    if typ == RandomTreeType.star:
      return cls._build_star(n)
    raise ValueError(typ)

  @classmethod
  def _build_star(cls, n: int) -> List[Tuple[int, int]]:
    center = random.randrange(0, n)
    edge = []
    for i in range(n):
      if i == center:
        continue
      if random.random() < 0.5:
        edge.append((center, i))
      else:
        edge.append((i, center))
    random.shuffle(edge)
    return edge

  @classmethod
  def _build_path(cls, n: int) -> List[Tuple[int, int]]:
    p = list(range(n))
    random.shuffle(p)
    edges = [(p[i], p[i+1]) for i in range(n-1)]
    random.shuffle(edges)
    return edges

  @classmethod
  def _build_random(cls, n: int) -> List[Tuple[int, int]]:
    edges = []
    D = [1] * n
    A = [0] * (n-2)
    for i in range(n-2):
      v = random.randrange(0, n)
      D[v] += 1
      A[i] = v
    avl: AVLTreeSet2[Tuple[int, int]] = AVLTreeSet2((D[i], i) for i in range(n))
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

