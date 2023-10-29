from Library_py.DataStructures.AVLTree.AVLTreeMultiset import AVLTreeMultiset
from typing import Optional, List, Tuple
import random

class RandomTree():

  def __init__(self, n: int, seed: Optional[int]=None):
    self.n = n
    random.seed(seed)

  def build(self, com='') -> List[Tuple[int, int]]:
    if com == '' or com == 'random':
      return self._build_random()
    if com == 'path':
      return self._build_path()
    raise ValueError(com)
  
  def _build_path(self) -> List[Tuple[int, int]]:
    p = list(range(self.n))
    random.shuffle(p)
    Edge = []
    for i in range(self.n-1):
      Edge.append((p[i], p[i+1]))
    random.shuffle(Edge)
    return Edge

  def _build_random(self) -> List[Tuple[int, int]]:
    Edge = []
    D = [1] * self.n
    A = [0] * (self.n-2)
    for i in range(self.n-2):
      v = random.randrange(0, self.n)
      D[v] += 1
      A[i] = v
    # start = 0
    # for a in A:
    #   v = self.n
    #   for j in range(start, self.n):
    #     if D[j] == 1:
    #       v = j
    #       break
    #     if D[j] < 1 and start == j-1:
    #       start = j
    #   else:
    #     assert False
    #   Edge.append((v, a))
    #   D[v] -= 1
    #   D[a] -= 1

    avl = AVLTreeMultiset((D[i], i) for i in range(self.n))
    for a in A:
      d, v = avl.pop_min()
      assert d == 1
      Edge.append((v, a))
      D[v] -= 1
      avl.remove((D[a], a))
      D[a] -= 1
      if D[a] >= 1:
        avl.add((D[a], a))

    u = D.index(1)
    D[u] -= 1
    v = D.index(1)
    D[v] -= 1
    Edge.append((u, v))
    return Edge

