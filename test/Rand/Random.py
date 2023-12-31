from typing import List, Any

class Random():

  _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

  @classmethod
  def _xor(cls) -> int:
    t = (cls._x ^ ((cls._x << 11) & 0xFFFFFFFF)) & 0xFFFFFFFF
    cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
    cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ ((t >> 8))&0xFFFFFFFF) & 0xFFFFFFFF
    return cls._w

  @classmethod
  def random(cls) -> float:
    return cls._xor() / 0xFFFFFFFF

  @classmethod
  def randint(cls, begin: int, end: int) -> int:
    assert begin <= end
    return begin + cls._xor() % (end - begin + 1)

  @classmethod
  def randrange(cls, begin: int, end: int) -> int:
    assert begin < end
    return begin + cls._xor() % (end - begin)

  @classmethod
  def shuffle(cls, a: List[Any]) -> None:
    n = len(a)
    for i in range(n-1):
      j = cls.randrange(i, n)
      a[i], a[j] = a[j], a[i]

