from typing import List, Iterable, TypeVar, Generic, Optional
T = TypeVar('T')
_titan23_PersistentArray32_BIT = 4
_titan23_PersistentArray32_M = 1 << _titan23_PersistentArray32_BIT
_titan23_PersistentArray32_MSK = _titan23_PersistentArray32_M - 1

class PersistentArray32(Generic[T]):

  class Node():

    def __init__(self, key: T, child=None):
      self.key: T = key
      self.child: List[Optional[PersistentArray32.Node]] = [None] * _titan23_PersistentArray32_M if child is None else child

    def copy(self) -> 'PersistentArray32.Node':
      return PersistentArray32.Node(self.key, None if self.child is None else self.child[:])

  def __init__(self, a: Iterable[T]=[], _root: Optional['PersistentArray32.Node']=None):
    self.root = self._build(a) if _root is None else _root

  def _build(self, a: Iterable[T]) -> Optional['PersistentArray32.Node']:
    Node = PersistentArray32.Node
    a = list(a)
    self.n = len(a)
    n = len(a)
    beki = [_titan23_PersistentArray32_M**i for i in range(n.bit_length()+1)]
    def dfs(indx: int, dep: int) -> Node:
      if indx >= n: return None
      node = Node(a[indx]) if indx+(1+1)*beki[dep] < n else Node(a[indx], None)
      for i in range(_titan23_PersistentArray32_M):
        node.child[(i+1)&_titan23_PersistentArray32_MSK] = dfs(indx+(i+1)*beki[dep], dep+1)
      return node
    root = dfs(0, 0)
    return root

  def _new(self, root: Optional['PersistentArray32.Node']) -> 'PersistentArray32[T]':
    return PersistentArray32(_root=root)

  def set(self, k: int, v: T) -> 'PersistentArray32[T]':
    node = self.root
    if node is None:
      return self._new(None)
    new_node = node.copy()
    res = self._new(new_node)
    while k:
      indx = k & _titan23_PersistentArray32_MSK
      k = (k-1) >> _titan23_PersistentArray32_BIT
      node = node.child[indx]
      new_node.child[indx] = node.copy()
      new_node = new_node.child[indx]
    new_node.key = v
    return res

  def get(self, k: int) -> T:
    node = self.root
    while k:
      node = node.child[k & _titan23_PersistentArray32_MSK]
      k = (k-1) >> _titan23_PersistentArray32_BIT
    return node.key

  __getitem__ = get

  def copy(self) -> 'PersistentArray32[T]':
    return self._new(None if self.root is None else self.root.copy())

  def tolist(self) -> List[T]:
    return [self[i] for i in range(self.n)]

  def __str__(self):
    return str(self)

  def __repr__(self):
    return f'PersistentArray32({self})'

