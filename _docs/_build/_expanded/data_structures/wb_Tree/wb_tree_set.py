# from titan_pylib.data_structures.wb_Tree.wb_tree_set import WBTreeSet
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

from math import sqrt
from array import array
from typing import Generic, Iterable, Optional, TypeVar, List, Final
T = TypeVar('T', bound=SupportsLessThan)

class WBTreeSet(OrderedSetInterface, Generic[T]):
  """
  [BINARY SEARCH TREES OF BOUNDED BALANCE](https://dl.acm.org/doi/pdf/10.1145/800152.804906)
  """

  _ALPHA: Final[float] = 1 - sqrt(2) / 2
  _BETA: Final[float] = (1 - 2*_ALPHA) / (1 - _ALPHA)

  def __init__(self, a: Iterable[T]=[], e: T=0) -> None:
    self.root: int = 0
    self.key: List[T] = [e]
    self.size: array[int] = array('I', bytes(4))
    self.left: array[int] = array('I', bytes(4))
    self.right: array[int] = array('I', bytes(4))
    self.end: int = 1
    self.e: T = e
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def reserve(self, n: int) -> None:
    self.key += [self.e] * n
    a = array('I', bytes(4 * n))
    self.left += a
    self.right += a
    self.size += array('I', [1] * n)

  def _balance(self, node: int) -> float:
    return (self.size[self.left[node]]+1) / (self.size[node]+1)

  def _build(self, a: List[T]) -> None:
    left, right, size = self.left, self.right, self.size
    def build(l: int, r: int) -> int:
      mid = (l + r) >> 1
      node = mid
      if l != mid:
        left[node] = build(l, mid)
        size[node] += size[left[node]]
      if mid+1 != r:
        right[node] = build(mid+1, r)
        size[node] += size[right[node]]
      return node
    n = len(a)
    if n == 0: return
    if not all(a[i] < a[i + 1] for i in range(n - 1)):
      b = sorted(a)
      a = [b[0]]
      for i in range(1, n):
        if b[i] != a[-1]:
          a.append(b[i])
      n = len(a)
    end = self.end
    self.end += n
    self.reserve(n)
    self.key[end:end+n] = a
    self.root = build(end, n+end)

  def _rotate_right(self, node: int) -> int:
    left, right, size = self.left, self.right, self.size
    u = left[node]
    size[u] = size[node]
    size[node] -= size[left[u]] + 1
    left[node] = right[u]
    right[u] = node
    return u

  def _rotate_left(self, node: int) -> int:
    left, right, size = self.left, self.right, self.size
    u = right[node]
    size[u] = size[node]
    size[node] -= size[right[u]] + 1
    right[node] = left[u]
    left[u] = node
    return u

  def _balance_left(self, node: int) -> int:
    right = self.right
    right[node] = right[node]
    u = right[node]
    if self._balance(u) >= self._BETA:
      right[node] = self._rotate_right(u)
    u = self._rotate_left(node)
    return u

  def _make_node(self, key: T) -> int:
    end = self.end
    if end >= len(self.key):
      self.key.append(key)
      self.size.append(1)
      self.left.append(0)
      self.right.append(0)
    else:
      self.key[end] = key
    self.end += 1
    return end

  def _balance_right(self, node: int) -> int:
    left = self.left
    left[node] = left[node]
    u = left[node]
    if self._balance(u) <= 1 - self._BETA:
      left[node] = self._rotate_left(u)
    u = self._rotate_right(node)
    return u

  def add(self, key: T) -> bool:
    if self.root == 0:
      self.root = self._make_node(key)
      return True
    left, right, size, keys = self.left, self.right, self.size, self.key
    node = self.root
    path: List[int] = []
    while node:
      if key == keys[node]:
        return False
      path.append(node)
      node = left[node] if key < keys[node] else right[node]
    if key < keys[path[-1]]:
      left[path[-1]] = self._make_node(key)
    else:
      right[path[-1]] = self._make_node(key)
    while path:
      new_node = 0
      node = path.pop()
      size[node] += 1
      b = self._balance(node)
      if b < self._ALPHA:
        new_node = self._balance_left(node)
      elif b > 1 - self._ALPHA:
        new_node = self._balance_right(node)
      if new_node:
        if path:
          node = path[-1]
          if keys[new_node] < keys[node]:
            left[node] = new_node
          else:
            right[node] = new_node
        else:
          self.root = new_node
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError(key)

  def discard(self, key: T) -> bool:
    left, right, size, keys = self.left, self.right, self.size, self.key
    path = []
    node = self.root
    d = 0
    while node:
      if key == keys[node]:
        break
      path.append(node)
      d = key < keys[node]
      node = left[node] if d else right[node]
    else:
      return False
    if left[node] and right[node]:
      path.append(node)
      lmax = left[node]
      d = 0 if right[lmax] else 1
      while right[lmax]:
        path.append(lmax)
        lmax = right[lmax]
      keys[node] = keys[lmax]
      node = lmax
    cnode = right[node] if left[node] == 0 else left[node]
    if path:
      if d:
        left[path[-1]] = cnode
      else:
        right[path[-1]] = cnode
    else:
      self.root = cnode
      return True
    while path:
      new_node = 0
      node = path.pop()
      size[node] -= 1
      b = self._balance(node)
      if b < self._ALPHA:
        new_node = self._balance_left(node)
      elif b > 1 - self._ALPHA:
        new_node = self._balance_right(node)
      if new_node:
        if not path:
          self.root = new_node
          return True
        if keys[new_node] < keys[path[-1]]:
          left[path[-1]] = new_node
        else:
          right[path[-1]] = new_node
    return True

  def _kth_elm(self, k: int) -> T:
    if k < 0:
      k += len(self)
    left, right, size, keys = self.left, self.right, self.size, self.key
    node = self.root
    while True:
      assert node
      t = size[left[node]]
      if t == k:
        return keys[node]
      elif t < k:
        k -= t + 1
        node = right[node]
      else:
        node = left[node]

  def tolist(self) -> List[T]:
    left, right, keys = self.left, self.right, self.key
    node = self.root
    stack = []
    a = []
    while stack or node:
      if node:
        stack.append(node)
        node = left[node]
      else:
        node = stack.pop()
        a.append(keys[node])
        node = right[node]
    return a

  def le(self, key: T) -> Optional[T]:
    left, right, keys = self.left, self.right, self.key
    res = None
    node = self.root
    while node:
      if key == keys[node]:
        res = key
        break
      elif key < keys[node]:
        node = left[node]
      else:
        res = keys[node]
        node = right[node]
    return res

  def lt(self, key: T) -> Optional[T]:
    left, right, keys = self.left, self.right, self.key
    res = None
    node = self.root
    while node:
      if key > keys[node]:
        res = keys[node]
        node = right[node]
      else:
        node = left[node]
    return res

  def ge(self, key: T) -> Optional[T]:
    left, right, keys = self.left, self.right, self.key
    res = None
    node = self.root
    while node:
      if key == keys[node]:
        res = key
        break
      elif key < keys[node]:
        res = keys[node]
        node = left[node]
      else:
        node = right[node]
    return res

  def gt(self, key: T) -> Optional[T]:
    left, right, keys = self.left, self.right, self.key
    res = None
    node = self.root
    while node:
      if key < keys[node]:
        res = keys[node]
        node = left[node]
      else:
        node = right[node]
    return res

  def index(self, key: T) -> int:
    left, right, size, keys = self.left, self.right, self.size, self.key
    k = 0
    node = self.root
    while node:
      if key == keys[node]:
        k += size[left[node]]
        break
      elif key < keys[node]:
        node = left[node]
      else:
        k += size[left[node]] + 1
        node = right[node]
    return k

  def index_right(self, key: T) -> int:
    left, right, size, keys = self.left, self.right, self.size, self.key
    k = 0
    node = self.root
    while node:
      if key == keys[node]:
        k += size[left[node]] + 1
        break
      elif key < keys[node]:
        node = left[node]
      else:
        k += size[left[node]] + 1
        node = right[node]
    return k

  def pop(self, k: int=-1) -> T:
    assert self.root, f'IndexError: {self.__class__.__name__}.pop({k}), pop({k}) from Empty {self.__class__.__name__}'
    x = self._kth_elm(k)
    self.discard(x)
    return x

  def pop_max(self) -> T:
    assert self.root, f'IndexError: {self.__class__.__name__}.pop_max(), pop_max from Empty {self.__class__.__name__}'
    return self.pop()

  def pop_min(self) -> T:
    assert self.root, f'IndexError: {self.__class__.__name__}.pop_min(), pop_min from Empty {self.__class__.__name__}'
    return self.pop(0)

  def get_max(self) -> Optional[T]:
    if not self.root: return
    return self._kth_elm(-1)

  def get_min(self) -> Optional[T]:
    if not self.root: return
    return self._kth_elm(0)

  def clear(self) -> None:
    self.root = 0

  def __contains__(self, key: T) -> bool:
    keys, left, right = self.key, self.left, self.right
    node = self.root
    while node:
      if key == keys[node]:
        return True
      node = left[node] if key < keys[node] else right[node]
    return False

  def __getitem__(self, k: int) -> T:
    return self._kth_elm(k)

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __len__(self):
    return self.size[self.root]

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __bool__(self):
    return self.root != 0

  def __repr__(self):
    return f'WBTreeSet({self})'

  def isok(self):
    left, right, size, keys = self.left, self.right, self.size, self.key
    def rec(node):
      ls, rs = 0, 0
      height = 0
      if left[node]:
        ls, h = rec(left[node])
        height = max(height, h)
      if right[node]:
        rs, h = rec(right[node])
        height = max(height, h)
      s = ls + rs + 1
      b = (ls+1) / (s+1)
      assert s == size[node]
      if not (self._ALPHA <= b <= 1-self._ALPHA):
        print('NG!')
        print(f'{keys[node]=}, {ls=}, {rs=}, {s=}, {b=}')
        print(f'{self._ALPHA=}, {1-self._ALPHA=}')
        assert False
      return s, height+1
    if not self.root: return
    _, h = rec(self.root)
    # print(f'isok.ok., height={h}')

