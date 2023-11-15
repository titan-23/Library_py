# from Library_py.DataStructures.WBTree.gomi.WBTreeSet import WBTreeSet
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

# from Library_py.MyClass.OrderedSetInterface import OrderedSetInterface
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
from typing import Generic, Iterable, Optional, TypeVar, List
T = TypeVar('T', bound=SupportsLessThan)

class WBTreeSet(OrderedSetInterface, Generic[T]):

  ALPHA: float = 1 - sqrt(2) / 2
  BETA : float = (1 - 2*ALPHA) / (1 - ALPHA)

  class Node():

    def __init__(self, key: T):
      self.key: T = key
      self.left: Optional[WBTreeSet.Node] = None
      self.right: Optional[WBTreeSet.Node] = None
      self.size: int = 1

    def balance(self) -> float:
      return ((self.left.size if self.left else 0)+1) / (self.size+1)

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key={self.key}, size={self.size}\n'
      return f'key={self.key}, size={self.size},\n left:{self.left},\n right:{self.right}\n'

    __repr__ = __str__

  def __init__(self, a: Iterable[T]=[], _root=None) -> None:
    self.root: Optional[WBTreeSet.Node] = _root
    a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    Node = WBTreeSet.Node
    def build(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = build(l, mid)
        node.size += node.left.size
      if mid+1 != r:
        node.right = build(mid+1, r)
        node.size += node.right.size
      return node
    self.root = build(0, len(a))

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
      else:
        node.size = 1 + node.right.size
    else:
      if node.right is None:
        node.size = 1 + node.left.size
      else:
        node.size = 1 + node.left.size + node.right.size

  def _rotate_right(self, node: Node) -> Node:
    assert node.left
    u = node.left
    node.left = u.right
    u.right = node
    self._update(node)
    self._update(u)
    return u

  def _rotate_left(self, node: Node) -> Node:
    assert node.right
    u = node.right
    node.right = u.left
    u.left = node
    self._update(node)
    self._update(u)
    return u

  def _balance_left(self, node: Node) -> Node:
    assert node.right
    node.right = node.right
    u = node.right
    if u.balance() >= self.BETA:
      assert u.left
      node.right = self._rotate_right(u)
    u = self._rotate_left(node)
    return u

  def _balance_right(self, node: Node) -> Node:
    assert node.left
    node.left = node.left
    u = node.left
    if u.balance() <= 1 - self.BETA:
      assert u.right
      node.left = self._rotate_left(u)
    u = self._rotate_right(node)
    return u

  def add(self, key: T) -> bool:
    if self.root is None:
      self.root = WBTreeSet.Node(key)
      return True
    node = self.root
    path: List[WBTreeSet.Node] = []
    while node:
      if key == node.key:
        return False
      path.append(node)
      node = node.left if key < node.key else node.right
    if key < path[-1].key:
      path[-1].left = WBTreeSet.Node(key)
    else:
      path[-1].right = WBTreeSet.Node(key)
    while path:
      new_node = None
      node = path.pop()
      node.size += 1
      b = node.balance()
      if b < self.ALPHA:
        new_node = self._balance_left(node)
      elif b > 1 - self.ALPHA:
        new_node = self._balance_right(node)
      if new_node:
        if path:
          node = path[-1]
          if new_node.key < node.key:
            node.left = new_node
          else:
            node.right = new_node
        else:
          self.root = new_node
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError(key)

  def discard(self, key: T) -> bool:
    path = []
    node = self.root
    d = 0
    while node:
      if key == node.key:
        break
      path.append(node)
      d = key < node.key
      node = node.left if d else node.right
    else:
      return False
    if node.left and node.right:
      path.append(node)
      lmax = node.left
      d = 0 if lmax.right else 1
      while lmax.right:
        path.append(lmax)
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if d:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.root = cnode
      return True
    while path:
      new_node = None
      node = path.pop()
      node.size -= 1
      b = node.balance()
      if b < self.ALPHA:
        new_node = self._balance_left(node)
      elif b > 1 - self.ALPHA:
        new_node = self._balance_right(node)
      if new_node:
        if not path:
          self.root = new_node
          return True
        if new_node.key < path[-1].key:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
    return True

  def _kth_elm(self, k: int) -> T:
    if k < 0:
      k += len(self)
    node = self.root
    while True:
      assert node
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      elif t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left

  def tolist(self) -> List[T]:
    node = self.root
    stack = []
    a = []
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        a.append(node.key)
        node = node.right
    return a

  def le(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def lt(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node is not None:
      if key > node.key:
        res = node.key
        node = node.right
      else:
        node = node.left
    return res

  def ge(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def gt(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def index(self, key: T) -> int:
    k = 0
    node = self.root
    while node is not None:
      if key == node.key:
        k += 0 if node.left is None else node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  def index_right(self, key: T) -> int:
    k = 0
    node = self.root
    while node is not None:
      if key == node.key:
        k += 1 if node.left is None else node.left.size + 1
        break
      elif key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  def pop(self, k: int=-1) -> T:
    assert self.root is not None, f'IndexError: {self.__class__.__name__}.pop({k}), pop({k}) from Empty {self.__class__.__name__}'
    x = self._kth_elm(k)
    self.discard(x)
    return x

  def pop_max(self) -> T:
    assert self.root is not None, f'IndexError: {self.__class__.__name__}.pop_max(), pop_max from Empty {self.__class__.__name__}'
    return self.pop()

  def pop_min(self) -> T:
    assert self.root is not None, f'IndexError: {self.__class__.__name__}.pop_min(), pop_min from Empty {self.__class__.__name__}'
    return self.pop(0)

  def get_max(self) -> Optional[T]:
    if self.root is None: return
    return self._kth_elm(-1)

  def get_min(self) -> Optional[T]:
    if self.root is None: return
    return self._kth_elm(0)

  def clear(self) -> None:
    self.root = None

  def __contains__(self, key: T) -> bool:
    node = self.root
    while node is not None:
      if key == node.key:
        return True
      node = node.left if key < node.key else node.right
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
    return 0 if self.root is None else self.root.size

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __bool__(self):
    return self.root is not None

  def __repr__(self):
    return f'WBTreeSet({self})'

  def isok(self):
    def rec(node):
      ls, rs = 0, 0
      height = 0
      if node.left:
        ls, h = rec(node.left)
        height = max(height, h)
      if node.right:
        rs, h = rec(node.right)
        height = max(height, h)
      s = ls + rs + 1
      b = (ls+1) / (s+1)
      assert s == node.size
      if not (self.ALPHA <= b <= 1-self.ALPHA):
        print('NG!')
        print(f'{node.key=}, {ls=}, {rs=}, {s=}, {b=}')
        print(f'{self.ALPHA=}, {1-self.ALPHA=}')
        assert False
      return s, height+1
    if not self.root: return
    _, h = rec(self.root)
    # print(f'isok.ok., height={h}')


