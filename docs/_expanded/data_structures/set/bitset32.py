# from titan_pylib.data_structures.set.bitset32 import Bitset32
from typing import List
from array import array

class Bitset32():

  TABLE = array('I', (1 << i for i in range(32)))

  def __init__(self, u: int):
    self._size = (u >> 5) + 1
    self._data = array('I', bytes(self._size*4))

  def add(self, k: int) -> None:
    self._data[k>>5] |= Bitset32.TABLE[k & 31]

  def discard(self, k: int) -> None:
    self._data[k>>5] &= ~Bitset32.TABLE[k & 31]

  def flip(self, k: int) -> None:
    self._data[k>>5] ^= Bitset32.TABLE[k & 31]

  def __contains__(self, k: int) -> bool:
    return self._data[k>>5] >> (k & 31) & 1 == 1

  def __getitem__(self, k: int):
    return self._data[k>>5] >> (k & 31) & 1

  def __setitem__(self, k: int, bit: bool):
    if bit:
      self._data[k>>5] |= Bitset32.TABLE[k & 31]
    else:
      self._data[k>>5] &= ~Bitset32.TABLE[k & 31]

  def tolist(self) -> List[int]:
    return [(i<<5)+j for i, a in enumerate(self._data) for j in range(32) if a >> j & 1 == 1]

  def __ior__(self, other: 'Bitset32'):
    s = self._data
    o = other._data
    for i in range(min(len(s), len(o))):
      s[i] |= o[i]
    return self

  def __rshift__(self, k: int):
    # x >> y: x.__rshift__(y)
    pass

  def __rrshift__(self, k: int):
    pass

  def __str__(self):
    return str(self.tolist())


