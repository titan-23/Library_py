# from Library_py.Graph.EulerTour import EulerTour
# from Library_py.DataStructures.FenwickTree.FenwickTree import FenwickTree
from typing import List, Union, Iterable, Optional

class FenwickTree():

  def __init__(self, n_or_a: Union[Iterable[int], int]):
    if isinstance(n_or_a, int):
      self._size = n_or_a
      self._tree = [0] * (self._size + 1)
    else:
      a = n_or_a if isinstance(n_or_a, list) else list(n_or_a)
      self._size = len(a)
      self._tree = [0] + a
      for i in range(1, self._size):
        if i + (i & -i) <= self._size:
          self._tree[i + (i & -i)] += self._tree[i]
    self._s = 1 << (self._size - 1).bit_length()

  def pref(self, r: int) -> int:
    assert 0 <= r <= self._size, \
        f'IndexError: FenwickTree.pref({r}), n={self._size}'
    ret, _tree = 0, self._tree
    while r > 0:
      ret += _tree[r]
      r &= r - 1
    return ret

  def suff(self, l: int) -> int:
    assert 0 <= l < self._size, \
        f'IndexError: FenwickTree.suff({l}), n={self._size}'
    return self.pref(self._size) - self.pref(l)

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self._size, \
        f'IndexError: FenwickTree.sum({l}, {r}), n={self._size}'
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
        f'IndexError: FenwickTree.__getitem__({k}), n={self._size}'
    if k < 0:
      k += self._size
    return self.sum(k, k+1)

  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self._size, \
        f'IndexError: FenwickTree.add({k}, {x}), n={self._size}'
    k += 1
    _tree = self._tree
    while k <= self._size:
      _tree[k] += x
      k += k & -k

  def __setitem__(self, k: int, x: int):
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTree.__setitem__({k}, {x}), n={self._size}'
    if k < 0: k += self._size
    pre = self.__getitem__(k)
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
    return f'FenwickTree({self})'

# from Library_py.DataStructures.SegmentTree.SegmentTreeRmQ import SegmentTreeRmQ
# from Library_py.DataStructures.SegmentTree.SegmentTreeInterface import SegmentTreeInterface
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
  
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Generic, Iterable, TypeVar, Union, List
T = TypeVar('T', bound=SupportsLessThan)

class SegmentTreeRmQ(SegmentTreeInterface, Generic[T]):

  def __init__(self, _n_or_a: Union[int, Iterable[T]], e: T) -> None:
    '''Build a new SegmentTreeRmQ. / O(N)'''
    self._e = e
    if isinstance(_n_or_a, int):
      self._n = _n_or_a
      self._log  = (self._n - 1).bit_length()
      self._size = 1 << self._log
      self._data = [self._e] * (self._size << 1)
    else:
      _n_or_a = list(_n_or_a)
      self._n = len(_n_or_a)
      self._log  = (self._n - 1).bit_length()
      self._size = 1 << self._log
      _data = [self._e] * (self._size << 1)
      _data[self._size:self._size+self._n] = _n_or_a
      for i in range(self._size-1, 0, -1):
        _data[i] = _data[i<<1] if _data[i<<1] < _data[i<<1|1] else _data[i<<1|1]
      self._data = _data

  def set(self, k: int, v: T) -> None:
    '''Update a[k] <- x. / O(logN)'''
    if k < 0: k += self._n
    assert 0 <= k < self._n, \
        f'IndexError: SegmentTreeRmQ.set({k}: int, {v}: T), n={self._n}'
    k += self._size
    self._data[k] = v
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._data[k<<1] if self._data[k<<1] < self._data[k<<1|1] else self._data[k<<1|1]

  def get(self, k: int) -> T:
    '''Return a[k]. / O(1)'''
    if k < 0: k += self._n
    assert 0 <= k < self._n, \
        f'IndexError: SegmentTreeRmQ.get({k}: int), n={self._n}'
    return self._data[k+self._size]

  def prod(self, l: int, r: int) -> T:
    '''Return op([l, r)). / 0 <= l <= r <= n / O(logN)'''
    assert 0 <= l <= r <= self._n, \
        f'IndexError: SegmentTreeRmQ.prod({l}: int, {r}: int)'
    l += self._size
    r += self._size
    res = self._e
    while l < r:
      if l & 1:
        if res > self._data[l]:
          res = self._data[l]
        l += 1
      if r & 1:
        r ^= 1
        if res > self._data[r]:
          res = self._data[r]
      l >>= 1
      r >>= 1
    return res

  def all_prod(self) -> T:
    '''Return min([0, n)). / O(1)'''
    return self._data[1]

  def max_right(self, l: int, f=lambda lr: lr):
    '''Find the largest index R s.t. f([l, R)) == True. / O(logN)'''
    assert 0 <= l <= self._n, \
        f'IndexError: SegmentTreeRmQ.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'SegmentTreeRmQ.max_right({l}, f), f({self._e}) must be true.'
    if l == self._n: return self._n 
    l += self._size
    s = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(min(s, self._data[l])):
        while l < self._size:
          l <<= 1
          if f(min(s, self._data[l])):
            if s > self._data[l]:
              s = self._data[l]
            l += 1
        return l - self._size
      s = min(s, self._data[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  def min_left(self, r: int, f=lambda lr: lr):
    '''Find the smallest index L s.t. f([L, r)) == True. / O(logN)'''
    assert 0 <= r <= self._n, \
        f'IndexError: SegmentTreeRmQ.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'SegmentTreeRmQ.min_left({r}, f), f({self._e}) must be true.'
    if r == 0: return 0 
    r += self._size
    s = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(min(self._data[r], s)):
        while r < self._size:
          r = r<<1|1
          if f(min(self._data[r], s)):
            if s > self._data[r]:
              s = self._data[r]
            r -= 1
        return r + 1 - self._size
      s = min(self._data[r], s)
      if r & -r == r:
        break 
    return 0

  def tolist(self) -> List[T]:
    '''Return List[self]. / O(NlogN)'''
    return [self.get(i) for i in range(self._n)]

  def show(self) -> None:
    '''Debug. / O(N)'''
    print('<SegmentTreeRmQ> [\n' + '\n'.join(['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]) + '\n]')

  def __getitem__(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTreeRmQ.__getitem__({k}: int), n={self._n}'
    return self.get(k)

  def __setitem__(self, k: int, v: T):
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTreeRmQ.__setitem__{k}: int, {v}: T), n={self._n}'
    self.set(k, v)

  def __str__(self):
    return '[' + ', '.join(map(str, (self.get(i) for i in range(self._n)))) + ']'

  def __repr__(self):
    return f'SegmentTreeRmQ({self})'

from typing import List, Tuple

class EulerTour():

  def __init__(self, G: List[List[Tuple[int, int]]], root: int, vertexcost: List[int]=[]) -> None:
    n = len(G)
    if not vertexcost:
      vertexcost = [0] * n

    path = [0] * (2*n)
    vcost1 = [0] * (2*n)  # for vertex subtree
    vcost2 = [0] * (2*n)  # for vertex path
    ecost1 = [0] * (2*n)  # for edge subtree
    ecost2 = [0] * (2*n)  # for edge path
    nodein = [0] * n
    nodeout = [0] * n
    depth = [-1] * n

    curtime = -1
    depth[root] = 0
    stack: List[Tuple[int, int]] = [(~root, 0), (root, 0)]
    while stack:
      curtime += 1
      v, ec = stack.pop()
      if v >= 0:
        nodein[v] = curtime
        path[curtime] = v
        ecost1[curtime] = ec
        ecost2[curtime] = ec
        vcost1[curtime] = vertexcost[v]
        vcost2[curtime] = vertexcost[v]
        if len(G[v]) == 1:
          nodeout[v] = curtime + 1
        for x, c in G[v]:
          if depth[x] != -1:
            continue
          depth[x] = depth[v] + 1
          stack.append((~v, c))
          stack.append((x, c))
      else:
        v = ~v
        path[curtime] = v
        ecost1[curtime] = 0
        ecost2[curtime] = -ec
        vcost1[curtime] = 0
        vcost2[curtime] = -vertexcost[v]
        nodeout[v] = curtime

    # ---------------------- #

    self._n = n
    self._depth = depth
    self._nodein = nodein
    self._nodeout = nodeout
    self._vertexcost = vertexcost
    self._path = path

    self._vcost_subtree = FenwickTree(vcost1)
    self._vcost_path    = FenwickTree(vcost2)
    self._ecost_subtree = FenwickTree(ecost1)
    self._ecost_path    = FenwickTree(ecost2)

    bit = len(path).bit_length()
    self.msk = (1 << bit) - 1
    a: List[int] = [(depth[v]<<bit)+i for i, v in enumerate(path)]
    self._st: SegmentTreeRmQ[int] = SegmentTreeRmQ(a, e=max(a))

  def lca(self, u: int, v: int) -> int:
    if u == v: return u
    l = min(self._nodein[u], self._nodein[v])
    r = max(self._nodeout[u], self._nodeout[v])
    ind = self._st.prod(l, r) & self.msk
    return self._path[ind]

  def lca_mul(self, a: List[int]) -> int:
    l, r = self._n+1, -self._n-1
    for e in a:
      l = min(l, self._nodein[e])
      r = max(r, self._nodeout[e])
    ind = self._st.prod(l, r) & self.msk
    return self._path[ind]

  def subtree_vcost(self, v: int) -> int:
    l = self._nodein[v]
    r = self._nodeout[v]
    return self._vcost_subtree.prod(l, r)

  def subtree_ecost(self, v: int) -> int:
    l = self._nodein[v]
    r = self._nodeout[v]
    return self._ecost_subtree.prod(l+1, r)

  def _path_vcost(self, v: int) -> int:
    '''頂点 v を含む'''
    return self._vcost_path.pref(self._nodein[v]+1)

  def _path_ecost(self, v: int) -> int:
    '''根から頂点 v までの辺'''
    return self._ecost_path.pref(self._nodein[v]+1)

  def path_vcost(self, u: int, v: int) -> int:
    a = self.lca(u, v)
    return self._path_vcost(u) + self._path_vcost(v) - 2 * self._path_vcost(a) + self._vertexcost[a]

  def path_ecost(self, u: int, v: int) -> int:
    return self._path_ecost(u) + self._path_ecost(v) - 2 * self._path_ecost(self.lca(u, v))

  def add_vertex(self, v: int, w: int) -> None:
    '''Add w to vertex x. / O(logN)'''
    l = self._nodein[v]
    r = self._nodeout[v]
    self._vcost_subtree.add(l, w)
    self._vcost_path.add(l, w)
    self._vcost_path.add(r, -w)
    self._vertexcost[v] += w

  def set_vertex(self, v: int, w: int) -> None:
    '''Set w to vertex v. / O(logN)'''
    self.add_vertex(v, w - self._vertexcost[v])

  def add_edge(self, u: int, v: int, w: int) -> None:
    '''Add w to edge([u - v]). / O(logN)'''
    if self._depth[u] < self._depth[v]:
      u, v = v, u
    l = self._nodein[u]
    r = self._nodeout[u]
    self._ecost_subtree.add(l, w)
    self._ecost_subtree.add(r+1, -w)
    self._ecost_path.add(l, w)
    self._ecost_path.add(r+1, -w)

  def set_edge(self, u: int, v: int, w: int) -> None:
    '''Set w to edge([u - v]). / O(logN)'''
    self.add_edge(u, v, w - self.path_ecost(u, v))

