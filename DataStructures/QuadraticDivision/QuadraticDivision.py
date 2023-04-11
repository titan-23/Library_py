from typing import Union, Callable, TypeVar, Generic, Iterable
from functools import reduce
T = TypeVar("T")


class QuadraticDivision(Generic[T]):

  def __init__(self, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T=None):
    if isinstance(n_or_a, int):
      self.n = n_or_a
      a = [e] * self.n
    else:
      a = list(n_or_a)
      self.n = len(a)
    self.op = op
    self.e = e
    self.size = int(self.n**.5) + 1
    self.bucket_cnt = (self.n+self.size-1) // self.size
    self.data = [a[k*self.size:(k+1)*self.size] for k in range(self.bucket_cnt)]
    self.bucket_data = [reduce(self.op, v) for v in self.data]

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
    else:
      s = None
      if l < len(self.data[k1]): s = reduce(self.op, self.data[k1][l:])
      if k1+1 < k2: s = reduce(self.op, self.bucket_data[k1+1:k2]) if s is None else reduce(self.op, self.bucket_data[k1+1:k2], s)
      if k2 < self.bucket_cnt and r > 0: s = reduce(self.op, self.data[k2][:r]) if s is None else reduce(self.op, self.data[k2][:r], s)
    return s

  '''Return op([0, n)). / O(√N)'''
  def all_prod(self):
    return reduce(self.op, self.bucket_data)

  def __getitem__(self, indx):
    k = indx // self.size
    return self.data[k][indx-k*self.size]

  def __setitem__(self, indx, key):
    k = indx // self.size
    self.data[k][indx-k*self.size] = key
    self.bucket_data[k] = reduce(self.op, self.data[k])

  def __str__(self):
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(self.n)])) + ']'

  def __repr__(self):
    return 'QuadraticDivision' + str(self)


def op(s, t):
  return

e = None

