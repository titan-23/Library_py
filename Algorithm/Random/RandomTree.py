from typing import Optional
import random

class RandomTree():

  def __init__(self, n: int, seed: Optional[int]=None):
    self.n = n
    random.seed(seed)

  def build(self):
    Edge = []
    D = [1] * self.n
    A = [0] * (self.n-2)
    for i in range(self.n-2):
      v = random.randrange(0, self.n)
      D[v] += 1
      A[i] = v
    start = 0
    for a in A:
      v = self.n
      for j in range(start, self.n):
        if D[j] == 1:
          v = j
          break
        if D[j] < 1 and start == j-1:
          start = j
      else:
        assert False
      Edge.append((v, a))
      D[v] -= 1
      D[a] -= 1
    u = D.index(1)
    D[u] -= 1
    v = D.index(1)
    D[v] -= 1
    Edge.append((u, v))
    return Edge

