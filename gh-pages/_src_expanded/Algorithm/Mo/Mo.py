# from Library_py.Algorithm.Mo.Mo import Mo
from typing import Callable
from itertools import chain
from __pypy__ import newlist_hint
from math import sqrt, ceil

class Mo():

  def __init__(self, n: int, q: int):
    self.n = n
    self.q = q
    self.bucket_size = ceil(sqrt(3)*n/sqrt(2*q)) if q > 0 else n
    if self.bucket_size == 0:
      self.bucket_size = 1
    self.bit = max(n, q).bit_length()
    self.msk = (1 << self.bit) - 1
    self.bucket = [newlist_hint(self.bucket_size//10) for _ in range(n//self.bucket_size+1)]
    self.cnt = 0

  def add_query(self, l: int, r: int) -> None:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: Mo.add_query({l}, {r}), self.n={self.n}'
    self.bucket[l//self.bucket_size].append((((r<<self.bit)|l)<<self.bit)|self.cnt)
    self.cnt += 1

  def run(self, add: Callable[[int], None], delete: Callable[[int], None], out: Callable[[int], None]) -> None:
    assert self.cnt == self.q, \
        f'Not Enough Queries, now:{self.cnt}, expected:{self.q}'
    bucket, bit, msk = self.bucket, self.bit, self.msk
    for i, b in enumerate(bucket):
      b.sort(reverse=i & 1)
    nl, nr = 0, 0
    for rli in chain(*bucket):
      r, l = rli >> bit >> bit, rli >> bit & msk
      while nl > l:
        nl -= 1
        add(nl)
      while nr < r:
        add(nr)
        nr += 1
      while nl < l:
        delete(nl)
        nl += 1
      while nr > r:
        nr -= 1
        delete(nr)
      out(rli & msk)

  def runrun(self, add_left: Callable[[int], None], add_right: Callable[[int], None], \
          delete_left: Callable[[int], None], delete_right: Callable[[int], None], out: Callable[[int], None]) -> None:
    assert self.cnt == self.q
    bucket, bit, msk = self.bucket, self.bit, self.msk
    for i, b in enumerate(bucket):
      b.sort(reverse=i & 1)
    nl, nr = 0, 0
    for rli in chain(*bucket):
      r, l = rli >> bit >> bit, rli >> bit & msk
      while nl > l:
        nl -= 1
        add_left(nl)
      while nr < r:
        add_right(nr)
        nr += 1
      while nl < l:
        delete_left(nl)
        nl += 1
      while nr > r:
        nr -= 1
        delete_right(nr)
      out(rli & msk)


