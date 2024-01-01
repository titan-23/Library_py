# from Library_py.DataStructures.Set.WordsizeTreeSet import WordsizeTreeSet
from array import array
from typing import Iterable, Optional, List

class WordsizeTreeSet():

  def __init__(self, u: int, a: Iterable[int]=[]):
    assert u > 0
    self.u = u
    data = []
    len_ = 0
    if a:
      u >>= 5
      A = array('I', bytes(4*(u+1)))
      for a_ in a:
        assert 0 <= a_ < u, \
            f'ValueError: {self.__class__.__name__}.__init__, {a_}, u={u}'
        if A[a_>>5] >> (a_&31) & 1 == 0:
          len_ += 1
          A[a_>>5] |= 1 << (a_&31)
      data.append(A)
      while u:
        a = array('I', bytes(4*((u>>5)+1)))
        for i in range(u+1):
          if A[i]:
            a[i>>5] |= 1 << (i&31)
        data.append(a)
        A = a
        u >>= 5
    else:
      while u:
        u >>= 5
        data.append(array('I', bytes(4*(u+1))))
    self.data: List[array[int]] = data
    self.len: int = len_
    self.len_data: int = len(data)

  def add(self, x: int) -> bool:
    assert 0 <= x < self.u, \
        f'ValueError: {self.__class__.__name__}.add({x}), u={self.u}'
    if self.data[0][x>>5] >> (x&31) & 1: return False
    self.len += 1
    for a in self.data:
      a[x>>5] |= 1 << (x&31)
      x >>= 5
    return True

  def discard(self, x: int) -> bool:
    assert 0 <= x < self.u, \
        f'ValueError: {self.__class__.__name__}.discard({x}), u={self.u}'
    if self.data[0][x>>5] >> (x&31) & 1 == 0: return False
    self.len -= 1
    for a in self.data:
      a[x>>5] &= ~(1 << (x&31))
      x >>= 5
      if a[x]: break
    return True

  def ge(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: {self.__class__.__name__}.ge({x}), u={self.u}'
    data = self.data
    d = 0
    while True:
      if d >= self.len_data or x>>5 >= len(data[d]): return None
      m = data[d][x>>5] & ((~0) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) + 1
      else:
        x = (x >> 5 << 5) + (m & -m).bit_length() - 1
        if d == 0: break
        x <<= 5
        d -= 1
    return x

  def gt(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: {self.__class__.__name__}.gt({x}), u={self.u}'
    if x + 1 == self.u: return
    return self.ge(x + 1)

  def le(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: {self.__class__.__name__}.le({x}), u={self.u}'
    data = self.data
    d = 0
    while True:
      if x < 0 or d >= self.len_data: return None
      m = data[d][x>>5] & ~((~1) << (x&31))
      if m == 0:
        d += 1
        x = (x >> 5) - 1
      else:
        x = (x >> 5 << 5) + m.bit_length() - 1
        if d == 0: break
        x <<= 5
        x += 31
        d -= 1
    return x

  def lt(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: {self.__class__.__name__}.lt({x}), u={self.u}'
    if x - 1 == 0: return
    return self.le(x - 1)

  def get_min(self) -> Optional[int]:
    return self.ge(0)

  def get_max(self) -> Optional[int]:
    return self.le(self.u - 1)

  def pop_min(self) -> int:
    v = self.get_min()
    assert v is not None, \
        f'IndexError: pop_min() from empty {self.__class__.__name__}.'
    self.discard(v)
    return v

  def pop_max(self) -> int:
    v = self.get_max()
    assert v is not None, \
        f'IndexError: pop_max() from empty {self.__class__.__name__}.'
    self.discard(v)
    return v

  def clear(self) -> None:
    for e in self:
      self.discard(e)
    self.len = 0

  def tolist(self) -> List[int]:
    return [x for x in self]

  def __bool__(self):
    return self.len > 0

  def __len__(self):
    return self.len

  def __contains__(self, x: int):
    assert 0 <= x < self.u, \
        f'ValueError: {x} in {self.__class__.__name__}, u={self.u}'
    return self.data[0][x>>5] >> (x&31) & 1 == 1

  def __iter__(self):
    self._val = self.ge(0)
    return self

  def __next__(self):
    if self._val is None:
      raise StopIteration
    pre = self._val
    self._val = self.gt(pre)
    return pre

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return f'{self.__class__.__name__}({self.u}, {self})'


