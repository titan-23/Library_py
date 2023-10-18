from Library_py.DataStructures.BitVector.AVLTreeBitVector import AVLTreeBitVector
from Library_py.DataStructures.WaveletMatrix.WaveletMatrix import WaveletMatrix
from typing import Sequence, List
from array import array

class DynamicWaveletMatrix(WaveletMatrix):

  def __init__(self, sigma: int, a: Sequence[int]=[]):
    self.sigma: int = sigma
    self.log: int = (sigma-1).bit_length()
    self.v: List[AVLTreeBitVector] = [AVLTreeBitVector()] * self.log
    self.mid: array[int] = array('I', bytes(4*self.log))
    self.size: int = len(a)
    self._build(a)

  def _build(self, a: Sequence[int]) -> None:
    '''列 a から Dwm を構築する'''
    v = array('B', bytes(self.size))
    for bit in range(self.log-1, -1, -1):
      # bit目の0/1に応じてvを構築 + aを安定ソート
      zero, one = [], []
      for i, e in enumerate(a):
        if e >> bit & 1:
          v[i] = 1
          one.append(e)
        else:
          v[i] = 0
          zero.append(e)
      self.mid[bit] = len(zero)  # 境界をmid[bit]に保持
      self.v[bit] = AVLTreeBitVector(v)
      a = zero + one

  def reserve(self, n: int) -> None:
    assert n >= 0, f'ValueError: DynamicWaveletMatrix.reserve({n})'
    for v in self.v:
      v.reserve(n)

  def insert(self, k: int, x: int) -> None:
    assert 0 <= k <= self.size,  f'IndexError: DynamicWaveletMatrix.insert({k}, {x}), n={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: DynamicWaveletMatrix.insert({k}, {x}), LIM={1<<self.log}'
    mid = self.mid
    for bit in range(self.log-1, -1, -1):
      v = self.v[bit]
      # if x >> bit & 1:
      #   v.insert(k, 1)
      #   k = v.rank1(k) + mid[bit]
      # else:
      #   v.insert(k, 0)
      #   mid[bit] += 1
      #   k = v.rank0(k)
      if x >> bit & 1:
        s = v._insert_and_rank1(k, 1)
        k = s + mid[bit]
      else:
        s = v._insert_and_rank1(k, 0)
        k -= s
        mid[bit] += 1
    self.size += 1

  def pop(self, k: int) -> int:
    assert 0 <= k < self.size,  f'IndexError: DynamicWaveletMatrix.pop({k}), n={self.size}'
    mid = self.mid
    ans = 0
    for bit in range(self.log-1, -1, -1):
      v = self.v[bit]
      # K = k
      # if v.access(k):
      #   ans |= 1 << bit
      #   k = v.rank1(k) + mid[bit]
      # else:
      #   mid[bit] -= 1
      #   k = v.rank0(k)
      # v.pop(K)
      sb = v._access_pop_and_rank1(k)
      s = sb >> 1
      if sb & 1:
        ans |= 1 << bit
        k = s + mid[bit]
      else:
        mid[bit] -= 1
        k -= s
    self.size -= 1
    return ans

  def update(self, k: int, x: int) -> None:
    assert 0 <= k < self.size,  f'IndexError: DynamicWaveletMatrix.update({k}, {x}), n={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: DynamicWaveletMatrix.update({k}, {x}), LIM={1<<self.log}'
    self.pop(k)
    self.insert(k, x)

  def __setitem__(self, k: int, x: int):
    assert 0 <= k < self.size,  f'IndexError: DynamicWaveletMatrix[{k}] = {x}, n={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: DynamicWaveletMatrix[{k}] = {x}, LIM={1<<self.log}'
    self.update(k, x)

  def __str__(self):
    return f'DynamicWaveletMatrix({[self[i] for i in range(self.size)]})'

