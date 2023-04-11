class Random():

  _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

  @classmethod
  def _xor128(cls) -> int:
    t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
    cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
    cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
    return cls._w

  @classmethod
  def random(cls) -> float:
    return cls._xor128() / 0xFFFFFFFF

  @classmethod
  def randint(cls, begin: int, end: int) -> int:
    return begin + cls._xor128() // (0xFFFFFFFF//(end+1-begin))

