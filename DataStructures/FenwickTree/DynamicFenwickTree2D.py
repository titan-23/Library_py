from typing import List

class FenwickTree2D():

  def __init__(self, h: int, w: int, a: List[List[int]]=[]):
    '''O(HWlogHlogW)'''
    self._h = h + 1
    self._w = w + 1
    self._bit = {}
    if a:
      assert len(a) == h and len(a[0]) == w
      self._build(a)

  def _build(self, a):
    for i in range(self._h-1):
      for j in range(self._w-1):
        self.add(i, j, a[i][j])

  def add(self, h: int, w: int, x) -> None:
    '''Add x to a[h][w]. / O(logH * logW)'''
    h += 1
    w += 1
    _h, _w, _bit = self._h, self._w, self._bit
    while h < _h:
      j = w
      bit_h = _bit.get(h, [])
      while j < _w:
        if j in bit_h:
          bit_h[j] += x
        else:
          bit_h[j] = x
        j += j & -j
      h += h & -h

  def set(self, h: int, w: int, x) -> None:
    self.add(h, w, x - self.get(h, w))

  def _sum(self, h: int, w: int):
    '''Return sum([0, h) x [0, w)) of a. / O(logH * logW)'''
    ret = 0
    while h > 0:
      j = w
      bit_h = self._bit.get(h, [])
      while j > 0:
        ret += bit_h.get(j, 0)
        j -= j & -j
      h -= h & -h
    return ret

  def sum(self, h1: int, w1: int, h2: int, w2: int):
    '''Retrun sum([h1, h2) x [w1, w2)) of a. / O(logH * logW)'''
    assert h1 <= h2 and w1 <= w2
    # w1, w2 = min(w1, w2), max(w1, w2)
    # h1, h2 = min(h1, h2), max(h1, h2)
    return self._sum(h2, w2) - self._sum(h2, w1) - self._sum(h1, w2) + self._sum(h1, w1)

  def get(self, h: int, w: int):
    return self.sum(h, h+1, w, w+1)
