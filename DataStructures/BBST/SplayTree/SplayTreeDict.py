import sys
from typing import Union, Generic, List, TypeVar, Any, Tuple, Callable
T = TypeVar('T')

class SplayTreeSetDict(Generic[T]):

  class Node:

    def __init__(self, key, val) -> None:
      self.key = key
      self.val = val
      self.left = None
      self.right = None

    def __str__(self) -> str:
      if self.left is None and self.right is None:
        return f'key:{self.key, self.val}\n'
      return f'key:{self.key, self.val},\n left:{self.left},\n right:{self.right}\n'

  NIL = Node(None, None)

  def __init__(self, default: Union[None, Callable[[], T]]=None) -> None:
    self.node = None
    self.len = 0
    self.default = default

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key: return
    par = SplayTreeSetDict.NIL
    left = par
    right = par
    while True:
      if node.key == key:
        break
      if key < node.key:
        if node.left is None: break
        if key < node.left.key:
          new = node.left
          node.left = new.right
          new.right = node
          node = new
          if node.left is None: break
        right.left = node
        right = node
        node = node.left
      else:
        if node.right is None: break
        if key > node.right.key:
          new = node.right
          node.right = new.left
          new.left = node
          node = new
          if node.right is None: break
        left.right = node
        left = node
        node = node.right
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    self.node = node

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None: return node
    par = SplayTreeSetDict.NIL
    left = par
    right = par
    while node.left is not None:
      new = node.left
      node.left = new.right
      new.right = node
      node = new
      if node.left is None: break
      right.left = node
      right = node
      node = node.left
    right.left = node.right
    left.right = node.left
    node.left = par.right
    node.right = par.left
    return node

  def __setitem__(self, key: T, val: Any):
    if self.node is None:
      self.node = SplayTreeSetDict.Node(key, val)
      self.len += 1
      return
    self._set_search_splay(key)
    if self.node.key == key:
      self.node.val = val
      return
    node = SplayTreeSetDict.Node(key, val)
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
    return

  def __delitem__(self, key: T) -> bool:
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

  def tolist(self) -> List[Tuple[T, Any]]:
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.val))
      if node.right is not None:
        rec(node.right)
    a = []
    if self.node is not None:
      rec(self.node)
    return a

  def __getitem__(self, key: T) -> Any:
    self._set_search_splay(key)
    if self.node is None or self.node.key != key:
      if self.default is not None:
        return self.default()
      else:
        raise KeyError(key)
    return self.node.val

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
    return 'SplayTreeSetDict(' + str(self) + ')'

