# from titan_pylib.data_structures.union_find.persistent_union_find import PersistentUnionFind
# from titan_pylib.data_structures.array.persistent_array import PersistentArray
from typing import List, Iterable, TypeVar, Generic, Optional
T = TypeVar('T')

class PersistentArray(Generic[T]):

  class Node():

    def __init__(self, key: T):
      self.key: T = key
      self.left: Optional[PersistentArray.Node] = None
      self.right: Optional[PersistentArray.Node] = None

    def copy(self) -> 'PersistentArray.Node':
      node = PersistentArray.Node(self.key)
      node.left = self.left
      node.right = self.right
      return node

  def __init__(self, a: Iterable[T]=[], _root: Optional['PersistentArray.Node']=None):
    self.root = self._build(a) if _root is None else _root

  def _build(self, a: Iterable[T]) -> Optional['PersistentArray.Node']:
    pool = [PersistentArray.Node(e) for e in a]
    self.n = len(pool)
    if not pool:
      return None
    n = len(pool)
    for i in range(1, n+1):
      if 2*i-1 < n:
        pool[i-1].left = pool[2*i-1]
      if 2*i < n:
        pool[i-1].right = pool[2*i]
    return pool[0]

  def _new(self, root: Optional['PersistentArray.Node']) -> 'PersistentArray[T]':
    res = PersistentArray(_root=root)
    res.n = self.n
    return res

  def set(self, k: int, v: T) -> 'PersistentArray[T]':
    node = self.root
    if node is None:
      return self._new(None)
    new_node = node.copy()
    res = self._new(new_node)
    k += 1
    b = k.bit_length()
    for i in range(b-2, -1, -1):
      if k >> i & 1:
        node = node.right
        new_node.right = node.copy()
        new_node = new_node.right
      else:
        node = node.left
        new_node.left = node.copy()
        new_node = new_node.left
    new_node.key = v
    return res

  def get(self, k: int) -> T:
    node = self.root
    k += 1
    b = k.bit_length()
    for i in range(b-2, -1, -1):
      if k >> i & 1:
        node = node.right
      else:
        node = node.left
    return node.key

  __getitem__ = get

  def copy(self) -> 'PersistentArray[T]':
    return self._new(None if self.root is None else self.root.copy())

  def tolist(self) -> List[T]:
    node = self.root
    a: List[T] = []
    if not node: return a
    q = [node]
    for node in q:
      a.append(node.key)
      if node.left:
        q.append(node.left)
      if node.right:
        q.append(node.right)
    return a

  def __len__(self):
    return self.n

  def __str__(self):
    return str(self)

  def __repr__(self):
    return f'PersistentArray({self})'

from typing import Optional

class PersistentUnionFind():

  def __init__(self, n: int, _parents: Optional[PersistentArray[int]]=None):
    """``n`` 個の要素からなる ``PersistentUnionFind`` を構築します。

    :math:`O(n)` です。
    """
    self._n: int = n
    self._parents: PersistentArray[int] = PersistentArray([-1] * n) if _parents is None else _parents

  def _new(self, _parents: PersistentArray[int]) -> 'PersistentUnionFind':
    return PersistentUnionFind(self._n, _parents)

  def copy(self) -> 'PersistentUnionFind':
    """コピーします。

    :math:`O(1)` です。
    """
    return self._new(self._parents.copy())

  def root(self, x: int) -> int:
    """要素 ``x`` を含む集合の代表元を返します。

    :math:`O(\\log{n}^2)` です。
    """
    _parents = self._parents
    while True:
      p = _parents.get(x)
      if p < 0:
        return x
      x = p

  def unite(self, x: int, y: int, update: bool=False) -> 'PersistentUnionFind':
    """要素 ``x`` を含む集合と要素 ``y`` を含む集合を併合します。

    :math:`O(\\log{n}^2)` です。

    Args:
      x (int): 集合の要素です。
      y (int): 集合の要素です。
      update (bool, optional): 併合後を新しいインスタンスにするなら ``True`` です。

    Returns:
      PersistentUnionFind: 併合後の uf です。
    """
    x = self.root(x)
    y = self.root(y)
    res_parents = self._parents.copy() if update else self._parents
    if x == y:
      return self._new(res_parents)
    px, py = res_parents.get(x), res_parents.get(y)
    if px > py:
      x, y = y, x
    res_parents = res_parents.set(x, px + py)
    res_parents = res_parents.set(y, x)
    return self._new(res_parents)

  def size(self, x: int) -> int:
    """要素 ``x`` を含む集合の要素数を返します。

    :math:`O(\\log{n}^2)` です。
    """
    return -self._parents.get(self.root(x))

  def same(self, x: int, y: int) -> bool:
    """
    要素 ``x`` と ``y`` が同じ集合に属するなら ``True`` を、
    そうでないなら ``False`` を返します。

    :math:`O(\\log{n}^2)` です。
    """
    return self.root(x) == self.root(y)


