from math import ceil, sqrt
from array import array
from itertools import chain
from typing import Iterable, Union

class QuadraticDivisionList():

  BUCKET_RATIO = 50
  REBUILD_RATIO = 170
  BUCKET_LIM = 100

  def __init__(self, n_or_a: Union[int, Iterable[int]]):
    a = [0] * n_or_a if isinstance(n_or_a, int) else list(n_or_a)
    self.n = len(a)
    self.bucket_size = int(ceil(sqrt(self.n / self.BUCKET_RATIO)))
    self.bucket_cnt = (self.n+self.bucket_size-1) // self.bucket_size
    self.data = [array('I', a[k*self.bucket_size:(k+1)*self.bucket_size]) for k in range(self.bucket_cnt)]
    self.bucket_data = array('I', (sum(v) for v in self.data))

  def _rebuild(self):
    a = list(chain.from_iterable(self.data))
    self.n = len(a)
    self.bucket_size = int(ceil(sqrt(self.n / self.BUCKET_RATIO)))
    self.bucket_cnt = (self.n+self.bucket_size-1) // self.bucket_size
    self.data = [array('I', a[k*self.bucket_size:(k+1)*self.bucket_size]) for k in range(self.bucket_cnt)]
    self.bucket_data = array('I', (sum(v) for v in self.data))

  def insert(self, k: int, v: int) -> None:
    assert v == 0 or v == 1
    self.n += 1
    if k < len(self) // 2:
      for i, a in enumerate(self.data):
        if k <= len(a):
          a.insert(k, v)
          self.bucket_data[i] += v
          if len(a) > self.BUCKET_LIM and len(a) > len(self.data) * self.REBUILD_RATIO:
            self._rebuild()
          return
        k -= len(a)
    else:
      l = len(self) - 1
      for i in range(self.bucket_cnt-1, -1, -1):
        a = self.data[i]
        l -= len(a)
        if k >= l:
          a.insert(k-l, v)
          self.bucket_data[i] += v
          if len(a) > self.BUCKET_LIM and len(a) > len(self.data) * self.REBUILD_RATIO:
            self._rebuild()
          return
    assert False, f'IndexError: insert'

  def pop(self, k: int) -> int:
    self.n -= 1
    if k < len(self) // 2:
      for i, a in enumerate(self.data):
        if k < len(a):
          v = a.pop(k)
          self.bucket_data[i] -= v
          if not a:
            self._rebuild()
          return v
        k -= len(a)
    else:
      l = len(self) + 1
      for i in range(self.bucket_cnt-1, -1, -1):
        a = self.data[i]
        l -= len(a)
        if k >= l:
          v = a.pop(k-l)
          self.bucket_data[i] -= v
          if not a:
            self._rebuild()
          return v
    assert False, f'IndexError'

  def prod(self, l: int, r: int) -> int:
    '''Return sum(a[l, r)). / 0 <= l <= r <= n / O(√N)'''
    assert 0 <= l <= r <= len(self)
    if l == r: return 0
    s = 0
    k = 0
    for i in range(self.bucket_cnt):
      d = self.data[i]
      if l <= k + len(d) < r:
        s += self.bucket_data[i]
      elif k + len(d) <= l:
        pass
      elif k + len(d) < r:
        break
      else:
        for j in range(k, k + len(d)):
          if l <= j < r:
            s += d[j-k]
      k += len(d)
    return s

  def __getitem__(self, k: int) -> int:
    for a in self.data:
      if k < len(a):
        return a[k]
      k -= len(a)
    assert False, f'IndexError'

  def __setitem__(self, k: int, x: int):
    assert x == 0 or x == 1
    for i, a in enumerate(self.data):
      if k < len(a):
        self.bucket_data[i] -= a[k]
        self.bucket_data[i] += x
        a[k] = x
        return
      k -= len(a)
    assert False, f'IndexError'

  def __len__(self):
    return self.n

  def __str__(self):
    return str(list(chain.from_iterable(self.data)))

