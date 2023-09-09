from array import array
from typing import Iterable, Optional, List

class WordsizeTreeSet():

  def __init__(self, u: int, a: Iterable[int]=[]):
    self.u = u
    data = []
    len_ = 0
    if a:
      u >>= 5
      A = array('I', bytes(4*(u+1)))
      for a_ in a:
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
    if self.data[0][x>>5] >> (x&31) & 1: return False
    for a in self.data:
      a[x>>5] |= 1 << (x&31)
      x >>= 5
    self.len += 1
    return True

  def discard(self, x: int) -> bool:
    if self.data[0][x>>5] >> (x&31) & 1 == 0: return False
    self.len -= 1
    for a in self.data:
      a[x>>5] &= ~(1 << (x&31))
      x >>= 5
      if a[x]: break
    return True

  def ge(self, x: int) -> Optional[int]:
    d = 0
    data = self.data
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
    return self.ge(x + 1)

  def le(self, x: int) -> Optional[int]:
    d = 0
    data = self.data
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
    return self.le(x - 1)

  def get_min(self) -> Optional[int]:
    return self.ge(0)

  def get_max(self) -> Optional[int]:
    return self.le(self.u - 1)

  def pop_min(self) -> int:
    v = self.get_min()
    assert v is not None, 'IndexError: pop_min() from empty WordsizeTreeSet.'
    self.discard(v)
    return v

  def pop_max(self) -> int:
    v = self.get_max()
    assert v is not None, 'IndexError: pop_max() from empty WordsizeTreeSet.'
    self.discard(v)
    return v

  def clear(self) -> None:
    for e in self:
      self.discard(e)
    self.len = 0

  def __bool__(self):
    return self.len > 0

  def __len__(self):
    return self.len

  def __contains__(self, x: int):
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
    return f'WordsizeTreeSet({self})'

