# from titan_pylib.data_structures.splay_tree.lazy_splay_tree import LazySplayTree
from typing import Generic, List, Union, TypeVar, Tuple, Callable, Iterable, Optional
from __pypy__ import newlist_hint
T = TypeVar('T')
F = TypeVar('F')

class LazySplayTree(Generic[T, F]):

  class _Node():

    def __init__(self, key: T, lazy: F) -> None:
      self.key: T = key
      self.data: T = key
      self.rdata: T = key
      self.lazy: F = lazy
      self.left: Optional['LazySplayTree._Node'] = None
      self.right: Optional['LazySplayTree._Node'] = None
      self.par: Optional['LazySplayTree._Node'] = None
      self.size: int = 1
      self.rev: int = 0

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               mapping: Callable[[F, T], T],
               composition: Callable[[F, F], F],
               e: T,
               id: F,
               _root: Optional[_Node]=None,
               ) -> None:
    """構築します。
    :math:`O(n)` です。

    Args:
      n_or_a (Union[int, Iterable[T]]): ``n`` のとき、 ``e`` から長さ ``n`` で構築します。
                                        ``a`` のとき、 ``a`` から構築します。
      op (Callable[[T, T], T]): 遅延セグ木のあれです。
      mapping (Callable[[F, T], T]): 遅延セグ木のあれです。
      composition (Callable[[F, F], F]): 遅延セグ木のあれです。
      e (T): 遅延セグ木のあれです。
      id (F): 遅延セグ木のあれです。
    """
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id = id
    self.root = _root
    if _root:
      return
    a = n_or_a
    if isinstance(a, int):
      a = [e for _ in range(a)]
    elif not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    _Node = LazySplayTree._Node
    id = self.id
    def build(l: int, r: int) -> LazySplayTree._Node:
      mid = (l + r) >> 1
      node = _Node(a[mid], id)
      if l != mid:
        node.left = build(l, mid)
        node.left.par = node
      if mid+1 != r:
        node.right = build(mid+1, r)
        node.right.par = node
      self._update(node)
      return node
    self.root = build(0, len(a))

  def _rotate(self, node: _Node) -> None:
    pnode = node.par
    gnode = pnode.par
    if gnode:
      if gnode.left is pnode:
        gnode.left = node
      else:
        gnode.right = node
    node.par = gnode
    if pnode.left is node:
      pnode.left = node.right
      if node.right:
        node.right.par = pnode
      node.right = pnode
    else:
      pnode.right = node.left
      if node.left:
        node.left.par = pnode
      node.left = pnode
    pnode.par = node
    self._update_double(pnode, node)

  def _propagate_rev(self, node: Optional[_Node]) -> None:
    if not node: return
    node.rev ^= 1

  def _propagate_lazy(self, node: Optional[_Node], f: F) -> None:
    if not node: return
    node.key = self.mapping(f, node.key)
    node.data = self.mapping(f, node.data)
    node.rdata = self.mapping(f, node.rdata)
    node.lazy = f if node.lazy == self.id else self.composition(f, node.lazy)

  def _propagate(self, node: Optional[_Node]) -> None:
    if not node: return
    if node.rev:
      node.data, node.rdata = node.rdata, node.data
      node.left, node.right = node.right, node.left
      self._propagate_rev(node.left)
      self._propagate_rev(node.right)
      node.rev = 0
    if node.lazy != self.id:
      self._propagate_lazy(node.left, node.lazy)
      self._propagate_lazy(node.right, node.lazy)
      node.lazy = self.id

  def _update_double(self, pnode: _Node, node: _Node) -> None:
    node.data = pnode.data
    node.rdata = pnode.rdata
    node.size = pnode.size
    self._update(pnode)

  def _update(self, node: _Node) -> None:
    node.data = node.key
    node.rdata = node.key
    node.size = 1
    if node.left:
      node.data = self.op(node.left.data, node.data)
      node.rdata = self.op(node.rdata, node.left.rdata)
      node.size += node.left.size
    if node.right:
      node.data = self.op(node.data, node.right.data)
      node.rdata = self.op(node.right.rdata, node.rdata)
      node.size += node.right.size

  def _splay(self, node: _Node) -> None:
    # while node.par and node.par.par:
    #   pnode = node.par
    #   self._rotate(pnode if (pnode.par.left is pnode) == (pnode.left is node) else node)
    #   self._rotate(node)
    # if node.par:
    #   self._rotate(node)
    while node.par:
      pnode = node.par
      if pnode:
        self._rotate(pnode if (pnode.par.left is pnode) == (pnode.left is node) else node)
      self._rotate(node)

  def kth_splay(self, node: Optional[_Node], k: int) -> None:
    if k < 0:
      k += len(self)
    while True:
      self._propagate(node)
      t = node.left.size if node.left else 0
      if t == k:
        break
      if t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1
    self._splay(node)
    return node

  def _left_splay(self, node: Optional[_Node]) -> Optional[_Node]:
    self._propagate(node)
    if not node or not node.left:
      return node
    while node.left:
      node = node.left
      self._propagate(node)
    self._splay(node)
    return node

  def _right_splay(self, node: Optional[_Node]) -> Optional[_Node]:
    self._propagate(node)
    if not node or not node.right:
      return node
    while node.right:
      node = node.right
      self._propagate(node)
    self._splay(node)
    return node

  def merge(self, other: 'LazySplayTree') -> None:
    """``other`` を後ろに連結します。
    償却 :math:`O(\\log{n})` です。

    Args:
      other (LazySplayTree):
    """
    if not self.root:
      self.root = other.root
      return
    if not other.root:
      return
    self.root = self._right_splay(self.root)
    self.root.right = other.root
    other.root.par = self.root
    self._update(self.root)

  def split(self, k: int) -> Tuple['LazySplayTree', 'LazySplayTree']:
    """位置 ``k`` で split します。
    償却 :math:`O(\\log{n})` です。

    Returns:
      Tuple['LazySplayTree', 'LazySplayTree']:
    """
    left, right = self._internal_split(self.root, k)
    left_splay = LazySplayTree(0, self.op, self.mapping, self.composition, self.e, self.id, left)
    right_splay = LazySplayTree(0, self.op, self.mapping, self.composition, self.e, self.id, right)
    return left_splay, right_splay

  def _internal_split(self, k: int) -> Tuple[_Node, _Node]:
    if k == len(self):
      return self.root, None
    right = self.kth_splay(self.root, k)
    left = right.left
    if left:
      left.par = None
    right.left = None
    self._update(right)
    return left, right

  def _internal_merge(self, left: Optional[_Node], right: Optional[_Node]) -> Optional[_Node]:
    # need (not right) or (not right.left)
    if not right:
      return left
    assert right.left is None
    right.left = left
    if left:
      left.par = right
    self._update(right)
    return right

  def reverse(self, l: int, r: int) -> None:
    """区間 ``[l, r)`` を反転します。
    償却 :math:`O(\\log{n})` です。

    Args:
      l (int):
      r (int):
    """
    assert 0 <= l <= r <= len(self), \
        f'IndexError: {self.__class__.__name__}.reverse({l}, {r}), len={len(self)}'
    left, right = self._internal_split(r)
    if l == 0:
      self._propagate_rev(left)
    else:
      left = self.kth_splay(left, l-1)
      self._propagate_rev(left.right)
    self.root = self._internal_merge(left, right)

  def all_reverse(self) -> None:
    """区間 ``[0, n)`` を反転します。
    :math:`O(1)` です。
    """
    self._propagate_rev(self.root)

  def apply(self, l: int, r: int, f: F) -> None:
    """区間 ``[l, r)`` に ``f`` を作用します。
    償却 :math:`O(\\log{n})` です。

    Args:
      l (int):
      r (int):
      f (F): 作用素です。
    """
    assert 0 <= l <= r <= len(self), \
        f'IndexError: {self.__class__.__name__}.apply({l}, {r}, {f}), len={len(self)}'
    left, right = self._internal_split(r)
    if l == 0:
      self._propagate_lazy(left, f)
    else:
      left = self.kth_splay(left, l-1)
      self._propagate_lazy(left.right, f)
      self._update(left)
    self.root = self._internal_merge(left, right)

  def all_apply(self, f: F) -> None:
    """区間 ``[0, n)`` に ``f`` を作用します。
    :math:`O(1)` です。
    """
    self._propagate_lazy(self.root, f)

  def prod(self, l: int, r: int) -> T:
    """区間 ``[l, r)`` の総積を求めます。
    償却 :math:`O(\\log{n})` です。
    """
    assert 0 <= l <= r <= len(self), \
        f'IndexError: {self.__class__.__name__}.prod({l}, {r}), len={len(self)}'
    if l == r:
      return self.e
    left, right = self._internal_split(r)
    if l == 0:
      res = left.data
    else:
      left = self.kth_splay(left, l-1)
      res = left.right.data
    self.root = self._internal_merge(left, right)
    return res

  def all_prod(self) -> T:
    """区間 ``[0, n)`` の総積を求めます。
    :math:`O(1)` です。
    """
    self._propagate(self.root)
    return self.root.data if self.root else self.e

  def insert(self, k: int, key: T) -> None:
    """位置 ``k`` に ``key`` を挿入します。
    償却 :math:`O(\\log{n})` です。

    Args:
      k (int):
      key (T):
    """
    assert 0 <= k <= len(self)
    node = self._Node(key, self.id)
    if not self.root:
      self.root = node
      return
    if k >= len(self):
      root = self.kth_splay(self.root, len(self)-1)
      node.left = root
    else:
      root = self.kth_splay(self.root, k)
      if root.left:
        node.left = root.left
        root.left.par = node
        root.left = None
        self._update(root)
      node.right = root
    root.par = node
    self.root = node
    self._update(self.root)

  def append(self, key: T) -> None:
    """末尾に ``key`` を追加します。
    償却 :math:`O(\\log{n})` です。

    Args:
      key (T):
    """
    node = self._right_splay(self.root)
    self.root = self._Node(key, self.id)
    self.root.left = node
    if node:
      node.par = self.root
    self._update(self.root)

  def appendleft(self, key: T) -> None:
    """先頭に ``key`` を追加します。
    償却 :math:`O(\\log{n})` です。

    Args:
      key (T):
    """
    node = self._left_splay(self.root)
    self.root = self._Node(key, self.id)
    self.root.right = node
    if node:
      node.par = self.root
    self._update(self.root)

  def pop(self, k: int=-1) -> T:
    """位置 ``k`` の要素を削除し、その値を返します。
    償却 :math:`O(\\log{n})` です。

    Args:
      k (int, optional): 指定するインデックスです。 Defaults to -1.
    """
    if k == -1:
      node = self._right_splay(self.root)
      if node.left:
        node.left.par = None
      self.root = node.left
      return node.key
    root = self.kth_splay(self.root, k)
    res = root.key
    if root.left and root.right:
      node = self._right_splay(root.left)
      node.par = None
      node.right = root.right
      if node.right:
        node.right.par = node
      self._update(node)
      self.root = node
    else:
      self.root = root.right if root.right else root.left
      if self.root:
        self.root.par = None
    return res

  def popleft(self) -> T:
    """先頭の要素を削除し、その値を返します。
    償却 :math:`O(\\log{n})` です。

    Returns:
      T:
    """
    node = self._left_splay(self.root)
    self.root = node.right
    if node.right:
      node.right.par = None
    return node.key

  def copy(self) -> 'LazySplayTree':
    """コピーします。

    Note:
      償却 :math:`O(n)` です。

    Returns:
      LazySplayTree:
    """
    return LazySplayTree(self.tolist(), self.op, self.mapping, self.composition, self.e, self.id)

  def clear(self) -> None:
    """全ての要素を削除します。
    :math:`O(1)` です。
    """
    self.root = None

  def tolist(self) -> List[T]:
    """``list`` にして返します。
    :math:`O(n)` です。非再帰です。

    Returns:
      List[T]:
    """
    node = self.root
    stack = []
    a = newlist_hint(len(self))
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

  def __setitem__(self, k: int, key: T) -> None:
    """位置 ``k`` の要素を値 ``key`` で更新します。
    償却 :math:`O(\\log{n})` です。

    Args:
      k (int):
      key (T):
    """
    self.root = self.kth_splay(self.root, k)
    self.root.key = key
    self._update(self.root)

  def __getitem__(self, k: int) -> T:
    """位置 ``k`` の値を返します。
    償却 :math:`O(\\log{n})` です。

    Args:
      k (int):
      key (T):
    """
    self.root = self.kth_splay(self.root, k)
    return self.root.key

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == len(self):
      raise StopIteration
    res = self[self.__iter]
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(len(self)):
      yield self[-i-1]

  def __len__(self):
    """要素数を返します。
    :math:`O(1)` です。

    Returns:
      int:
    """
    return self.root.size if self.root else 0

  def __str__(self):
    return str(self.tolist())

  def __bool__(self):
    return self.root is not None

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'

