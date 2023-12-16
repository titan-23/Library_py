from Library_py.DataStructures.SegmentTree.SegmentTreeInterface import SegmentTreeInterface
from Library_py.MyClass.SupportsAdd import SupportsAdd
from typing import Generic, Iterable, TypeVar, Union, List
T = TypeVar('T', bound=SupportsAdd)

class SegmentTreeRSQ(SegmentTreeInterface, Generic[T]):

  def __init__(self, _n_or_a: Union[int, Iterable[T]], e: T=0) -> None:
    self._e = e
    if isinstance(_n_or_a, int):
      self._n = _n_or_a
      self._log = (self._n - 1).bit_length()
      self._size = 1 << self._log
      self._data = [self._e] * (self._size << 1)
    else:
      _n_or_a = list(_n_or_a)
      self._n = len(_n_or_a)
      self._log = (self._n - 1).bit_length()
      self._size = 1 << self._log
      _data = [self._e] * (self._size << 1)
      _data[self._size:self._size+self._n] = _n_or_a
      for i in range(self._size-1, 0, -1):
        _data[i] = _data[i<<1] + _data[i<<1|1]
      self._data = _data

  def set(self, k: int, v: T) -> None:
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.set({k}: int, {v}: T), n={self._n}'
    if k < 0: k += self._n
    k += self._size
    self._data[k] = v
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._data[k<<1] + self._data[k<<1|1]

  def get(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.get({k}: int), n={self._n}'
    if k < 0: k += self._n
    return self._data[k+self._size]

  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n, \
        f'IndexError: {self.__class__.__name__}.prod({l}: int, {r}: int)'
    l += self._size
    r += self._size
    res = self._e
    while l < r:
      if l & 1:
        res += self._data[l]
        l += 1
      if r & 1:
        res += self._data[r^1]
      l >>= 1
      r >>= 1
    return res

  def all_prod(self):
    return self._data[1]

  def max_right(self, l: int, f=lambda lr: lr):
    assert 0 <= l <= self._n, \
        f'IndexError: {self.__class__.__name__}.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'{self.__class__.__name__}.max_right({l}, f), f({self._e}) must be true.'
    if l == self._n:
      return self._n
    l += self._size
    s = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(s + self._data[l]):
        while l < self._size:
          l <<= 1
          if f(s + self._data[l]):
            s += self._data[l]
            l += 1
        return l - self._size
      s += self._data[l]
      l += 1
      if l & -l == l:
        break
    return self._n

  def min_left(self, r: int, f=lambda lr: lr):
    assert 0 <= r <= self._n, \
        f'IndexError: {self.__class__.__name__}.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'{self.__class__.__name__}.min_left({r}, f), f({self._e}) must be true.'
    if r == 0:
      return 0
    r += self._size
    s = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._data[r] + s):
        while r < self._size:
          r = r<<1|1
          if f(self._data[r] + s):
            s += self._data[r]
            r -= 1
        return r + 1 - self._size
      s += self._data[r]
      if r & -r == r:
        break
    return 0

  def tolist(self) -> List[T]:
    return [self.get(i) for i in range(self._n)]

  def show(self) -> None:
    print(f'<{self.__class__.__name__}> [\n' + '\n'.join(['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]) + '\n]')

  def __getitem__(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.__getitem__({k}: int), n={self._n}'
    return self.get(k)

  def __setitem__(self, k: int, v: T):
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.__setitem__{k}: int, {v}: T), n={self._n}'
    self.set(k, v)

  def __str__(self):
    return '[' + ', '.join(map(str, (self.get(i) for i in range(self._n)))) + ']'

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'

