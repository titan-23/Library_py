# from Library_py.DataStructures.UnionFind.PersistentUnionFind import PersistentUnionFind
# from Library_py.DataStructures.Array.PersistentArray import PersistentArray
from typing import Dict, List, Sequence, Iterable, TypeVar, Generic, Optional, Union
T = TypeVar('T')

class PersistentArray(Generic[T]):

  class Node():

    def __init__(self, key: T):
      self.key: T = key
      self.size: int = 1
      self.left: Optional[PersistentArray.Node] = None
      self.right: Optional[PersistentArray.Node] = None

    def copy(self) -> 'PersistentArray.Node':
      node = PersistentArray.Node(self.key)
      node.size = self.size
      node.left = self.left
      node.right = self.right
      return node

  def __init__(self, a: Iterable[T], init_t: int=0, max_t: int=-1):
    root = self._build(a)
    if max_t == -1:
      self.a: Union[Dict[int, Optional[PersistentArray.Node]], List[Optional[PersistentArray.Node]]] = {init_t: root}
    else:
      assert max_t >= 0 and init_t >= 0
      b: List[Optional[PersistentArray.Node]] = [None] * (max_t+1)
      self.a: Union[Dict[int, Optional[PersistentArray.Node]], List[Optional[PersistentArray.Node]]] = b
      self.a[init_t] = root

  def _build(self, a: Iterable[T]) -> Optional[Node]:
    Node = PersistentArray.Node
    if not isinstance(a, Sequence):
      a = list(a)
    def rec(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = rec(l, mid)
        node.size += node.left.size
      if mid + 1 != r:
        node.right = rec(mid+1, r)
        node.size += node.right.size
      return node
    if not a:
      return None
    root = rec(0, len(a))
    return root

  def set(self, k: int, v: T, pre_t: int, new_t: int) -> None:
    node = self.a[pre_t]
    if node is None:
      self.a[new_t] = None
      return
    new_node = node.copy()
    self.a[new_t] = new_node
    while node:
      t = 0 if node.left is None else node.left.size
      if t == k:
        new_node.key = v
        return
      if t < k:
        k -= t + 1
        assert node.right
        new_node.right = node.right.copy()
        new_node = new_node.right
        node = node.right
      else:
        assert node.left
        new_node.left = node.left.copy()
        new_node = new_node.left
        node = node.left

  def get(self, k: int, t: int) -> T:
    node = self.a[t]
    while node:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      if t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left
    assert False, f'IndexError'

  def copy(self, pre_t: int, new_t: int) -> None:
    node = self.a[pre_t]
    if node is None:
      self.a[new_t] = None
      return
    new_node = node.copy()
    self.a[new_t] = new_node

  def tolist(self, t: int) -> List[T]:
    node = self.a[t]
    stack = []
    a: List[T] = []
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        a.append(node.key)
        node = node.right
    return a


class PersistentUnionFind():

  def __init__(self, n: int, init_t: int=0, max_t: int=-1):
    self._n: int = n
    self._parents: PersistentArray[int] = PersistentArray([-1]*n, init_t=init_t, max_t=max_t)

  def root(self, x: int, t: int) -> int:
    stack = []
    while True:
      p = self._parents.get(x, t)
      if p < 0:
        break
      stack.append(x)
      x = p
    while stack:
      v = stack.pop()
      self._parents.set(v, x, t, t)
    return x

  def unite(self, x: int, y: int, pre_t: int, new_t: int) -> bool:
    x = self.root(x, pre_t)
    y = self.root(y, pre_t)
    if x == y:
      self._parents.copy(pre_t, new_t)
      return False
    px, py = self._parents.get(x, pre_t), self._parents.get(y, pre_t)
    if px > py:
      x, y = y, x
    self._parents.set(x, px + py, pre_t, new_t)
    self._parents.set(y, x, pre_t, new_t)
    return True

  def size(self, x: int, t: int) -> int:
    return -self._parents.get(self.root(x, t), t)

  def same(self, x: int, y: int, t: int) -> bool:
    return self.root(x, t) == self.root(y, t)


