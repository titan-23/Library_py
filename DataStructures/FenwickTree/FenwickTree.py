from typing import List, Union, Iterable, Optional

class FenwickTree():

  def __init__(self, _n_or_a: Union[Iterable[int], int]):
    if isinstance(_n_or_a, int):
      self._size = _n_or_a
      self._tree = [0] * (self._size + 1)
    else:
      a = _n_or_a if isinstance(_n_or_a, list) else list(_n_or_a)
      self._size = len(a)
      self._tree = [0] + a
      for i in range(1, self._size):
        if i + (i & -i) <= self._size:
          self._tree[i + (i & -i)] += self._tree[i]
    self._s = 1 << (self._size - 1).bit_length()

  def pref(self, r: int) -> int:
    '''Return sum(a[0, r)) / O(logN)'''
    assert 0 <= r <= self._size, \
        f'IndexError: FenwickTree.pref({r}), n={self._size}'
    ret, _tree = 0, self._tree
    while r > 0:
      ret += _tree[r]
      r &= r - 1
    return ret

  def suff(self, l: int) -> int:
    '''Return sum(a[l, n)). / O(logN)'''
    assert 0 <= l < self._size, \
        f'IndexError: FenwickTree.suff({l}), n={self._size}'
    return self.pref(self._size) - self.pref(l)

  def sum(self, l: int, r: int) -> int:
    '''Return sum(a[l, r)]. / O(logN)'''
    assert 0 <= l <= r <= self._size, \
        f'IndexError: FenwickTree.sum({l}, {r}), n={self._size}'
    _tree = self._tree
    res = 0
    while r > l:
      res += _tree[r]
      r &= r - 1
    while l > r:
      res -= _tree[l]
      l &= l - 1
    return res

  def __getitem__(self, k: int) -> int:
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTree.__getitem__({k}), n={self._size}'
    if k < 0: k += self._size
    return self.sum(k, k+1)

  def add(self, k: int, x: int) -> None:
    '''Add x to a[k]. / O(logN)'''
    assert 0 <= k < self._size, \
        f'IndexError: FenwickTree.add({k}, {x}), n={self._size}'
    k += 1
    _tree = self._tree
    while k <= self._size:
      _tree[k] += x
      k += k & -k

  def __setitem__(self, k: int, x: int):
    '''Update A[k] to x. / O(logN)'''
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTree.__setitem__({k}, {x}), n={self._size}'
    if k < 0: k += self._size
    pre = self.__getitem__(k)
    self.add(k, x - pre)

  def bisect_left(self, w: int) -> Optional[int]:
    '''bisect_left(acc) / O(logN)'''
    i, s, _size, _tree = 0, self._s, self._size, self._tree
    while s:
      if i + s <= _size and _tree[i + s] < w:
        w -= _tree[i + s]
        i += s
      s >>= 1
    return i if w else None

  def bisect_right(self, w: int) -> int:
    '''bisect_right(acc) / O(logN)'''
    i, s, _size, _tree = 0, self._s, self._size, self._tree
    while s:
      if i + s <= _size and _tree[i + s] <= w:
        w -= _tree[i + s]
        i += s
      s >>= 1
    return i

  def show(self) -> None:
    '''for debug'''
    print('[' + ', '.join(map(str, (self.pref(i) for i in range(self._size+1)))) + ']')

  def tolist(self) -> List[int]:
    sub = [self.pref(i) for i in range(self._size+1)]
    return [sub[i+1]-sub[i] for i in range(self._size)]

  @staticmethod
  def get_inversion_num(a: List[int], compress: bool=False) -> int:
    inv = 0
    if compress:
      a_ = sorted(set(a))
      z = {e: i for i, e in enumerate(a_)}
      fw = FenwickTree(len(a_))
      for i, e in enumerate(a):
        inv += i - fw.pref(z[e])
        fw.add(z[e], 1)
    else:
      fw = FenwickTree(len(a))
      for i, e in enumerate(a):
        inv += i - fw.pref(e)
        fw.add(e, 1)
    return inv

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'FenwickTree({self})'

