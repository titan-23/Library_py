# from titan_pylib.data_structures.wavelet_matrix.fenwick_tree_wavelet_matrix import FenwickTreeWaveletMatrix
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
# from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
from typing import List, Union, Iterable, Optional

class FenwickTree():
  """FenwickTreeです。
  """

  def __init__(self, n_or_a: Union[Iterable[int], int]):
    """構築します。
    :math:`O(n)` です。

    Args:
      n_or_a (Union[Iterable[int], int]): `n_or_a` が `int` のとき、初期値 `0` 、長さ `n` で構築します。
                                          `n_or_a` が `Iterable` のとき、初期値 `a` で構築します。
    """
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
    """区間 ``[0, r)`` の総和を返します。
    :math:`O(\\log{n})` です。
    """
    assert 0 <= r <= self._size, \
        f'IndexError: {self.__class__.__name__}.pref({r}), n={self._size}'
    ret, _tree = 0, self._tree
    while r > 0:
      ret += _tree[r]
      r &= r - 1
    return ret

  def suff(self, l: int) -> int:
    """区間 ``[l, n)`` の総和を返します。
    :math:`O(\\log{n})` です。
    """
    assert 0 <= l < self._size, \
        f'IndexError: {self.__class__.__name__}.suff({l}), n={self._size}'
    return self.pref(self._size) - self.pref(l)

  def sum(self, l: int, r: int) -> int:
    """区間 ``[l, r)`` の総和を返します。
    :math:`O(\\log{n})` です。
    """
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
    """位置 ``k`` の要素を返します。
    :math:`O(\\log{n})` です。
    """
    assert -self._size <= k < self._size, \
        f'IndexError: {self.__class__.__name__}[{k}], n={self._size}'
    if k < 0:
      k += self._size
    return self.sum(k, k+1)

  def add(self, k: int, x: int) -> None:
    """``k`` 番目の値に ``x`` を加えます。
    :math:`O(\\log{n})` です。
    """
    assert 0 <= k < self._size, \
        f'IndexError: {self.__class__.__name__}.add({k}, {x}), n={self._size}'
    k += 1
    _tree = self._tree
    while k <= self._size:
      _tree[k] += x
      k += k & -k

  def __setitem__(self, k: int, x: int):
    """``k`` 番目の値を ``x`` に更新します。
    :math:`O(\\log{n})` です。
    """
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

  def tolist(self) -> List[int]:
    """リストにして返します。
    :math:`O(n)` です。
    """
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
from typing import List, Tuple, Sequence
from bisect import bisect_left

class FenwickTreeWaveletMatrix():

  def __init__(self, sigma: int, pos: List[Tuple[int, int, int]] = []):
    self.sigma: int = sigma
    self.log: int = (sigma-1).bit_length()
    self.mid: array[int] = array('I', bytes(4*self.log))
    self.xy: List[Tuple[int, int]] = self._sort_unique([(x, y) for x, y, _ in pos])
    self.y: List[int] = self._sort_unique([y for _, y, _ in pos])
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
    # sum([w1, w2) x [h1, h2))
    l = bisect_left(self.xy, (w1, 0))
    r = bisect_left(self.xy, (w2, 0))
    return self._sum(l, r, bisect_left(self.y, h2)) - self._sum(l, r, bisect_left(self.y, h1))

