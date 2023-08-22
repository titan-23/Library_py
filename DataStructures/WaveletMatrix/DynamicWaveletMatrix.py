from typing import Sequence, List
from array import array

class DynamicWaveletMatrix(WaveletMatrix):

  def __init__(self, sigma: int, a: Sequence[int]=[]):
    self.sigma: int = sigma
    self.log: int = (sigma-1).bit_length()
    self.v: List[DynamicBitVector] = [None] * self.log
    self.mid: array[int] = array('I', bytes(4*self.log))
    self.size: int = len(a)
    self._build(a)

  def _build(self, a: Sequence[int]) -> None:
    '''列 a から wm を構築する'''
    data = LazySplayTreeData(op=lambda s, t: s + t, e=0)
    data.reserve(self.size * self.log)
    for bit in range(self.log-1, -1, -1):
      # bit目の0/1に応じてvを構築 + aを安定ソート
      v = DynamicBitVector(self.size, data)
      zero, one = [], []
      for i, e in enumerate(a):
        if e >> bit & 1:
          v.set(i)
          one.append(e)
        else:
          zero.append(e)
      v.build()
      self.mid[bit] = len(zero)  # 境界をmid[bit]に保持
      self.v[bit] = v
      a = zero + one

  def reserve(self, n: int) -> None:
    for bit in range(self.log):
      self.v[bit].reserve(n)

  def __str__(self):
    return f'DynamicWaveletMatrix({[self.access(i) for i in range(self.size)]})'

  def insert(self, k: int, x: int) -> None:
    for bit in range(self.log-1, -1, -1):
      v = self.v[bit]
      if x >> bit & 1:
        v.insert(k, 1)
        k = v.rank1(k) + self.mid[bit]
      else:
        v.insert(k, 0)
        self.mid[bit] += 1
        k = v.rank0(k)
    self.size += 1

  def pop(self, k: int) -> int:
    ans = self.access(k)
    for bit in range(self.log-1, -1, -1):
      v = self.v[bit]
      K = k
      if v.access(K):
        k = v.rank1(k) + self.mid[bit]
      else:
        self.mid[bit] -= 1
        k = v.rank0(k)
      v.pop(K)
    self.size -= 1
    return ans

  def update(self, k: int, x: int) -> None:
    self.pop(k)
    self.insert(k, x)

  def __setitem__(self, k: int, x: int):
    self.update(k, x)

