# from Library_py.DataStructures.SplayTree.SplayTreeSet import SplayTreeSet
# from Library_py.MyClass.OrderedSetInterface import OrderedSetInterface
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic, List
T = TypeVar('T', bound=SupportsLessThan)

class OrderedSetInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, a: Iterable[T]) -> None:
    raise NotImplementedError

  @abstractmethod
  def add(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def discard(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def remove(self, key: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def le(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def lt(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def ge(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def gt(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def get_max(self) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def get_min(self) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def pop_max(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def pop_min(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def clear(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def tolist(self) -> List[T]:
    raise NotImplementedError

  @abstractmethod
  def __iter__(self) -> Iterator:
    raise NotImplementedError

  @abstractmethod
  def __next__(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def __contains__(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def __len__(self) -> int:
    raise NotImplementedError

  @abstractmethod
  def __bool__(self) -> bool:
    raise NotImplementedError

  @abstractmethod
  def __str__(self) -> str:
    raise NotImplementedError

  @abstractmethod
  def __repr__(self) -> str:
    raise NotImplementedError

from array import array
from __pypy__ import newlist_hint
from typing import Generic, Iterable, List, TypeVar, Optional
T = TypeVar('T', bound=SupportsLessThan)

class SplayTreeSet(OrderedSetInterface, Generic[T]):

  def __init__(self, a: Iterable[T]=[], e: T=0):
    self.keys: List[T] = [e]
    self.size = array('I', bytes(4))
    self.child = array('I', bytes(8))
    self.end = 1
    self.node = 0
    self.e = e
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> int:
      mid = (l + r) >> 1
      if l != mid:
        child[mid<<1] = sort(l, mid)
      if mid + 1 != r:
        child[mid<<1|1] = sort(mid+1, r)
      size[mid] = 1 + size[child[mid<<1]] + size[child[mid<<1|1]]
      return mid
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    n = len(a)
    key, child, size = self.keys, self.child, self.size
    self.reserve(n-len(key)+2)
    self.end += n
    key[1:n+1] = a
    self.node = sort(1, n+1)

  def _make_node(self, key: T) -> int:
    end = self.end
    if end >= len(self.keys):
      self.keys.append(key)
      self.size.append(1)
      self.child.append(0)
      self.child.append(0)
    else:
      self.keys[end] = key
    self.end += 1
    return end

  def _update(self, node: int) -> None:
    self.size[node] = 1 + self.size[self.child[node<<1]] + self.size[self.child[node<<1|1]]

  def _update_triple(self, x: int, y: int, z: int) -> None:
    size, child = self.size, self.child
    size[z] = size[x]
    size[x] = 1 + size[child[x<<1]] + size[child[x<<1|1]]
    size[y] = 1 + size[child[y<<1]] + size[child[y<<1|1]]

  def _splay(self, path: List[int], d: int) -> int:
    child = self.child
    g = d & 1
    while len(path) > 1:
      node = path.pop()
      pnode = path.pop()
      f = d >> 1 & 1
      tmp = child[node<<1|g^1]
      child[node<<1|g^1] = child[tmp<<1|g]
      child[tmp<<1|f^(g != f)] = node
      child[pnode<<1|f^1] = child[(node if g == f else tmp)<<1|f]
      child[(node if g == f else tmp)<<1|f] = pnode
      self._update_triple(pnode, node, tmp)
      if not path:
        return tmp
      d >>= 2
      g = d & 1
      child[path[-1]<<1|g^1] = tmp
    pnode = path[0]
    node = child[pnode<<1|g^1]
    child[pnode<<1|g^1] = child[node<<1|g]
    child[node<<1|g] = pnode
    self._update(pnode)
    self._update(node)
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    keys, child = self.keys, self.child
    if (not node) or keys[node] == key: return
    path = []
    d = 0
    while keys[node] != key:
      nxt = child[node<<1|(key>keys[node])]
      if not nxt: break
      path.append(node)
      d, node = d << 1 | (key < keys[node]), nxt
    if path:
      self.node = self._splay(path, d)

  def _set_kth_elm_splay(self, k: int) -> None:
    size, child = self.size, self.child
    node = self.node
    if k < 0: k += size[node]
    d = 0
    path = []
    while True:
      t = size[child[node<<1]]
      if t == k:
        if path:
          self.node = self._splay(path, d)
        return
      path.append(node)
      d, node = d << 1 | (t > k), child[node<<1|(t<k)]
      if t < k:
        k -= t + 1

  def _get_min_splay(self, node: int) -> int:
    if not node: return 0
    child = self.child
    if not child[node<<1]: return node
    path = []
    while child[node<<1]:
      path.append(node)
      node = child[node<<1]
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: int) -> int:
    if not node: return 0
    child = self.child
    if not child[node<<1|1]: return node
    path = []
    while child[node<<1|1]:
      path.append(node)
      node = child[node<<1|1]
    return self._splay(path, 0)

  def reserve(self, n: int) -> None:
    assert n >= 0, f'ValueError: SplayTreeSet.reserve({n})'
    self.keys += [self.e] * n
    self.size += array('I', [1] * n)
    self.child += array('I', bytes(8 * n))

  def add(self, key: T) -> bool:
    keys, child = self.keys, self.child
    self._set_search_splay(key)
    if keys[self.node] == key:
      return False
    node = self._make_node(key)
    if not self.node:
      self.node = node
      return True
    f = key > keys[self.node]
    child[node<<1|f^1] = self.node
    child[node<<1|f] = child[self.node<<1|f]
    child[self.node<<1|f] = 0
    self._update(child[node<<1|f^1])
    self._update(node)
    self.node = node
    return True

  def discard(self, key: T) -> bool:
    if not self.node: return False
    self._set_search_splay(key)
    if self.keys[self.node] != key: return False
    child = self.child
    if not child[self.node<<1]:
      self.node = child[self.node<<1|1]
    elif not child[self.node<<1|1]:
      self.node = child[self.node<<1]
    else:
      node = self._get_min_splay(child[self.node<<1|1])
      child[node<<1] = child[self.node<<1]
      self._update(child[node<<1])
      self.node = node
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError(key)

  def le(self, key: T) -> Optional[T]:
    node = self.node
    keys, child = self.keys, self.child
    path = []
    d = 0
    res = None
    while node:
      if keys[node] == key:
        res = key
        break
      path.append(node)
      d = d << 1 | (key < keys[node])
      if key > keys[node]:
        res = keys[node]
      node = child[node<<1|(key>keys[node])]
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def lt(self, key: T) -> Optional[T]:
    node = self.node
    keys, child = self.keys, self.child
    path = []
    d = 0
    res = None
    while node:
      path.append(node)
      d = d << 1 | (key <= keys[node])
      if key > keys[node]:
        res = keys[node]
      node = child[node<<1|(key>keys[node])]
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def ge(self, key: T) -> Optional[T]:
    node = self.node
    keys, child = self.keys, self.child
    path = []
    d = 0
    res = None
    while node:
      if keys[node] == key:
        res = keys[node]
        break
      path.append(node)
      d = d << 1 | (key < keys[node])
      if key < keys[node]:
        res = keys[node]
      node = child[node<<1|(key>=keys[node])]
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def gt(self, key: T) -> Optional[T]:
    node = self.node
    keys, child = self.keys, self.child
    path = []
    d = 0
    res = None
    while node:
      path.append(node)
      d = d << 1 | (key<keys[node])
      if key < keys[node]:
        res = keys[node]
      node = child[node<<1|(key>=keys[node])]
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def index(self, key: T) -> int:
    if not self.node: return 0
    self._set_search_splay(key)
    res = self.size[self.child[self.node<<1]]
    if self.keys[self.node] < key:
      res += 1
    return res

  def index_right(self, key: T) -> int:
    if not self.node: return 0
    self._set_search_splay(key)
    res = self.size[self.child[self.node<<1]]
    if self.keys[self.node] <= key:
      res += 1
    return res

  def get_min(self) -> T:
    return self.__getitem__(0)

  def get_max(self) -> T:
    return self.__getitem__(-1)

  def pop(self, k: int=-1) -> T:
    assert self.node, f'IndexError: SplayTreeSet.pop({k})'
    keys, child = self.keys, self.child
    if k == -1:
      node = self._get_max_splay(self.node)
      self.node = child[node<<1]
      return keys[node]
    self._set_kth_elm_splay(k)
    res = keys[self.node]
    if not [self.node<<1]:
      self.node = child[self.node<<1|1]
    elif not child[self.node<<1|1]:
      self.node = child[self.node<<1]
    else:
      node = self._get_min_splay(child[self.node<<1|1])
      child[node<<1] = child[self.node<<1]
      self._update(node)
      self.node = node
    return res

  def pop_max(self) -> T:
    return self.pop()

  def pop_min(self) -> T:
    assert self.node, f'IndexError: SplayTreeSet.popleft()'
    node = self._get_min_splay(self.node)
    self.node = self.child[node<<1|1]
    return self.keys[node]

  def clear(self) -> None:
    self.node = 0

  def tolist(self) -> List[T]:
    node = self.node
    child, keys = self.child, self.keys
    stack, res = newlist_hint(len(self)), newlist_hint(len(self))
    while stack or node:
      if node:
        stack.append(node)
        node = child[node<<1]
      else:
        node = stack.pop()
        res.append(keys[node])
        node = child[node<<1|1]
    return res

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    self.__iter += 1
    return self.__getitem__(self.__iter - 1)

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.keys[self.node] == key

  def __getitem__(self, k: int) -> T:
    self._set_kth_elm_splay(k)
    return self.keys[self.node]

  def __len__(self):
    return self.size[self.node]

  def __bool__(self):
    return self.node != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'SplayTreeSet({self})'


