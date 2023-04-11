from __pypy__ import newlist_hint
from array import array
from typing import Callable

class MoHi:
  
  def __init__(self, n, q):
    self.bit = max(n, q).bit_length()
    self.q = q
    self.l = newlist_hint(q)
    self.r = newlist_hint(q)

  def add_query(self, i, l, r):
    self.l.append(l)
    self.r.append(r)

  def run(self, add: Callable[[int], None], delete: Callable[[int], None], out: Callable[[int], None]) -> None:
    bit = self.bit
    maxn = 1 << bit
    l, r = self.l, self.r
    def hilbertorder(i) -> int:
      x, y = l[i], r[i]
      rx, ry, d, s = 0, 0, 0, maxn >> 1
      while s:
        rx, ry = x & s > 0, y & s > 0
        d += s * s * ((rx * 3) ^ ry)
        s >>= 1
        if not ry:
          x, y = (maxn-1-y, maxn-1-x) if rx else (y, x)
      return d
    hil = list(range(self.q))
    hil.sort(key=lambda i: hilbertorder(i))
    nl, nr = 0, 0
    for i in hil:
      il, ir = l[i], r[i]
      while nl > il:
        nl -= 1
        add(nl)
      while nl < il:
        delete(nl)
        nl += 1
      while nr < ir:
        add(nr)
        nr += 1
      while nr > ir:
        nr -= 1
        delete(nr)
      out(i)


