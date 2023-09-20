raise NotImplementedError

# pop_right で回転をサボると速くなる

from typing import Generic, Iterable, Optional, TypeVar, Callable, List, Tuple
T = TypeVar('T')
F = TypeVar('F')

class PersistentLazyWeightBalancedTree(Generic[T, F]):

  class Node:

    def __init__(self,
                 key: T,
                 lazy: F,
                 copy_t: Callable[[T], T],
                 copy_f: Callable[[F], F],
                 ):
      self.key: T = key
      self.data: T = key
      self.left: Optional[PersistentLazyWeightBalancedTree.Node] = None
      self.right: Optional[PersistentLazyWeightBalancedTree.Node] = None
      self.lazy: F = lazy
      self.rev: int = 0
      self.size: int = 1
      self.copy_t: Callable[[T], T] = copy_t
      self.copy_f: Callable[[F], F] = copy_f

    def copy(self):
      node = PersistentLazyWeightBalancedTree.Node(self.copy_t(self.key), self.copy_f(self.lazy), self.copy_t, self.copy_f)
      node.data = self.copy_t(self.data)
      node.left = self.left
      node.right = self.right
      node.rev = self.rev
      node.size = self.size
      return node

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key={self.key}, size={self.size}, data={self.data}, lazy={self.lazy}, rev={self.rev}\n'
      return f'key={self.key}, size={self.size}, data={self.data}, lazy={self.lazy}, rev={self.rev},\n left:{self.left},\n right:{self.right}\n'

    __repr__ = __str__

  def __init__(self, a: Iterable[T],
               op: Callable[[T, T], T],
               mapping: Callable[[F, T], T],
               composition: Callable[[F, F], F],
               e: T,
               id: F,
               copy_t: Callable[[T], T],
               copy_f: Callable[[F], F],
               _root=None
               ) -> None:
    self.root: Optional[PersistentLazyWeightBalancedTree.Node] = _root
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
    Node = PersistentLazyWeightBalancedTree.Node
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
      l = node.left.copy() if node.left else None
      r = node.right.copy() if node.right else None
      node.left, node.right = r, l
      if node.left is not None:
        node.left.rev ^= 1
      if node.right is not None:
        node.right.rev ^= 1
      node.rev = 0
    if node.lazy != self.id:
      lazy = node.lazy
      if node.left:
        node.left = node.left.copy()
        node.left.data = self.mapping(lazy, node.left.data)
        node.left.key = self.mapping(lazy, node.left.key)
        node.left.lazy = self.composition(lazy, node.left.lazy)
      if node.right:
        node.right = node.right.copy()
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

  def _get_balance(self, node: Node) -> int:
    # 左がでかい -> balance がでかい
    l = node.left.size if node.left else 0
    r = node.right.size if node.right else 0
    return (l+1) / (r+1)

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
    if self._get_balance(u) > 2:
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
    if self._get_balance(u) < 1/2:
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
    diff = (ls+1) / (rs+1)
    if diff > 3:
      assert l
      l = l.copy()
      self._propagate(l)
      l.right = self._merge_with_root(l.right, root, r)
      self._update(l)
      if self._get_balance(l) < 1/3:
        return self._balance_left(l)
      return l
    if diff < 1/3:
      assert r
      r = r.copy()
      self._propagate(r)
      r.left = self._merge_with_root(l, root, r.left)
      self._update(r)
      if self._get_balance(r) > 3:
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

  def merge(self, other: 'PersistentLazyWeightBalancedTree') -> 'PersistentLazyWeightBalancedTree':
    root = self._merge_node(self.root, other.root)
    return self._new(root)

  def _pop_right(self, node: Node) -> Tuple[Node, Node]:
    path = []
    node = node.copy()
    self._propagate(node)
    mx = node
    while node.right:
      path.append(node)
      node = node.right.copy()
      self._propagate(node)
      mx = node
    path.append(node.left.copy() if node.left else None)
    while len(path) > 1:
      path[-1].right = path.pop()
      self._update(path[-1])
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

  def split(self, k: int) -> Tuple['PersistentLazyWeightBalancedTree', 'PersistentLazyWeightBalancedTree']:
    l, r = self._split_node(self.root, k)
    return self._new(l), self._new(r)

  def _new(self, root: Optional['PersistentLazyWeightBalancedTree.Node']) -> 'PersistentLazyWeightBalancedTree':
    return PersistentLazyWeightBalancedTree([], self.op, self.mapping, self.composition, self.e, self.id, self.copy_t, self.copy_f, root)

  def apply(self, l: int, r: int, f: F) -> 'PersistentLazyWeightBalancedTree':
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
    root = self._merge_node(self._merge_node(u, s), t)
    return res

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
    return f'PersistentLazyWeightBalancedTree({self})'

import os
from __pypy__.builders import StringBuilder

class FastO():

  sb = StringBuilder()

  @classmethod
  def write(cls, *args, sep: str=' ', end: str='\n', flush: bool=False) -> None:
    append = cls.sb.append
    for i in range(len(args)-1):
      append(str(args[i]))
      append(sep)
    if args:
      append(str(args[-1]))
    append(end)
    if flush:
      cls.flush()

  @classmethod
  def flush(cls) -> None:
    os.write(1, cls.sb.build().encode())
    cls.sb = StringBuilder()

write = FastO.write
flush = FastO.flush

import sys
input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

op = lambda s, t: None
mapping = lambda f, s: None
composition = lambda f, g: None
e = None
id = None
copy_t = lambda s: s
copy_f = lambda f: f

m = int(input())
s = input()
wb = PersistentLazyWeightBalancedTree(s, op, mapping, composition, e, id, copy_t, copy_f)
n = int(input())
for _ in range(n):
  a, b, c = map(int, input().split())
  u, _ = wb.split(b)
  _, ab = u.split(a)
  y, z = wb.split(c)
  y = y.merge(ab)
  wb = y.merge(z)
  wb, _ = wb.split(m)
ans = wb.tolist()
print(''.join(ans))
