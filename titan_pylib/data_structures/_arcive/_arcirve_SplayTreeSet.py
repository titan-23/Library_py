from __pypy__ import newlist_hint
from typing import Generic, Iterable, List, TypeVar, Optional
T = TypeVar('T')

class SplayTreeSet(Generic[T]):

  class Node():

    def __init__(self, key: T):
      self.key: T = key
      self.left: Optional['SplayTreeSet.Node'] = None
      self.right: Optional['SplayTreeSet.Node'] = None
      self.par: Optional['SplayTreeSet.Node'] = None
      self.size: int = 1

  def __init__(self, a: Iterable[T]=[]):
    self.root = None
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    Node = self.Node
    def build(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = build(l, mid)
        node.left.par = node
      if mid+1 != r:
        node.right = build(mid+1, r)
        node.right.par = node
      self._update(node)
      return node
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    self.root = build(0, len(a))

  def _rotate(self, node: Node) -> None:
    pnode = node.par
    gnode = pnode.par
    if gnode:
      if gnode.left is pnode:
        gnode.left = node
      else:
        gnode.right = node
    node.par = gnode
    if pnode.left is node:
      pnode.left = node.right
      if node.right:
        node.right.par = pnode
      node.right = pnode
    else:
      pnode.right = node.left
      if node.left:
        node.left.par = pnode
      node.left = pnode
    pnode.par = node
    self._update(pnode)
    self._update(node)

  def _update(self, node: Node) -> None:
    node.size = 1
    if node.left:
      node.size += node.left.size
    if node.right:
      node.size += node.right.size

  def _splay(self, node: Node) -> None:
    while node.par and node.par.par:
      pnode = node.par
      self._rotate(pnode if (pnode.par.left is pnode) == (pnode.left is node) else node)
      self._rotate(node)
    if node.par:
      self._rotate(node)

  def _set_search_splay(self, key: T) -> None:
    node = self.root
    if not node:
      return
    pnode = None
    while node and node.key != key:
      pnode = node
      node = node.left if key < node.key else node.right
    node = pnode if not node else node
    self._splay(node)
    self.root = node

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += len(self)
    assert 0 <= k < len(self), f'{k=}'
    node = self.root
    while True:
      t = node.left.size if node.left else 0
      if t == k:
        break
      if t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1
    self._splay(node)
    self.root = node

  def _get_min_splay(self, node: int) -> int:
    if not node or not node.left:
      return node
    while node.left:
      node = node.left
    self._splay(node)
    return node

  def _get_max_splay(self, node: int) -> int:
    if not node or not node.right:
      return node
    while node.right:
      node = node.right
    self._splay(node)
    return node

  def add(self, key: T) -> bool:
    if not self.root:
      self.root = self.Node(key)
      return True
    self._set_search_splay(key)
    if self.root.key == key:
      return False
    node = self.Node(key)
    if key < self.root.key:
      node.left = self.root.left
      self.root.left = None
      self._update(self.root)
      node.right = self.root
      if node.left:
        node.left.par = node
      if node.right:
        node.right.par = node
      self._update(node)
      self.root = node
    else:
      node.right = self.root.right
      self.root.right = None
      self._update(self.root)
      node.left = self.root
      if node.right:
        node.right.par = node
      if node.left:
        node.left.par = node
      self._update(node)
      self.root = node
    return True

  def discard(self, key: T) -> bool:
    if not self.root: return False
    self._set_search_splay(key)
    if self.root.key != key: return False
    if not self.root.left:
      self.root = self.root.right
      if self.root:
        self.root.par = None
    elif not self.root.right:
      self.root = self.root.left
      if self.root:
        self.root.par = None
    else:
      node = self._get_min_splay(self.root.right)
      node.par = None
      node.left = self.root.left
      if node.left:
        node.left.par = node
      self._update(node.left)
      self.root = node
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError(key)

  def le(self, key: T) -> Optional[T]:
    node = self.root
    pnode = None
    res = None
    while node:
      pnode = node
      if key == node.key:
        res = key
        break
      if key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    self._splay(pnode)
    self.root = pnode
    return res

  def lt(self, key: T) -> Optional[T]:
    node = self.root
    pnode = None
    res = None
    while node:
      pnode = node
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    self._splay(pnode)
    self.root = pnode
    return res

  def ge(self, key: T) -> Optional[T]:
    node = self.root
    pnode = None
    res = None
    while node:
      pnode = node
      if key == node.key:
        res = key
        break
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    self._splay(pnode)
    self.root = pnode
    return res

  def gt(self, key: T) -> Optional[T]:
    node = self.root
    res = None
    pnode = node
    while node:
      pnode = node
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    self._splay(pnode)
    self.root = pnode
    return res

  def index(self, key: T) -> int:
    if not self.root: return 0
    self._set_search_splay(key)
    res = self.root.left.size if self.root.left else 0
    if self.root.key < key:
      res += 1
    return res

  def index_right(self, key: T) -> int:
    if not self.root: return 0
    self._set_search_splay(key)
    res = self.root.left.size if self.root.left else 0
    if self.root.key <= key:
      res += 1
    return res

  def get_min(self) -> T:
    return self[0]

  def get_max(self) -> T:
    return self[-1]

  def pop(self, k: int=-1) -> T:
    if k == -1:
      node = self._get_max_splay(self.root)
      self.root = node.left
      if self.root:
        self.root.par = None
      return node.key
    self._set_kth_elm_splay(k)
    res = self.root.key
    if not self.root.left:
      self.root = self.root.right
      if self.root:
        self.root.par = None
    elif not self.root.right:
      self.root = self.root.left
      if self.root:
        self.root.par = None
    else:
      node = self._get_min_splay(self.root.right)
      node.par = None
      node.left = self.root.left
      if node.left:
        node.left.par = node
      self._update(node)
      self.root = node
    return res

  def pop_max(self) -> T:
    return self.pop()

  def pop_min(self) -> T:
    node = self._get_min_splay(self.root)
    self.root = node.right
    return self.keys[node]

  def clear(self) -> None:
    self.root = None

  def tolist(self) -> List[T]:
    node = self.root
    res = newlist_hint(len(self))
    stack = []
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        res.append(node.key)
        node = node.right
    return res

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == len(self):
      raise StopIteration
    self.__iter += 1
    return self[self.__iter - 1]

  def __reversed__(self):
    for i in range(len(self)):
      yield self[-i-1]

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.root.key == key

  def __getitem__(self, k: int) -> T:
    self._set_kth_elm_splay(k)
    return self.root.key

  def __len__(self):
    return self.root.size if self.root else 0

  def __bool__(self):
    return self.root != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'SplayTreeSet({self})'

