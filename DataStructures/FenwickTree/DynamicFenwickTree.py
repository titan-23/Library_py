from typing import Optional

class DynamicFenwickTree():

  def __init__(self, u: int):
    '''Build DynamicFenwickTree [0, u).'''
    assert isinstance(u, int), \
        f'TypeError: DynamicFenwickTree({u}), {u} must be int'
    self._u = u
    self._tree = {}
    self._s = 1 << (u-1).bit_length()

  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self._u, \
        f'IndexError: DynamicFenwickTree.add({k}, {x}), u={self._u}'
    k += 1
    while k <= self._u:
      if k in self._tree:
        self._tree[k] += x
      else:
        self._tree[k] = x
      k += k & -k

  def pref(self, r: int) -> int:
    assert 0 <= r <= self._u, \
        f'IndexError: DynamicFenwickTree.pref({r}), u={self._u}'
    ret = 0
    while r > 0:
      if r in self._tree:
        ret += self._tree[r]
      r -= r & -r
    return ret

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self._u, \
        f'IndexError: DynamicFenwickTree.sum({l}, {r}), u={self._u}'
    # return self.pref(r) - self.pref(l)
    _tree = self._tree
    res = 0
    while r > l:
      if r in _tree:
        res += _tree[r]
      r -= r & -r
    while l > r:
      if l in _tree:
        res -= _tree[l]
      l -= l & -l
    return res

  def bisect_left(self, w: int) -> Optional[int]:
    i, s = 0, self._s
    while s:
      if i+s <= self._u:
        if i+s in self._tree and self._tree[i+s] < w:
          w -= self._tree[i+s]
          i += s
        elif i+s not in self._tree and 0 < w:
          i += s
      s >>= 1
    return i if w else None

  def bisect_right(self, w: int) -> int:
    i, s = 0, self._s
    while s:
      if i+s <= self._u:
        if i+s in self._tree and self._tree[i+s] <= w:
          w -= self._tree[i+s]
          i += s
        elif i+s not in self._tree and 0 <= w:
          i += s
      s >>= 1
    return i

  def __str__(self):
    return str(self._tree)

