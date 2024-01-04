from typing import List, Any

class Random():
  '''Random
  乱数系のライブラリです。
  標準ライブラリよりも高速なつもりでいます。
  '''

  _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

  @classmethod
  def _xor(cls) -> int:
    t = (cls._x ^ ((cls._x << 11) & 0xFFFFFFFF)) & 0xFFFFFFFF
    cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
    cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ ((t >> 8))&0xFFFFFFFF) & 0xFFFFFFFF
    return cls._w

  @classmethod
  def random(cls) -> float:
    """random
    0以上1以下の一様ランダムな値を1つ生成して返すはずです。
    """
    return cls._xor() / 0xFFFFFFFF

  @classmethod
  def randint(cls, begin: int, end: int) -> int:
    """``begin`` 以上 ``end`` **以下** のランダムな整数を返します。
    """
    assert begin <= end
    return begin + cls._xor() % (end - begin + 1)

  @classmethod
  def randrange(cls, begin: int, end: int) -> int:
    """``begin`` 以上 ``end`` **未満** のランダムな整数を返します。
    """
    assert begin < end
    return begin + cls._xor() % (end - begin)

  @classmethod
  def shuffle(cls, a: List[Any]) -> None:
    """インプレースにシャッフルします。

    :math:`O(n)` です。

    Args:
      a (List[Any]): ``a`` をシャッフルします。
    """
    n = len(a)
    for i in range(n-1):
      j = cls.randrange(i, n)
      a[i], a[j] = a[j], a[i]

