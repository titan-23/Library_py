# from titan_pylib.data_structures.rbst.lazy_rbst import LazyRBST
from typing import Generic, List, TypeVar, Tuple, Callable, Iterable, Optional
T = TypeVar('T')
F = TypeVar('F')

class LazyRBST(Generic[T, F]):

  class Random():

    x: int = 2463534242

    @classmethod
    def random32(cls) -> int:
      cls.x ^= cls.x << 13 & 0xFFFFFFFF
      cls.x ^= cls.x >> 17
      cls.x ^= cls.x << 5 & 0xFFFFFFFF
      return cls.x & 0xFFFFFFFF

  class Node():

    def __init__(self, key: T, id: F):
      self.key: T = key
      self.data: T = key
      self.lazy: F = id
      self.left: Optional[LazyRBST.Node] = None
      self.right: Optional[LazyRBST.Node] = None
      self.size: int = 1
      self.rev: int = 0

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
               _root: Optional[Node]=None,
               ):
    self.root = _root
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id = id
    if a:
      self.build(a)

  def build(self, a: Iterable[T]) -> None:
    Node = LazyRBST.Node
    def rec(l: int, r: int):
      mid = (l + r) >> 1
      node = Node(a[mid], id)
      if l != mid:
        node.left = rec(l, mid)
      if mid+1 != r:
        node.right = rec(mid+1, r)
      self._update(node)
      return node
    a = list(a)
    if not a: return
    id = self.id
    self.root = rec(0, len(a))

  def _propagate(self, node: Node) -> None:
    if node.rev:
      node.left, node.right = node.right, node.left
      if node.left:
        node.left.rev ^= 1
      if node.right:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy != self.id:
      lazy = node.lazy
      if node.left:
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.lazy = lazy if node.left.lazy == self.id else self.composition(lazy, node.left.lazy)
      if node.right:
        node.right.key = self.mapping(lazy, node.right.key)
        node.right.data = self.mapping(lazy, node.right.data)
        node.right.lazy = lazy if node.right.lazy == self.id else self.composition(lazy, node.right.lazy)
      node.lazy = self.id

  def _update(self, node: Node) -> None:
    node.size = 1
    node.data = node.key
    if node.left:
      node.size += node.left.size
      node.data = self.op(node.left.data, node.key)
    if node.right:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)

  def _update_lr(self, l: Node, r: Node):
    l.size += r.size
    l.data = self.op(l.data, r.data)

  def _merge_node(self, l: Optional[Node], r: Optional[Node]) -> Optional[Node]:
    root = None
    r_root = None
    d = -1
    rand = LazyRBST.Random.random32
    while l and r:
      nd = rand() % (l.size + r.size) < l.size
      node = l if nd else r
      self._propagate(node)
      if not root:
        r_root = node
      elif d == 0:
        root.left = node
      else:
        root.right = node
      root = node
      d = nd
      if d:
        self._update_lr(l, r)
        l = l.right
      else:
        self._update_lr(r, l)
        r = r.left
    if not root:
      return l if l else r
    if d == 0:
      root.left = l if l else r
    else:
      root.right = l if l else r
    return r_root

  def merge(self, other: 'LazyRBST') -> None:
    self.root = self._merge_node(self.root, other.root)

  def _split_node(self, node: Optional[Node], k: int) -> Tuple[Optional[Node], Optional[Node]]:
    left_path, right_path = [], []
    while node:
      self._propagate(node)
      s = k if node.left is None else k-node.left.size
      if s <= 0:
        right_path.append(node)
        node = node.left
      else:
        k = s - 1
        left_path.append(node)
        node = node.right
    l, r = None, None
    while left_path:
      node = left_path.pop()
      l, node.right = node, l
      self._update(l)
    while right_path:
      node = right_path.pop()
      r, node.left = node, r
      self._update(r)
    return l, r

  def split(self, k: int) -> Tuple['LazyRBST', 'LazyRBST']:
    left, right = self._split_node(self.root, k)
    return (
        LazyRBST([], self.op, self.mapping, self.composition, self.e, self.id, _root=left),
        LazyRBST([], self.op, self.mapping, self.composition, self.e, self.id, _root=right)
    )

  def apply(self, l: int, r: int, f) -> None:
    if l >= r: return
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    s.key = self.mapping(f, s.key)
    s.data = self.mapping(f, s.data)
    s.lazy = self.composition(f, s.lazy)
    self.root = self._merge_node(self._merge_node(u, s), t)

  def prod(self, l: int, r: int):
    if l >= r: return self.e
    s, t = self._split_node(self.root, r)
    u, s = self._split_node(s, l)
    assert s
    res = s.data
    self.root = self._merge_node(self._merge_node(u, s), t)
    return res

  def insert(self, k: int, key: T) -> None:
    s, t = self._split_node(self.root, k)
    self.root = self._merge_node(self._merge_node(s, LazyRBST.Node(key, self.id)), t)

  def pop(self, k: int) -> T:
    s, t = self._split_node(self.root, k+1)
    assert s
    s, tmp = self._split_node(s, s.size-1)
    res = tmp.key
    self.root = self._merge_node(s, t)
    return res

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
    stack, res = [], []
    while stack or node:
      if node:
        self._propagate(node)
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        res.append(node.key)
        node = node.right
    return res

  def __getitem__(self, k: int) -> T:
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

  def __setitem__(self, k: int, key: T):
    if k < 0:
      k += len(self)
    node = self.root
    path = []
    while True:
      self._propagate(node)
      path.append(node)
      t = 0 if node.left is None else node.left.size
      if t == k:
        node.key = key
        break
      elif t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left
    while path:
      self._update(path.pop())

  def __len__(self):
    return 0 if self.root is None else self.root.size

  def __str__(self):
    return str(self.tolist())

  __repr__ = __str__


