import sys
from __pypy__ import newlist_hint
from typing import Iterator, Optional, Generic, Iterable, List, TypeVar, Tuple
T = TypeVar('T')

class SplayTreeMultisetSum(Generic[T]):

  class Node():

    def __init__(self, key, cnt: int) -> None:
      self.data = key * cnt
      self.key = key
      self.size = 1
      self.cnt = cnt
      self.cntsize = cnt
      self.left = None
      self.right = None

    def __str__(self) -> str:
      if self.left is None and self.right is None:
        return f'key:{self.key, self.size, self.cnt, self.cntsize}\n'
      return f'key:{self.key, self.size, self.cnt, self.cntsize},\n left:{self.left},\n right:{self.right}\n'

    __repr__ = __str__

  def __init__(self, e: T, a: Iterable[T]=[], _node=None) -> None:
    self.node = _node
    self.e = e
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    Node = SplayTreeMultisetSum.Node
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(key[mid], cnt[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      self._update(node)
      return node
    key, cnt = self._rle(sorted(a))
    self.node = sort(0, len(key))

  def _rle(self, a: List[T]) -> Tuple[List[T], List[int]]:
    x = newlist_hint(len(a))
    y = newlist_hint(len(a))
    x.append(a[0])
    y.append(1)
    for i, e in enumerate(a):
      if i == 0:
        continue
      if e == x[-1]:
        y[-1] += 1
        continue
      x.append(e)
      y.append(1)
    return x, y

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
        node.cntsize = node.cnt
        node.data = node.key*node.cnt
      else:
        node.size = 1 + node.right.size
        node.cntsize = node.cnt + node.right.cntsize
        node.data = node.key*node.cnt + node.right.data
    else:
      if node.right is None:
        node.size = 1 + node.left.size
        node.cntsize = node.cnt + node.left.cntsize
        node.data = node.key*node.cnt + node.left.data
      else:
        node.size = 1 + node.left.size + node.right.size
        node.cntsize = node.cnt + node.left.cntsize + node.right.cntsize
        node.data = node.key*node.cnt + node.left.data + node.right.data

  def _splay(self, path: List[Node], d: int) -> Node:
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      if d&1 == d>>1&1:
        if d & 1:
          tmp = node.left
          node.left = tmp.right
          tmp.right = node
          pnode.left = node.right
          node.right = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
      else:
        if d & 1:
          tmp = node.left
          node.left = tmp.right
          pnode.right = tmp.left
          tmp.right = node
          tmp.left = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          pnode.left = tmp.right
          tmp.left = node
          tmp.right = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      d >>= 2
      if d & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if d & 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
    self._update(gnode)
    self._update(node)
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key:
      return
    path = []
    d = 0
    while True:
      if node.key == key:
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        if node.right is None:
          break
        path.append(node)
        d <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, d)

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    d = 0
    node = self.node
    path = []
    while True:
      t = node.cnt if node.left is None else node.cnt + node.left.cntsize
      if t-node.cnt <= k < t:
        if path:
          self.node = self._splay(path, d)
        break
      elif t > k:
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        path.append(node)
        d <<= 1
        node = node.right
        k -= t

  def _set_kth_elm_tree_splay(self, k: int) -> None:
    if k < 0: k += self.len_elm()
    assert 0 <= k < self.len_elm()
    d = 0
    node = self.node
    path = []
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        if path:
          self.node = self._splay(path, d)
        return
      elif t > k:
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        path.append(node)
        d <<= 1
        node = node.right
        k -= t + 1

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  def add(self, key: T, cnt: int=1) -> None:
    if self.node is None:
      self.node = SplayTreeMultisetSum.Node(key, cnt)
      return
    self._set_search_splay(key)
    if self.node.key == key:
      self.node.cnt += cnt
      self._update(self.node)
      return
    node = SplayTreeMultisetSum.Node(key, cnt)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
      self._update(node.right)
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
      self._update(node.left)
    self._update(node)
    self.node = node
    return

  def discard(self, key: T, cnt: int=1) -> bool:
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.cnt > cnt:
      self.node.cnt -= cnt
      self._update(self.node)
      return True
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self._update(node)
      self.node = node
    return True

  def discard_all(self, key: T) -> bool:
    return self.discard(key, self.count(key))

  def count(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    return self.node.cnt if self.node.key == key else 0

  def le(self, key: T) -> Optional[T]:
    node = self.node
    if node is None: return None
    path = []
    d = 0
    res = None
    while True:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        res = node.key
        if node.right is None:
          break
        path.append(node)
        d <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, d)
    return res

  def lt(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    d = 0
    res = None
    while node is not None:
      if key <= node.key:
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        path.append(node)
        d <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def ge(self, key: T) -> Optional[T]:
    node = self.node
    if node is None: return None
    path = []
    d = 0
    res = None
    while True:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        res = node.key
        if node.left is None:
          break
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        if node.right is None:
          break
        path.append(node)
        d <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, d)
    return res

  def gt(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    d = 0
    res = None
    while node is not None:
      if key < node.key:
        path.append(node)
        d <<= 1
        d |= 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        d <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def index(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.cntsize
    if self.node.key < key:
      res += self.node.cnt
    return res

  def index_right(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.cntsize
    if self.node.key <= key:
      res += self.node.cnt
    return res

  def index_keys(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.size
    if self.node.key < key:
      res += 1
    return res

  def index_right_keys(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.size
    if self.node.key <= key:
      res += 1
    return res

  def pop(self, k: int=-1) -> T:
    self._set_kth_elm_splay(k)
    res = self.node.key
    self.discard(res)
    return res

  def pop_max(self) -> T:
    return self.pop()

  def pop_min(self) -> T:
    return self.pop(0)

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self.len_elm():
      sys.setrecursionlimit(self.len_elm()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      for _ in range(node.cnt):
        a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def tolist_items(self) -> List[Tuple[T, int]]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self.len_elm():
      sys.setrecursionlimit(self.len_elm()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.cnt))
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def get_elm(self, k: int) -> T:
    assert -self.len_elm() <= k < self.len_elm()
    self._set_kth_elm_tree_splay(k)
    return self.node.key

  def items(self) -> Iterator[Tuple[T, int]]:
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.key, self.node.cnt

  def keys(self) -> Iterator[T]:
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.key

  def cntues(self) -> Iterator[int]:
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.cnt

  def len_elm(self) -> int:
    return 0 if self.node is None else self.node.size

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.tolist_items())) + '}')

  def clear(self) -> None:
    self.node = None

  def get_sum(self) -> T:
    if self.node is None:
      return self.e
    return self.node.data

  def merge(self, other: 'SplayTreeMultisetSum') -> None:
    if self.node is None:
      self.node = other.node
      return
    if other.node is None:
      return
    self.node = self._get_max_splay(self.node)
    other.node = other._get_min_splay(other.node)
    assert self.node.key <= other.node.key
    if self.node.key == other.node.key:
      self.node.cnt += other.node.cnt
      self._update(self.node)
      other.discard(other.node.key, other.node.cnt)
    self.node.right = other.node
    self._update(self.node)

  def split(self, k: int) -> Tuple['SplayTreeMultisetSum', 'SplayTreeMultisetSum']:
    if self.node is None:
      return SplayTreeMultisetSum(self.e), self
    if k >= len(self):
      return self, SplayTreeMultisetSum(self.e)
    self._set_kth_elm_splay(k)
    if self.node.left is None:
      left = SplayTreeMultisetSum(self.e)
    else:
      left = SplayTreeMultisetSum(self.e, _node=self.node.left)
    if len(left) != k:
      assert k-len(left) > 0
      self.node.cnt -= k-len(left)
      self._update(self.node)
      root = SplayTreeMultisetSum.Node(self.node.key, k-len(left))
      root.left = left.node
      left = SplayTreeMultisetSum(self.e, _node=root)
      left._update(left.node)
    if self.node:
      self.node.left = None
      self._update(self.node)
    return left, self

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __contains__(self, key: T) -> bool:
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __getitem__(self, k: int) -> T:
    self._set_kth_elm_splay(k)
    return self.node.key

  def __len__(self):
    return 0 if self.node is None else self.node.cntsize

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'SplayTreeMultisetSum(' + str(self) + ')'

  __repr__ = __str__


