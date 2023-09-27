from typing import Union, Callable, TypeVar, Generic, Iterable, List
from functools import reduce
from itertools import chain
T = TypeVar('T')
F = TypeVar('F')

class SegmentLazyQuadraticDivision(Generic[T, F]):

  def __init__(self, n_or_a: Union[int, Iterable[T]], \
              op: Callable[[T, T], T], mapping: Callable[[F, T], T], \
              composition: Callable[[F, F], F], e: T, id: F):
    if isinstance(n_or_a, int):
      self.n = n_or_a
      a = [e] * self.n
    else:
      if not isinstance(n_or_a, list):
        a = list(n_or_a)
      else:
        a = n_or_a
    self.n = len(a)
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id = id
    self.bucket_size = int(self.n**.5) + 1
    self.bucket_cnt = (self.n+self.bucket_size-1) // self.bucket_size
    self.data = [a[k*self.bucket_size:(k+1)*self.bucket_size] for k in range(self.bucket_cnt)]
    self.bucket_data = [reduce(self.op, v) for v in self.data]
    self.bucket_lazy = [id] * self.bucket_cnt

  def apply(self, l: int, r: int, f: F) -> None:
    '''Applay f to a[l,r). / O(√N)'''
    assert 0 <= l <= r <= self.n
    def _change_data(k: int, l: int, r: int) -> None:
      self._propagate(k)
      self.data[k][l:r] = [self.mapping(f, d) for d in self.data[k][l:r]]
      self.bucket_data[k] = reduce(self.op, self.data[k])
    k1 = l // self.bucket_size
    k2 = r // self.bucket_size
    l -= k1 * self.bucket_size
    r -= k2 * self.bucket_size
    if k1 == k2:
      if k1 < self.bucket_cnt:
        _change_data(k1, l, r)
    else:
      if k1 < self.bucket_cnt:
        if l == 0:
          self.bucket_lazy[k1] = f if self.bucket_lazy[k1] == self.id else self.composition(f, self.bucket_lazy[k1])
          self.bucket_data[k1] = self.mapping(f, self.bucket_data[k1])
        else:
          _change_data(k1, l, len(self.data[k1]))
      for i in range(k1+1, k2):
        self.bucket_lazy[i] = f if self.bucket_lazy[i] == self.id else self.composition(f, self.bucket_lazy[i])
        self.bucket_data[i] = self.mapping(f, self.bucket_data[i])
      if k2 < self.bucket_cnt:
        if r == len(self.data[k2]):
          self.bucket_lazy[k2] = f if self.bucket_lazy[k2] == self.id else self.composition(f, self.bucket_lazy[k2])
          self.bucket_data[k2] = self.mapping(f, self.bucket_data[k2])
        else:
          _change_data(k2, 0, r)

  def all_apply(self, f: F) -> None:
    self.bucket_lazy = [f if bl == self.id else self.composition(f, bl) for bl in self.bucket_lazy]

  def _propagate(self, k: int) -> None:
    if self.bucket_lazy[k] == self.id: return
    f = self.bucket_lazy[k]
    self.data[k] = [self.mapping(f, d) for d in self.data[k]]
    self.bucket_lazy[k] = self.id

  def _all_propagatae(self) -> None:
    for k in range(self.bucket_cnt):
      self._propagate(k)
    self.bucket_lazy = [self.id] * self.bucket_cnt

  def prod(self, l: int, r: int) -> T:
    '''Return op([l, r)). / 0 <= l <= r <= n / O(√N)'''
    assert 0 <= l <= r <= self.n
    if l == r: return self.e
    k1 = l // self.bucket_size
    k2 = r // self.bucket_size
    l -= k1 * self.bucket_size
    r -= k2 * self.bucket_size
    s = self.e
    if k1 == k2:
      s = reduce(self.op, self.data[k1][l:r])
      if self.bucket_lazy[k1] != self.id:
        s = self.mapping(self.bucket_lazy[k1], s)
    else:
      if l < len(self.data[k1]):
        s = reduce(self.op, self.data[k1][l:])
        if self.bucket_lazy[k1] != self.id:
          s = self.mapping(self.bucket_lazy[k1], s)
      if k1+1 < k2:
        s = reduce(self.op, self.bucket_data[k1+1:k2], s)
      if k2 < self.bucket_cnt and r > 0:
        s_ = reduce(self.op, self.data[k2][:r])
        if self.bucket_lazy[k2] != self.id:
          s_ = self.mapping(self.bucket_lazy[k2], s_)
        s = self.op(s, s_)
    return s

  def all_prod(self) -> T:
    '''Return op([0, n)). / O(√N)'''
    return reduce(self.op, self.bucket_data)

  def tolist(self) -> List[T]:
    self._all_propagatae()
    return list(chain(*self.data))

  def __getitem__(self, k: int) -> T:
    p = k // self.bucket_size
    return self.data[p][k-p*self.bucket_size] if self.bucket_lazy[p] == self.id else self.mapping(self.bucket_lazy[p], self.data[p][k-p*self.bucket_size])

  def __setitem__(self, k, v):
    p = k // self.bucket_size
    self._propagate(p)
    self.data[p][k-p*self.bucket_size] = v
    self.bucket_data[p] = reduce(self.op, self.data[p])

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'SegmentLazyQuadraticDivision({self})'

# def op(s, t):
#   return

# def mapping(f, s):
#   return

# def composition(f, g):
#   return

# e = None
# id = None

