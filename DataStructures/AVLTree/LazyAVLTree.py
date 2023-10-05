from typing import Generic, Iterable, TypeVar, Callable, List, Tuple
T = TypeVar('T')
F = TypeVar('F')

class Node:

  def __init__(self, key):
    self.key = key
    self.data = key
    self.left = None
    self.right = None
    self.lazy = None
    self.rev = 0
    self.height = 1
    self.size = 1

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.height, self.size, self.data, self.lazy, self.rev}\n'
    return f'key:{self.key, self.height, self.size, self.data, self.lazy, self.rev},\n left:{self.left},\n right:{self.right}\n'

class LazyAVLTree(Generic[T, F]):

  def __init__(self, a: Iterable[T]=[], op: Callable[[T, T], T]=lambda x,y:None, mapping: Callable[[F, T], T]=None, composition: Callable[[F, F], F]=None, e: T=None, id: F=None, node: Node=None) -> None:
    self.node = node
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id = id
    if a:
      self._build(list(a))

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      self._update(node)
      return node
    self.node = sort(0, len(a))

  def _propagate(self, node: Node) -> None:
    if node.rev:
      node.left, node.right = node.right, node.left
      if node.left is not None:
        node.left.rev ^= 1
      if node.right is not None:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy is not None:
      lazy = node.lazy
      if node.left is not None:
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.lazy = lazy if node.left.lazy is None else self.composition(lazy, node.left.lazy)
      if node.right is not None:
        node.right.data = self.mapping(lazy, node.right.data)
        node.right.key = self.mapping(lazy, node.right.key)
        node.right.lazy = lazy if node.right.lazy is None else self.composition(lazy, node.right.lazy)
      node.lazy = None

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
        node.data = node.key
        node.height = 1
      else:
        node.size = 1 + node.right.size
        node.data = self.op(node.key, node.right.data)
        node.height = node.right.height+1
    else:
      if node.right is None:
        node.size = 1 + node.left.size
        node.data = self.op(node.left.data, node.key)
        node.height = node.left.height+1
      else:
        node.size = 1 + node.left.size + node.right.size
        node.data = self.op(self.op(node.left.data, node.key), node.right.data)
        node.height = node.left.height+1 if node.left.height > node.right.height else node.right.height+1

  def _get_balance(self, node: Node) -> int:
    return (0 if node.right is None else -node.right.height) if node.left is None else (node.left.height if node.right is None else node.left.height-node.right.height)

  def _balance_left(self, node: Node) -> Node:
    self._propagate(node.left)
    if node.left.left is None or node.left.left.height+2 == node.left.height:
      u = node.left.right
      self._propagate(u)
      node.left.right = u.left
      u.left = node.left
      node.left = u.right
      u.right = node
      self._update(u.left)
    else:
      u = node.left
      node.left = u.right
      u.right = node
    self._update(u.right)
    self._update(u)
    return u

  def _balance_right(self, node: Node) -> Node:
    self._propagate(node.right)
    if node.right.right is None or node.right.right.height+2 == node.right.height:
      u = node.right.left
      self._propagate(u)
      node.right.left = u.right
      u.right = node.right
      node.right = u.left
      u.left = node
      self._update(u.right)
    else:
      u = node.right
      node.right = u.left
      u.left = node
    self._update(u.left)
    self._update(u)
    return u

  def _kth_elm(self, k: int) -> T:
    if k < 0: k += self.__len__()
    node = self.node
    while True:
      self._propagate(node)
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      elif t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left

  def _merge_with_root(self, l: Node, root: Node, r: Node) -> Node:
    diff = (0 if r is None else -r.height) if l is None else (l.height if r is None else l.height-r.height) 
    if diff > 1:
      self._propagate(l)
      l.right = self._merge_with_root(l.right, root, r)
      self._update(l)
      if -l.right.height if l.left is None else l.left.height-l.right.height == -2:
        return self._balance_right(l)
      return l
    elif diff < -1:
      self._propagate(r)
      r.left = self._merge_with_root(l, root, r.left)
      self._update(r)
      if r.left.height if r.right is None else r.left.height-r.right.height == 2:
        return self._balance_left(r)
      return r
    else:
      root.left = l
      root.right = r
      self._update(root)
      return root

  def _merge_node(self, l: Node, r: Node) -> Node:
    if l is None: return r
    if r is None: return l
    l, tmp = self._pop_max(l)
    return self._merge_with_root(l, tmp, r)

  def merge(self, other: "LazyAVLTree") -> None:
    self.node = self._merge_node(self.node, other.node)

  def _pop_max(self, node: Node) -> Tuple[Node, Node]:
    self._propagate(node)
    path = []
    mx = node
    while node.right is not None:
      path.append(node)
      mx = node.right
      node = node.right
      self._propagate(node)
    path.append(node.left)
    for _ in range(len(path)-1):
      node = path.pop()
      if node is None:
        path[-1].right = None
        self._update(path[-1])
        continue
      b = self._get_balance(node)
      path[-1].right = self._balance_left(node) if b == 2 else self._balance_right(node) if b == -2 else node
      self._update(path[-1])
    if path[0] is not None:
      b = self._get_balance(path[0])
      path[0] = self._balance_left(path[0]) if b == 2 else self._balance_right(path[0]) if b == -2 else path[0]
    mx.left = None
    self._update(mx)
    return path[0], mx

  def _split_node(self, node: Node, k: int) -> Tuple[Node, Node]:
    if node is None: return None, None
    self._propagate(node)
    tmp = k if node.left is None else k-node.left.size
    if tmp == 0:
      return node.left, self._merge_with_root(None, node, node.right)
    elif tmp < 0:
      s, t = self._split_node(node.left, k)
      return s, self._merge_with_root(t, node, node.right)
    else:
      s, t = self._split_node(node.right, tmp-1)
      return self._merge_with_root(node.left, node, s), t

  def split(self, k: int) -> Tuple["LazyAVLTree", "LazyAVLTree"]:
    l, r = self._split_node(self.node, k)
    return LazyAVLTree([], self.op, self.mapping, self.composition, self.e, self.id, l), LazyAVLTree([], self.op, self.mapping, self.composition, self.e, self.id, r)

  def insert(self, k: int, key: T) -> None:
    s, t = self._split_node(self.node, k)
    self.node = self._merge_with_root(s, Node(key), t)

  def pop(self, k: int) -> T:
    s, t = self._split_node(self.node, k+1)
    s, tmp = self._pop_max(s)
    self.node = self._merge_node(s, t)
    return tmp.key

  def apply(self, l: int, r: int, f: F) -> None:
    if l >= r: return
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    s.key = self.mapping(f, s.key)
    s.data = self.mapping(f, s.data)
    s.lazy = f if s.lazy is None else self.composition(f, s.lazy)
    self.node = self._merge_node(self._merge_node(r, s), t)

  def all_apply(self, f: F) -> None:
    if self.node is None: return
    self.node.key = self.mapping(f, self.node.key)
    self.node.data = self.mapping(f, self.node.data)
    self.node.lazy = f if self.node.lazy is None else self.composition(f, self.node.lazy)

  def reverse(self, l: int, r: int) -> None:
    if l >= r: return
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    s.rev ^= 1
    self.node = self._merge_node(self._merge_node(r, s), t)

  def all_reverse(self) -> None:
    if self.node is None: return
    self.node.rev ^= 1

  def prod(self, l: int, r: int) -> T:
    if l >= r: return self.e
    s, t = self._split_node(self.node, r)
    r, s = self._split_node(s, l)
    res = s.data
    self.node = self._merge_node(self._merge_node(r, s), t)
    return res

  def all_prod(self) -> T:
    return self.e if self.node is None else self.node.data

  def clear(self) -> None:
    self.node = None

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    def rec(node):
      self._propagate(node)
      if node.left is not None:
        rec(node.left)
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == len(self):
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(len(self)):
      yield self.__getitem__(-i-1)

  def __bool__(self):
    return self.node is not None

  def __getitem__(self, k: int) -> T:
    return self._kth_elm(k)

  def __setitem__(self, k, key: T):
    if k < 0: k += self.__len__()
    node = self.node
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
    for p in path:
      self._update(p)

  def __str__(self):
    return '[' + ', '.join(map(str, self.tolist())) + ']'

  def __repr__(self):
    return 'LazyAVLTree(' + str(self) + ')'

