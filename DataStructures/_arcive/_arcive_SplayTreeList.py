# 2023.4.8
# 移植
# 理由: Lazyのほうで良くないか

import sys
from typing import Callable, Generic, Tuple, TypeVar, Union, List, Iterable
T = TypeVar('T')

class Node:

  def __init__(self, key) -> None:
    self.key = key
    self.size = 1
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size}\n'
    return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeList(Generic[T]):

  def __init__(self, a: Iterable[T]=[], node :Union[Node, None]=None) -> None:
    self.node = node
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

  def _update(self, node: Node) -> None:
    node.size = 1 + (0 if node.left is None else node.left.size) + (0 if node.right is None else node.right.size)

  def _splay(self, path: List[Node], di: int) -> Node:
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      if di&1 == di>>1&1:
        if di & 1:
          tmp = node.left
          node.left = tmp.right
          tmp.right = node
          pnode.left = node.right
          node.right = pnode
          self._update(pnode)
          node.size = 1 + (0 if node.left is None else node.left.size) + pnode.size
          tmp.size = 1 + (0 if tmp.left is None else tmp.left.size) + node.size
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
          self._update(pnode)
          node.size = 1 + pnode.size + (0 if node.right is None else node.right.size)
          tmp.size = 1 + node.size + (0 if tmp.right is None else tmp.right.size)
      else:
        if di & 1:
          tmp = node.left
          node.left = tmp.right
          pnode.right = tmp.left
          tmp.right = node
          tmp.left = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          pnode.left = tmp.right
          tmp.left = node
          tmp.right = pnode
        self._update(pnode)
        self._update(node)
        tmp.size = 1 + node.size + pnode.size
      if not path:
        return tmp
      di >>= 2
      if di & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if di & 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
      self._update(gnode)
      node.size = 1 + (0 if node.left is None else node.left.size) + gnode.size
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
      self._update(gnode)
      node.size = 1 + gnode.size + (0 if node.right is None else node.right.size)
    return node

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0: k += self.__len__()
    di = 0
    node = self.node
    path = []
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        if path:
          self.node = self._splay(path, di)
        return
      elif t > k:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
        k -= t + 1

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None: return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None: return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  def merge(self, other: "SplayTreeList") -> None:
    if self.node is None:
      self.node = other.node
      return
    if other.node is None:
      return
    self.node = self._get_max_splay(self.node)
    self.node.right = other.node
    self._update(self.node)

  def split(self, p: int) -> Tuple["SplayTreeList", "SplayTreeList"]:
    if p >= self.__len__(): return self, SplayTreeList()
    self._set_kth_elm_splay(p)
    left = SplayTreeList(node=self.node.left)
    self.node.left, right = None, self
    self._update(right.node)
    return left, right

  def insert(self, k: int, key: T) -> None:
    node = Node(key)
    if self.node is None:
      self.node = node
      return
    if k >= self.__len__():
      self._set_kth_elm_splay(self.__len__()-1)
      node.left = self.node
      self.node = node
    else:
      self._set_kth_elm_splay(k)
      if self.node.left is not None:
        node.left = self.node.left
        self.node.left = None
        self._update(self.node)
      node.right = self.node
      self.node = node
    self._update(self.node)

  def append(self, key: T) -> None:
    node = self._get_max_splay(self.node)
    self.node = Node(key)
    self.node.left = node
    self._update(self.node)

  def appendleft(self, key: T) -> None:
    node = self._get_min_splay(self.node)
    self.node = Node(key)
    self.node.right = node
    self._update(self.node)

  def pop(self, k: int =-1) -> T:
    if k == -1:
      node = self._get_max_splay(self.node)
      self.node = node.left
      return node.key
    self._set_kth_elm_splay(k)
    res = self.node.key
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_max_splay(self.node.left)
      node.right, self.node = self.node.right, node
    self._update(self.node)
    return res

  def popleft(self) -> T:
    node = self._get_min_splay(self.node)
    self.node = node.right
    return node.key

  # 「末尾をを削除し先頭に挿入」をx回
  def rotate(self, x: int) -> None:
    n = len(self)
    x %= n
    l, self = self.split(n-x)
    self.merge(l)

  def copy(self) -> "SplayTreeList":
    return SplayTreeList(self.tolist())

  def clear(self) -> None:
    self.node = None

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self.node.size:
      sys.setrecursionlimit(self.node.size+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def pprint(self, sep=' ', end='\n') -> None:
    if self.node is None:
      print(end=end)
      return
    if sys.getrecursionlimit() < self.node.size:
      sys.setrecursionlimit(self.node.size+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      print(node.key, sep=sep)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    print(end=end)
    return

  def __setitem__(self, k: int, key: T):
    self._set_kth_elm_splay(k)
    self.node.key = key
    self._update(self.node)

  def __getitem__(self, k: int) -> T:
    self._set_kth_elm_splay(k)
    return self.node.key

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __str__(self):
    return '[' + ', '.join(map(str, self.tolist())) + ']'

  def __bool__(self):
    return self.node is not None

  def __repr__(self):
    return 'SplayTreeList(' + str(self) + ')'

