from typing import Generic, Iterable, Optional, TypeVar, Callable, List, Tuple
T = TypeVar('T')
F = TypeVar('F')

class PersistentLazyAVLTree(Generic[T, F]):

  class Node():

    def __init__(self,
                 key: T,
                 lazy: F,
                 copy_t: Callable[[T], T],
                 copy_f: Callable[[F], F],
                 ) -> None:
      self.key: T = key
      self.data: T = key
      self.left: Optional[PersistentLazyAVLTree.Node] = None
      self.right: Optional[PersistentLazyAVLTree.Node] = None
      self.lazy: F = lazy
      self.rev: int = 0
      self.height: int = 1
      self.size: int = 1
      self.copy_t: Callable[[T], T] = copy_t
      self.copy_f: Callable[[F], F] = copy_f

    def copy(self) -> 'PersistentLazyAVLTree.Node':
      node = PersistentLazyAVLTree.Node(self.copy_t(self.key), self.copy_f(self.lazy), self.copy_t, self.copy_f)
      node.data = self.copy_t(self.data)
      node.left = self.left
      node.right = self.right
      node.rev = self.rev
      node.height = self.height
      node.size = self.size
      return node

    def balance(self) -> int:
      return (0 if self.right is None else -self.right.height) if self.left is None else (self.left.height if self.right is None else self.left.height-self.right.height)

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key={self.key}, height={self.height}, size={self.size}, data={self.data}, lazy={self.lazy}, rev={self.rev}\n'
      return f'key={self.key}, height={self.height}, size={self.size}, data={self.data}, lazy={self.lazy}, rev={self.rev},\n left:{self.left},\n right:{self.right}\n'

    __repr__ = __str__


  def __init__(self, a: Iterable[T],
               op: Callable[[T, T], T],
               mapping: Callable[[F, T], T],
               composition: Callable[[F, F], F],
               e: T,
               id: F,
               copy_t: Callable[[T], T] = lambda t: t,
               copy_f: Callable[[F], F] = lambda f: f,
               _root=None
               ) -> None:
    self.root: Optional[PersistentLazyAVLTree.Node] = _root
    self.op: Callable[[T, T], T] = op
    self.mapping: Callable[[F, T], T] = mapping
    self.composition: Callable[[F, F], F] = composition
    self.e: T = e
    self.id: F = id
    self.copy_t: Callable[[T], T] = copy_t
    self.copy_f: Callable[[F], F] = copy_f
    a = list(a)
    if a:
      self._build(list(a))

  def _build(self, a: List[T]) -> None:
    Node = PersistentLazyAVLTree.Node
    def build(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid], id, copy_t, copy_f)
      if l != mid:
        node.left = build(l, mid)
      if mid+1 != r:
        node.right = build(mid+1, r)
      self._update(node)
      return node
    id = self.id
    copy_t = self.copy_t
    copy_f = self.copy_f
    self.root = build(0, len(a))

  def _propagate(self, node: Node) -> None:
    if node.rev:
      node.rev = 0
      l = node.left.copy() if node.left else None
      r = node.right.copy() if node.right else None
      node.left, node.right = r, l
      if l:
        l.rev ^= 1
      if r:
        r.rev ^= 1
    if node.lazy != self.id:
      lazy = node.lazy
      node.lazy = self.id
      if node.left:
        l = node.left.copy()
        l.data = self.mapping(lazy, l.data)
        l.key = self.mapping(lazy, l.key)
        l.lazy = self.composition(lazy, l.lazy)
        node.left = l
      if node.right:
        r = node.right.copy()
        r.data = self.mapping(lazy, r.data)
        r.key = self.mapping(lazy, r.key)
        r.lazy = self.composition(lazy, r.lazy)
        node.right = r

  def _update(self, node: Node) -> None:
    if node.left:
      if node.right:
        node.size = 1 + node.left.size + node.right.size
        node.data = self.op(self.op(node.left.data, node.key), node.right.data)
        node.height = node.left.height+1 if node.left.height > node.right.height else node.right.height+1
      else:
        node.size = 1 + node.left.size
        node.data = self.op(node.left.data, node.key)
        node.height = node.left.height+1
    else:
      if node.right:
        node.size = 1 + node.right.size
        node.data = self.op(node.key, node.right.data)
        node.height = node.right.height+1
      else:
        node.size = 1
        node.data = node.key
        node.height = 1

  def _rotate_right(self, node: Node) -> Node:
    assert node.left
    u = node.left.copy()
    node.left = u.right
    u.right = node
    self._update(node)
    self._update(u)
    return u

  def _rotate_left(self, node: Node) -> Node:
    assert node.right
    u = node.right.copy()
    node.right = u.left
    u.left = node
    self._update(node)
    self._update(u)
    return u

  def _balance_left(self, node: Node) -> Node:
    assert node.right
    node.right = node.right.copy()
    u = node.right
    self._propagate(u)
    if u.balance() == 1:
      assert u.left
      self._propagate(u.left)
      node.right = self._rotate_right(u)
    u = self._rotate_left(node)
    return u

  def _balance_right(self, node: Node) -> Node:
    assert node.left
    node.left = node.left.copy()
    u = node.left
    self._propagate(u)
    if u.balance() == -1:
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
    diff = 0
    if l:
      diff += l.height
    if r:
      diff -= r.height
    if diff > 1:
      assert l
      l = l.copy()
      self._propagate(l)
      l.right = self._merge_with_root(l.right, root, r)
      self._update(l)
      if l.balance() == -2:
        return self._balance_left(l)
      return l
    if diff < -1:
      assert r
      r = r.copy()
      self._propagate(r)
      r.left = self._merge_with_root(l, root, r.left)
      self._update(r)
      if r.balance() == 2:
        return self._balance_right(r)
      return r
    root = root.copy()
    root.left = l
    root.right = r
    self._update(root)
    return root

  def _merge_node(self, l: Optional[Node], r: Optional[Node]) -> Optional[Node]:
    if l is None and r is None:
      return None
    if l is None:
      assert r
      return r.copy()
    if r is None:
      return l.copy()
    l = l.copy()
    r = r.copy()
    l, root = self._pop_right(l)
    return self._merge_with_root(l, root, r)

  def merge(self, other: 'PersistentLazyAVLTree') -> 'PersistentLazyAVLTree':
    root = self._merge_node(self.root, other.root)
    return self._new(root)

  def _pop_right(self, node: Node) -> Tuple[Node, Node]:
    path = []
    node = node.copy()
    self._propagate(node)
    mx = node
    while node.right is not None:
      path.append(node)
      node = node.right.copy()
      mx = node
      self._propagate(node)
    path.append(node.left.copy() if node.left else None)
    for _ in range(len(path)-1):
      node = path.pop()
      if node is None:
        path[-1].right = None
        self._update(path[-1])
        continue
      b = node.balance()
      if b == 2:
        path[-1].right = self._balance_right(node)
      elif b == -2:
        path[-1].right = self._balance_left(node)
      else:
        path[-1].right = node
      self._update(path[-1])
    if path[0] is not None:
      b = path[0].balance()
      if b == 2:
        path[0] = self._balance_right(path[0])
      elif b == -2:
        path[0] = self._balance_left(path[0])
    mx.left = None
    self._update(mx)
    return path[0], mx

  def _split_node(self, node: Optional[Node], k: int) -> Tuple[Optional[Node], Optional[Node]]:
    if node is None:
      return None, None
    self._propagate(node)
    tmp = k if node.left is None else k-node.left.size
    l, r = None, None
    if tmp == 0:
      return node.left, self._merge_with_root(None, node, node.right)
    elif tmp < 0:
      l, r = self._split_node(node.left, k)
      return l, self._merge_with_root(r, node, node.right)
    else:
      l, r = self._split_node(node.right, tmp-1)
      return self._merge_with_root(node.left, node, l), r

  def split(self, k: int) -> Tuple['PersistentLazyAVLTree', 'PersistentLazyAVLTree']:
    l, r = self._split_node(self.root, k)
    return self._new(l), self._new(r)

  def _new(self, root: Optional['PersistentLazyAVLTree.Node']) -> 'PersistentLazyAVLTree':
    return PersistentLazyAVLTree([], self.op, self.mapping, self.composition, self.e, self.id, self.copy_t, self.copy_f, root)

  def apply(self, l: int, r: int, f: F) -> 'PersistentLazyAVLTree':
    if l >= r:
      return self._new(self.root.copy() if self.root else None)
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    s.key = self.mapping(f, s.key)
    s.data = self.mapping(f, s.data)
    s.lazy = self.composition(f, s.lazy)
    root = self._merge_node(self._merge_node(u, s), t)
    return self._new(root)

  def prod(self, l: int, r) -> T:
    if l >= r: return self.e
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    res = s.data
    self.root = self._merge_node(self._merge_node(u, s), t)
    return res

  def insert(self, k: int, key: T) -> 'PersistentLazyAVLTree':
    s, t = self._split_node(self.root, k)
    root = self._merge_with_root(s, PersistentLazyAVLTree.Node(key, self.id, self.copy_t, self.copy_f), t)
    return self._new(root)

  def pop(self, k: int) -> Tuple['PersistentLazyAVLTree', T]:
    s, t = self._split_node(self.root, k+1)
    assert s
    s, tmp = self._pop_right(s)
    root = self._merge_node(s, t)
    return self._new(root), tmp.key

  def reverse(self, l: int, r: int) -> 'PersistentLazyAVLTree':
    if l >= r:
      return self._new(self.root.copy() if self.root else None)
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    s.rev ^= 1
    root = self._merge_node(self._merge_node(u, s), t)
    return self._new(root)

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

  def __len__(self):
    return 0 if self.root is None else self.root.size

  def __str__(self):
    return '[' + ', '.join(map(str, self.tolist())) + ']'

  def __repr__(self):
    return f'PersistentLazyAVLTree({self})'


