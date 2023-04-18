from array import array
from typing import Generic, List, TypeVar, Tuple, Callable, Iterable, Optional, Union, Sequence

from sympy import sequence
from __pypy__ import newlist_hint
T = TypeVar('T')
F = TypeVar('F')

class MonoidData(Generic[T, F]):

  def __init__(self, op: Optional[Callable[[T, T], T]]=None, \
              mapping: Optional[Callable[[F, T], T]]=None, \
              composition: Optional[Callable[[F, F], F]]=None, \
              e: T=None, id: F=None):
    self.op = (lambda s, t: e) if op is None else op
    self.mapping = (lambda f, s: e) if op is None else mapping
    self.composition = (lambda f, g: id) if op is None else composition
    self.e = e
    self.id = id
    self.keydata: List[T] = [e, e]
    self.lazy: List[F] = [id]
    self.arr: array[int] = array('I', bytes(16))
    '''
    left:  arr[node<<2]
    right: arr[node<<2|1]
    size:  arr[node<<2|2]
    rev:   arr[node<<2|3]
    '''
    self.end: int = 1

  def reserve(self, n: int) -> None:
    if n <= 0: return
    self.keydata += [self.e] * (2 * n)
    self.lazy += [self.id] * n
    self.arr += array('I', bytes(16 * n))

class LazySplayTree(Generic[T, F]):

  def __init__(self, monoiddata: 'MonoidData', n_or_a: Union[int, Iterable[T]]=0, _root: int=0):
    self.monoiddata = monoiddata
    self.root = _root
    if not n_or_a:
      return
    if isinstance(n_or_a, int):
      a = [monoiddata.e for _ in range(n_or_a)]
    elif not isinstance(n_or_a, Sequence):
      a = list(n_or_a)
    else:
      a = n_or_a
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int) -> int:
      mid = (l + r) >> 1
      if l != mid:
        arr[mid<<2] = sort(l, mid)
      if mid + 1 != r:
        arr[mid<<2|1] = sort(mid+1, r)
      self._update(mid)
      return mid
    n = len(a)
    keydata, arr = self.monoiddata.keydata, self.monoiddata.arr
    end = self.monoiddata.end
    self.monoiddata.reserve(n+end-len(keydata)//2+1)
    self.monoiddata.end += n
    for i, e in enumerate(a):
      keydata[end+i<<1] = e
      keydata[end+i<<1|1] = e
    self.root = sort(end, n+end)

  def _make_node(self, key: T) -> int:
    monoiddata = self.monoiddata
    if monoiddata.end >= len(monoiddata.arr)//4:
      monoiddata.keydata.append(key)
      monoiddata.keydata.append(key)
      monoiddata.lazy.append(monoiddata.id)
      monoiddata.arr.append(0)
      monoiddata.arr.append(0)
      monoiddata.arr.append(1)
      monoiddata.arr.append(0)
    else:
      monoiddata.keydata[monoiddata.end<<1] = key
      monoiddata.keydata[monoiddata.end<<1|1] = key
    monoiddata.end += 1
    return monoiddata.end - 1

  def _propagate(self, node: int) -> None:
    monoiddata = self.monoiddata
    arr = monoiddata.arr
    if arr[node<<2|3]:
      arr[node<<2], arr[node<<2|1] = arr[node<<2|1], arr[node<<2]
      arr[node<<2|3] = 0
      arr[arr[node<<2]<<2|3] ^= 1
      arr[arr[node<<2|1]<<2|3] ^= 1
    nlazy = monoiddata.lazy[node]
    if nlazy == monoiddata.id:
      return
    lnode, rnode = arr[node<<2], arr[node<<2|1]
    keydata, lazy = monoiddata.keydata, monoiddata.lazy
    lazy[node] = monoiddata.id
    if lnode:
      lazy[lnode] = monoiddata.composition(nlazy, lazy[lnode])
      lnode <<= 1
      keydata[lnode] = monoiddata.mapping(nlazy, keydata[lnode])
      keydata[lnode|1] = monoiddata.mapping(nlazy, keydata[lnode|1])
    if rnode:
      lazy[rnode] = monoiddata.composition(nlazy, lazy[rnode])
      rnode <<= 1
      keydata[rnode] = monoiddata.mapping(nlazy, keydata[rnode])
      keydata[rnode|1] = monoiddata.mapping(nlazy, keydata[rnode|1])

  def _update_triple(self, x: int, y: int, z: int) -> None:
    monoiddata = self.monoiddata
    keydata, arr = monoiddata.keydata, monoiddata.arr
    lx, rx = arr[x<<2], arr[x<<2|1]
    ly, ry = arr[y<<2], arr[y<<2|1]
    arr[z<<2|2] = arr[x<<2|2]
    arr[x<<2|2] = 1 + arr[lx<<2|2] + arr[rx<<2|2]
    arr[y<<2|2] = 1 + arr[ly<<2|2] + arr[ry<<2|2]
    keydata[z<<1|1] = keydata[x<<1|1]
    keydata[x<<1|1] = monoiddata.op(monoiddata.op(keydata[lx<<1|1], keydata[x<<1]), keydata[rx<<1|1])
    keydata[y<<1|1] = monoiddata.op(monoiddata.op(keydata[ly<<1|1], keydata[y<<1]), keydata[ry<<1|1])

  def _update_double(self, x: int, y: int) -> None:
    monoiddata = self.monoiddata
    keydata, arr = monoiddata.keydata, monoiddata.arr
    lx, rx = arr[x<<2], arr[x<<2|1]
    arr[y<<2|2] = arr[x<<2|2]
    arr[x<<2|2] = 1 + arr[lx<<2|2] + arr[rx<<2|2]
    keydata[y<<1|1] = keydata[x<<1|1]
    keydata[x<<1|1] = monoiddata.op(monoiddata.op(keydata[lx<<1|1], keydata[x<<1]), keydata[rx<<1|1])

  def _update(self, node: int) -> None:
    monoiddata = self.monoiddata
    keydata, arr = monoiddata.keydata, monoiddata.arr
    lnode, rnode = arr[node<<2], arr[node<<2|1]
    arr[node<<2|2] = 1 + arr[lnode<<2|2] + arr[rnode<<2|2]
    keydata[node<<1|1] = monoiddata.op(monoiddata.op(keydata[lnode<<1|1], keydata[node<<1]), keydata[rnode<<1|1])

  def _splay(self, path: List[int], d: int) -> None:
    arr = self.monoiddata.arr
    g = d & 1
    while len(path) > 1:
      pnode = path.pop()
      gnode = path.pop()
      f = d >> 1 & 1
      node = arr[pnode<<2|g^1]
      nnode = (pnode if g == f else node) << 2 | f
      arr[pnode<<2|g^1] = arr[node<<2|g]
      arr[node<<2|g] = pnode
      arr[gnode<<2|f^1] = arr[nnode]
      arr[nnode] = gnode
      self._update_triple(gnode, pnode, node)
      if not path:
        return
      d >>= 2
      g = d & 1
      arr[path[-1]<<2|g^1] = node
    pnode = path.pop()
    node = arr[pnode<<2|g^1]
    arr[pnode<<2|g^1] = arr[node<<2|g]
    arr[node<<2|g] = pnode
    self._update_double(pnode, node)

  def _kth_elm_splay(self, node: int, k: int) -> int:
    arr = self.monoiddata.arr
    if k < 0: k += arr[node<<2|2]
    d = 0
    path = []
    while True:
      self._propagate(node)
      t = arr[arr[node<<2]<<2|2]
      if t == k:
        if path:
          self._splay(path, d)
        return node
      d = d << 1 | (t > k)
      path.append(node)
      node = arr[node<<2|(t<k)]
      if t < k:
        k -= t + 1

  def _left_splay(self, node: int) -> int:
    if not node: return 0
    self._propagate(node)
    arr = self.monoiddata.arr
    if not arr[node<<2]: return node
    path = []
    while arr[node<<2]:
      path.append(node)
      node = arr[node<<2]
      self._propagate(node)
    self._splay(path, (1<<len(path))-1)
    return node

  def _right_splay(self, node: int) -> int:
    if not node: return 0
    self._propagate(node)
    arr = self.monoiddata.arr
    if not arr[node<<2|1]: return node
    path = []
    while arr[node<<2|1]:
      path.append(node)
      node = arr[node<<2|1]
      self._propagate(node)
    self._splay(path, 0)
    return node

  def reserve(self, n: int) -> None:
    self.monoiddata.reserve(n)

  def merge(self, other: 'LazySplayTree') -> None:
    assert self.monoiddata is other.monoiddata
    if not other.root: return
    if not self.root:
      self.root = other.root
      return
    self.root = self._right_splay(self.root)
    self.monoiddata.arr[self.root<<2|1] = other.root
    self._update(self.root)

  def split(self, k: int) -> Tuple['LazySplayTree', 'LazySplayTree']:
    assert -len(self) < k <= len(self), \
        f'IndexError: LazySplayTree.split({k}), len={len(self)}'
    if k < 0: k += len(self)
    if k >= self.monoiddata.arr[self.root<<2|2]:
      return self, LazySplayTree(self.monoiddata, _root=0)
    self.root = self._kth_elm_splay(self.root, k)
    left = LazySplayTree(self.monoiddata, _root=self.monoiddata.arr[self.root<<2])
    self.monoiddata.arr[self.root<<2] = 0
    self._update(self.root)
    return left, self

  def _internal_split(self, k: int) -> Tuple[int, int]:
    if k >= self.monoiddata.arr[self.root<<2|2]:
      return self.root, 0
    self.root = self._kth_elm_splay(self.root, k)
    left = self.monoiddata.arr[self.root<<2]
    self.monoiddata.arr[self.root<<2] = 0
    self._update(self.root)
    return left, self.root

  def reverse(self, l: int, r: int) -> None:
    assert 0 <= l <= r <= len(self), \
        f'IndexError: LazySplayTree.reverse({l}, {r}), len={len(self)}'
    if l == r: return
    monoiddata = self.monoiddata
    left, right = self._internal_split(r)
    if l:
      left = self._kth_elm_splay(left, l-1)
    monoiddata.arr[(monoiddata.arr[left<<2|1] if l else left)<<2|3] ^= 1
    if right:
      monoiddata.arr[right<<2] = left
      self._update(right)
    self.root = right if right else left

  def all_reverse(self) -> None:
    self.monoiddata.arr[self.root<<2|3] ^= 1

  def apply(self, l: int, r: int, f: F) -> None:
    assert 0 <= l <= r <= len(self), \
        f'IndexError: LazySplayTree.apply({l}, {r}), len={len(self)}'
    monoiddata = self.monoiddata
    left, right = self._internal_split(r)
    keydata, lazy = monoiddata.keydata, monoiddata.lazy
    if l:
      left = self._kth_elm_splay(left, l-1)
    node = monoiddata.arr[left<<2|1] if l else left
    keydata[node<<1] = monoiddata.mapping(f, keydata[node<<1])
    keydata[node<<1|1] = monoiddata.mapping(f, keydata[node<<1|1])
    lazy[node] = monoiddata.composition(f, lazy[node])
    if l:
      self._update(left)
    if right:
      monoiddata.arr[right<<2] = left
      self._update(right)
    self.root = right if right else left

  def all_apply(self, f: F) -> None:
    if not self.root: return
    monoiddata, node = self.monoiddata, self.root
    monoiddata.keydata[node<<1] = monoiddata.mapping(f, monoiddata.keydata[node<<1])
    monoiddata.keydata[node<<1|1] = monoiddata.mapping(f, monoiddata.keydata[node<<1|1])
    monoiddata.lazy[node] = monoiddata.composition(f, monoiddata.lazy[node])

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= len(self), \
        f'IndexError: LazySplayTree.prod({l}, {r}), len={len(self)}'
    monoiddata = self.monoiddata
    left, right = self._internal_split(r)
    if l:
      left = self._kth_elm_splay(left, l-1)
    res = monoiddata.keydata[(monoiddata.arr[left<<2|1] if l else left)<<1|1]
    if right:
      monoiddata.arr[right<<2] = left
      self._update(right)
    self.root = right if right else left
    return res

  def all_prod(self) -> T:
    return self.monoiddata.keydata[self.root<<1|1]

  def insert(self, k: int, key: T) -> None:
    assert -len(self) <= k <= len(self), \
        f'IndexError: LazySplayTree.insert({k}, {key}), len={len(self)}'
    if k < 0: k += len(self)
    monoiddata = self.monoiddata
    node = self._make_node(key)
    if not self.root:
      self.root = node
      return
    arr = monoiddata.arr
    if k == monoiddata.arr[self.root<<2|2]:
      arr[node<<2] = self._right_splay(self.root)
    else:
      node_ = self._kth_elm_splay(self.root, k)
      if arr[node_<<2]:
        arr[node<<2] = arr[node_<<2]
        arr[node_<<2] = 0
        self._update(node_)
      arr[node<<2|1] = node_
    self._update(node)
    self.root = node

  def append(self, key: T) -> None:
    monoiddata = self.monoiddata
    node = self._right_splay(self.root)
    self.root = self._make_node(key)
    monoiddata.arr[self.root<<2] = node
    self._update(self.root)

  def appendleft(self, key: T) -> None:
    node = self._left_splay(self.root)
    self.root = self._make_node(key)
    self.monoiddata.arr[self.root<<2|1] = node
    self._update(self.root)

  def pop(self, k: int=-1) -> T:
    assert -len(self) <= k < len(self), \
        f'IndexError: LazySplayTree.pop({k})'
    monoiddata = self.monoiddata
    if k == -1:
      node = self._right_splay(self.root)
      self._propagate(node)
      self.root = monoiddata.arr[node<<2]
      return monoiddata.keydata[node<<1]
    self.root = self._kth_elm_splay(self.root, k)
    res = monoiddata.keydata[self.root<<1]
    if not monoiddata.arr[self.root<<2]:
      self.root = monoiddata.arr[self.root<<2|1]
    elif not monoiddata.arr[self.root<<2|1]:
      self.root = monoiddata.arr[self.root<<2]
    else:
      node = self._right_splay(monoiddata.arr[self.root<<2])
      monoiddata.arr[node<<2|1] = monoiddata.arr[self.root<<2|1]
      self.root = node
      self._update(self.root)
    return res

  def popleft(self) -> T:
    assert self, f'IndexError: LazySplayTree.popleft()'
    node = self._left_splay(self.root)
    self.root = self.monoiddata.arr[node<<2|1]
    return self.monoiddata.keydata[node<<1]

  def rotate(self, x: int) -> None:
    # 「末尾をを削除し先頭に挿入」をx回
    n = self.monoiddata.arr[self.root<<2|2]
    l, self = self.split(n-(x%n))
    self.merge(l)

  def tolist(self) -> List[T]:
    node = self.root
    arr, keydata = self.monoiddata.arr, self.monoiddata.keydata
    stack = newlist_hint(len(self))
    res = newlist_hint(len(self))
    while stack or node:
      if node:
        self._propagate(node)
        stack.append(node)
        node = arr[node<<2]
      else:
        node = stack.pop()
        res.append(keydata[node<<1])
        node = arr[node<<2|1]
    return res

  def clear(self) -> None:
    self.root = 0

  def __setitem__(self, k: int, key: T):
    assert -len(self) <= k < len(self), f'IndexError: LazyAVLTree.__setitem__({k})'
    self.root = self._kth_elm_splay(self.root, k)
    self.monoiddata.keydata[self.root<<1] = key
    self._update(self.root)

  def __getitem__(self, k: int) -> T:
    assert -len(self) <= k < len(self), f'IndexError: LazyAVLTree.__getitem__({k})'
    self.root = self._kth_elm_splay(self.root, k)
    return self.monoiddata.keydata[self.root<<1]

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.monoiddata.arr[self.root<<2|2]:
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(len(self)):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return self.monoiddata.arr[self.root<<2|2]

  def __str__(self):
    return str(self.tolist())

  def __bool__(self):
    return self.root != 0

  def __repr__(self):
    return f'LazySplayTree({self.tolist()})'

def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

e = None
id = None

