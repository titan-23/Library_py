from Library_py.DataStructures.BitVector.BitVector import BitVector
from typing import Sequence, List, Tuple
from heapq import heappush, heappop
from array import array

class WaveletMatrix():

  def __init__(self, sigma: int, a: Sequence[int]=[]):
    self.sigma: int = sigma
    self.log: int = (sigma-1).bit_length()
    self.mid: array[int] = array('I', bytes(4*self.log))
    self.size: int = len(a)
    self.v: List[BitVector] = [BitVector(self.size) for _ in range(self.log)]
    self._build(a)

  def _build(self, a: Sequence[int]) -> None:
    '''列 a から wm を構築する'''
    for bit in range(self.log-1, -1, -1):
      # bit目の0/1に応じてvを構築 + aを安定ソート
      v = self.v[bit]
      zero, one = [], []
      for i, e in enumerate(a):
        if e >> bit & 1:
          v.set(i)
          one.append(e)
        else:
          zero.append(e)
      v.build()
      self.mid[bit] = len(zero)  # 境界をmid[bit]に保持
      a = zero + one

  def access(self, k: int) -> int:
    '''a[k] を返す'''
    assert 0 <= k < self.size, \
        f'IndexError: WaveletMatrix.access({k}), size={self.size}'
    s = 0  # 答え
    for bit in range(self.log-1, -1, -1):
      if self.v[bit].access(k):
        # k番目が立ってたら、
        # kまでの1とすべての0が次のk
        s |= 1 << bit
        k = self.v[bit].rank1(k) + self.mid[bit]
      else:
        # kまでの0が次のk
        k = self.v[bit].rank0(k)
    return s

  def __getitem__(self, k: int) -> int:
    assert 0 <= k < self.size, \
        f'IndexError: WaveletMatrix.__getitem__({k}), size={self.size}'
    return self.access(k)

  def rank(self, r: int, x: int) -> int:
    '''a[0, r) に含まれる x の個数'''
    assert 0 <= r <= self.size, f'IndexError: r={r}, size={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: x={x}, LIM={1<<self.log}'
    l = 0
    mid = self.mid
    for bit in range(self.log-1, -1, -1):
      # 位置 r より左に x が何個あるか
      # x の bit 目で場合分け
      if x >> bit & 1:
        # 立ってたら、次のl, rは以下
        l = self.v[bit].rank1(l) + mid[bit]
        r = self.v[bit].rank1(r) + mid[bit]
      else:
        # そうでなければ次のl, rは以下
        l = self.v[bit].rank0(l)
        r = self.v[bit].rank0(r)
    return r - l

  def select(self, k: int, x: int) -> int:
    '''k 番目の v のindex'''
    assert 0 <= k < self.size, f'IndexError: select({k}, {x}), k={k}, size={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: select({k}, {x}), x={x}, LIM={1<<self.log}'
    # x の開始位置 s を探す
    s = 0
    for bit in range(self.log-1, -1, -1):
      if x >> bit & 1:
        s = self.v[bit].rank0(self.size) + self.v[bit].rank1(s)
      else:
        s = self.v[bit].rank0(s)
    s += k  # s から k 進んだ位置が、元の列で何番目か調べる
    for bit in range(self.log):
      if x >> bit & 1:
        s = self.v[bit].select1(s - self.v[bit].rank0(self.size))
      else:
        s = self.v[bit].select0(s)
    return s

  def kth_smallest(self, l: int, r: int, k: int) -> int:
    '''a[l, r) の中で k 番目に小さい値'''
    assert 0 <= l <= r <= self.size, \
        f'IndexError: kth_smallest({l}, {r}, {k}), size={self.size}'
    assert 0 <= k < r-l, \
        f'IndexError: kth_smallest({l}, {r}, {k}), wrong k'
    s = 0
    mid = self.mid
    for bit in range(self.log-1, -1, -1):
      r0, l0 = self.v[bit].rank0(r), self.v[bit].rank0(l)
      cnt = r0 - l0  # 区間内の 0 の個数
      if cnt <= k:  # 0 が k 以下のとき、 k 番目は 1
        s |= 1 << bit
        k -= cnt
        # この 1 が次の bit 列でどこに行くか
        l = l - l0 + mid[bit]
        r = r - r0 + mid[bit]
      else:
        # この 0 が次の bit 列でどこに行くか
        l = l0
        r = r0
    return s

  quantile = kth_smallest

  def kth_largest(self, l: int, r: int, k: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: kth_largest({l}, {r}, {k}), size={self.size}'
    assert 0 <= k < r-l, \
        f'IndexError: kth_largest({l}, {r}, {k}), wrong k'
    return self.kth_smallest(l, r, r-l-k-1)

  def topk(self, l: int, r: int, k: int) -> List[Tuple[int, int]]:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: topk({l}, {r}, {k}), size={self.size}'
    assert 0 <= k < r-l, \
        f'IndexError: topk({l}, {r}, {k}), wrong k'
    # heap[-length, x, l, bit]
    hq: List[Tuple[int, int, int, int]] = [(-(r-l), 0, l, self.log-1)]
    ans = []
    while hq:
      length, x, l, bit = heappop(hq)
      length = -length
      if bit == -1:
        ans.append((x, length))
        k -= 1
        if k == 0:
          break
      else:
        r = l + length
        l0 = self.v[bit].rank0(l)
        r0 = self.v[bit].rank0(r)
        if l0 < r0:
          heappush(hq, (-(r0-l0), x, l0, bit-1))
        l1 = self.v[bit].rank1(l) + self.mid[bit]
        r1 = self.v[bit].rank1(r) + self.mid[bit]
        if l1 < r1:
          heappush(hq, (-(r1-l1), x|(1<<bit), l1, bit-1))
    return ans

  def sum(self, l: int, r: int) -> int:
    assert False, f'Yabai Keisanryo Error'
    return sum(k*v for k, v in self.topk(l, r, r-l))

  def _range_freq(self, l: int, r: int, x: int) -> int:
    '''a[l, r) で x 未満の要素の数を返す'''
    ans = 0
    for bit in range(self.log-1, -1, -1):
      l0 = self.v[bit].rank0(l)
      r0 = self.v[bit].rank0(r)
      if x >> bit & 1:
        # bit が立ってたら、区間の 0 の個数を答えに加算し、新たな区間は 1 のみ
        ans += r0 - l0
        # 1 が次の bit 列でどこに行くか
        l += self.mid[bit] - l0
        r += self.mid[bit] - r0
      else:
        # 0 が次の bit 列でどこに行くか
        l = l0
        r = r0
    return ans

  def range_freq(self, l: int, r: int, x: int, y: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: range_freq({l}, {r}, {x}, {y})'
    return self._range_freq(l, r, y) - self._range_freq(l, r, x)

  def prev_value(self, l: int, r: int, x: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: prev_value({l}, {r}, {x})'
    return self.kth_smallest(l, r, self._range_freq(l, r, x)-1)

  def next_value(self, l: int, r: int, x: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: next_value({l}, {r}, {x})'
    return self.kth_smallest(l, r, self._range_freq(l, r, x))

  def range_count(self, l: int, r: int, x: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: range_count({l}, {r}, {x})'
    return self.rank(r, x) - self.rank(l, x)

  def __len__(self):
    return self.size

  def __str__(self):
    return f'WaveletMatrix({[self.access(i) for i in range(self.size)]})'

  __repr__ = __str__

