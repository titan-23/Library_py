from typing import Union, Callable, List, TypeVar, Generic, Iterable
T = TypeVar('T')
F = TypeVar('F')

class DualSegmentTree(Generic[T, F]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               mapping: Callable[[F, T], T],
               composition: Callable[[F, F], F],
               e: T,
               id: F):
    self.mapping: Callable[[F, T], T] = mapping
    self.composition: Callable[[F, F], F] = composition
    self.e: T = e
    self.id: F = id
    if isinstance(n_or_a, int):
      self.n = n_or_a
      self.log = (self.n - 1).bit_length()
      self.size = 1 << self.log
      self.data = [e] * self.size
    else:
      a = list(n_or_a)
      self.n = len(a)
      self.log = (self.n - 1).bit_length()
      self.size = 1 << self.log
      data = [e] * self.size
      data[:self.n] = a
      self.data = data
    self.lazy = [id] * self.size

  def _all_apply(self, k: int, f: F) -> None:
    if k-self.size >= 0:
      self.data[k-self.size] = self.mapping(f, self.data[k-self.size])
    else:
      self.lazy[k] = self.composition(f, self.lazy[k])

  def _propagate(self, k: int) -> None:
    self._all_apply(k<<1, self.lazy[k])
    self._all_apply(k<<1|1, self.lazy[k])
    self.lazy[k] = self.id

  def apply_point(self, k: int, f: F) -> None:
    k += self.size
    for i in range(self.log, 0, -1):
      self._propagate(k >> i)
    self.data[k-self.size] = self.mapping(f, self.data[k-self.size])

  def apply(self, l: int, r: int, f: F) -> None:
    if l == r: return
    if f == self.id: return
    l += self.size
    r += self.size
    lazy = self.lazy
    for i in range(self.log, 0, -1):
      if l >> i << i != l and lazy[l>>i] != self.id:
        self._propagate(l>>i)
      if r >> i << i != r and lazy[(r-1)>>i] != self.id:
        self._propagate((r-1)>>i)
    data, lazy = self.data, self.lazy
    if (l-self.size) & 1:
      data[l-self.size] = self.mapping(f, data[l-self.size])
      l += 1
    if (r-self.size) & 1:
      r ^= 1
      data[r-self.size] = self.mapping(f, data[r-self.size])
    l >>= 1
    r >>= 1
    while l < r:
      if l & 1:
        lazy[l] = self.composition(f, lazy[l])
        l += 1
      if r & 1:
        r ^= 1
        lazy[r] = self.composition(f, lazy[r])
      l >>= 1
      r >>= 1

  def all_apply(self, f: F) -> None:
    self.lazy[1] = self.composition(f, self.lazy[1])

  def all_propagate(self) -> None:
    for i in range(self.size):
      self._propagate(i)

  def tolist(self) -> List[T]:
    self.all_propagate()
    return self.data[self.size:self.size+self.n]

  def __getitem__(self, k: int) -> T:
    k += self.size
    for i in range(self.log, 0, -1):
      self._propagate(k >> i)
    return self.data[k-self.size]

  def __setitem__(self, k: int, v: T):
    k += self.size
    for i in range(self.log, 0, -1):
      self._propagate(k >> i)
    self.data[k-self.size] = v

  def __str__(self) -> str:
    return str([self[i] for i in range(self.n)])

  def __repr__(self):
    return f'DualSegmentTree({self})'

