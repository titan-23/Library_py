from typing import Optional

class DynamicBitVector():

  def __init__(self, n: int, data: Optional[LazySplayTreeData]=None):
    self.N = n
    if data is None:
      data = LazySplayTreeData(op=lambda s, t: s + t, e=0)
    self.bit = LazySplayTree(data, n)

  def build(self) -> None:
    pass

  def reserve(self, n: int) -> None:
    self.bit.reserve(n)

  def insert(self, k: int, v: int) -> None:
    self.N += 1
    self.bit.insert(k, v)

  def pop(self, k: int) -> int:
    self.N -= 1
    return self.bit.pop(k)

  def set(self, k: int, v: int=1) -> None:
    self.bit[k] = v

  def access(self, k: int) -> int:
    return self.bit[k]

  def rank0(self, r: int) -> int:
    # a[0, r) に含まれる 0 の個数
    assert r <= self.N
    return r - self.bit.prod(0, r)

  def rank1(self, r: int) -> int:
    # a[0, r) に含まれる 1 の個数
    assert r <= self.N, f'{r=}'
    return self.bit.prod(0, r)

  def rank(self, r: int, v: int) -> int:
    # a[0, r) に含まれる v の個数
    return self.rank1(r) if v else self.rank0(r)

  def select0(self, k: int) -> int:
    # k 番目の 0 のindex
    # O(log(N))
    if k < 0 or self.rank0(self.N) <= k:
      return -1
    l, r = 0, self.N
    while r - l > 1:
      m = (l + r) >> 1
      if m - self.bit.sum(0, m) > k:
        r = m
      else:
        l = m
    return l

  def select1(self, k: int) -> int:
    # k 番目の 1 のindex
    # O(log(N))
    if k < 0 or self.rank1(self.N) <= k:
      return -1
    l, r = 0, self.N
    while r - l > 1:
      m = (l + r) >> 1
      if self.bit.sum(0, m) > k:
        r = m
      else:
        l = m
    return l

  def select(self, k: int, v: int) -> int:
    # k 番目の v のindex
    # O(log(N))
    return self.select1(k) if v else self.select0(k)

  def __str__(self):
    return str(self.bit)

  __repr__ = __str__

