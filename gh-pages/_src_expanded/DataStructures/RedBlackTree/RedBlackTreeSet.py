# from Library_py.DataStructures.RedBlackTree.RedBlackTreeSet import RedBlackTreeSet
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

# from Library_py.DataStructures.BSTBase.BSTSetNodeBase import BSTSetNodeBase
from __pypy__ import newlist_hint
from typing import List, TypeVar, Generic, Optional
T = TypeVar('T')
Node = TypeVar('Node')
# protcolで、key,left,right を規定

class BSTSetNodeBase(Generic[T, Node]):

  @staticmethod
  def sort_unique(a: List[T]) -> List[T]:
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(a)
      new_a = [a[0]]
      for elm in a:
        if new_a[-1] == elm:
          continue
        new_a.append(elm)
      a = new_a
    return a

  @staticmethod
  def contains(node: Node, key: T) -> bool:
    while node:
      if key == node.key:
        return True
      node = node.left if key < node.key else node.right
    return False

  @staticmethod
  def get_min(node: Node) -> Optional[T]:
    if not node:
      return None
    while node.left:
      node = node.left
    return node.key

  @staticmethod
  def get_max(node: Node) -> Optional[T]:
    if not node:
      return None
    while node.right:
      node = node.right
    return node.key

  @staticmethod
  def le(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key == node.key:
        res = key
        break
      if key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  @staticmethod
  def lt(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  @staticmethod
  def ge(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key == node.key:
        res = key
        break
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  @staticmethod
  def gt(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  @staticmethod
  def index(node: Node, key: T) -> int:
    k = 0
    while node is not None:
      if key == node.key:
        if node.left is not None:
          k += node.left.size
        break
      if key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  @staticmethod
  def index_right(node: Node, key: T) -> int:
    k = 0
    while node is not None:
      if key == node.key:
        k += 1 if node.left is None else node.left.size + 1
        break
      if key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  @staticmethod
  def tolist(node: Node, _len: int=0) -> List[T]:
    stack = []
    res = newlist_hint(_len)
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        res.append(node.key)
        node = node.right
    return res

  @staticmethod
  def kth_elm(node: Node, k: int, _len: int) -> T:
    if k < 0:
      k += _len
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      if t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

from typing import Iterable, Optional, TypeVar, Generic, List, Sequence
from __pypy__ import newlist_hint
T = TypeVar('T', bound=SupportsLessThan)

class RedBlackTreeSet(OrderedSetInterface, Generic[T]):

  class Node():

    def __init__(self, key: T):
      self.key = key
      self.left = RedBlackTreeSet.NIL
      self.right = RedBlackTreeSet.NIL
      self.par = RedBlackTreeSet.NIL
      self.col = 0

    @property
    def count(self) -> int:
      return 1

    def _min(self):
      now = self
      while now.left:
        now = now.left
      return now

    def _max(self):
      now = self
      while now.right:
        now = now.right
      return now

    def _next(self):
      now = self
      pre = RedBlackTreeSet.NIL
      flag = now.right is pre
      while now.right is pre:
        pre, now = now, now.par
      if not now:
        return None
      return now if flag and pre is now.left else now.right._min()

    def _prev(self):
      now, pre = self, RedBlackTreeSet.NIL
      flag = now.left is pre
      while now.left is pre:
        pre, now = now, now.par
      if not now:
        return None
      return now if flag and pre is now.right else now.left._max()

    def __iadd__(self, other: int):
      res = self
      for _ in range(other):
        assert res is not None, 'RedBlackTreeSet Node.__iadd__() Error'
        res = res._next()
      return res

    def __isub__(self, other: int):
      res = self
      for _ in range(other):
        assert res is not None, 'RedBlackTreeSet Node.__isub__() Error'
        res = res._prev()
      return res

    def __add__(self, other: int):
      res = self
      for _ in range(other):
        assert res is not None, 'RedBlackTreeSet Node.__add__() Error'
        res = res._next()
      return res

    def __sub__(self, other: int):
      res = self
      for _ in range(other):
        assert res is not None, 'RedBlackTreeSet Node.__add__() Error'
        res = res._prev()
      return res

    def __str__(self):
      if self.left is RedBlackTreeSet.NIL and self.right is RedBlackTreeSet.NIL:
        return f'(key,col,par.key):{self.key, self.col, self.par.key}\n'
      return f'(key,col,par.key):{self.key, self.col, self.par.key},\n left:{self.left},\n right:{self.right}\n'

  class NILNode():

    key = None
    left = None
    right = None
    par = None
    col = 0

    def _min(self):
      return None

    def _max(self):
      return None

    def __bool__(self):
      return False

    def __str__(self):
      return 'NIL'

  NIL = NILNode()

  def __init__(self, a: Iterable[T]=[]):
    self.node = RedBlackTreeSet.NIL
    self.size = 0
    self.min_node = None
    self.max_node = None
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Sequence[T]) -> None:
    Node = RedBlackTreeSet.Node
    def rec(l: int, r: int, d: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.col = int((not flag and d&1) or (flag and d > 1 and not d&1))
      if l != mid:
        node.left = rec(l, mid, d+1)
        node.left.par = node
      if mid+1 != r:
        node.right = rec(mid+1, r, d+1)
        node.right.par = node
      return node
    a = BSTSetNodeBase[T, RedBlackTreeSet.Node].sort_unique(a)
    flag = len(a).bit_length() & 1
    self.node = rec(0, len(a), 0)
    self.min_node = self.node._min()
    self.max_node = self.node._max()
    self.size = len(a)

  def _rotate_left(self, node: Node) -> None:
    u = node.right
    p = node.par
    node.right = u.left
    if u.left:
      u.left.par = node
    u.par = p
    if not p:
      self.node = u
    elif node is p.left:
      p.left = u
    else:
      p.right = u
    u.left = node
    node.par = u

  def _rotate_right(self, node: Node) -> None:
    u = node.left
    p = node.par
    node.left = u.right
    if u.right:
      u.right.par = node
    u.par = p
    if not p:
      self.node = u
    elif node is p.right:
      p.right = u
    else:
      p.left = u
    u.right = node
    node.par = u

  def _transplant(self, u: Node, v: Node) -> None:
    if not u.par:
      self.node = v
    elif u is u.par.left:
      u.par.left = v
    else:
      u.par.right = v
    v.par = u.par

  def _get_min(self, node: Node) -> Node:
    while node.left:
      node = node.left
    return node

  def _get_max(self, node: Node) -> Node:
    while node.right:
      node = node.right
    return node

  def add(self, key: T) -> bool:
    if not self.node:
      node = RedBlackTreeSet.Node(key)
      self.node = node
      self.min_node = node
      self.max_node = node
      self.size = 1
      return True
    pnode = RedBlackTreeSet.NIL
    node = self.node
    while node:
      pnode = node
      if key == node.key:
        return False
      node = node.left if key < node.key else node.right
    self.size += 1
    z = RedBlackTreeSet.Node(key)
    if key < self.min_node.key:
      self.min_node = z
    if key > self.max_node.key:
      self.max_node = z
    z.par = pnode
    if not pnode:
      self.node = z
    elif key < pnode.key:
      pnode.left = z
    else:
      pnode.right = z
    z.col = 1
    while z.par.col:
      g = z.par.par
      if z.par is g.left:
        y = g.right
        if y.col:
          z.par.col = 0
          y.col = 0
          g.col = 1
          z = g
        else:
          if z is z.par.right:
            z = z.par
            self._rotate_left(z)
          z.par.col = 0
          g.col = 1
          self._rotate_right(g)
          break
      else:
        y = g.left
        if y.col:
          z.par.col = 0
          y.col = 0
          g.col = 1
          z = g
        else:
          if z is z.par.left:
            z = z.par
            self._rotate_right(z)
          z.par.col = 0
          g.col = 1
          self._rotate_left(g)
          break
    self.node.col = 0
    return True

  def discard_iter(self, node: Node) -> None:
    assert isinstance(node, RedBlackTreeSet.Node)
    self.size -= 1
    if node.key == self.min_node.key:
      self.min_node = node._next()
    if node.key == self.max_node.key:
      self.max_node = node._prev()
    y = node
    y_col = y.col
    if not node.left:
      x = node.right
      self._transplant(node, node.right)
    elif not node.right:
      x = node.left
      self._transplant(node, node.left)
    else:
      y = self._get_min(node.right)
      y_col = y.col
      x = y.right
      if y.par is node:
        x.par = y
      else:
        self._transplant(y, y.right)
        y.right = node.right
        y.right.par = y
      self._transplant(node, y)
      y.left = node.left
      y.left.par = y
      y.col = node.col
    if y_col:
      return
    while x is not self.node and not x.col:
      if x is x.par.left:
        y = x.par
        w = y.right
        if w.col:
          w.col = 0
          y.col = 1
          self._rotate_left(y)
          w = y.right
        if not (w.left.col or w.right.col):
          w.col = 1
          x = y
        else:
          if not w.right.col:
            w.left.col = 0
            w.col = 1
            self._rotate_right(w)
            w = y.right
          w.col = y.col
          y.col = 0
          w.right.col = 0
          self._rotate_left(x.par)
          x = self.node
      else:
        y = x.par
        w = y.left
        if w.col:
          w.col = 0
          y.col = 1
          self._rotate_right(y)
          w = y.left
        if not (w.right.col or w.left.col):
          w.col = 1
          x = y
        else:
          if not w.left.col:
            w.right.col = 0
            w.col = 1
            self._rotate_left(w)
            w = y.left
          w.col = y.col
          y.col = 0
          w.left.col = 0
          self._rotate_right(y)
          x = self.node
    x.col = 0

  def discard(self, key: T) -> bool:
    node = self.node
    while node:
      if key == node.key:
        break
      node = node.left if key < node.key else node.right
    else:
      return False
    self.discard_iter(node)
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError

  def count(self, key: T) -> int:
    return 1 if self.find(key) else 0

  def get_max(self) -> Optional[T]:
    if self.max_node is None: return
    return self.max_node.key

  def get_min(self) -> Optional[T]:
    if self.min_node is None: return
    return self.min_node.key

  def get_max_iter(self) -> Optional[Node]:
    return self.max_node

  def get_min_iter(self) -> Optional[Node]:
    return self.min_node

  def le(self, key: T) -> Optional[T]:
    res = self.le_iter(key)
    return None if res is None else res.key

  def lt(self, key: T) -> Optional[T]:
    res = self.lt_iter(key)
    return None if res is None else res.key

  def ge(self, key: T) -> Optional[T]:
    res = self.ge_iter(key)
    return None if res is None else res.key

  def gt(self, key: T) -> Optional[T]:
    res = self.gt_iter(key)
    return None if res is None else res.key

  def le_iter(self, key: T) -> Optional[Node]:
    res, node = None, self.node
    while node:
      if key == node.key:
        res = node
        break
      elif key < node.key:
        node = node.left
      else:
        res = node
        node = node.right
    return res

  def lt_iter(self, key: T) -> Optional[Node]:
    res, node = None, self.node
    while node:
      if key <= node.key:
        node = node.left
      else:
        res = node
        node = node.right
    return res

  def ge_iter(self, key: T) -> Optional[Node]:
    res, node = None, self.node
    while node:
      if key == node.key:
        res = node
        break
      if key < node.key:
        res = node
        node = node.left
      else:
        node = node.right
    return res

  def gt_iter(self, key: T) -> Optional[Node]:
    res, node = None, self.node
    while node:
      if key < node.key:
        res = node
        node = node.left
      else:
        node = node.right
    return res

  def find(self, key: T) -> Optional[Node]:
    node = self.node
    while node:
      if key == node.key:
        return node
      node = node.left if key < node.key else node.right
    return None

  def tolist(self) -> List[T]:
    return BSTSetNodeBase[T, RedBlackTreeSet.Node].tolist(self.node, len(self))

  def pop_max(self) -> T:
    assert self.node, f'IndexError: pop_max() from empty {self.__class__.__name__}.'
    node = self.max_node
    self.discard_iter(node)
    return node.key

  def pop_min(self) -> T:
    assert self.node, f'IndexError: pop_min() from empty {self.__class__.__name__}.'
    node = self.min_node
    self.discard_iter(node)
    return node.key

  def clear(self) -> None:
    self.node = RedBlackTreeSet.NIL
    self.size = 0
    self.min_node = None
    self.max_node = None

  def __iter__(self):
    self.it = self.min_node
    return self

  def __next__(self):
    if not self.it:
      raise StopIteration
    res = self.it.key
    self.it += 1
    return res

  def __bool__(self):
    return self.node is not RedBlackTreeSet.NIL

  def __contains__(self, key: T):
    node = self.node
    while node:
      if key == node.key:
        return True
      node = node.left if key < node.key else node.right
    return False

  def __len__(self):
    return self.size

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'


