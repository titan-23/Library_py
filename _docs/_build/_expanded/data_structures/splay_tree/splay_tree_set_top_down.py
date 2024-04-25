# from titan_pylib.data_structures.splay_tree.splay_tree_set_top_down import SplayTreeSetTopDown
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

# from titan_pylib.my_class.ordered_set_interface import OrderedSetInterface
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
from typing import Optional, Generic, Iterable, List, TypeVar
T = TypeVar('T', bound=SupportsLessThan)

class SplayTreeSetTopDown(OrderedSetInterface, Generic[T]):

  def __init__(self, a: Iterable[T]=[], e: T=0):
    self.keys: List[T] = [e]
    self.child = array('I', bytes(8))
    self.end: int = 1
    self.root: int = 0
    self.len: int = 0
    self.e: T = e
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def rec(l: int, r: int) -> int:
      mid = (l + r) >> 1
      if l != mid:
        child[mid<<1] = rec(l, mid)
      if mid + 1 != r:
        child[mid<<1|1] = rec(mid+1, r)
      return mid
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(a)
      b = [a[0]]
      for e in a:
        if b[-1] == e:
          continue
        b.append(e)
      a = b
    n = len(a)
    key, child = self.keys, self.child
    self.reserve(n-len(key)+2)
    self.end += n
    key[1:n+1] = a
    self.root = rec(1, n+1)
    self.len = n

  def _make_node(self, key: T) -> int:
    if self.end >= len(self.keys):
      self.keys.append(key)
      self.child.append(0)
      self.child.append(0)
    else:
      self.keys[self.end] = key
    self.end += 1
    return self.end - 1

  def _rotate_right(self, node: int) -> int:
    child = self.child
    u = child[node<<1]
    child[node<<1] = child[u<<1|1]
    child[u<<1|1] = node
    return u

  def _rotate_left(self, node: int) -> int:
    child = self.child
    u = child[node<<1|1]
    child[node<<1|1] = child[u<<1]
    child[u<<1] = node
    return u

  def _set_search_splay(self, key: T) -> None:
    def set_left(node: int) -> int:
      nonlocal left
      child[left<<1|1] = node
      left = node
      return child[node<<1|1]
    def set_right(node: int) -> int:
      nonlocal right
      child[right<<1] = node
      right = node
      return child[node<<1]
    node = self.root
    keys, child = self.keys, self.child
    if (not node) or keys[node] == key: return
    left, right = 0, 0
    while keys[node] != key:
      if key > keys[node]:
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          node = self._rotate_left(node)
          if not child[node<<1|1]: break
          node = set_left(node)
        elif child[child[node<<1|1]<<1] and key < keys[child[child[node<<1|1]<<1]]:
          node = set_left(node)
          node = set_right(node)
        else:
          node = set_left(node)
      else:
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          node = self._rotate_right(node)
          if not child[node<<1]: break
          node = set_right(node)
        elif child[child[node<<1]<<1|1] and key > keys[child[child[node<<1]<<1|1]]:
          node = set_right(node)
          node = set_left(node)
        else:
          node = set_right(node)
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.root = node

  def _get_min_splay(self, node: int) -> int:
    child = self.child
    if (not node) or (not child[node<<1]): return node
    right = 0
    while child[node<<1]:
      node = self._rotate_right(node)
      if not child[node<<1]: break
      child[right<<1] = node
      right = node
      node = child[node<<1]
    child[right<<1] = child[node<<1|1]
    child[1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    return node

  def _get_max_splay(self, node: int) -> int:
    child = self.child
    if (not node) or (not child[node<<1|1]): return node
    left = 0
    while child[node<<1|1]:
      node = self._rotate_left(node)
      if not child[node<<1|1]: break
      child[left<<1|1] = node
      left = node
      node = child[node<<1|1]
    child[0] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    return node

  def reserve(self, n: int) -> None:
    assert n >= 0, 'ValueError'
    self.keys += [self.e] * n
    self.child += array('I', bytes(8 * n))

  def add(self, key: T) -> bool:
    if not self.root:
      self.root = self._make_node(key)
      self.len += 1
      return True
    keys, child = self.keys, self.child
    self._set_search_splay(key)
    if keys[self.root] == key:
      return False
    node = self._make_node(key)
    f = key > keys[self.root]
    child[node<<1|f] = child[self.root<<1|f]
    child[node<<1|f^1] = self.root
    child[self.root<<1|f] = 0
    self.root = node
    return True

  def discard(self, key: T) -> bool:
    if not self.root: return False
    self._set_search_splay(key)
    keys, child = self.keys, self.child
    if keys[self.root] != key: return False
    if not child[self.root<<1]:
      self.root = child[self.root<<1|1]
    elif not child[self.root<<1|1]:
      self.root = child[self.root<<1]
    else:
      node = self._get_min_splay(child[self.root<<1|1])
      child[node<<1] = child[self.root<<1]
      self.root = node
    self.len -= 1
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError(key)

  def ge(self, key: T) -> Optional[T]:
    def set_left(node: int) -> int:
      nonlocal left
      child[left<<1|1] = node
      left = node
      return child[node<<1|1]
    def set_right(node: int) -> int:
      nonlocal right
      child[right<<1] = node
      right = node
      return child[node<<1]
    node = self.root
    if not node: return None
    keys, child = self.keys, self.child
    if keys[node] == key: return key
    ge = None
    left, right = 0, 0
    while True:
      if keys[node] == key:
        ge = key
        break
      if key < keys[node]:
        ge = keys[node]
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          node = self._rotate_right(node)
          ge = keys[node]
          if not child[node<<1]: break
          node = set_right(node)
        elif child[child[node<<1]<<1|1] and key > keys[child[child[node<<1]<<1|1]]:
          node = set_right(node)
          node = set_left(node)
        else:
          node = set_right(node)
      else:
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          node = self._rotate_left(node)
          if not child[node<<1|1]: break
          node = set_left(node)
        elif child[child[node<<1|1]<<1] and key < keys[child[child[node<<1|1]<<1]]:
          node = set_left(node)
          node = set_right(node)
        else:
          node = set_left(node)
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.root = node
    return ge

  def gt(self, key: T) -> Optional[T]:
    def set_left(node: int) -> int:
      nonlocal left
      child[left<<1|1] = node
      left = node
      return child[node<<1|1]
    def set_right(node: int) -> int:
      nonlocal right
      child[right<<1] = node
      right = node
      return child[node<<1]
    node = self.root
    if not node: return None
    keys, child = self.keys, self.child
    gt = None
    left, right = 0, 0
    while True:
      if key < keys[node]:
        gt = keys[node]
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          node = self._rotate_right(node)
          gt = keys[node]
          if not child[node<<1]: break
          node = set_right(node)
        elif child[child[node<<1]<<1|1] and key > keys[child[child[node<<1]<<1|1]]:
          node = set_right(node)
          node = set_left(node)
        else:
          node = set_right(node)
      else:
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          node = self._rotate_left(node)
          if not child[node<<1|1]: break
          node = set_left(node)
        elif child[child[node<<1|1]<<1] and key < keys[child[child[node<<1|1]<<1]]:
          node = set_left(node)
          node = set_right(node)
        else:
          node = set_left(node)
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.root = node
    return gt

  def le(self, key: T) -> Optional[T]:
    def set_left(node: int) -> int:
      nonlocal left
      child[left<<1|1] = node
      left = node
      return child[node<<1|1]
    def set_right(node: int) -> int:
      nonlocal right
      child[right<<1] = node
      right = node
      return child[node<<1]
    node = self.root
    if not node: return None
    keys, child = self.keys, self.child
    if keys[node] == key: return key
    le = None
    left, right = 0, 0
    while True:
      if keys[node] == key:
        le = key
        break
      if key > keys[node]:
        le = keys[node]
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          node = self._rotate_left(node)
          le = keys[node]
          if not child[node<<1|1]: break
          node = set_left(node)
        elif child[child[node<<1|1]<<1] and key < keys[child[child[node<<1|1]<<1]]:
          node = set_left(node)
          node = set_right(node)
        else:
          node = set_left(node)
      else:
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          node = self._rotate_right(node)
          if not child[node<<1]: break
          node = set_right(node)
        elif child[child[node<<1]<<1|1] and key > keys[child[child[node<<1]<<1|1]]:
          node = set_right(node)
          node = set_left(node)
        else:
          node = set_right(node)
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.root = node
    return le

  def lt(self, key: T) -> Optional[T]:
    def set_left(node: int) -> int:
      nonlocal left
      child[left<<1|1] = node
      left = node
      return child[node<<1|1]
    def set_right(node: int) -> int:
      nonlocal right
      child[right<<1] = node
      right = node
      return child[node<<1]
    node = self.root
    if not node: return None
    keys, child = self.keys, self.child
    lt = None
    left, right = 0, 0
    while True:
      if key > keys[node]:
        lt = keys[node]
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          node = self._rotate_left(node)
          lt = keys[node]
          if not child[node<<1|1]: break
          node = set_left(node)
        elif child[child[node<<1|1]<<1] and key < keys[child[child[node<<1|1]<<1]]:
          node = set_left(node)
          node = set_right(node)
        else:
          node = set_left(node)
      else:
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          node = self._rotate_right(node)
          if not child[node<<1]: break
          node = set_right(node)
        elif child[child[node<<1]<<1|1] and key > keys[child[child[node<<1]<<1|1]]:
          node = set_right(node)
          node = set_left(node)
        else:
          node = set_right(node)
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.root = node
    return lt

  def tolist(self) -> List[T]:
    node = self.root
    child, keys = self.child, self.keys
    stack, res = [], []
    while stack or node:
      if node:
        stack.append(node)
        node = child[node<<1]
      else:
        node = stack.pop()
        res.append(keys[node])
        node = child[node<<1|1]
    return res

  def get_max(self) -> T:
    assert self.root, 'IndexError: get_max() from empty SplayTreeSetTopDown'
    self.root = self._get_max_splay(self.root)
    return self.keys[self.root]

  def get_min(self) -> T:
    assert self.root, 'IndexError: get_min() from empty SplayTreeSetTopDown'
    self.root = self._get_min_splay(self.root)
    return self.keys[self.root]

  def pop_max(self) -> T:
    assert self.root, 'IndexError: pop_max() from empty SplayTreeSetTopDown'
    self.len -= 1
    node = self._get_max_splay(self.root)
    self.root = self.child[node<<1]
    return self.keys[node]

  def pop_min(self) -> T:
    assert self.root, 'IndexError: pop_min() from empty SplayTreeSetTopDown'
    self.len -= 1
    node = self._get_min_splay(self.root)
    self.root = self.child[node<<1|1]
    return self.keys[node]

  def clear(self) -> None:
    self.root = 0

  def __iter__(self):
    self.it = self.get_min()
    return self

  def __next__(self):
    if self.it is None:
      raise StopIteration
    res = self.it
    self.it = self.gt(res)
    return res

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.keys[self.root] == key

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.root != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'SplayTreeSetTopDown({self})'


