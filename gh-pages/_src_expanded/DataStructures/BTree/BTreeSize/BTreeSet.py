# from Library_py.DataStructures.BTree.BTreeSize.BTreeSet import BTreeSet
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

# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from collections import deque
from bisect import bisect_left, bisect_right, insort
from typing import Deque, Generic, Tuple, TypeVar, List, Optional, Iterable
from __pypy__ import newlist_hint
T = TypeVar('T', bound=SupportsLessThan)

class BTreeSet(OrderedSetInterface, Generic[T]):

  class Node():

    def __init__(self):
      self.key: List[T] = []
      self.child: List['BTreeSet.Node'] = []
      self.size: int = 0

    def is_leaf(self) -> bool:
      return not self.child

    def _add_size(self, s: int):
      self.size += s

    def split(self, i: int) -> 'BTreeSet.Node':
      right = BTreeSet.Node()
      self.key, right.key = self.key[:i], self.key[i:]
      self.child, right.child = self.child[:i+1], self.child[i+1:]
      size = len(self.key) + sum(cnode.size for cnode in self.child)
      right.size = self.size - size
      self.size = size
      return right

    def insert_key(self, i: int, key: T) -> None:
      self.size += 1
      self.key.insert(i, key)

    def insert_child(self, i: int, node: 'BTreeSet.Node', size=-1) -> None:
      self.size += node.size if size == -1 else size
      self.child.insert(i, node)

    def append_key(self, key: T) -> None:
      self.size += 1
      self.key.append(key)

    def append_child(self, node: 'BTreeSet.Node') -> None:
      self.size += node.size
      self.child.append(node)

    def pop_key(self, i: int=-1) -> T:
      self.size -= 1
      return self.key.pop(i)

    def len_key(self) -> int:
      return len(self.key)

    def insort_key(self, key: T) -> None:
      self.size += 1
      insort(self.key, key)

    def pop_child(self, i: int=-1, size: int=-1) -> 'BTreeSet.Node':
      cnode = self.child.pop(i)
      self.size -= cnode.size if size == -1 else size
      return cnode

    def extend_key(self, keys: List[T]) -> None:
      self.size += len(keys)
      self.key += keys

    def extend_child(self, children: List['BTreeSet.Node']) -> None:
      self.size += sum(cnode.size for cnode in children)
      self.child += children

    def __str__(self):
      return str((str(self.key), self.size))

    __repr__ = __str__

  def __init__(self, a: Iterable[T]=[]):
    self._m: int = 1000
    self._root: 'BTreeSet.Node' = BTreeSet.Node()
    self._len: int = 0
    self._build(a)

  def _build(self, a: Iterable[T]):
    for e in a:
      self.add(e)

  def __getitem__(self, k: int) -> T:
    node = self._root
    while True:
      if node.is_leaf():
        return node.key[k]
      for i in range(node.len_key()+1):
        if k < node.child[i].size:
          node = node.child[i]
          break
        k -= node.child[i].size
        if k == 0 and i < node.len_key():
          return node.key[i]
        k -= 1

  def _is_over(self, node: 'BTreeSet.Node') -> bool:
    return node.len_key() > self._m

  def add(self, key: T) -> bool:
    node = self._root
    stack = []
    while True:
      i = bisect_left(node.key, key)
      if i < node.len_key() and node.key[i] == key:
        return False
      if i >= len(node.child):
        break
      stack.append(node)
      node = node.child[i]
    self._len += 1
    node.insort_key(key)
    while stack:
      if not self._is_over(node):
        break
      pnode = stack.pop()
      i = node.len_key() // 2
      center = node.pop_key(i)
      right = node.split(i)
      indx = bisect_left(pnode.key, center)
      pnode.insert_key(indx, center)
      pnode.insert_child(indx+1, right, size=0)
      node = pnode
    while stack:
      pnode = stack.pop()
      pnode._add_size(1)
    if self._is_over(node):
      pnode = BTreeSet.Node()
      i = node.len_key() // 2
      center = node.pop_key(i)
      right = node.split(i)
      pnode.append_key(center)
      pnode.append_child(node)
      pnode.append_child(right)
      self._root = pnode
    return True

  def __contains__(self, key: T) -> bool:
    node = self._root
    while True:
      i = bisect_left(node.key, key)
      if i < node.len_key() and node.key[i] == key:
        return True
      if node.is_leaf():
        break
      node = node.child[i]
    return False

  def _discard_right(self, node: 'BTreeSet.Node') -> T:
    stack = []
    while not node.is_leaf():
      stack.append(node)
      if node.child[-1].len_key() == self._m//2:
        if node.child[-2].len_key() > self._m//2:
          cnode = node.child[-2]
          node.child[-1].insert_key(0, node.key[-1])
          node.key[-1] = cnode.pop_key()
          if cnode.child:
            node.child[-1].insert_child(0, cnode.pop_child())
          node = node.child[-1]
          continue
        cnode = self._merge(node, node.len_key()-1)
        if node is self._root and not node.key:
          self._root = cnode
        node = cnode
        continue
      node = node.child[-1]
    self._update_stack(stack)
    return node.pop_key()

  def _discard_left(self, node: 'BTreeSet.Node') -> T:
    stack = []
    while not node.is_leaf():
      stack.append(node)
      if node.child[0].len_key() == self._m//2:
        if node.child[1].len_key() > self._m//2:
          cnode = node.child[1]
          node.child[0].append_key(node.key[0])
          node.key[0] = cnode.pop_key(0)
          if cnode.child:
            node.child[0].append_child(cnode.pop_child(0))
          node = node.child[0]
          continue
        cnode = self._merge(node, 0)
        if node is self._root and not node.key:
          self._root = cnode
        node = cnode
        continue
      node = node.child[0]
    self._update_stack(stack)
    return node.pop_key(0)

  def _merge(self, node: 'BTreeSet.Node', i: int) -> 'BTreeSet.Node':
    y = node.child[i]
    z = node.pop_child(i+1, size=0)
    y.append_key(node.pop_key(i))
    node.size += 1
    y.extend_key(z.key)
    y.extend_child(z.child)
    return y

  def _merge_key(self, key: T, node: 'BTreeSet.Node', i: int) -> None:
    if node.child[i].len_key() > self._m//2:
      node.key[i] = self._discard_right(node.child[i])
      return
    if node.child[i+1].len_key() > self._m//2:
      node.key[i] = self._discard_left(node.child[i+1])
      return
    y = self._merge(node, i)
    self._discard(key, y)
    if node is self._root and not node.key:
      self._root = y

  def _update_stack(self, stack: List['BTreeSet.Node']) -> None:
    for s in stack:
      s.size -= 1

  def _discard(self, key: T, node: Optional['BTreeSet.Node']=None) -> bool:
    if node is None:
      node = self._root
    if not node.key:
      return False
    stack = []
    while True:
      i = bisect_left(node.key, key)
      if node.is_leaf():
        if i < node.len_key() and node.key[i] == key:
          node.pop_key(i)
          self._update_stack(stack)
          return True
        return False
      stack.append(node)
      if i < node.len_key() and node.key[i] == key:
        assert i+1 < len(node.child)
        self._merge_key(key, node, i)
        self._update_stack(stack)
        return True
      if node.child[i].len_key() == self._m//2:
        if i+1 < len(node.child) and node.child[i+1].len_key() > self._m//2:
          cnode = node.child[i+1]
          node.child[i].append_key(node.key[i])
          node.key[i] = cnode.pop_key(0)
          if cnode.child:
            node.child[i].append_child(cnode.pop_child(0))
          node = node.child[i]
          continue
        if i-1 >= 0 and node.child[i-1].len_key() > self._m//2:
          cnode = node.child[i-1]
          node.child[i].insert_key(0, node.key[i-1])
          node.key[i-1] = cnode.pop_key()
          if cnode.child:
            node.child[i].insert_child(0, cnode.pop_child())
          node = node.child[i]
          continue
        if i+1 >= len(node.child):
          i -= 1
        cnode = self._merge(node, i)
        if node is self._root and not node.key:
          self._root = cnode
        node = cnode
        continue
      node = node.child[i]

  def discard(self, key: T) -> bool:
    if self._discard(key):
      self._len -= 1
      return True
    return False

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise ValueError

  def tolist(self) -> List[T]:
    a = newlist_hint(len(self))
    def dfs(node):
      if not node.child:
        a.extend(node.key)
        return
      dfs(node.child[0])
      for i in range(node.len_key()):
        a.append(node.key[i])
        dfs(node.child[i+1])
    dfs(self._root)
    return a

  def get_max(self) -> Optional[T]:
    node = self._root
    while True:
      if not node.child:
        return node.key[-1] if node.key else None
      node = node.child[-1]

  def get_min(self) -> Optional[T]:
    node = self._root
    while True:
      if not node.child:
        return node.key[0] if node.key else None
      node = node.child[0]

  def debug(self) -> None:
    dep = [[] for _ in range(10)]
    dq: Deque[Tuple['BTreeSet.Node', int]] = deque([(self._root, 0)])
    while dq:
      node, d = dq.popleft()
      dep[d].append((node.key, node.size))
      if node.child:
        print(node, 'child=', node.child)
      for e in node.child:
        if e:
          dq.append((e, d+1))
    for i in range(10):
      if not dep[i]: break
      for e in dep[i]:
        print(e, end='  ')
      print()

  def pop(self, k: int=-1) -> T:
    assert -len(self) <= k < len(self), f'IndexError'
    if k < 0:
      k += len(self)
    node = self._root
    self._len -= 1
    stack = []
    while True:
      if node.is_leaf():
        v = node.pop_key(k)
        self._update_stack(stack)
        return v
      stack.append(node)
      i = -1
      for i in range(node.len_key()+1):
        if k < node.child[i].size:
          break
        k -= node.child[i].size
        if k == 0 and i < node.len_key():
          v = node.key[i]
          self._merge_key(v, node, i)
          self._update_stack(stack)
          return v
        k -= 1
      if node.child[i].len_key() == self._m//2:
        if i+1 < len(node.child) and node.child[i+1].len_key() > self._m//2:
          cnode = node.child[i+1]
          node.child[i].append_key(node.key[i])
          node.key[i] = cnode.pop_key(0)
          if cnode.child:
            node.child[i].append_child(cnode.pop_child(0))
          node = node.child[i]
          continue
        if i-1 >= 0 and node.child[i-1].len_key() > self._m//2:
          cnode = node.child[i-1]
          k += 1
          if cnode.child:
            k += cnode.child[-1].size
          node.child[i].insert_key(0, node.key[i-1])
          node.key[i-1] = cnode.pop_key()
          if cnode.child:
            node.child[i].insert_child(0, cnode.pop_child())
          node = node.child[i]
          continue
        if i+1 >= len(node.child):
          i -= 1
          k += node.child[i].size + 1
        cnode = self._merge(node, i)
        if node is self._root and not node.key:
          self._root = cnode
        node = cnode
        continue
      node = node.child[i]

  def pop_max(self) -> T:
    assert self, f'IndexError'
    return self.pop()

  def pop_min(self) -> T:
    assert self, f'IndexError'
    return self.pop(0)

  def ge(self, key: T) -> Optional[T]:
    res, node = None, self._root
    while node.key:
      i = bisect_left(node.key, key)
      if i < node.len_key() and node.key[i] == key:
        return node.key[i]
      if i < node.len_key():
        res = node.key[i]
      if not node.child:
        break
      node = node.child[i]
    return res

  def gt(self, key: T) -> Optional[T]:
    res, node = None, self._root
    while node.key:
      i = bisect_right(node.key, key)
      if i < node.len_key():
        res = node.key[i]
      if not node.child:
        break
      node = node.child[i]
    return res

  def le(self, key: T) -> Optional[T]:
    res, node = None, self._root
    while node.key:
      i = bisect_left(node.key, key)
      if i < node.len_key() and node.key[i] == key:
        return node.key[i]
      if i-1 >= 0:
        res = node.key[i-1]
      if not node.child:
        break
      node = node.child[i]
    return res

  def lt(self, key: T) -> Optional[T]:
    res, node = None, self._root
    while node.key:
      i = bisect_left(node.key, key)
      if i-1 >= 0:
        res = node.key[i-1]
      if not node.child:
        break
      node = node.child[i]
    return res

  def clear(self) -> None:
    self._root = BTreeSet.Node()

  def __iter__(self):
    self._iter_val = self.get_min()
    return self

  def __next__(self):
    if self._iter_val is None:
      raise StopIteration
    p = self._iter_val
    self._iter_val = self.gt(self._iter_val)
    return p

  def __bool__(self):
    return self._len > 0

  def __len__(self):
    return self._len

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'BTreeSet({self.tolist()})'


