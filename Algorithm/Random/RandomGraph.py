import enum
from enum import Enum
from typing import Optional, List, Tuple
import random

class RandomGraphType(Enum):
  random_undir = enum.auto()

class RandomGraph():

  @classmethod
  def build(cls, n: int, m: int, typ: RandomGraphType=RandomGraphType.random_undir, seed: Optional[int]=None) -> List[Tuple[int, int]]:
    random.seed(seed)
    if typ == RandomGraphType.random_undir:
      return cls._build_random_undir(n, m)
    raise ValueError(typ)

  @classmethod
  def _build_random_undir(cls, n: int, m: int) -> List[Tuple[int, int]]:
    assert m <= n*(n-1)//2
    edges = set()
    while len(edges) < m:
      u = random.randrange(0, n)
      v = random.randrange(0, n)
      while u == v:
        v = random.randrange(0, n)
      if u > v:
        u, v = v, u
      edges.add((u, v))
    edges = list(edges)
    for i in range(m):
      u, v = edges[i]
      if random.random() < 0.5:
        edges[i] = (v, u)
    random.shuffle(edges)
    assert len(edges) == m
    return edges

