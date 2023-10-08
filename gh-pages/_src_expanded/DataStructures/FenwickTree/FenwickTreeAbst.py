from typing import List, Union, Iterable, TypeVar, Generic, Callable
T = TypeVar('T')

class FenwickTreeAbst(Generic[T]):

  def __init__(self, n_or_a: Union[Iterable[T], T], op: Callable[[T, T], T], inv: Callable[[T], T], e: T):
    if isinstance(n_or_a, int):
      self._size = n_or_a
      self._tree = [e] * (self._size + 1)
    else:
      a = n_or_a if isinstance(n_or_a, list) else list(n_or_a)
      self._size = len(a)
      self._tree = [e] + a
      for i in range(1, self._size):
        if i + (i & -i) <= self._size:
          self._tree[i + (i & -i)] = op(self._tree[i + (i & -i)], self._tree[i])
    self.op = op
    self.inv = inv
    self.e = e
    self._s = 1 << (self._size - 1).bit_length()

  def pref(self, r: int) -> T:
    '''Return sum(a[0, r)) / O(logN)'''
    assert 0 <= r <= self._size, \
        f'IndexError: FenwickTreeAbst.pref({r}), n={self._size}'
    ret = self.e
    while r > 0:
      ret = self.op(ret, self._tree[r])
      r -= r & -r
    return ret

  def suff(self, l: int) -> T:
    '''Return sum(a[l, n)). / O(logN)'''
    assert 0 <= l < self._size, \
        f'IndexError: FenwickTreeAbst.suff({l}), n={self._size}'
    return self.op(self.pref(self._size), self.inv(self.pref(l)))

  def sum(self, l: int, r: int) -> T:
    '''Return sum(a[l, r)]. / O(logN)'''
    assert 0 <= l <= r <= self._size, \
        f'IndexError: FenwickTreeAbst.sum({l}, {r}), n={self._size}'
    return self.op(self.pref(r), self.inv(self.pref(l)))

  def __getitem__(self, k: int) -> T:
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTreeAbst.__getitem__({k}), n={self._size}'
    if k < 0: k += self._size
    return self.op(self.pref(k+1), self.inv(self.pref(k)))

  def add(self, k: int, x: T) -> None:
    '''Add x to a[k]. / O(logN)'''
    assert 0 <= k < self._size, \
        f'IndexError: FenwickTreeAbst.add({k}, {x}), n={self._size}'
    k += 1
    while k <= self._size:
      self._tree[k] = self.op(self._tree[k], x)
      k += k & -k

  def __setitem__(self, k: int, x: T):
    '''Update A[k] to x. / O(logN)'''
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTreeAbst.__setitem__({k}, {x}), n={self._size}'
    if k < 0: k += self._size
    pre = self.__getitem__(k)
    self.add(k, self.op(x, self.inv(pre)))

  def tolist(self) -> List[T]:
    sub = [self.pref(i) for i in range(self._size+1)]
    return [self.op(sub[i+1], self.inv(sub[i])) for i in range(self._size)]

  def __str__(self):
    return '[' + ', '.join(map(str, self.tolist())) + ']'

  def __repr__(self):
    return f'FenwickTreeAbst({self})'

# def op(s, t):
#   # return s + t
#   return

# def inv(s):
#   # return -s
#   return

# e = None


