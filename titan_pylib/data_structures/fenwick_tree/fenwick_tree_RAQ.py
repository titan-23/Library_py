from typing import List, Iterable, Sequence, Union

class FenwickTreeRAQ():
  """区間加算ができます。
  """

  def __init__(self, n_or_a: Union[Iterable[int], int]):
    if isinstance(n_or_a, int):
      self.n = n_or_a
      self.bit0 = [0] * (n_or_a + 2)
      self.bit1 = [0] * (n_or_a + 2)
      self.bit_size = self.n + 1
    else:
      if not isinstance(n_or_a, Sequence):
        n_or_a = list(n_or_a)
      self.n = len(n_or_a)
      self.bit0 = [0] * (self.n + 2)
      self.bit1 = [0] * (self.n + 2)
      self.bit_size = self.n + 1
      for i, e in enumerate(n_or_a):
        self.add_range(i, i+1, e)

  def __add(self, bit: List[int], k: int, x: int) -> None:
    k += 1
    while k <= self.bit_size:
      bit[k] += x
      k += k & -k

  def __pref(self, bit: List[int], r: int) -> int:
    ret = 0
    while r > 0:
      ret += bit[r]
      r -= r & -r
    return ret

  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self.n, \
        f'IndexError: FenwickTreeRAQ.add({k}, {x}), n={self.n}'
    self.add_range(k, k+1, x)

  def add_range(self, l: int, r: int, x: int) -> None:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: FenwickTreeRAQ.add_range({l}, {r}, {x}), l={l},r={r},n={self.n}'
    self.__add(self.bit0, l, -x*l)
    self.__add(self.bit0, r, x*r)
    self.__add(self.bit1, l, x)
    self.__add(self.bit1, r, -x)

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: FenwickTreeRAQ.sum({l}, {r}), l={l},r={r},n={self.n}'
    return self.__pref(self.bit0, r) + r*self.__pref(self.bit1, r) - self.__pref(self.bit0, l) - l*self.__pref(self.bit1, l)

  def tolist(self) -> List[int]:
    return [self.sum(i, i+1) for i in range(self.n)]

  def __getitem__(self, k: int) -> int:
    assert 0 <= k < self.n, \
        f'IndexError: FenwickTreeRAQ.__getitem__({k}), n={self.n}'
    return self.sum(k, k+1)

  def __str__(self):
    return '[' + ', '.join(map(str, (self.sum(i, i+1) for i in range(self.n)))) + ']'

  def __repr__(self):
    return f'FenwickTreeRAQ({self})'

