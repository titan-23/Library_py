# from titan_pylib.algorithm.random.random import Random
from typing import List, Any

class Random():
  '''Random
  乱数系のライブラリです。
  標準ライブラリよりも高速なつもりでいます。
  '''

  def __init__(self):
    self._x = 123456789
    self._y = 362436069
    self._z = 521288629
    self._w = 88675123

  def _xor(self) -> int:
    t = (self._x ^ ((self._x << 11) & 0xFFFFFFFF)) & 0xFFFFFFFF
    self._x, self._y, self._z = self._y, self._z, self._w
    self._w = (self._w ^ (self._w >> 19)) ^ (t ^ ((t >> 8))&0xFFFFFFFF) & 0xFFFFFFFF
    return self._w

  def random(self) -> float:
    """random
    0以上1以下の一様ランダムな値を1つ生成して返すはずです。
    """
    return self._xor() / 0xFFFFFFFF

  def randint(self, begin: int, end: int) -> int:
    """``begin`` 以上 ``end`` **以下** のランダムな整数を返します。
    """
    assert begin <= end
    return begin + self._xor() % (end - begin + 1)

  def randrange(self, begin: int, end: int) -> int:
    """``begin`` 以上 ``end`` **未満** のランダムな整数を返します。
    """
    assert begin < end
    return begin + self._xor() % (end - begin)

  def shuffle(self, a: List[Any]) -> None:
    """インプレースにシャッフルします。

    :math:`O(n)` です。

    Args:
      a (List[Any]): ``a`` をシャッフルします。
    """
    n = len(a)
    for i in range(n-1):
      j = self.randrange(i, n)
      a[i], a[j] = a[j], a[i]


