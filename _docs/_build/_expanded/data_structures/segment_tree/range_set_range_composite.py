# from titan_pylib.data_structures.segment_tree.range_set_range_composite import RangeSetRangeComposite
# from titan_pylib.data_structures.segment_tree.segment_tree import SegmentTree
# from titan_pylib.data_structures.segment_tree.segment_tree_interface import SegmentTreeInterface
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union, Iterable, Callable, List
T = TypeVar('T')

class SegmentTreeInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               e: T):
    raise NotImplementedError

  @abstractmethod
  def set(self, k: int, v: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def get(self, k: int) -> T:
    raise NotImplementedError

  @abstractmethod
  def prod(self, l: int, r: int) -> T:
    raise NotImplementedError

  @abstractmethod
  def all_prod(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    raise NotImplementedError

  @abstractmethod
  def min_left(self, r: int, f: Callable[[T], bool]) -> int:
    raise NotImplementedError

  @abstractmethod
  def tolist(self) -> List[T]:
    raise NotImplementedError

  @abstractmethod
  def __getitem__(self, k: int) -> T:
    raise NotImplementedError

  @abstractmethod
  def __setitem__(self, k: int, v: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def __str__(self):
    raise NotImplementedError

  @abstractmethod
  def __repr__(self):
    raise NotImplementedError

from typing import Generic, Iterable, TypeVar, Callable, Union, List
T = TypeVar('T')

class SegmentTree(SegmentTreeInterface, Generic[T]):
  """セグ木です。非再帰です。
  """

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               e: T) -> None:
    """``SegmentTree`` を構築します。
    :math:`O(n)` です。

    Args:
      n_or_a (Union[int, Iterable[T]]): ``n: int`` のとき、 ``e`` を初期値として長さ ``n`` の ``SegmentTree`` を構築します。
                                        ``a: Iterable[T]`` のとき、 ``a`` から ``SegmentTree`` を構築します。
      op (Callable[[T, T], T]): 2項演算の関数です。
      e (T): 単位元です。
    """
    self._op = op
    self._e = e
    if isinstance(n_or_a, int):
      self._n = n_or_a
      self._log = (self._n - 1).bit_length()
      self._size = 1 << self._log
      self._data = [e] * (self._size << 1)
    else:
      n_or_a = list(n_or_a)
      self._n = len(n_or_a)
      self._log = (self._n - 1).bit_length()
      self._size = 1 << self._log
      _data = [e] * (self._size << 1)
      _data[self._size:self._size+self._n] = n_or_a
      for i in range(self._size-1, 0, -1):
        _data[i] = op(_data[i<<1], _data[i<<1|1])
      self._data = _data

  def set(self, k: int, v: T) -> None:
    """一点更新です。
    :math:`O(\\log{n})` です。

    Args:
      k (int): 更新するインデックスです。
      v (T): 更新する値です。

    制約:
      :math:`-n \\leq n \\leq k < n`
    """
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.set({k}, {v}), n={self._n}'
    if k < 0:
      k += self._n
    k += self._size
    self._data[k] = v
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._op(self._data[k<<1], self._data[k<<1|1])

  def get(self, k: int) -> T:
    """一点取得です。
    :math:`O(1)` です。

    Args:
      k (int): インデックスです。

    制約:
      :math:`-n \\leq n \\leq k < n`
    """
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.get({k}), n={self._n}'
    if k < 0:
      k += self._n
    return self._data[k+self._size]

  def prod(self, l: int, r: int) -> T:
    """区間 ``[l, r)`` の総積を返します。
    :math:`O(\\log{n})` です。

    Args:
      l (int): インデックスです。
      r (int): インデックスです。

    制約:
      :math:`0 \\leq l \\leq r \\leq n`
    """
    assert 0 <= l <= r <= self._n, \
        f'IndexError: {self.__class__.__name__}.prod({l}, {r})'
    l += self._size
    r += self._size
    lres = self._e
    rres = self._e
    while l < r:
      if l & 1:
        lres = self._op(lres, self._data[l])
        l += 1
      if r & 1:
        rres = self._op(self._data[r^1], rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  def all_prod(self) -> T:
    """区間 ``[0, n)`` の総積を返します。
    :math:`O(1)` です。
    """
    return self._data[1]

  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    '''Find the largest index R s.t. f([l, R)) == True. / O(\\log{n})'''
    assert 0 <= l <= self._n, \
        f'IndexError: {self.__class__.__name__}.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'{self.__class__.__name__}.max_right({l}, f), f({self._e}) must be true.'
    if l == self._n:
      return self._n
    l += self._size
    s = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self._op(s, self._data[l])):
        while l < self._size:
          l <<= 1
          if f(self._op(s, self._data[l])):
            s = self._op(s, self._data[l])
            l |= 1
        return l - self._size
      s = self._op(s, self._data[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  def min_left(self, r: int, f: Callable[[T], bool]) -> int:
    '''Find the smallest index L s.t. f([L, r)) == True. / O(\\log{n})'''
    assert 0 <= r <= self._n, \
        f'IndexError: {self.__class__.__name__}.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'{self.__class__.__name__}.min_left({r}, f), f({self._e}) must be true.'
    if r == 0:
      return 0
    r += self._size
    s = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._op(self._data[r], s)):
        while r < self._size:
          r = r << 1 | 1
          if f(self._op(self._data[r], s)):
            s = self._op(self._data[r], s)
            r ^= 1
        return r + 1 - self._size
      s = self._op(self._data[r], s)
      if r & -r == r:
        break
    return 0

  def tolist(self) -> List[T]:
    """
    :math:`O(n)` です。
    """
    return [self.get(i) for i in range(self._n)]

  def show(self) -> None:
    """デバッグ用のメソッドです。
    """
    print(f'<{self.__class__.__name__}> [\n' + '\n'.join(['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]) + '\n]')

  def __getitem__(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.__getitem__({k}), n={self._n}'
    return self.get(k)

  def __setitem__(self, k: int, v: T):
    assert -self._n <= k < self._n, \
        f'IndexError: {self.__class__.__name__}.__setitem__{k}, {v}), n={self._n}'
    self.set(k, v)

  def __len__(self):
    return self._n

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'
# from titan_pylib.data_structures.set.wordsize_tree_set import WordsizeTreeSet
from array import array
from typing import Iterable, Optional, List

class WordsizeTreeSet():
  """``[0, u)`` の整数集合を管理する32分木です。
  空間 :math:`O(u)` であることに注意してください。
  """

  def __init__(self, u: int, a: Iterable[int]=[]) -> None:
    """:math:`O(u)` です。
    """
    assert u >= 0
    u += 1  # 念のため
    self.u = u
    data = []
    len_ = 0
    if a:
      u >>= 5
      A = array('I', bytes(4*(u+1)))
      for a_ in a:
        assert 0 <= a_ < self.u, \
            f'ValueError: {self.__class__.__name__}.__init__, {a_}, u={u}'
        if A[a_>>5] >> (a_&31) & 1 == 0:
          len_ += 1
          A[a_>>5] |= 1 << (a_&31)
      data.append(A)
      while u:
        a = array('I', bytes(4*((u>>5)+1)))
        for i in range(u+1):
          if A[i]:
            a[i>>5] |= 1 << (i&31)
        data.append(a)
        A = a
        u >>= 5
    else:
      while u:
        u >>= 5
        data.append(array('I', bytes(4*(u+1))))
    self.data: List[array[int]] = data
    self.len: int = len_
    self.len_data: int = len(data)

  def add(self, v: int) -> bool:
    """整数 ``v`` を個追加します。
    :math:`O(\\log{u})` です。
    """
    assert 0 <= v < self.u, \
        f'ValueError: {self.__class__.__name__}.add({v}), u={self.u}'
    if self.data[0][v>>5] >> (v&31) & 1: return False
    self.len += 1
    for a in self.data:
      a[v>>5] |= 1 << (v&31)
      v >>= 5
    return True

  def discard(self, v: int) -> bool:
    """整数 ``v`` を削除します。
    :math:`O(\\log{u})` です。
    """
    assert 0 <= v < self.u, \
        f'ValueError: {self.__class__.__name__}.discard({v}), u={self.u}'
    if self.data[0][v>>5] >> (v&31) & 1 == 0: return False
    self.len -= 1
    for a in self.data:
      a[v>>5] &= ~(1 << (v&31))
      v >>= 5
      if a[v]: break
    return True

  def ge(self, v: int) -> Optional[int]:
    """``v`` 以上で最小の要素を返します。存在しないとき、 ``None``を返します。
    :math:`O(\\log{u})` です。
    """
    assert 0 <= v < self.u, \
        f'ValueError: {self.__class__.__name__}.ge({v}), u={self.u}'
    data = self.data
    d = 0
    while True:
      if d >= self.len_data or v>>5 >= len(data[d]): return None
      m = data[d][v>>5] & ((~0) << (v&31))
      if m == 0:
        d += 1
        v = (v >> 5) + 1
      else:
        v = (v >> 5 << 5) + (m & -m).bit_length() - 1
        if d == 0: break
        v <<= 5
        d -= 1
    return v

  def gt(self, v: int) -> Optional[int]:
    """``v`` より大きい値で最小の要素を返します。存在しないとき、 ``None``を返します。
    :math:`O(\\log{u})` です。
    """
    assert 0 <= v < self.u, \
        f'ValueError: {self.__class__.__name__}.gt({v}), u={self.u}'
    if v + 1 == self.u: return
    return self.ge(v + 1)

  def le(self, v: int) -> Optional[int]:
    """``v`` 以下で最大の要素を返します。存在しないとき、 ``None``を返します。
    :math:`O(\\log{u})` です。
    """
    assert 0 <= v < self.u, \
        f'ValueError: {self.__class__.__name__}.le({v}), u={self.u}'
    data = self.data
    d = 0
    while True:
      if v < 0 or d >= self.len_data: return None
      m = data[d][v>>5] & ~((~1) << (v&31))
      if m == 0:
        d += 1
        v = (v >> 5) - 1
      else:
        v = (v >> 5 << 5) + m.bit_length() - 1
        if d == 0: break
        v <<= 5
        v += 31
        d -= 1
    return v

  def lt(self, v: int) -> Optional[int]:
    """``v`` より小さい値で最大の要素を返します。存在しないとき、 ``None``を返します。
    :math:`O(\\log{u})` です。
    """
    assert 0 <= v < self.u, \
        f'ValueError: {self.__class__.__name__}.lt({v}), u={self.u}'
    if v - 1 == 0: return
    return self.le(v - 1)

  def get_min(self) -> Optional[int]:
    """`最小値を返します。存在しないとき、 ``None``を返します。
    :math:`O(\\log{u})` です。
    """
    return self.ge(0)

  def get_max(self) -> Optional[int]:
    """最大値を返します。存在しないとき、 ``None``を返します。
    :math:`O(\\log{u})` です。
    """
    return self.le(self.u - 1)

  def pop_min(self) -> int:
    """最小値を削除して返します。
    :math:`O(\\log{u})` です。
    """
    v = self.get_min()
    assert v is not None, \
        f'IndexError: pop_min() from empty {self.__class__.__name__}.'
    self.discard(v)
    return v

  def pop_max(self) -> int:
    """最大値を削除して返します。
    :math:`O(\\log{u})` です。
    """
    v = self.get_max()
    assert v is not None, \
        f'IndexError: pop_max() from empty {self.__class__.__name__}.'
    self.discard(v)
    return v

  def clear(self) -> None:
    """集合を空にします。
    :math:`O(n\\log{u})` です。
    """
    for e in self:
      self.discard(e)
    self.len = 0

  def tolist(self) -> List[int]:
    """リストにして返します。
    :math:`O(n\\log{u})` です。
    """
    return [x for x in self]

  def __bool__(self):
    return self.len > 0

  def __len__(self):
    return self.len

  def __contains__(self, v: int):
    assert 0 <= v < self.u, \
        f'ValueError: {v} in {self.__class__.__name__}, u={self.u}'
    return self.data[0][v>>5] >> (v&31) & 1 == 1

  def __iter__(self):
    self._val = self.ge(0)
    return self

  def __next__(self):
    if self._val is None:
      raise StopIteration
    pre = self._val
    self._val = self.gt(pre)
    return pre

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return f'{self.__class__.__name__}({self.u}, {self})'

from typing import Union, Callable, TypeVar, Generic, Iterable
T = TypeVar('T')

class RangeSetRangeComposite(Generic[T]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               pow_: Callable[[T, int], T],
               e: T,
               id: T
               ) -> None:
    self.op = op
    self.pow = pow_
    self.e = e
    self.id = id
    a = [e] * n_or_a if isinstance(n_or_a, int) else list(n_or_a)
    a.append(e)
    self.seg = SegmentTree(a, op, e)
    self.n = len(self.seg)
    self.indx = WordsizeTreeSet(self.n+1, range(self.n+1))
    self.val = a
    self.beki = [1] * self.n

  def prod(self, l: int, r: int) -> T:
    ll = self.indx.ge(l)
    rr = self.indx.le(r)
    ans = self.e
    if ll != l:
      l0 = self.indx.le(l)
      beki = self.beki[l0] - (l-l0) if l0+self.beki[l0] <= r else r - l
      ans = self.pow(self.val[l0], beki)
    if ll < rr:
      ans = self.op(ans, self.seg.prod(ll, rr))
    if rr != r and l <= rr:
      ans = self.op(ans, self.pow(self.val[rr], r - rr))
    return ans

  def apply(self, l: int, r: int, f: T) -> None:
    indx, val, beki, seg = self.indx, self.val, self.beki, self.seg

    l0 = indx.le(l)
    r0 = indx.le(r)
    if l != l0:
      seg[l0] = self.pow(val[l0], l - l0)
    if r != r0:
      beki[r] = beki[r0] - (r - r0)
      indx.add(r)
      val[r] = val[r0]
      seg[r] = self.pow(val[r], beki[r])
    if l != l0:
      beki[l0] = l - l0

    i = indx.gt(l)
    while i < r:
      seg[i] = self.e
      indx.discard(i)
      i = indx.gt(i)
    val[l] = f
    indx.add(l)
    beki[l] = r - l
    seg[l] = self.pow(f, beki[l])

