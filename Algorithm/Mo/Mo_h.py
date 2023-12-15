from __pypy__ import newlist_hint
from typing import Callable

class Mo_h():

  # https://take44444.github.io/Algorithm-Book/range/mo/main.html

  def __init__(self, n: int, q: int):
    self.n = n
    self.q = q
    self.l = newlist_hint(q)
    self.r = newlist_hint(q)

  def add_query(self, l: int, r: int) -> None:
    self.l.append(l)
    self.r.append(r)

  def run(self, add: Callable[[int], None], delete: Callable[[int], None], out: Callable[[int], None]) -> None:
    def hilbertorder(i: int) -> int:
      x, y = l[i], r[i]
      rx, ry, d, s = 0, 0, 0, maxn >> 1
      while s:
        rx, ry = x & s > 0, y & s > 0
        d += s * s * ((rx * 3) ^ ry)
        s >>= 1
        if not ry:
          x, y = (maxn-1-y, maxn-1-x) if rx else (y, x)
      return d

    assert len(self.l) == len(self.r) == self.q
    maxn = 1 << self.n.bit_length()
    bit = self.q.bit_length()
    msk = (1 << bit) - 1
    l, r = self.l, self.r
    H = [hilbertorder(x)<<bit|x for x in range(self.q)]
    H.sort()
    nl, nr = 0, 0
    for i in H:
      i &= msk
      il, ir = l[i], r[i]
      while nl > il:
        nl -= 1
        add(nl)
      while nr < ir:
        add(nr)
        nr += 1
      while nl < il:
        delete(nl)
        nl += 1
      while nr > ir:
        nr -= 1
        delete(nr)
      out(i)

