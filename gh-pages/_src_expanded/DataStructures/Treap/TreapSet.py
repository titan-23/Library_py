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

from typing import Generic, Iterable, TypeVar, Optional, List, Sequence
T = TypeVar('T', bound=SupportsLessThan)

class TreapSet(OrderedSetInterface, Generic[T]):

  class Random():

    _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

    @classmethod
    def random(cls) -> int:
      t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
      cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
      cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
      return cls._w

  class Node():

    def __init__(self, key: T, priority: int=-1):
      self.key: T = key
      self.left: Optional['TreapSet.Node'] = None
      self.right: Optional['TreapSet.Node'] = None
      self.priority: int = TreapSet.Random.random() if priority == -1 else priority

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.priority}\n'
      return f'key:{self.key, self.priority},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]):
    self.root: Optional['TreapSet.Node'] = None
    self._len: int = 0
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Sequence[T]) -> None:
    Node = TreapSet.Node
    def rec(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid], rand[mid])
      if l != mid:
        node.left = rec(l, mid)
      if mid+1 != r:
        node.right = rec(mid+1, r)
      return node
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(a)
      b = [a[0]]
      for e in a:
        if b[-1] == e:
          continue
        b.append(e)
      a = b
    self._len = len(a)
    rand = sorted(TreapSet.Random.random() for _ in range(self._len))
    self.root = rec(0, self._len)

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    node.left = u.right
    u.right = node
    return u

  def _rotate_R(self, node: Node) -> Node:
    u = node.right
    node.right = u.left
    u.left = node
    return u

  def add(self, key: T) -> bool:
    if not self.root:
      self.root = TreapSet.Node(key)
      self._len += 1
      return True
    node = self.root
    path = []
    di = 0
    while node:
      if key == node.key:
        return False
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    if di & 1:
      path[-1].left = TreapSet.Node(key)
    else:
      path[-1].right = TreapSet.Node(key)
    while path:
      new_node = None
      node = path.pop()
      if di & 1:
        if node.left.priority < node.priority:
          new_node = self._rotate_L(node)
      else:
        if node.right.priority < node.priority:
          new_node = self._rotate_R(node)
      di >>= 1
      if new_node:
        if path:
          if di & 1:
            path[-1].left = new_node
          else:
            path[-1].right = new_node
        else:
          self.root = new_node
    self._len += 1
    return True

  def discard(self, key: T) -> bool:
    node = self.root
    pnode = None
    while node:
      if key == node.key:
        break
      elif key < node.key:
        pnode = node
        node = node.left
      else:
        pnode = node
        node = node.right
    else:
      return False
    self._len -= 1
    while node.left and node.right:
      if node.left.priority < node.right.priority:
        if not pnode:
          pnode = self._rotate_L(node)
          self.root = pnode
          continue
        new_node = self._rotate_L(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      else:
        if not pnode:
          pnode = self._rotate_R(node)
          self.root = pnode
          continue
        new_node = self._rotate_R(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      pnode = new_node
    if not pnode:
      if node.left is None:
        self.root = node.right
      else:
        self.root = node.left
      return True
    if node.left is None:
      if node.key < pnode.key:
        pnode.left = node.right
      else:
        pnode.right = node.right
    else:
      if node.key < pnode.key:
        pnode.left = node.left
      else:
        pnode.right = node.left
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError

  def le(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node:
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
    while node:
      if key == node.key or key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def ge(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node:
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
    while node:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def get_min(self) -> Optional[T]:
    node = self.root
    if not node:
      return None
    while node.left:
      node = node.left
    return node.key

  def get_max(self) -> Optional[T]:
    node = self.root
    if not node:
      return None
    while node.right:
      node = node.right
    return node.key

  def pop_min(self) -> T:
    assert self.root is not None, f'IndexError'
    node = self.root
    pnode = None
    while node.left:
      pnode = node
      node = node.left
    self._len -= 1
    res = node.key
    if not pnode:
      self.root = self.root.right
    else:
      pnode.left = node.right
    return res

  def pop_max(self) -> T:
    assert self.root is not None, f'IndexError'
    node = self.root
    pnode = None
    while node.right:
      pnode = node
      node = node.right
    self._len -= 1
    res = node.key
    if not pnode:
      self.root = self.root.left
    else:
      pnode.right = node.left
    return res

  def clear(self) -> None:
    self.root = None

  def tolist(self) -> List[T]:
    a = []
    if not self.root:
      return a
    def rec(node):
      if node.left:
        rec(node.left)  
      a.append(node.key)
      if node.right:
        rec(node.right)
    rec(self.root)
    return a

  def __iter__(self):
    self._it = self.get_min()
    return self
  
  def __next__(self):
    if self._it is None:
      raise StopIteration
    res = self._it
    self._it = self.gt(self._it)
    return res

  def __contains__(self, key: T):
    node = self.root
    while node:
      if key == node.key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __len__(self):
    return self._len

  def __bool__(self):
    return self._len > 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'TreapSet({self.tolist()})'


