from math import sqrt
from typing import Generic, Iterable, Optional, TypeVar, Callable, List, Tuple, Final
T = TypeVar('T')
F = TypeVar('F')

class LazyWBTree(Generic[T, F]):

  ALPHA: Final[float] = 1 - sqrt(2) / 2
  BETA : Final[float] = (1 - 2*ALPHA) / (1 - ALPHA)

  class Node():

    def __init__(self, key: T, lazy: F):
      self.key: T = key
      self.data: T = key
      self.left: Optional[LazyWBTree.Node] = None
      self.right: Optional[LazyWBTree.Node] = None
      self.lazy: F = lazy
      self.rev: int = 0
      self.size: int = 1

    def balance(self) -> float:
      return ((self.left.size if self.left else 0)+1) / (self.size+1)

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key={self.key}, size={self.size}, data={self.data}, lazy={self.lazy}, rev={self.rev}\n'
      return f'key={self.key}, size={self.size}, data={self.data}, lazy={self.lazy}, rev={self.rev},\n left:{self.left},\n right:{self.right}\n'

    __repr__ = __str__

  def __init__(self,
               a: Iterable[T],
               op: Callable[[T, T], T],
               mapping: Callable[[F, T], T],
               composition: Callable[[F, F], F],
               e: T,
               id: F,
               _root: Optional[Node]=None
               ) -> None:
    self.root: Optional[LazyWBTree.Node] = _root
    self.op: Callable[[T, T], T] = op
    self.mapping: Callable[[F, T], T] = mapping
    self.composition: Callable[[F, F], F] = composition
    self.e: T = e
    self.id: F = id
    a = list(a)
    if a:
      self._build(list(a))

  def _build(self, a: List[T]) -> None:
    Node = LazyWBTree.Node
    def build(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid], id)
      if l != mid:
        node.left = build(l, mid)
      if mid+1 != r:
        node.right = build(mid+1, r)
      self._update(node)
      return node
    id = self.id
    self.root = build(0, len(a))

  def _propagate(self, node: Node) -> None:
    if node.rev:
      l = node.left
      r = node.right
      node.left, node.right = r, l
      if l:
        l.rev ^= 1
      if r:
        r.rev ^= 1
      node.rev = 0
    if node.lazy != self.id:
      lazy = node.lazy
      if node.left:
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.lazy = self.composition(lazy, node.left.lazy)
      if node.right:
        node.right.data = self.mapping(lazy, node.right.data)
        node.right.key = self.mapping(lazy, node.right.key)
        node.right.lazy = self.composition(lazy, node.right.lazy)
      node.lazy = self.id

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
        node.data = node.key
      else:
        node.size = 1 + node.right.size
        node.data = self.op(node.key, node.right.data)
    else:
      if node.right is None:
        node.size = 1 + node.left.size
        node.data = self.op(node.left.data, node.key)
      else:
        node.size = 1 + node.left.size + node.right.size
        node.data = self.op(self.op(node.left.data, node.key), node.right.data)

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
    self._propagate(u)
    if u.balance() >= self.BETA:
      assert u.left
      self._propagate(u.left)
      node.right = self._rotate_right(u)
    u = self._rotate_left(node)
    return u

  def _balance_right(self, node: Node) -> Node:
    assert node.left
    node.left = node.left
    u = node.left
    self._propagate(u)
    if u.balance() <= 1 - self.BETA:
      assert u.right
      self._propagate(u.right)
      node.left = self._rotate_left(u)
    u = self._rotate_right(node)
    return u

  def _kth_elm(self, k: int) -> T:
    if k < 0:
      k += len(self)
    node = self.root
    while True:
      assert node
      self._propagate(node)
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      elif t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left

  def _merge_with_root(self, l: Optional[Node], root: Node, r: Optional[Node]) -> Node:
    ls = l.size if l else 0
    rs = r.size if r else 0
    diff = (ls+1) / (ls+rs+2)
    if diff > 1-self.ALPHA:
      assert l
      self._propagate(l)
      l.right = self._merge_with_root(l.right, root, r)
      self._update(l)
      if not (self.ALPHA <= l.balance() <= 1-self.ALPHA):
        return self._balance_left(l)
      return l
    if diff < self.ALPHA:
      assert r
      self._propagate(r)
      r.left = self._merge_with_root(l, root, r.left)
      self._update(r)
      if not (self.ALPHA <= r.balance() <= 1-self.ALPHA):
        return self._balance_right(r)
      return r
    root.left = l
    root.right = r
    self._update(root)
    return root

  def _merge_node(self, l: Optional[Node], r: Optional[Node]) -> Optional[Node]:
    if l is None and r is None:
      return None
    if l is None:
      return r
    if r is None:
      return l
    l, root = self._pop_right(l)
    return self._merge_with_root(l, root, r)

  def merge(self, other: 'LazyWBTree') -> 'LazyWBTree':
    root = self._merge_node(self.root, other.root)
    return self._new(root)

  def _pop_right(self, node: Node) -> Tuple[Optional[Node], Node]:
    path = []
    self._propagate(node)
    mx = node
    while node.right is not None:
      path.append(node)
      node = node.right
      mx = node
      self._propagate(node)
    path.append(node.left)
    for _ in range(len(path)-1):
      node = path.pop()
      if node is None:
        path[-1].right = None
        self._update(path[-1])
        continue
      b = node.balance()
      if self.ALPHA <= b <= 1-self.ALPHA:
        path[-1].right = node
      elif b > 1-self.ALPHA:
        path[-1].right = self._balance_right(node)
      else:
        path[-1].right = self._balance_left(node)
      self._update(path[-1])
    if path[0] is not None:
      b = path[0].balance()
      if b > 1-self.ALPHA:
        path[0] = self._balance_right(path[0])
      elif b < self.ALPHA:
        path[0] = self._balance_left(path[0])
    mx.left = None
    self._update(mx)
    return path[0], mx

  def _split_node(self, node: Optional[Node], k: int) -> Tuple[Optional[Node], Optional[Node]]:
    if node is None:
      return None, None
    self._propagate(node)
    tmp = k if node.left is None else k-node.left.size
    if tmp == 0:
      return node.left, self._merge_with_root(None, node, node.right)
    elif tmp < 0:
      l, r = self._split_node(node.left, k)
      return l, self._merge_with_root(r, node, node.right)
    else:
      l, r = self._split_node(node.right, tmp-1)
      return self._merge_with_root(node.left, node, l), r

  def split(self, k: int) -> Tuple['LazyWBTree', 'LazyWBTree']:
    l, r = self._split_node(self.root, k)
    return self._new(l), self._new(r)

  def _new(self, root: Optional['Node']) -> 'LazyWBTree':
    return LazyWBTree([], self.op, self.mapping, self.composition, self.e, self.id, root)

  def apply(self, l: int, r: int, f: F) -> None:
    if l >= r:
      return
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    s.key = self.mapping(f, s.key)
    s.data = self.mapping(f, s.data)
    s.lazy = self.composition(f, s.lazy)
    self.root = self._merge_node(self._merge_node(u, s), t)

  def prod(self, l: int, r) -> T:
    if l >= r: return self.e
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    res = s.data
    self.root = self._merge_node(self._merge_node(u, s), t)
    return res

  def insert(self, k: int, key: T) -> None:
    s, t = self._split_node(self.root, k)
    self.root = self._merge_with_root(s, LazyWBTree.Node(key, self.id), t)

  def pop(self, k: int) -> T:
    s, t = self._split_node(self.root, k+1)
    assert s
    s, tmp = self._pop_right(s)
    self.root = self._merge_node(s, t)
    return tmp.key

  def reverse(self, l: int, r: int) -> None:
    if l >= r:
      return 
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    s.rev ^= 1
    self.root = self._merge_node(self._merge_node(u, s), t)

  def tolist(self) -> List[T]:
    node = self.root
    stack = []
    a = []
    while stack or node:
      if node:
        self._propagate(node)
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        a.append(node.key)
        node = node.right
    return a

  def __getitem__(self, k: int) -> T:
    return self._kth_elm(k)

  def __setitem__(self, k, key: T):
    if k < 0: k += self.__len__()
    node = self.root
    path = []
    while True:
      self._propagate(node)
      path.append(node)
      t = 0 if node.left is None else node.left.size
      if t == k:
        node.key = key
        break
      if t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left
    while path:
      self._update(path.pop())

  def __len__(self):
    return 0 if self.root is None else self.root.size

  def __str__(self):
    return '[' + ', '.join(map(str, self.tolist())) + ']'

  def __repr__(self):
    return f'LazyWBTree({self})'

