# https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
# を少しか変えたもの
import math
from bisect import bisect_left, bisect_right, insort
from typing import Generic, Iterable, Iterator, TypeVar, Union, List
T = TypeVar('T')

class SortedMultiset(Generic[T]):

  BUCKET_RATIO = 50
  REBUILD_RATIO = 170

  def _build(self, a=None) -> None:
    if a is None: a = list(self)
    size = len(a)
    bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
    self.a = [a[size*i//bucket_size : size*(i+1)//bucket_size] for i in range(bucket_size)]

  def __init__(self, a: Iterable[T] = []) -> None:
    a = list(a)
    self.size = len(a)
    if not all(a[i] <= a[i+1] for i in range(self.size-1)):
      a.sort()
    self._build(a)

  def __iter__(self) -> Iterator[T]:
    for i in self.a:
      for j in i: yield j

  def __reversed__(self) -> Iterator[T]:
    for i in reversed(self.a):
      for j in reversed(i): yield j

  def __len__(self) -> int:
    return self.size

  def __repr__(self) -> str:
    return 'SortedMultiset' + str(self.a)

  def __str__(self) -> str:
    s = str(list(self))
    return '{' + s[1 : len(s) - 1] + '}'

  def __bool__(self) -> bool:
    return self.size > 0

  def _find_bucket(self, x: T) -> List[T]:
    for a in self.a:
      if x <= a[-1]: return a
    return a

  def __contains__(self, x: T) -> bool:
    if self.size == 0: return False
    a = self._find_bucket(x)
    i = bisect_left(a, x)
    return i != len(a) and a[i] == x

  def count(self, x: T) -> int:
    return self.range_cnt(x, x)

  def add(self, x: T) -> None:
    if self.size == 0:
      self.a = [[x]]
      self.size = 1
      return
    a = self._find_bucket(x)
    insort(a, x)
    self.size += 1
    if len(a) > len(self.a) * self.REBUILD_RATIO:
      self._build()

  def discard(self, x: T) -> bool:
    if self.size == 0: return False
    a = self._find_bucket(x)
    i = bisect_left(a, x)
    if i == len(a) or a[i] != x: return False
    a.pop(i)
    self.size -= 1
    if len(a) == 0: self._build()
    return True

  def lt(self, x: T) -> Union[T, None]:
    for a in reversed(self.a):
      if a[0] < x:
        return a[bisect_left(a, x) - 1]

  def le(self, x: T) -> Union[T, None]:
    for a in reversed(self.a):
      if a[0] <= x:
        return a[bisect_right(a, x) - 1]

  def gt(self, x: T) -> Union[T, None]:
    for a in self.a:
      if a[-1] > x:
        return a[bisect_right(a, x)]

  def ge(self, x: T) -> Union[T, None]:
    for a in self.a:
      if a[-1] >= x:
        return a[bisect_left(a, x)]

  def __getitem__(self, k: int) -> T:
    if k < 0:
      for a in reversed(self.a):
        k += len(a)
        if k >= 0: return a[k]
    else:
      for a in self.a:
        if k < len(a): return a[k]
        k -= len(a)
    raise IndexError

  def index(self, x: T) -> int:
    ans = 0
    for a in self.a:
      if a[-1] >= x:
        return ans + bisect_left(a, x)
      ans += len(a)
    return ans

  def index_right(self, x: T) -> int:
    ans = 0
    for a in self.a:
      if a[-1] > x:
        return ans + bisect_right(a, x)
      ans += len(a)
    return ans

  def _pop(self, a: List[T], k: int) -> T:
    ans = a.pop(k)
    self.size -= 1
    if not a: self._build()
    return ans

  def pop(self, k: int=-1) -> T:
    if k < 0:
      for a in reversed(self.a):
        k += len(a)
        if k >= 0: return self._pop(a, k)
    else:
      for a in self.a:
        if k < len(a): return self._pop(a, k)
        k -= len(a)
    raise IndexError

  def pop_min(self) -> T:
    a = self.a[0]
    x = a.pop(0)
    self.size -= 1
    if len(a) == 0: self._build()
    return x

  def range_cnt(self, l: T, r: T) -> int:
    "l以上r以下の要素数"
    ans_l = 0
    ans_r = 0
    flag = True
    for a in self.a:
      if flag and a[-1] >= l:
        flag = False
        ans_l += bisect_left(a, l)
      if a[-1] > r:
        return ans_r + bisect_right(a, r) - ans_l
      if flag: ans_l += len(a)
      ans_r += len(a)
    return ans_r - ans_l

