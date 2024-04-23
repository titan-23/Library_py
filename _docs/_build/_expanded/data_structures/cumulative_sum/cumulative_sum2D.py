# from titan_pylib.data_structures.cumulative_sum.cumulative_sum2D import CumulativeSum2D
from typing import List

class CumulativeSum2D():
  """2次元累積和です。
  """

  def __init__(self, h: int, w: int, a: List[List[int]]):
    """``h x w`` の配列 ``a`` から2次元累積和の前計算をします。
    :math:`O(hw)` です。

    Args:
      h (int): 行数です。
      w (int): 列数です。
      a (List[List[int]]):  ``CumulativeSum2D`` を構築する配列です。
    """
    acc = [0] * ((h+1)*(w+1))
    for ij in range(h*w):
      i, j = divmod(ij, w)
      acc[(i+1)*(w+1)+j+1] = acc[i*(w+1)+j+1] + acc[(i+1)*(w+1)+j] - acc[i*(w+1)+j] + a[i][j]
    self.h = h
    self.w = w
    self.acc = acc

  def sum(self, h1: int, w1: int, h2: int, w2: int) -> int:
    """長方形領域 ``[h1, h2) x [w1, w2)`` の総和を返します。
    :math:`O(hw)` です。

    Args:
      h1 (int):
      w1 (int):
      h2 (int):
      w2 (int):
    """
    assert h1 <= h2, f'IndexError: {self.__class__.__name__}.sum({h1}, {w1}, {h2}, {w2}), h={self.h}'
    assert w1 <= w2, f'IndexError: {self.__class__.__name__}.sum({h1}, {w1}, {h2}, {w2}), w={self.w}'
    return self.acc[h2*(self.w+1)+w2] - self.acc[h2*(self.w+1)+w1] - self.acc[h1*(self.w+1)+w2] + self.acc[h1*(self.w+1)+w1]

