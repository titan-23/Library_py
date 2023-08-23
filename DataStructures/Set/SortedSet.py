# https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, TypeVar, Union, List, Optional
T = TypeVar('T')

class SortedSet(Generic[T]):

  BUCKET_RATIO = 50
  REBUILD_RATIO = 170

  def _build(self, a=None) -> None:
    if a is None: a = list(self)
    size = self.size = len(a)
    bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
    self.a = [a[size*i//bucket_size : size*(i+1)//bucket_size] for i in range(bucket_size)]

  def __init__(self, a: Iterable[T] = []) -> None:
    a = list(a)
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
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
    return f"SortedSet({self})"

  def __str__(self) -> str:
    return "{" + ', '.join(map(str, self)) + "}"

  def _find_bucket(self, x: T) -> List[T]:
    for a in self.a:
      if x <= a[-1]: return a
    return a

  def __contains__(self, x: T) -> bool:
    if self.size == 0: return False
    a = self._find_bucket(x)
    i = bisect_left(a, x)
    return i != len(a) and a[i] == x

  def add(self, x: T) -> bool:
    if self.size == 0:
      self.a = [[x]]
      self.size = 1
      return True
    a = self._find_bucket(x)
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x: return False
    a.insert(i, x)
    self.size += 1
    if len(a) > len(self.a) * self.REBUILD_RATIO:
      self._build()
    return True

  def discard(self, x: T) -> bool:
    if self.size == 0: return False
    a = self._find_bucket(x)
    i = bisect_left(a, x)
    if i == len(a) or a[i] != x: return False
    a.pop(i)
    self.size -= 1
    if len(a) == 0: self._build()
    return True

  def lt(self, x: T) -> Optional[T]:
    for a in reversed(self.a):
      if a[0] < x:
        return a[bisect_left(a, x) - 1]

  def le(self, x: T) -> Optional[T]:
    for a in reversed(self.a):
      if a[0] <= x:
        return a[bisect_right(a, x) - 1]

  def gt(self, x: T) -> Optional[T]:
    for a in self.a:
      if a[-1] > x:
        return a[bisect_right(a, x)]

  def ge(self, x: T) -> Optional[T]:
    for a in self.a:
      if a[-1] >= x:
        return a[bisect_left(a, x)]

  # s[-1]はO(1)
  def __getitem__(self, x: int) -> T:
    if x < 0: x += self.size
    if x < 0: raise IndexError
    if x == self.size-1:
      return self.a[-1][-1]
    for a in self.a:
      if x < len(a): return a[x]
      x -= len(a)
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

  def pop(self, k: int=-1) -> T:
    if k < 0: k += self.size
    if k == self.size-1:
      a = self.a[-1]
      x = a.pop()
      self.size -= 1
    else:
      for a in self.a:
        if k < len(a):
          x = a.pop(k)
          self.size -= 1
          break
        k -= len(a)
    if len(a) == 0: self._build()
    return x

  def pop_min(self) -> T:
    a = self.a[0]
    x = a.pop(0)
    self.size -= 1
    if len(a) == 0: self._build()
    return x

  def range_cnt(self, l: T, r: T) -> int:
    "index_right(r) - index(l)"
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

