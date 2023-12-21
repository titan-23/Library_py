from __pypy__ import newlist_hint
from typing import List, Tuple, TypeVar, Generic, Optional
T = TypeVar('T')
Node = TypeVar('Node')
# protcolで、key,val,left,right を規定

class BSTMultisetNodeBase(Generic[T, Node]):

  @staticmethod
  def count(node, key: T) -> int:
    while node is not None:
      if node.key == key:
        return node.val
      node = node.left if key < node.key else node.right
    return 0

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
  def contains(node: Node, key: T) -> bool:
    while node:
      if key == node.key:
        return True
      node = node.left if key < node.key else node.right
    return False

  @staticmethod
  def tolist(node: Node, _len: int=0) -> List[T]:
    stack = []
    a = newlist_hint(_len)
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        for _ in range(node.val):
          a.append(node.key)
        node = node.right
    return a

  @staticmethod
  def tolist_items(node: Node, _len: int=0) -> List[Tuple[T, int]]:
    stack = newlist_hint(_len)
    a = newlist_hint(_len)
    while stack or node:
      if node:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        a.append((node.key, node.val))
        node = node.right
    return a

  @staticmethod
  def _rle(a: List[T]) -> Tuple[List[T], List[int]]:
    keys, vals = newlist_hint(len(a)), newlist_hint(len(a))
    keys.append(a[0])
    vals.append(1)
    for i, elm in enumerate(a):
      if i == 0:
        continue
      if elm == keys[-1]:
        vals[-1] += 1
        continue
      keys.append(elm)
      vals.append(1)
    return keys, vals

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
    while node:
      if key == node.key:
        if node.left:
          k += node.left.valsize
        break
      if key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return k

  @staticmethod
  def index_right(node: Node, key: T) -> int:
    k = 0
    while node:
      if key == node.key:
        k += node.val if node.left is None else node.left.valsize + node.val
        break
      if key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return k

