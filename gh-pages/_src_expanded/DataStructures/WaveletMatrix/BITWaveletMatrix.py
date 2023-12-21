# from Library_py.DataStructures.WaveletMatrix.BITWaveletMatrix import BITWaveletMatrix
# from Library_py.DataStructures.BitVector.BitVector import BitVector
# from .BitVectorInterface import BitVectorInterface
from abc import ABC, abstractmethod

class BitVectorInterface(ABC):

  @abstractmethod
  def access(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def __getitem__(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def rank0(self, r: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def rank1(self, r: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def rank(self, r: int, v: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def select0(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def select1(self, k: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def select(self, k: int, v: int) -> int:
    raise NotImplementedError

  @abstractmethod
  def __len__(self) -> int:
    raise NotImplementedError

  @abstractmethod
  def __str__(self) -> str:
    raise NotImplementedError

  @abstractmethod
  def __repr__(self) -> str:
    raise NotImplementedError

from array import array

class BitVector(BitVectorInterface):

  # 簡潔ではない
  # コンパクトのつもり

  def __init__(self, n: int):
    assert 0 <= n < 4294967295
    self.N = n
    self.block_size = (n + 31) >> 5
    # bit数 32*n/32 * 2 = 2n bit
    b = bytes(4*(self.block_size+1))
    self.bit = array('I', b)
    self.acc = array('I', b)

  @staticmethod
  def _popcount(x: int) -> int:
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = x + (x >> 4) & 0x0f0f0f0f
    x += x >> 8
    x += x >> 16
    return x & 0x0000007f

  def set(self, k: int) -> None:
    self.bit[k>>5] |= 1 << (k & 31)

  def build(self) -> None:
    acc, bit = self.acc, self.bit
    for i in range(self.block_size):
      acc[i+1] = acc[i] + BitVector._popcount(bit[i])

  def access(self, k: int) -> int:
    return (self.bit[k >> 5] >> (k & 31)) & 1

  def __getitem__(self, k: int) -> int:
    return (self.bit[k >> 5] >> (k & 31)) & 1

  def rank0(self, r: int) -> int:
    # a[0, r) に含まれる 0 の個数
    return r - (self.acc[r>>5] + BitVector._popcount(self.bit[r>>5] & ((1 << (r & 31)) - 1)))

  def rank1(self, r: int) -> int:
    # a[0, r) に含まれる 1 の個数
    return self.acc[r>>5] + BitVector._popcount(self.bit[r>>5] & ((1 << (r & 31)) - 1))

  def rank(self, r: int, v: int) -> int:
    # a[0, r) に含まれる v の個数
    return self.rank1(r) if v else self.rank0(r)

  def select0(self, k: int) -> int:
    # k 番目の 0 のindex
    # O(log(N))
    if k < 0 or self.rank0(self.N) <= k:
      return -1
    l, r = 0, self.block_size+1
    while r - l > 1:
      m = (l + r) >> 1
      if m*32 - self.acc[m] > k:
        r = m
      else:
        l = m
    indx = 32 * l
    k = k - (l*32 - self.acc[l]) + self.rank0(indx)
    l, r = indx, indx+32
    while r - l > 1:
      m = (l + r) >> 1
      if self.rank0(m) > k:
        r = m
      else:
        l = m
    return l

  def select1(self, k: int) -> int:
    # k 番目の 1 のindex
    # O(log(N))
    if k < 0 or self.rank1(self.N) <= k:
      return -1
    l, r = 0, self.block_size+1
    while r - l > 1:
      m = (l + r) >> 1
      if self.acc[m] > k:
        r = m
      else:
        l = m
    indx = 32 * l
    k = k - self.acc[l] + self.rank1(indx)
    l, r = indx, indx+32
    while r - l > 1:
      m = (l + r) >> 1
      if self.rank1(m) > k:
        r = m
      else:
        l = m
    return l

  def select(self, k: int, v: int) -> int:
    # k 番目の v のindex
    # O(log(N))
    return self.select1(k) if v else self.select0(k)

  def __len__(self):
    return self.N

  def __str__(self):
    return str([self.access(i) for i in range(self.N)])

  def __repr__(self):
    return f'BitVector({self})'

# from Library_py.DataStructures.WaveletMatrix.WaveletMatrix import WaveletMatrix
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
    assert -self.size <= k < self.size, \
        f'IndexError: {self.__class__.__name__}.access({k}), size={self.size}'
    if k < 0:
      k += self.size
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
    assert -self.size <= k < self.size, f'IndexError: {self.__class__.__name__}[{k}], size={self.size}'
    return self.access(k)

  def rank(self, r: int, x: int) -> int:
    '''a[0, r) に含まれる x の個数'''
    assert 0 <= r <= self.size, f'IndexError: {self.__class__.__name__}.rank(), r={r}, size={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: {self.__class__.__name__}.rank(), x={x}, LIM={1<<self.log}'
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
    assert 0 <= k < self.size, f'IndexError: {self.__class__.__name__}.select({k}, {x}), k={k}, size={self.size}'
    assert 0 <= x < 1<<self.log, f'ValueError: {self.__class__.__name__}.select({k}, {x}), x={x}, LIM={1<<self.log}'
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
    assert 0 <= l <= r <= self.size, f'IndexError: {self.__class__.__name__}.kth_smallest({l}, {r}, {k}), size={self.size}'
    assert 0 <= k < r-l, f'IndexError: {self.__class__.__name__}.kth_smallest({l}, {r}, {k}), wrong k'
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
    assert 0 <= l <= r <= self.size, f'IndexError: {self.__class__.__name__}.kth_largest({l}, {r}, {k}), size={self.size}'
    assert 0 <= k < r-l, f'IndexError: {self.__class__.__name__}.kth_largest({l}, {r}, {k}), wrong k'
    return self.kth_smallest(l, r, r-l-k-1)

  def topk(self, l: int, r: int, k: int) -> List[Tuple[int, int]]:
    assert 0 <= l <= r <= self.size, f'IndexError: {self.__class__.__name__}.topk({l}, {r}, {k}), size={self.size}'
    assert 0 <= k < r-l, f'IndexError: {self.__class__.__name__}.topk({l}, {r}, {k}), wrong k'
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
    assert False, 'Yabai Keisanryo Error'
    return sum(k*v for k, v in self.topk(l, r, r-l))

  def _range_freq(self, l: int, r: int, x: int) -> int:
    '''a[l, r) で x 未満の要素の数を返す'''
    ans = 0
    for bit in range(self.log-1, -1, -1):
      l0, r0 = self.v[bit].rank0(l), self.v[bit].rank0(r)
      if x >> bit & 1:
        # bit が立ってたら、区間の 0 の個数を答えに加算し、新たな区間は 1 のみ
        ans += r0 - l0
        # 1 が次の bit 列でどこに行くか
        l += self.mid[bit] - l0
        r += self.mid[bit] - r0
      else:
        # 0 が次の bit 列でどこに行くか
        l, r = l0, r0
    return ans

  def range_freq(self, l: int, r: int, x: int, y: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: {self.__class__.__name__}.range_freq({l}, {r}, {x}, {y})'
    return self._range_freq(l, r, y) - self._range_freq(l, r, x)

  def prev_value(self, l: int, r: int, x: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: {self.__class__.__name__}.prev_value({l}, {r}, {x})'
    return self.kth_smallest(l, r, self._range_freq(l, r, x)-1)

  def next_value(self, l: int, r: int, x: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: {self.__class__.__name__}.next_value({l}, {r}, {x})'
    return self.kth_smallest(l, r, self._range_freq(l, r, x))

  def range_count(self, l: int, r: int, x: int) -> int:
    assert 0 <= l <= r <= self.size, \
        f'IndexError: {self.__class__.__name__}.range_count({l}, {r}, {x})'
    return self.rank(r, x) - self.rank(l, x)

  def __len__(self):
    return self.size

  def __str__(self):
    return f'{self.__class__.__name__}({[self.access(i) for i in range(self.size)]})'

  __repr__ = __str__

# from Library_py.DataStructures.FenwickTree.FenwickTree import FenwickTree
from typing import List, Union, Iterable, Optional

class FenwickTree():

  def __init__(self, n_or_a: Union[Iterable[int], int]):
    if isinstance(n_or_a, int):
      self._size = n_or_a
      self._tree = [0] * (self._size + 1)
    else:
      a = n_or_a if isinstance(n_or_a, list) else list(n_or_a)
      _size = len(a)
      _tree = [0] + a
      for i in range(1, _size):
        if i + (i & -i) <= _size:
          _tree[i + (i & -i)] += _tree[i]
      self._size = _size
      self._tree = _tree
    self._s = 1 << (self._size - 1).bit_length()

  def pref(self, r: int) -> int:
    assert 0 <= r <= self._size, \
        f'IndexError: {self.__class__.__name__}.pref({r}), n={self._size}'
    ret, _tree = 0, self._tree
    while r > 0:
      ret += _tree[r]
      r &= r - 1
    return ret

  def suff(self, l: int) -> int:
    assert 0 <= l < self._size, \
        f'IndexError: {self.__class__.__name__}.suff({l}), n={self._size}'
    return self.pref(self._size) - self.pref(l)

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self._size, \
        f'IndexError: {self.__class__.__name__}.sum({l}, {r}), n={self._size}'
    _tree = self._tree
    res = 0
    while r > l:
      res += _tree[r]
      r &= r - 1
    while l > r:
      res -= _tree[l]
      l &= l - 1
    return res

  prod = sum

  def __getitem__(self, k: int) -> int:
    assert -self._size <= k < self._size, \
        f'IndexError: {self.__class__.__name__}[{k}], n={self._size}'
    if k < 0:
      k += self._size
    return self.sum(k, k+1)

  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self._size, \
        f'IndexError: {self.__class__.__name__}.add({k}, {x}), n={self._size}'
    k += 1
    _tree = self._tree
    while k <= self._size:
      _tree[k] += x
      k += k & -k

  def __setitem__(self, k: int, x: int):
    assert -self._size <= k < self._size, \
        f'IndexError: {self.__class__.__name__}[{k}] = {x}, n={self._size}'
    if k < 0: k += self._size
    pre = self[k]
    self.add(k, x - pre)

  def bisect_left(self, w: int) -> Optional[int]:
    i, s, _size, _tree = 0, self._s, self._size, self._tree
    while s:
      if i + s <= _size and _tree[i + s] < w:
        w -= _tree[i + s]
        i += s
      s >>= 1
    return i if w else None

  def bisect_right(self, w: int) -> int:
    i, s, _size, _tree = 0, self._s, self._size, self._tree
    while s:
      if i + s <= _size and _tree[i + s] <= w:
        w -= _tree[i + s]
        i += s
      s >>= 1
    return i

  def _pop(self, k: int) -> int:
    assert k >= 0
    i, acc, s, _size, _tree = 0, 0, self._s, self._size, self._tree
    while s:
      if i+s <= _size:
        if acc + _tree[i+s] <= k:
          acc += _tree[i+s]
          i += s
        else:
          _tree[i+s] -= 1
      s >>= 1
    return i

  def show(self) -> None:
    print('[' + ', '.join(map(str, (self.pref(i) for i in range(self._size+1)))) + ']')

  def tolist(self) -> List[int]:
    sub = [self.pref(i) for i in range(self._size+1)]
    return [sub[i+1]-sub[i] for i in range(self._size)]

  @staticmethod
  def get_inversion_num(a: List[int], compress: bool=False) -> int:
    inv = 0
    if compress:
      a_ = sorted(set(a))
      z = {e: i for i, e in enumerate(a_)}
      fw = FenwickTree(len(a_))
      for i, e in enumerate(a):
        inv += i - fw.pref(z[e])
        fw.add(z[e], 1)
    else:
      fw = FenwickTree(len(a))
      for i, e in enumerate(a):
        inv += i - fw.pref(e)
        fw.add(e, 1)
    return inv

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'

from array import array
from typing import List, Tuple
from bisect import bisect_left

class BITWaveletMatrix(WaveletMatrix):

  def __init__(self, sigma: int, pos: List[Tuple[int, int, int]] = []):
    self.sigma: int = sigma
    self.log: int = (sigma-1).bit_length()
    self.mid: array[int] = array('I', bytes(4*self.log))
    self.xy: List[Tuple[int, int]] = self._zaatsu([(x, y) for x, y, _ in pos])
    self.y: List[int] = self._zaatsu([y for _, y, _ in pos])
    self.size: int = len(self.xy)
    self.v: List[BitVector] = [BitVector(self.size) for _ in range(self.log)]
    self._build([bisect_left(self.y, y) for _, y in self.xy])
    ws = [[0]*self.size for _ in range(self.log)]
    for x, y, w in pos:
      k = bisect_left(self.xy, (x, y))
      i_y = bisect_left(self.y, y)
      for bit in range(self.log-1, -1, -1):
        if i_y >> bit & 1:
          k = self.v[bit].rank1(k) + self.mid[bit]
        else:
          k = self.v[bit].rank0(k)
        ws[bit][k] += w
    self.bit: List[FenwickTree] = [FenwickTree(a) for a in ws]

  def _zaatsu(self, a: List) -> List:
    if not a:
      return a
    a.sort()
    b = [a[0]]
    for e in a:
      if b[-1] == e:
        continue
      b.append(e)
    return b

  def add_point(self, x: int, y: int, w: int) -> None:
    k = bisect_left(self.xy, (x, y))
    i_y = bisect_left(self.y, y)
    for bit in range(self.log-1, -1, -1):
      if i_y >> bit & 1:
        k = self.v[bit].rank1(k) + self.mid[bit]
      else:
        k = self.v[bit].rank0(k)
      self.bit[bit].add(k, w)

  def _sum(self, l: int, r: int, x: int) -> int:
    ans = 0
    for bit in range(self.log-1, -1, -1):
      l0, r0 = self.v[bit].rank0(l), self.v[bit].rank0(r)
      if x >> bit & 1:
        l += self.mid[bit] - l0
        r += self.mid[bit] - r0
        ans += self.bit[bit].sum(l0, r0)
      else:
        l, r = l0, r0
    return ans

  def sum(self, w1: int, w2: int, h1: int, h2: int) -> int:
    # sum([h1, h2) x [w1, w2))
    l = bisect_left(self.xy, (w1, 0))
    r = bisect_left(self.xy, (w2, 0))
    return self._sum(l, r, bisect_left(self.y, h2)) - self._sum(l, r, bisect_left(self.y, h1))


