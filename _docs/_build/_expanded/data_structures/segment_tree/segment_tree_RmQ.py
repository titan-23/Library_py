# from titan_pylib.data_structures.segment_tree.segment_tree_RmQ import SegmentTreeRmQ
# from titan_pylib.data_structures.segment_tree.segment_tree_interface import SegmentTreeInterface
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union, Iterable, Callable, List
T = TypeVar('T')

class SegmentTreeInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               e: T):
    raise NotImplementedError

  @abstractmethod
  def set(self, k: int, v: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def get(self, k: int) -> T:
    raise NotImplementedError

  @abstractmethod
  def prod(self, l: int, r: int) -> T:
    raise NotImplementedError

  @abstractmethod
  def all_prod(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    raise NotImplementedError

  @abstractmethod
  def min_left(self, r: int, f: Callable[[T], bool]) -> int:
    raise NotImplementedError

  @abstractmethod
  def tolist(self) -> List[T]:
    raise NotImplementedError

  @abstractmethod
  def __getitem__(self, k: int) -> T:
    raise NotImplementedError

  @abstractmethod
  def __setitem__(self, k: int, v: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def __str__(self):
    raise NotImplementedError

  @abstractmethod
  def __repr__(self):
    raise NotImplementedError

# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Generic, Iterable, TypeVar, Union, List
T = TypeVar('T', bound=SupportsLessThan)

class SegmentTreeRmQ(SegmentTreeInterface, Generic[T]):
  """RmQ セグ木です。
  """

  def __init__(self, _n_or_a: Union[int, Iterable[T]], e: T) -> None:
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
        _data[i] = _data[i<<1] if _data[i<<1] < _data[i<<1|1] else _data[i<<1|1]
      self._data = _data

  def set(self, k: int, v: T) -> None:
    if k < 0: k += self._n
    assert 0 <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.set({k}: int, {v}: T), n={self._n}'
    k += self._size
    self._data[k] = v
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._data[k<<1] if self._data[k<<1] < self._data[k<<1|1] else self._data[k<<1|1]

  def get(self, k: int) -> T:
    if k < 0: k += self._n
    assert 0 <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.get({k}: int), n={self._n}'
    return self._data[k+self._size]

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self._n, \
        f'IndexError: {self.__class__.__name__}.prod({l}: int, {r}: int)'
    l += self._size
    r += self._size
    res = self._e
    while l < r:
      if l & 1:
        if res > self._data[l]:
          res = self._data[l]
        l += 1
      if r & 1:
        r ^= 1
        if res > self._data[r]:
          res = self._data[r]
      l >>= 1
      r >>= 1
    return res

  def all_prod(self) -> T:
    return self._data[1]

  def max_right(self, l: int, f=lambda lr: lr):
    assert 0 <= l <= self._n, \
        f'IndexError: {self.__class__.__name__}.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'{self.__class__.__name__}.max_right({l}, f), f({self._e}) must be true.'
    if l == self._n: return self._n
    l += self._size
    s = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(min(s, self._data[l])):
        while l < self._size:
          l <<= 1
          if f(min(s, self._data[l])):
            if s > self._data[l]:
              s = self._data[l]
            l += 1
        return l - self._size
      s = min(s, self._data[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  def min_left(self, r: int, f=lambda lr: lr):
    assert 0 <= r <= self._n, \
        f'IndexError: {self.__class__.__name__}.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'{self.__class__.__name__}.min_left({r}, f), f({self._e}) must be true.'
    if r == 0: return 0
    r += self._size
    s = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(min(self._data[r], s)):
        while r < self._size:
          r = r<<1|1
          if f(min(self._data[r], s)):
            if s > self._data[r]:
              s = self._data[r]
            r -= 1
        return r + 1 - self._size
      s = min(self._data[r], s)
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


