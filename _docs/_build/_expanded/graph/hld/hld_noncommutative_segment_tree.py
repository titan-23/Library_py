# from titan_pylib.graph.hld.hld_noncommutative_segment_tree import HLDNoncommutativeSegmentTree
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
# from titan_pylib.graph.hld.hld import HLD
from typing import Any, Iterator, List, Tuple

class HLD():

  def __init__(self, G: List[List[int]], root: int):
    """``root`` を根とする木 ``G`` を HLD します。
    :math:`O(n)` です。

    Args:
      G (List[List[int]]): 木を表す隣接リストです。
      root (int): 根です。
    """
    n = len(G)
    self.n: int = n
    self.G: List[List[int]] = G
    self.size: List[int] = [1] * n
    self.par: List[int] = [-1] * n
    self.dep: List[int] = [-1] * n
    self.nodein: List[int] = [0] * n
    self.nodeout: List[int] = [0] * n
    self.head: List[int] = [0] * n
    self.hld: List[int] = [0] * n
    self._dfs(root)

  def _dfs(self, root: int) -> None:
    dep, par, size, G = self.dep, self.par, self.size, self.G
    dep[root] = 0
    stack = [root]
    while stack:
      v = stack.pop()
      if v >= 0:
        dep_nxt = dep[v] + 1
        for x in G[v]:
          if dep[x] != -1:
            continue
          dep[x] = dep_nxt
          stack.append(~x)
          stack.append(x)
      else:
        v = ~v
        G_v, dep_v = G[v], dep[v]
        for i, x in enumerate(G_v):
          if dep[x] < dep_v:
            par[v] = x
            continue
          size[v] += size[x]
          if size[x] > size[G_v[0]]:
            G_v[0], G_v[i] = G_v[i], G_v[0]

    head, nodein, nodeout, hld = self.head, self.nodein, self.nodeout, self.hld
    curtime = 0
    stack = [~root, root]
    while stack:
      v = stack.pop()
      if v >= 0:
        if par[v] == -1:
          head[v] = v
        nodein[v] = curtime
        hld[curtime] = v
        curtime += 1
        if not G[v]:
          continue
        G_v0 = G[v][0]
        for x in reversed(G[v]):
          if x == par[v]:
            continue
          head[x] = head[v] if x == G_v0 else x
          stack.append(~x)
          stack.append(x)
      else:
        nodeout[~v] = curtime

  def build_list(self, a: List[Any]) -> List[Any]:
    """``hld配列`` を基にインデックスを振りなおします。非破壊的です。
    :math:`O(n)` です。

    Args:
      a (List[Any]): 元の配列です。

    Returns:
      List[Any]: 振りなおし後の配列です。
    """
    return [a[e] for e in self.hld]

  def for_each_vertex(self, u: int, v: int) -> Iterator[Tuple[int, int]]:
    """``u-v`` パスに対応する区間のインデックスを返します。
    :math:`O(\\log{n})` です。
    """
    head, nodein, dep, par = self.head, self.nodein, self.dep, self.par
    while head[u] != head[v]:
      if dep[head[u]] < dep[head[v]]:
        u, v = v, u
      yield nodein[head[u]], nodein[u]+1
      u = par[head[u]]
    if dep[u] < dep[v]:
      u, v = v, u
    yield nodein[v], nodein[u]+1

  def for_each_vertex_subtree(self, v: int) -> Iterator[Tuple[int, int]]:
    """頂点 ``v`` の部分木に対応する区間のインデックスを返します。
    :math:`O(1)` です。
    """
    yield self.nodein[v], self.nodeout[v]

  def path_kth_elm(self, s: int, t: int, k: int) -> int:
    """``s`` から ``t`` に向かって ``k`` 個進んだ頂点のインデックスを返します。
    存在しないときは ``-1`` を返します。
    :math:`O(\\log{n})` です。
    """
    head, dep, par = self.head, self.dep, self.par
    lca = self.lca(s, t)
    d = dep[s] + dep[t] - 2*dep[lca]
    if d < k:
      return -1
    if dep[s] - dep[lca] < k:
      s = t
      k = d - k
    hs = head[s]
    while dep[s] - dep[hs] < k:
      k -= dep[s] - dep[hs] + 1
      s = par[hs]
      hs = head[s]
    return self.hld[self.nodein[s] - k]

  def lca(self, u: int, v: int) -> int:
    """``u``, ``v`` の LCA を返します。
    :math:`O(\\log{n})` です。
    """
    nodein, head, par = self.nodein, self.head, self.par
    while True:
      if nodein[u] > nodein[v]:
        u, v = v, u
      if head[u] == head[v]:
        return u
      v = par[head[v]]

from typing import Union, Iterable, Callable, TypeVar, Generic
T = TypeVar('T')

class HLDNoncommutativeSegmentTree(Generic[T]):
  """セグ木搭載HLDです。

  Note:
    **非可換に対応してます。**
  """

  def __init__(self, hld: HLD, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T):
    self.hld: HLD = hld
    a = [e] * n_or_a if isinstance(n_or_a, int) else self.hld.build_list(list(n_or_a))
    self.seg: SegmentTree[T] = SegmentTree(a, op, e)
    self.rseg: SegmentTree[T] = SegmentTree(a[::-1], op, e)
    self.op: Callable[[T, T], T] = op
    self.e: T = e

  def path_prod(self, u: int, v: int) -> T:
    """頂点 ``u`` から頂点 ``v`` へのパスの集約値を返します。
    :math:`O(\\log^2{n})` です。

    Args:
      u (int): パスの **始点** です。
      v (int): パスの **終点** です。

    Returns:
      T: 求める集約値です。
    """
    head, nodein, dep, par, n = self.hld.head, self.hld.nodein, self.hld.dep, self.hld.par, self.hld.n
    lres, rres = self.e, self.e
    seg, rseg = self.seg, self.rseg
    while head[u] != head[v]:
      if dep[head[u]] > dep[head[v]]:
        lres = self.op(lres, rseg.prod(n-nodein[u]-1, n-nodein[head[u]]))
        u = par[head[u]]
      else:
        rres = self.op(seg.prod(nodein[head[v]], nodein[v]+1), rres)
        v = par[head[v]]
    if dep[u] > dep[v]:
      lres = self.op(lres, rseg.prod(n-nodein[u]-1, n-nodein[v]))
    else:
      lres = self.op(lres, seg.prod(nodein[u], nodein[v]+1))
    return self.op(lres, rres)

  def get(self, k: int) -> T:
    """頂点の値を返します。
    :math:`O(\\log{n})` です。

    Args:
      k (int): 頂点のインデックスです。

    Returns:
      T: 頂点の値です。
    """
    return self.seg[self.hld.nodein[k]]

  def set(self, k: int, v: T) -> None:
    """頂点の値を更新します。
    :math:`O(\\log{n})` です。

    Args:
      k (int): 頂点のインデックスです。
      v (T): 更新する値です。
    """
    self.seg[self.hld.nodein[k]] = v
    self.rseg[self.hld.n-self.hld.nodein[k]-1] = v

  __getitem__ = get
  __setitem__ = set

  def subtree_prod(self, v: int) -> T:
    return self.seg.prod(self.hld.nodein[v], self.hld.nodeout[v])


