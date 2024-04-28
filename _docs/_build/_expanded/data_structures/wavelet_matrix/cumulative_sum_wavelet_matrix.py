# from titan_pylib.data_structures.wavelet_matrix.cumulative_sum_wavelet_matrix import CumulativeSumWaveletMatrix
# from titan_pylib.data_structures.bit_vector.bit_vector import BitVector
# from titan_pylib.data_structures.bit_vector.bit_vector_interface import BitVectorInterface
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
  """コンパクトな bit vector です。
  """

  def __init__(self, n: int):
    """長さ ``n`` の ``BitVector`` です。

    bit を保持するのに ``array[I]`` を使用します。
    ``block_size= n / 32`` として、使用bitは ``32*block_size=2n bit`` です。

    累積和を保持するのに同様の ``array[I]`` を使用します。
    32bitごとの和を保存しています。同様に使用bitは ``2n bit`` です。
    """
    assert 0 <= n < 4294967295
    self.N = n
    self.block_size = (n + 31) >> 5
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
    """``k`` 番目の bit を ``1`` にします。
    :math:`O(1)` です。

    Args:
      k (int): インデックスです。
    """
    self.bit[k>>5] |= 1 << (k & 31)

  def build(self) -> None:
    """構築します。
    **これ以降 ``set`` メソッドを使用してはいけません。**
    :math:`O(n)` です。
    """
    acc, bit = self.acc, self.bit
    for i in range(self.block_size):
      acc[i+1] = acc[i] + BitVector._popcount(bit[i])

  def access(self, k: int) -> int:
    """``k`` 番目の bit を返します。
    :math:`O(1)` です。
    """
    return (self.bit[k >> 5] >> (k & 31)) & 1

  def __getitem__(self, k: int) -> int:
    return (self.bit[k >> 5] >> (k & 31)) & 1

  def rank0(self, r: int) -> int:
    """``a[0, r)`` に含まれる ``0`` の個数を返します。
    :math:`O(1)` です。
    """
    return r - (self.acc[r>>5] + BitVector._popcount(self.bit[r>>5] & ((1 << (r & 31)) - 1)))

  def rank1(self, r: int) -> int:
    """``a[0, r)`` に含まれる ``1`` の個数を返します。
    :math:`O(1)` です。
    """
    return self.acc[r>>5] + BitVector._popcount(self.bit[r>>5] & ((1 << (r & 31)) - 1))

  def rank(self, r: int, v: int) -> int:
    """``a[0, r)`` に含まれる ``v`` の個数を返します。
    :math:`O(1)` です。
    """
    return self.rank1(r) if v else self.rank0(r)

  def select0(self, k: int) -> int:
    """``k`` 番目の ``0`` のインデックスを返します。
    :math:`O(\\log{n})` です。
    """
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
    """``k`` 番目の ``1`` のインデックスを返します。
    :math:`O(\\log{n})` です。
    """
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
    """``k`` 番目の ``v`` のインデックスを返します。
    :math:`O(\\log{n})` です。
    """
    return self.select1(k) if v else self.select0(k)

  def __len__(self):
    return self.N

  def __str__(self):
    return str([self.access(i) for i in range(self.N)])

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'
# from titan_pylib.data_structures.cumulative_sum.cumulative_sum import CumulativeSum
from typing import Iterable

class CumulativeSum():
  """1次元累積和です。
  """

  def __init__(self, a: Iterable[int], e: int=0):
    """
    :math:`O(n)` です。

    Args:
      a (Iterable[int]): ``CumulativeSum`` を構築する配列です。
      e (int): 単位元です。デフォルトは ``0`` です。
    """
    a = list(a)
    n = len(a)
    acc = [e] * (n+1)
    for i in range(n):
      acc[i+1] = acc[i] + a[i]
    self.n = n
    self.acc = acc
    self.a = a

  def pref(self, r: int) -> int:
    """区間 ``[0, r)`` の演算結果を返します。
    :math:`O(1)` です。

    Args:
      r (int): インデックスです。
    """
    assert 0 <= r <= self.n, \
        f'IndexError: {self.__class__.__name__}.pref({r}), n={self.n}'
    return self.acc[r]

  def all_sum(self) -> int:
    """区間 `[0, n)` の演算結果を返します。
    :math:`O(1)` です。

    Args:
      l (int): インデックスです。
      r (int): インデックスです。
    """
    return self.acc[-1]

  def sum(self, l: int, r: int) -> int:
    """区間 `[l, r)` の演算結果を返します。
    :math:`O(1)` です。

    Args:
      l (int): インデックスです。
      r (int): インデックスです。
    """
    assert 0 <= l <= r <= self.n, \
        f'IndexError: {self.__class__.__name__}.sum({l}, {r}), n={self.n}'
    return self.acc[r] - self.acc[l]

  prod = sum
  all_prod = all_sum

  def __getitem__(self, k: int) -> int:
    assert -self.n <= k < self.n, \
        f'IndexError: {self.__class__.__name__}[{k}], n={self.n}'
    return self.a[k]

  def __len__(self):
    return len(self.a)

  def __str__(self):
    return str(self.acc)

  __repr__ = __str__
from array import array
from typing import List, Tuple, Sequence, Iterable
from bisect import bisect_left

class CumulativeSumWaveletMatrix():

  def __init__(self,
               sigma: int,
               pos: Iterable[Tuple[int, int, int]]=[]
               ) -> None:
    """
    Args:
      sigma (int): yの最大値
      pos (List[Tuple[int, int, int]], optional): List[(x, y, w)]
    """
    self.sigma: int = sigma
    self.log: int = (sigma-1).bit_length()
    self.mid: array[int] = array('I', bytes(4*self.log))
    self.xy: List[Tuple[int, int]] = self._sort_unique([(x, y) for x, y, _ in pos])
    self.y: List[int] = self._sort_unique([y for _, y in self.xy])
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
    self.bit: List[CumulativeSum] = [CumulativeSum(a) for a in ws]

  def _build(self, a: Sequence[int]) -> None:
    # 列 a から wm を構築する
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

  def _sort_unique(self, a: List) -> List:
    if not a:
      return a
    a.sort()
    b = [a[0]]
    for e in a:
      if b[-1] == e:
        continue
      b.append(e)
    return b

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
    """sum([w1, w2) x [h1, h2))"""
    assert 0 <= w1 <= w2
    assert 0 <= h1 <= h2
    l = bisect_left(self.xy, (w1, 0))
    r = bisect_left(self.xy, (w2, 0))
    return self._sum(l, r, bisect_left(self.y, h2)) - self._sum(l, r, bisect_left(self.y, h1))

