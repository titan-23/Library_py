from typing import Iterable

class CumulativeSum():

  def __init__(self, a: Iterable[int], e: int=0):
    if not isinstance(a, list):
      a = list(a)
    n = len(a)
    acc = [e] * (n+1)
    for i in range(n):
      acc[i+1] = acc[i] + a[i]
    self.n = n
    self.acc = acc
    self.a = a

  def pref(self, r: int) -> int:
    assert 0 <= r <= self.n, \
        f'IndexError: CumulativeSum.pref({r}), n={self.n}'
    return self.acc[r]

  def all_sum(self) -> int:
    return self.acc[-1]

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: CumulativeSum.sum({l}, {r}), n={self.n}'
    return self.acc[r] - self.acc[l]

  prod = sum
  all_prod = all_sum

  def __getitem__(self, k: int) -> int:
    assert -self.n <= k < self.n, \
        f'IndexError: CumulativeSum[{k}], n={self.n}'
    return self.a[k]

  def __str__(self):
    return str(self.acc)

