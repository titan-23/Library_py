from typing import Union, Callable, List, TypeVar, Generic, Iterable
T = TypeVar('T')
F = TypeVar('F')

class LazySegmentTree(Generic[T, F]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               mapping: Callable[[F, T], T],
               composition: Callable[[F, F], F],
               e: T,
               id: F
               ) -> None:
    self.op: Callable[[T, T], T] = op
    self.mapping: Callable[[F, T], T] = mapping
    self.composition: Callable[[F, F], F] = composition
    self.e: T = e
    self.id: F = id
    if isinstance(n_or_a, int):
      self.n = n_or_a
      self.log = (self.n - 1).bit_length()
      self.size = 1 << self.log
      self.data = [e] * (self.size << 1)
    else:
      a = list(n_or_a)
      self.n = len(a)
      self.log = (self.n - 1).bit_length()
      self.size = 1 << self.log
      data = [e] * (self.size << 1)
      data[self.size:self.size+self.n] = a
      for i in range(self.size-1, 0, -1):
        data[i] = op(data[i<<1], data[i<<1|1])
      self.data = data
    self.lazy = [id] * self.size

  def _update(self, k: int) -> None:
    self.data[k] = self.op(self.data[k<<1], self.data[k<<1|1])

  def _all_apply(self, k: int, f: F) -> None:
    self.data[k] = self.mapping(f, self.data[k])
    if k >= self.size: return
    self.lazy[k] = self.composition(f, self.lazy[k])

  def _propagate(self, k: int) -> None:
    self._all_apply(k<<1, self.lazy[k])
    self._all_apply(k<<1|1, self.lazy[k])
    self.lazy[k] = self.id

  def apply_point(self, k: int, f: F) -> None:
    k += self.size
    for i in range(self.log, 0, -1):
      self._propagate(k >> i)
    self.data[k] = self.mapping(f, self.data[k])
    for i in range(1, self.log+1):
      self._update(k >> i)

  def apply(self, l: int, r: int, f: F) -> None:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: {self.__class__.__name__}.apply({l}, {r}, {f}), n={self.n}'
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
    l2, r2 = l, r
    while l < r:
      if l & 1:
        self._all_apply(l, f)
        l += 1
      if r & 1:
        self._all_apply(r^1, f)
      l >>= 1
      r >>= 1
    ll, rr = l2, r2-1
    for i in range(1, self.log+1):
      ll >>= 1
      rr >>= 1
      if ll << i != l2:
        self._update(ll)
      if r2 >> i << i != r2:
        self._update(rr)

  def all_apply(self, f: F) -> None:
    self.lazy[1] = self.composition(f, self.lazy[1])

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: {self.__class__.__name__}.prod({l}, {r}), n={self.n}'
    if l == r: return self.e
    l += self.size
    r += self.size
    lazy = self.lazy
    for i in range(self.log, 0, -1):
      ll, rr = l>>i, r>>i
      if ll << i != l and lazy[ll] != self.id:
        self._propagate(ll)
      if rr << i != r and lazy[rr] != self.id:
        self._propagate(rr)
    lres = self.e
    rres = self.e
    while l < r:
      if l & 1:
        lres = self.op(lres, self.data[l])
        l += 1
      if r & 1:
        rres = self.op(self.data[r^1], rres)
      l >>= 1
      r >>= 1
    return self.op(lres, rres)

  def all_prod(self) -> T:
    return self.data[1]

  def all_propagate(self) -> None:
    for i in range(self.size):
      self._propagate(i)

  def tolist(self) -> List[T]:
    self.all_propagate()
    return self.data[self.size:self.size+self.n]

  def max_right(self, l, f) -> int:
    assert 0 <= l <= self.n
    assert f(self.e)
    if l == self.size:
      return self.n
    l += self.size
    for i in range(self.log, 0, -1):
      self._propagate(l >> i)
    s = self.e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self.op(s, self.data[l])):
        while l < self.size:
          self._propagate(l)
          l <<= 1
          if f(self.op(s, self.data[l])):
            s = self.op(s, self.data[l])
            l |= 1
        return l - self.size
      s = self.op(s, self.data[l])
      l += 1
      if l & -l == l:
        break
    return self.n

  def min_left(self, r: int, f) -> int:
    assert 0 <= r <= self.n
    assert f(self.e)
    if r == 0:
      return 0
    r += self.size
    for i in range(self.log, 0, -1):
      self._propagate((r-1) >> i)
    s = self.e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self.op(self.data[r], s)):
        while r < self.size:
          self._propagate(r)
          r = r << 1 | 1
          if f(self.op(self.data[r], s)):
            s = self.op(self.data[r], s)
            r ^= 1
        return r + 1 - self.size
      s = self.op(self.data[r], s)
      if r & -r == r:
        break
    return 0

  def __getitem__(self, k: int) -> T:
    assert -self.n <= k < self.n, \
        f'IndexError: {self.__class__.__name__}[{k}], n={self.n}'
    if k < 0:
      k += self.n
    k += self.size
    for i in range(self.log, 0, -1):
      self._propagate(k >> i)
    return self.data[k]

  def __setitem__(self, k: int, v: T):
    assert -self.n <= k < self.n, \
        f'IndexError: {self.__class__.__name__}[{k}] = {v}, n={self.n}'
    if k < 0:
      k += self.n
    k += self.size
    for i in range(self.log, 0, -1):
      self._propagate(k >> i)
    self.data[k] = v
    for i in range(1, self.log+1):
     self._update(k >> i)

  def __str__(self) -> str:
    return '[' + ', '.join(map(str, (self.__getitem__(i) for i in range(self.n)))) + ']'

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'

