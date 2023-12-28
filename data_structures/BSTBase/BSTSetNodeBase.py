try:
  from __pypy__ import newlist_hint
except ImportError:
  pass
from typing import List, TypeVar, Generic, Optional
T = TypeVar('T')
Node = TypeVar('Node')
# protcolで、key,left,right を規定

class BSTSetNodeBase(Generic[T, Node]):

  @staticmethod
  def sort_unique(a: List[T]) -> List[T]:
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(a)
      new_a = [a[0]]
      for elm in a:
        if new_a[-1] == elm:
          continue
        new_a.append(elm)
      a = new_a
    return a

  @staticmethod
  def contains(node: Node, key: T) -> bool:
    while node:
      if key == node.key:
        return True
      node = node.left if key < node.key else node.right
    return False

  @staticmethod
  def get_min(node: Node) -> Optional[T]:
    if not node:
      return None
    while node.left:
      node = node.left
    return node.key

  @staticmethod
  def get_max(node: Node) -> Optional[T]:
    if not node:
      return None
    while node.right:
      node = node.right
    return node.key

  @staticmethod
  def le(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key == node.key:
        res = key
        break
      if key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  @staticmethod
  def lt(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  @staticmethod
  def ge(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key == node.key:
        res = key
        break
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  @staticmethod
  def gt(node: Node, key: T) -> Optional[T]:
    res = None
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  @staticmethod
  def index(node: Node, key: T) -> int:
    k = 0
    while node is not None:
      if key == node.key:
        if node.left is not None:
          k += node.left.size
        break
      if key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  @staticmethod
  def index_right(node: Node, key: T) -> int:
    k = 0
    while node is not None:
      if key == node.key:
        k += 1 if node.left is None else node.left.size + 1
        break
      if key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  @staticmethod
  def tolist(node: Node, _len: int=0) -> List[T]:
    stack = []
    res = newlist_hint(_len)
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        res.append(node.key)
        node = node.right
    return res

  @staticmethod
  def kth_elm(node: Node, k: int, _len: int) -> T:
    if k < 0:
      k += _len
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      if t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

