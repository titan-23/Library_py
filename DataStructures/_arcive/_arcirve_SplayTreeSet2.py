import sys
from typing import Union, Generic, Iterable, List, TypeVar, Optional
T = TypeVar("T")

# SplayTreeSet2
# ノードクラスを使用、各ノードにはsizeが載らない

class Node:

  def __init__(self, key) -> None:
    self.key = key
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key}\n'
    return f'key:{self.key},\n left:{self.left},\n right:{self.right}\n'

class SplayTreeSet2(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    self.len = 0
    if not (hasattr(a, '__getitem__') and hasattr(a, '__len__')):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      return node
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      aa = sorted(a)
      a = [aa[0]]
      for i in range(1, len(aa)):
        if aa[i] != a[-1]:
          a.append(aa[i])
    self.len = len(a)
    self.node = sort(0, len(a))

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
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
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
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key: return
    path = []
    di = 0
    while True:
      if node.key == key:
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        if node.right is None:
          break
        path.append(node)
        di <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, di)

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  def add(self, key: T) -> bool:
    if self.node is None:
      self.node = Node(key)
      self.len += 1
      return True
    self._set_search_splay(key)
    if self.node.key == key:
      return False
    node = Node(key)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
    self.node = node
    self.len += 1
    return True

  def discard(self, key: T) -> bool:
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self.node = node
    self.len -= 1
    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if key <= node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    di = 0
    res = None
    while node is not None:
      if key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  def pop_max(self) -> T:
    node = self._get_max_splay(self.node)
    self.node = node.left
    self.len -= 1
    return node.key

  def pop_min(self) -> T:
    node = self._get_min_splay(self.node)
    self.node = node.right
    self.len -= 1
    return node.key

  def get_min(self) -> T:
    self.node = self._get_min_splay(self.node)
    return self.node.key
 
  def get_max(self) -> T:
    self.node = self._get_max_splay(self.node)
    return self.node.key

  def clear(self) -> None:
    self.node = None

  def tolist(self) -> List[T]:
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    a = []
    if self.node is not None:
      rec(self.node)
    return a

  def __getitem__(self, k):  # 先頭と末尾しか対応していない
    if k == -1 or k == self.len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'SplayTreeSet2(' + str(self) + ')'

