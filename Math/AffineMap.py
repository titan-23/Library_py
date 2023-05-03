from typing import List, Tuple
from math import sin, cos, radians

class AffineMap():

  # 平面のアフィン変換クラス
  # 
  # 使い方:
  # - mat = AffineMap.new()
  # 

  def _matmul3(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    res = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
      for k in range(3):
        for j in range(3):
          res[i][j] += b[k][j] * a[i][k]
    return res

  @classmethod
  def new(cls) -> List[List[float]]:
    return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

  @classmethod
  def shift(cls, a: List[float], shift_x: float=0, shift_y: float=0) -> List[float]:
    b = [[1, 0, shift_x], [0, 1, shift_y], [0, 0, 1]]
    return cls._matmul3(b, a)

  @classmethod
  def expand(cls, a: List[float], ratio_x: float=1, ratio_y: float=1) -> List[float]:
    b = [[ratio_x, 0, 0], [0, ratio_y, 0], [0, 0, 1]]
    return cls._matmul3(b, a)

  @classmethod
  def rotate(cls, a: List[List[float]], theta: float=0) -> List[List[float]]:
    if theta == 90:
     b = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    elif theta == -90:
     b = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
    else:
      theta = radians(theta)
      b = [[cos(theta), -sin(theta), 0], [sin(theta), cos(theta), 0], [0, 0, 1]]
    return cls._matmul3(b, a)

  @classmethod
  def x_symmetrical_move(cls, a: List[List[float]], p: float) -> List[List[float]]:
    b = [[-1, 0, 2*p], [0, 1, 0], [0, 0, 1]]
    return cls._matmul3(b, a)

  @classmethod
  def y_symmetrical_move(cls, a: List[List[float]], p: float) -> List[List[float]]:
    b = [[1, 0, 0], [0, -1, 2*p], [0, 0, 1]]
    return cls._matmul3(b, a)

  @staticmethod
  def get(a: List[float], x: float, y: float) -> Tuple[float, float]:
    a0, a1, _ = a
    x, y = a0[0]*x + a0[1]*y + a0[2], a1[0]*x + a1[1]*y + a1[2]
    return x, y

