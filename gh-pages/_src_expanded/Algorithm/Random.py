class Random():

  _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

  x = 2463534242

  @classmethod
  def random32(cls) -> int:
    cls.x ^= cls.x << 13 & 0xFFFFFFFF
    cls.x ^= cls.x >> 17
    cls.x ^= cls.x << 5  & 0xFFFFFFFF
    return cls.x & 0xFFFFFFFF

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
    assert begin <= end
    return begin + cls._xor128() % (end - begin + 1)

  @classmethod
  def randrange(cls, begin: int, end: int) -> int:
    assert begin < end
    return begin + cls._xor128() % (end - begin)


