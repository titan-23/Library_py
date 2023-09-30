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

  def __init__(self, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T):
    '''Build a new SegmentTree. / O(N)'''
    self._op = op
    self._e = e
    if isinstance(n_or_a, int):
      self._n = n_or_a
      self._log  = (self._n - 1).bit_length()
      self._size = 1 << self._log
      self._data = [e] * (self._size << 1)
    else:
      n_or_a = list(n_or_a)
      self._n = len(n_or_a)
      self._log  = (self._n - 1).bit_length()
      self._size = 1 << self._log
      _data = [e] * (self._size << 1)
      _data[self._size:self._size+self._n] = n_or_a
      for i in range(self._size-1, 0, -1):
        _data[i] = op(_data[i<<1], _data[i<<1|1])
      self._data = _data

  def set(self, k: int, v: T) -> None:
    '''Update a[k] <- x. / O(logN)'''
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.set({k}, {v}), n={self._n}'
    if k < 0:
      k += self._n
    k += self._size
    self._data[k] = v
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._op(self._data[k<<1], self._data[k<<1|1])

  def get(self, k: int) -> T:
    '''Return a[k]. / O(1)'''
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.get({k}), n={self._n}'
    if k < 0:
      k += self._n
    return self._data[k+self._size]

  def prod(self, l: int, r: int) -> T:
    '''Return op([l, r)). / O(logN)'''
    assert 0 <= l <= r <= self._n, \
        f'IndexError: SegmentTree.prod({l}, {r})'
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
    '''Return op([0, n)). / O(1)'''
    return self._data[1]

  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    '''Find the largest index R s.t. f([l, R)) == True. / O(logN)'''
    assert 0 <= l <= self._n, \
        f'IndexError: SegmentTree.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'SegmentTree.max_right({l}, f), f({self._e}) must be true.'
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
    '''Find the smallest index L s.t. f([L, r)) == True. / O(logN)'''
    assert 0 <= r <= self._n, \
        f'IndexError: SegmentTree.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'SegmentTree.min_left({r}, f), f({self._e}) must be true.'
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
    '''Return List[self]. / O(N)'''
    return [self.get(i) for i in range(self._n)]

  def show(self) -> None:
    '''Debug. / O(N)'''
    print('<SegmentTree> [\n' + '\n'.join(['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]) + '\n]')

  def __getitem__(self, k: int) -> T:
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.__getitem__({k}), n={self._n}'
    return self.get(k)

  def __setitem__(self, k: int, v: T):
    assert -self._n <= k < self._n, \
        f'IndexError: SegmentTree.__setitem__{k}, {v}), n={self._n}'
    self.set(k, v)

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'SegmentTree({self})'

# def op(s, t):
#   return

# e = None

from typing import Any, Iterator, List, Tuple

class HLD():

  def __init__(self, G: List[List[int]], root: int):
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
    return [a[e] for e in self.hld]

  def for_each_vertex(self, u: int, v: int) -> Iterator[Tuple[int, int]]:
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
    yield self.nodein[v], self.nodeout[v]

  def path_kth_elm(self, s: int, t: int, k: int) -> int:
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
    nodein, head, par = self.nodein, self.head, self.par
    while True:
      if nodein[u] > nodein[v]:
        u, v = v, u
      if head[u] == head[v]:
        return u
      v = par[head[v]]

from typing import Union, Iterable, Callable, TypeVar, Generic
T = TypeVar('T')

class HLDSegmentTree(Generic[T]):

  def __init__(self, hld: HLD, n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T):
    self.hld: HLD = hld
    n_or_a = n_or_a if isinstance(n_or_a, int) else self.hld.build_list(list(n_or_a))
    self.seg: SegmentTree[T] = SegmentTree(n_or_a, op, e)
    self.op: Callable[[T, T], T] = op
    self.e: T = e

  def path_prod(self, u: int, v: int) -> T:
    head, nodein, dep, par = self.hld.head, self.hld.nodein, self.hld.dep, self.hld.par
    res = self.e
    while head[u] != head[v]:
      if dep[head[u]] < dep[head[v]]:
        u, v = v, u
      res = self.op(res, self.seg.prod(nodein[head[u]], nodein[u]+1))
      u = par[head[u]]
    if dep[u] < dep[v]:
      u, v = v, u
    return self.op(res, self.seg.prod(nodein[v], nodein[u]+1))

  def get(self, k: int) -> T:
    return self.seg[self.hld.nodein[k]]

  def set(self, k: int, v: T) -> None:
    self.seg[self.hld.nodein[k]] = v

  __getitem__ = get
  __setitem__ = set

  def subtree_prod(self, v: int) -> T:
    return self.seg.prod(self.hld.nodein[v], self.hld.nodeout[v])


