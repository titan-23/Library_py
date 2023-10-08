from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic, List
T = TypeVar('T', bound=SupportsLessThan)

class OrderedMultisetInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, a: Iterable[T]) -> None:
    raise NotImplementedError

  @abstractmethod
  def add(self, key: T, cnt: int) -> None:
    raise NotImplementedError

  @abstractmethod
  def discard(self, key: T, cnt: int) -> bool:
    raise NotImplementedError

  @abstractmethod
  def discard_all(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def count(self, key: T) -> int:
    raise NotImplementedError

  @abstractmethod
  def remove(self, key: T, cnt: int) -> None:
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

from typing import Generic, Iterable, TypeVar, Tuple, List, Optional, Sequence
from __pypy__ import newlist_hint
T = TypeVar('T', bound=SupportsLessThan)

class TreapMultiset(OrderedMultisetInterface, Generic[T]):

  class Random():

    _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

    @classmethod
    def random(cls) -> int:
      t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
      cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
      cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
      return cls._w

  class Node():

    def __init__(self, key: T, val: int=1, priority: int=-1):
      self.key: T = key
      self.val: int = val
      self.left: Optional['TreapMultiset.Node'] = None
      self.right: Optional['TreapMultiset.Node'] = None
      self.priority: int = TreapMultiset.Random.random() if priority == -1 else priority

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.priority}\n'
      return f'key:{self.key, self.priority},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]):
    self.root: Optional['TreapMultiset.Node'] = None
    self._len: int = 0
    self._len_elm: int = 0
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _rle(self, a: Sequence[T]) -> Tuple[List[T], List[int]]:
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

  def _build(self, a: Iterable[T]) -> None:
    Node = TreapMultiset.Node
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(key[mid], val[mid], rand[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      return node
    a = sorted(a)
    self._len = len(a)
    key, val = self._rle(a)
    self._len_elm = len(key)
    rand = [TreapMultiset.Random.random() for _ in range(self._len_elm)]
    rand.sort()
    self.root = sort(0, len(key))

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

  def add(self, key: T, val: int=1) -> None:
    self._len += val
    if self.root is None:
      self.root = TreapMultiset.Node(key, val)
      self._len_elm += 1
      return
    node = self.root
    path = []
    di = 0
    while node is not None:
      if key == node.key:
        node.val += val
        return
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    self._len_elm += 1
    if di & 1:
      path[-1].left = TreapMultiset.Node(key, val)
    else:
      path[-1].right = TreapMultiset.Node(key, val)
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
      if new_node is not None:
        if path:
          if di & 1:
            path[-1].left = new_node
          else:
            path[-1].right = new_node
        else:
          self.root = new_node
    self._len += 1

  def discard(self, key: T, val: int=1) -> bool:
    node = self.root
    pnode = None
    while node is not None:
      if key == node.key:
        break
      pnode = node
      node = node.left if key < node.key else node.right
    else:
      return False
    self._len -= min(val, node.val)
    if node.val > val:
      node.val -= val
      return True
    self._len_elm -= 1
    while node.left is not None and node.right is not None:
      if node.left.priority < node.right.priority:
        if pnode is None:
          pnode = self._rotate_L(node)
          self.root = pnode
          continue
        new_node = self._rotate_L(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      else:
        if pnode is None:
          pnode = self._rotate_R(node)
          self.root = pnode
          continue
        new_node = self._rotate_R(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      pnode = new_node
    if pnode is None:
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

  def discard_all(self, key: T) -> bool:
    return self.discard(key, self.count(key))

  def remove(self, key: T, val: int=1) -> None:
    if self.discard(key, val):
      return
    raise KeyError(key)

  def count(self, key: T) -> int:
    node = self.root
    while node is not None:
      if node.key == key:
        return node.val
      node = node.left if key < node.key else node.right
    return 0

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
      if node.key > key:
        node = node.left
      else:
        res = node.key
        node = node.right
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

  def len_elm(self) -> int:
    return self._len_elm

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.tolist_items())) + '}')

  def tolist(self) -> List[T]:
    a = []
    if self.root is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.extend([node.key]*node.val)
      if node.right is not None:
        rec(node.right)
    rec(self.root)
    return a

  def tolist_items(self) -> List[Tuple[T, int]]:
    a = []
    if self.root is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.val))
      if node.right is not None:
        rec(node.right)
    rec(self.root)
    return a

  def get_min(self) -> Optional[T]:
    if self.root is None:
      return
    node = self.root
    while node.left is not None:
      node = node.left
    return node.key

  def get_max(self) -> Optional[T]:
    if self.root is None:
      return
    node = self.root
    while node.right is not None:
      node = node.right
    return node.key

  def pop_min(self) -> T:
    assert self
    self._len -= 1
    node = self.root
    pnode = None
    while node.left is not None:
      pnode = node
      node = node.left
    if node.val > 1:
      node.val -= 1
      return node.key
    self._len_elm -= 1
    res = node.key
    if pnode is None:
      self.root = self.root.right
    else:
      pnode.left = node.right
    return res

  def pop_max(self) -> T:
    assert self, f'IndexError'
    self._len -= 1
    node = self.root
    pnode = None
    while node.right is not None:
      pnode = node
      node = node.right
    if node.val > 1:
      node.val -= 1
      return node.key
    self._len_elm -= 1
    res = node.key
    if pnode is None:
      self.root = self.root.left
    else:
      pnode.right = node.left
    return res

  def clear(self) -> None:
    self.root = None

  def __iter__(self):
    self._it = self.get_min()
    self._cnt = 1
    return self
  
  def __next__(self):
    if self._it is None:
      raise StopIteration
    res = self._it
    if self._cnt == self.count(self._it):
      self._it = self.gt(self._it)
      self._cnt = 1
    else:
      self._cnt += 1
    return res

  def __contains__(self, key: T):
    node = self.root
    while node is not None:
      if key == node.key:
        return True
      if key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __bool__(self):
    return self.root is not None

  def __len__(self):
    return self._len

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'TreapMultiset({self.tolist()})'


