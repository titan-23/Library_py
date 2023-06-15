from typing import List

class CumulativeSum2D():

  def __init__(self, h: int, w: int, a: List[List[int]]):
    acc = [[0]*(w+1) for _ in range(h+1)]
    for i in range(h):
      for j in range(w):
        acc[i+1][j+1] = acc[i][j+1] + acc[i+1][j] - acc[i][j] + a[i][j]
    self.h = h
    self.w = w
    self.acc = acc

  def sum(self, h1: int, w1: int, h2: int, w2: int) -> int:
    assert h1 <= h2 and w1 <= w2, f'IndexError'
    return self.acc[h2][w2] - self.acc[h2][w1] - self.acc[h1][w2] + self.acc[h1][w1]

