from typing import Union, Callable, TypeVar, Generic, Iterable
from functools import reduce
T = TypeVar("T")
F = TypeVar("F")


class LazyQuadraticDivision(Generic[T, F]):

  def __init__(self, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], mapping: Callable[[F, T], T], composition: Callable[[F, F], F], e: T=None):
    if isinstance(n_or_a, int):
      self.n = n_or_a
      a = [e] * self.n
    else:
      a = list(n_or_a)
      self.n = len(a)
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.size = int(self.n**.5) + 1
    self.bucket_cnt = (self.n+self.size-1) // self.size
    self.data = [a[k*self.size:(k+1)*self.size] for k in range(self.bucket_cnt)]
    self.bucket_data = [reduce(self.op, v) for v in self.data]
    self.bucket_lazy = [None] * self.bucket_cnt
 
  '''Applay f to a[l:r). / O(√N)'''
  def apply(self, l: int, r: int, f: F) -> None:
    assert 0 <= l <= r <= self.n
    def _change_data(k: int, l: int, r: int) -> None:
      self._propagate(k)
      self.data[k][l:r] = [self.mapping(f, d) for d in self.data[k][l:r]]
      self.bucket_data[k] = reduce(self.op, self.data[k])
 
    k1 = l // self.size
    k2 = r // self.size
    l -= k1 * self.size
    r -= k2 * self.size
    if k1 == k2:
      if k1 < self.bucket_cnt: _change_data(k1, l, r)
    else:
      if k1 < self.bucket_cnt:
        if l == 0:
          self.bucket_lazy[k1] = f if self.bucket_lazy[k1] is None else self.composition(f, self.bucket_lazy[k1])
          self.bucket_data[k1] = self.mapping(f, self.bucket_data[k1])
        else:
          _change_data(k1, l, len(self.data[k1]))

      for i in range(k1+1, k2):
        self.bucket_lazy[i] = f if self.bucket_lazy[i] is None else self.composition(f, self.bucket_lazy[i])
        self.bucket_data[i] = self.mapping(f, self.bucket_data[i])

      if k2 < self.bucket_cnt:
        if r == len(self.data[k2]):
          self.bucket_lazy[k2] = f if self.bucket_lazy[k2] is None else self.composition(f, self.bucket_lazy[k2])
          self.bucket_data[k2] = self.mapping(f, self.bucket_data[k2])
        else:
          _change_data(k2, 0, r)

  def all_apply(self, f: F) -> None:
    self.bucket_lazy = [f if bl is None else self.composition(f, bl) for bl in self.bucket_lazy]
 
  def _propagate(self, k: int) -> None:
    '''propagate bucket_lazy[k]. / O(√N)'''
    if self.bucket_lazy[k] is None: return
    f = self.bucket_lazy[k]
    self.data[k] = [self.mapping(f, d) for d in self.data[k]]
    self.bucket_lazy[k] = None
 
  '''Return op([l, r)). / 0 <= l <= r <= n / O(√N)'''
  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.n
    if l == r: return self.e
    k1 = l // self.size
    k2 = r // self.size
    l -= k1 * self.size
    r -= k2 * self.size
    if k1 == k2:
      s = reduce(self.op, self.data[k1][l:r])
      if self.bucket_lazy[k1] is not None:
        s = self.mapping(self.bucket_lazy[k1], s)
    else:
      s = None
      if l < len(self.data[k1]):
        s = reduce(self.op, self.data[k1][l:])
        if self.bucket_lazy[k1] is not None:
          s = self.mapping(self.bucket_lazy[k1], s)
      if k1+1 < k2:
        if s is None:
          s = reduce(self.op, self.bucket_data[k1+1:k2])
        else:
          s = reduce(self.op, self.bucket_data[k1+1:k2], s)
      if k2 < self.bucket_cnt and r > 0:
        s_ = reduce(self.op, self.data[k2][:r])
        if self.bucket_lazy[k2] is not None:
          s_ = self.mapping(self.bucket_lazy[k2], s_)
        if s is not None:
          s = self.op(s, s_)
    return s
 
  '''Return op([0, n)). / O(√N)'''
  def all_prod(self) -> T:
    return reduce(self.op, self.bucket_data)

  def __getitem__(self, k: int) -> T:
    p = k // self.size
    return self.data[p][k-p*self.size] if self.bucket_lazy[p] is None else self.mapping(self.bucket_lazy[p], self.data[p][k-p*self.size])

  def __setitem__(self, indx, key):
    k = indx // self.size
    self._propagate(k)
    self.data[k][indx-k*self.size] = key
    self.bucket_data[k] = reduce(self.op, self.data[k])

  def __str__(self):
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(self.n)])) + ']'

  def __repr__(self):
    return 'LazyQuadraticDivision' + str(self)
 
 
def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

e = None

