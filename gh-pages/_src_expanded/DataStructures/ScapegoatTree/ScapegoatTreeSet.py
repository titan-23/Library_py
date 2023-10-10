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

import math
from typing import Final, Iterator, List, Sequence, TypeVar, Generic, Iterable, Optional
from __pypy__ import newlist_hint
T = TypeVar('T', bound=SupportsLessThan)

class ScapegoatTreeSet(OrderedSetInterface, Generic[T]):

  alpha: Final[float] = 0.75
  beta: Final[float] = math.log2(1 / alpha)

  class Node():

    def __init__(self, key: T):
      self.key: T = key
      self.left: Optional['ScapegoatTreeSet.Node'] = None
      self.right: Optional['ScapegoatTreeSet.Node'] = None
      self.size: int = 1

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.size}\n'
      return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]):
    self.root: Optional['ScapegoatTreeSet.Node'] = None
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Sequence[T]) -> None:
    Node = ScapegoatTreeSet.Node
    def rec(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = rec(l, mid)
        node.size += node.left.size
      if mid+1 != r:
        node.right = rec(mid+1, r)
        node.size += node.right.size
      return node
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(a)
      b = newlist_hint(len(a))
      b.append(a[0])
      for e in a:
        if b[-1] == e:
          continue
        b.append(e)
      a = b
    self.root = rec(0, len(a))

  def _rebuild(self, node: Node) -> Node:
    def rec(l: int, r: int) -> 'ScapegoatTreeSet.Node':
      mid = (l + r) >> 1
      node = a[mid]
      node.size = 1
      if l != mid:
        node.left = rec(l, mid)
        node.size += node.left.size
      else:
        node.left = None
      if mid+1 != r:
        node.right = rec(mid+1, r)
        node.size += node.right.size
      else:
        node.right = None
      return node
    a = newlist_hint(node.size)
    stack = []
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        a.append(node)
        node = node.right
    return rec(0, len(a))

  def add(self, key: T) -> bool:
    Node = ScapegoatTreeSet.Node
    node = self.root
    if node is None:
      self.root = Node(key)
      return True
    path = []
    while node:
      path.append(node)
      if key == node.key:
        return False
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    if key < path[-1].key:
      path[-1].left = Node(key)
    else:
      path[-1].right = Node(key)
    if len(path)*ScapegoatTreeSet.beta > math.log(self.root.size):
      node_size = 1
      while path:
        pnode = path.pop()
        pnode_size = pnode.size + 1
        if ScapegoatTreeSet.alpha * pnode_size < node_size:
          break
        node_size = pnode_size
      new_node = self._rebuild(pnode)
      if not path:
        self.root = new_node
        return True
      if new_node.key < path[-1].key:
        path[-1].left = new_node
      else:
        path[-1].right = new_node
    for p in path:
      p.size += 1
    return True

  def discard(self, key: T) -> bool:
    di = 1
    node = self.root
    path = []
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        di = 1
        node = node.left
      else:
        path.append(node)
        di = 0
        node = node.right
    else:
      return False
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else 0
      while lmax.right is not None:
        path.append(lmax)
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.root = cnode
    for p in path:
      p.size -= 1
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError

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
      if key <= node.key:
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

  def index(self, key: T) -> int:
    k = 0
    node = self.root
    while node is not None:
      if key == node.key:
        if node.left is not None:
          k += node.left.size
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
    if k < 0:
      k += len(self)
    di = 1
    node = self.root
    path = []
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        break
      path.append(node)
      if t < k:
        node = node.right
        k -= t + 1
        di = 0
      elif t > k:
        di = 1
        node = node.left
    res = node.key
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else 0
      while lmax.right is not None:
        path.append(lmax)
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.root = cnode
    for p in path:
      p.size -= 1
    return res

  def pop_min(self) -> T:
    return self.pop(0)

  def pop_max(self) -> T:
    return self.pop()

  def clear(self) -> None:
    self.root = None

  def tolist(self) -> List[T]:
    a = newlist_hint(len(self))
    if self.root is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.root)
    return a

  def get_min(self) -> T:
    return self.__getitem__(0)

  def get_max(self) -> T:
    return self.__getitem__(-1)

  def __contains__(self, key: T):
    node = self.root
    while node is not None:
      if key == node.key:
        return True
      node = node.left if key < node.key else node.right
    return False

  def __getitem__(self, k: int) -> T:
    if k < 0:
      k += len(self)
    node = self.root
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

  def __iter__(self) -> Iterator:
    self.__iter = 0
    return self

  def __next__(self) -> T:
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return 0 if self.root is None else self.root.size

  def __bool__(self):
    return self.root is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'ScapegoatTreeSet({self})'


