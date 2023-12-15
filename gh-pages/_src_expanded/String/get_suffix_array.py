# from Library_py.String.get_suffix_array import get_suffix_array
# from Library_py.String.HashString import HashString
# ref: https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
# from Library_py.DataStructures.SegmentTree.SegmentTree import SegmentTree
# from Library_py.DataStructures.SegmentTree.SegmentTreeInterface import SegmentTreeInterface
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

from typing import Generic, Iterable, TypeVar, Callable, Union, List
T = TypeVar('T')

class SegmentTree(SegmentTreeInterface, Generic[T]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               e: T) -> None:
    self._op = op
    self._e = e
    if isinstance(n_or_a, int):
      self._n = n_or_a
      self._log = (self._n - 1).bit_length()
      self._size = 1 << self._log
      self._data = [e] * (self._size << 1)
    else:
      n_or_a = list(n_or_a)
      self._n = len(n_or_a)
      self._log = (self._n - 1).bit_length()
      self._size = 1 << self._log
      _data = [e] * (self._size << 1)
      _data[self._size:self._size+self._n] = n_or_a
      for i in range(self._size-1, 0, -1):
        _data[i] = op(_data[i<<1], _data[i<<1|1])
      self._data = _data

  def set(self, k: int, v: T) -> None:
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.set({k}, {v}), n={self._n}'
    if k < 0:
      k += self._n
    k += self._size
    self._data[k] = v
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._op(self._data[k<<1], self._data[k<<1|1])

  def get(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.get({k}), n={self._n}'
    if k < 0:
      k += self._n
    return self._data[k+self._size]

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self._n, \
        f'IndexError: SegmentTree.prod({l}, {r})'
    l += self._size
    r += self._size
    lres = self._e
    rres = self._e
    while l < r:
      if l & 1:
        lres = self._op(lres, self._data[l])
        l += 1
      if r & 1:
        rres = self._op(self._data[r^1], rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  def all_prod(self) -> T:
    return self._data[1]

  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    '''Find the largest index R s.t. f([l, R)) == True. / O(logN)'''
    assert 0 <= l <= self._n, \
        f'IndexError: SegmentTree.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'SegmentTree.max_right({l}, f), f({self._e}) must be true.'
    if l == self._n:
      return self._n
    l += self._size
    s = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self._op(s, self._data[l])):
        while l < self._size:
          l <<= 1
          if f(self._op(s, self._data[l])):
            s = self._op(s, self._data[l])
            l |= 1
        return l - self._size
      s = self._op(s, self._data[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  def min_left(self, r: int, f: Callable[[T], bool]) -> int:
    '''Find the smallest index L s.t. f([L, r)) == True. / O(logN)'''
    assert 0 <= r <= self._n, \
        f'IndexError: SegmentTree.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'SegmentTree.min_left({r}, f), f({self._e}) must be true.'
    if r == 0:
      return 0
    r += self._size
    s = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._op(self._data[r], s)):
        while r < self._size:
          r = r << 1 | 1
          if f(self._op(self._data[r], s)):
            s = self._op(self._data[r], s)
            r ^= 1
        return r + 1 - self._size
      s = self._op(self._data[r], s)
      if r & -r == r:
        break
    return 0

  def tolist(self) -> List[T]:
    return [self.get(i) for i in range(self._n)]

  def show(self) -> None:
    print('<SegmentTree> [\n' + '\n'.join(['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]) + '\n]')

  def __getitem__(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.__getitem__({k}), n={self._n}'
    return self.get(k)

  def __setitem__(self, k: int, v: T):
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.__setitem__{k}, {v}), n={self._n}'
    self.set(k, v)

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'SegmentTree({self})'

from typing import Optional, List, Dict, Final
import random
import string
_titan23_HashString_MOD: Final[int] = (1 << 61) - 1
_titan23_HashString_DIC: Final[Dict[str, int]] = {c: i for i, c in enumerate(string.ascii_lowercase, 1)}
_titan23_HashString_MASK30: Final[int] = (1 << 30) - 1
_titan23_HashString_MASK31: Final[int] = (1 << 31) - 1
_titan23_HashString_MASK61: Final[int] = _titan23_HashString_MOD

class HashStringBase():

  def __init__(self, n: int, base: int=-1, seed: Optional[int]=None) -> None:
    random.seed(seed)
    base = random.randint(37, 10**9) if base < 0 else base
    powb = [1] * (n+1)
    invb = [1] * (n+1)
    invbpow = pow(base, -1, _titan23_HashString_MOD)
    for i in range(1, n+1):
      powb[i] = HashStringBase.get_mul(powb[i-1], base)
      invb[i] = HashStringBase.get_mul(invb[i-1], invbpow)
    self.n = n
    self.powb = powb
    self.invb = invb

  @staticmethod
  def get_mul(a: int, b: int) -> int:
    au = a >> 31
    ad = a & _titan23_HashString_MASK31
    bu = b >> 31
    bd = b & _titan23_HashString_MASK31
    mid = ad * bu + au * bd
    midu = mid >> 30
    midd = mid & _titan23_HashString_MASK30
    return HashStringBase.get_mod(au * bu * 2 + midu + (midd << 31) + ad * bd)

  @staticmethod
  def get_mod(x: int) -> int:
    xu = x >> 61
    xd = x & _titan23_HashString_MASK61
    res = xu + xd
    if res >= _titan23_HashString_MOD:
      res -= _titan23_HashString_MOD
    return res

  def unite(self, h1: int, h2: int, k: int) -> int:
    # len(h2) == k
    # h1 <- h2
    return self.get_mod(self.get_mul(h1, self.powb[k]) + h2)

class HashString():

  def __init__(self, hsb: HashStringBase, s: str, update: bool=False) -> None:
    n = len(s)
    data = [0] * n
    acc = [0] * (n+1)
    powb = hsb.powb
    for i, c in enumerate(s):
      data[i] = hsb.get_mul(powb[n-i-1], _titan23_HashString_DIC[c])
      acc[i+1] = hsb.get_mod(acc[i] + data[i])
    self.hsb = hsb
    self.n = n
    self.acc = acc
    self.used_seg = False
    if update:
      self.seg = SegmentTree(data, lambda s, t: (s+t)%_titan23_HashString_MOD, 0)

  def get(self, l: int, r: int) -> int:
    if self.used_seg:
      return self.hsb.get_mul(self.seg.prod(l, r), self.hsb.invb[self.n-r])
    return self.hsb.get_mul(self.hsb.get_mod(self.acc[r]-self.acc[l]), self.hsb.invb[self.n-r])

  def __getitem__(self, k: int) -> int:
    return self.get(k, k+1)

  def set(self, k: int, c: str) -> None:
    self.used_seg = True
    self.seg[k] = self.hsb.get_mul(self.hsb.powb[self.n-k-1], _titan23_HashString_DIC[c])

  def __setitem__(self, k: int, c: str) -> None:
    return self.set(k, c)

  def __len__(self):
    return self.n

  def get_lcp(self) -> List[int]:
    a = [0] * self.n
    memo = [-1] * (self.n+1)
    for i in range(self.n):
      ok, ng = 0, self.n-i+1
      while ng - ok > 1:
        mid = (ok + ng) >> 1
        if memo[mid] == -1:
          memo[mid] = self.get(0, mid)
        if memo[mid] == self.get(i, i+mid):
          ok = mid
        else:
          ng = mid
      a[i] = ok
    return a

# from Library_py.Algorithm.Sort.merge_sort import merge_sort
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Iterable, TypeVar, Callable, List
from __pypy__ import newlist_hint
T = TypeVar('T', bound=SupportsLessThan)

def merge_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:
  def _sort(a: List[T]) -> List[T]:
    n = len(a)
    if n <= 1:
      return a
    if n == 2:
      if not key(a[0], a[1]):
        a[0], a[1] = a[1], a[0]
      return a
    left = _sort(a[:n//2])
    right = _sort(a[n//2:])
    res = newlist_hint(n)
    i, j, l, r = 0, 0, len(left), len(right)
    while i < l and j < r:
      if key(left[i], right[j]):
        res.append(left[i])
        i += 1
      else:
        res.append(right[j])
        j += 1
    for i in range(i, l):
      res.append(left[i])
    for j in range(j, r):
      res.append(right[j])
    return res
  return _sort(list(a))

from typing import List

def get_suffix_array(s: str, hs: HashString) -> List[int]:
  def cmp(u: int, v: int) -> bool:
    ok, ng = 0, min(n-u, n-v)
    while ng - ok > 1:
      mid = (ok + ng) >> 1
      if hs.get(u, u+mid) == hs.get(v, v+mid):
        ok = mid
      else:
        ng = mid
    return s[u+ok] < s[v+ok]
  n = len(s)
  return merge_sort(range(n), key=cmp)


