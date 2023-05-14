from typing import Generic, Iterable, TypeVar, Optional, List, Sequence
T = TypeVar('T')

class TreapSet(Generic[T]):

  class Random():

    _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

    @classmethod
    def random(cls) -> int:
      t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
      cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
      cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
      return cls._w

  class Node():

    def __init__(self, key, priority: int=-1):
      self.key = key
      self.left: Optional['TreapSet.Node'] = None
      self.right: Optional['TreapSet.Node'] = None
      self.priority = TreapSet.Random.random() if priority == -1 else priority

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.priority}\n'
      return f'key:{self.key, self.priority},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]):
    self.root = None
    self._len = 0
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Sequence[T]) -> None:
    Node = TreapSet.Node
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid], rand[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      return node
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    self._len = len(a)
    rand = [TreapSet.Random.random() for _ in range(self._len)]
    rand.sort()
    self.root = sort(0, self._len)

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    node.left = u.right
    u.right = node
    return u

  def _rotate_R(self, node: Node) -> Node:
    u = node.right
    node.right = u.left
    u.left = node
    return u

  def add(self, key: T) -> bool:
    if not self.root:
      self.root = TreapSet.Node(key)
      self._len += 1
      return True
    node = self.root
    path = []
    di = 0
    while node:
      if key == node.key:
        return False
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    if di & 1:
      path[-1].left = TreapSet.Node(key)
    else:
      path[-1].right = TreapSet.Node(key)
    while path:
      new_node = None
      node = path.pop()
      if di & 1:
        if node.left.priority < node.priority:
          new_node = self._rotate_L(node)
      else:
        if node.right.priority < node.priority:
          new_node = self._rotate_R(node)
      di >>= 1
      if new_node:
        if path:
          if di & 1:
            path[-1].left = new_node
          else:
            path[-1].right = new_node
        else:
          self.root = new_node
    self._len += 1
    return True

  def discard(self, key: T) -> bool:
    node = self.root
    pnode = None
    while node:
      if key == node.key:
        break
      elif key < node.key:
        pnode = node
        node = node.left
      else:
        pnode = node
        node = node.right
    else:
      return False
    self._len -= 1
    while node.left and node.right:
      if node.left.priority < node.right.priority:
        if not pnode:
          pnode = self._rotate_L(node)
          self.root = pnode
          continue
        new_node = self._rotate_L(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      else:
        if not pnode:
          pnode = self._rotate_R(node)
          self.root = pnode
          continue
        new_node = self._rotate_R(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      pnode = new_node
    if not pnode:
      if node.left is None:
        self.root = node.right
      else:
        self.root = node.left
      return True
    if node.left is None:
      if node.key < pnode.key:
        pnode.left = node.right
      else:
        pnode.right = node.right
    else:
      if node.key < pnode.key:
        pnode.left = node.left
      else:
        pnode.right = node.left
    return True

  def le(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node:
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
    while node:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def ge(self, key: T) -> Optional[T]:
    res = None
    node = self.root
    while node:
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
    while node:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def tolist(self) -> List[T]:
    a = []
    if not self.root:
      return a
    def rec(node):
      if node.left:
        rec(node.left)  
      a.append(node.key)
      if node.right:
        rec(node.right)
    rec(self.root)
    return a

  def get_min(self) -> Optional[T]:
    node = self.root
    if not node:
      return None
    while node.left:
      node = node.left
    return node.key

  def get_max(self) -> Optional[T]:
    node = self.root
    if not node:
      return None
    while node.right:
      node = node.right
    return node.key

  def pop_min(self) -> T:
    assert self.root is not None
    node = self.root
    pnode = None
    while node.left:
      pnode = node
      node = node.left
    self._len -= 1
    res = node.key
    if not pnode:
      self.root = self.root.right
    else:
      pnode.left = node.right
    return res

  def pop_max(self) -> T:
    assert self.root is not None
    node = self.root
    pnode = None
    while node.right:
      pnode = node
      node = node.right
    self._len -= 1
    res = node.key
    if not pnode:
      self.root = self.root.left
    else:
      pnode.right = node.left
    return res

  def __getitem__(self, k: int) -> T:
    assert self._len > 0
    if k == -1 or k == self._len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    assert False, f'IndexError'

  def __contains__(self, key: T):
    node = self.root
    while node:
      if key == node.key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __len__(self):
    return self._len

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'TreapSet({self.tolist()})'

