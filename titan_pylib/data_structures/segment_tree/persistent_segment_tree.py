from typing import Generic, Iterable, Optional, Union, TypeVar, Callable, List, Tuple, Final
T = TypeVar('T')

class PersistentSegmentTree(Generic[T]):

  class Node():

    def __init__(self, key: T) -> None:
      self.key: T = key
      self.data: T = key
      self.left: Optional[PersistentSegmentTree.Node] = None
      self.right: Optional[PersistentSegmentTree.Node] = None
      self.size: int = 1

    def copy(self) -> 'PersistentSegmentTree.Node':
      node = PersistentSegmentTree.Node(self.key)
      node.data = self.data
      node.left = self.left
      node.right = self.right
      node.size = self.size
      return node

  def __init__(self,
               a: Iterable[T],
               op: Callable[[T, T], T],
               e: T,
               __root: Optional[Node]=None
               ) -> None:
    self.root: Optional[PersistentSegmentTree.Node] = __root
    self.op: Callable[[T, T], T] = op
    self.e: T = e
    if __root is not None:
      return
    a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    Node = PersistentSegmentTree.Node
    def build(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = build(l, mid)
      if mid+1 != r:
        node.right = build(mid+1, r)
      self._update(node)
      return node
    self.root = build(0, len(a))

  def _update(self, node: Node) -> None:
    node.size = 1
    node.data = node.key
    if node.left:
      node.size += node.left.size
      node.data = self.op(node.left.data, node.data)
    if node.right:
      node.size += node.right.size
      node.data = self.op(node.data, node.right.data)

  def prod(self, l: int, r) -> T:
    if l >= r or (not self.root): return self.e
    def dfs(node: PersistentSegmentTree.Node, left: int, right: int) -> T:
      if right <= l or r <= left:
        return self.e
      if l <= left and right < r:
        return node.data
      lsize = node.left.size if node.left else 0
      res = self.e
      if node.left:
        res = dfs(node.left, left, left+lsize)
      if l <= left+lsize < r:
        res = self.op(res, node.key)
      if node.right:
        res = self.op(res, dfs(node.right, left+lsize+1, right))
      return res
    return dfs(self.root, 0, len(self))

  def tolist(self) -> List[T]:
    node = self.root
    stack = []
    a = []
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        a.append(node.key)
        node = node.right
    return a

  def _new(self, root: Optional['Node']) -> 'PersistentSegmentTree[T]':
    return PersistentSegmentTree([], self.op, self.e, root)

  def copy(self) -> 'PersistentSegmentTree[T]':
    root = self.root.copy() if self.root else None
    return self._new(root)

  def set(self, k: int, v: T) -> 'PersistentSegmentTree[T]':
    if k < 0:
      k += len(self)
    node = self.root.copy()
    root = node
    pnode = None
    d = 0
    path = [node]
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        node = node.copy()
        node.key = v
        path.append(node)
        if pnode:
          if d:
            pnode.left = node
          else:
            pnode.right = node
        else:
          root = node
        while path:
          self._update(path.pop())
        return self._new(root)
      pnode = node
      if t < k:
        k -= t + 1
        d = 0
        node = node.right.copy()
        pnode.right = node
      else:
        d = 1
        node = node.left.copy()
        pnode.left = node
      path.append(node)

  def __getitem__(self, k: int) -> T:
    if k < 0:
      k += len(self)
    node = self.root
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      if t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left

  def __len__(self):
    return 0 if self.root is None else self.root.size

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'

