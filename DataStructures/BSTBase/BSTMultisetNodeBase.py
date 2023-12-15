from __pypy__ import newlist_hint
from typing import List, Tuple

class BSTMultisetNodeBase():

  @staticmethod
  def tolist(node, _len: int=0) -> List:
    stack = newlist_hint(_len)
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
  def tolist_items(node, _len: int=0) -> List[Tuple]:
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
  def _rle(L):
    x, y = newlist_hint(len(L)), newlist_hint(len(L))
    x.append(L[0])
    y.append(1)
    for i, a in enumerate(L):
      if i == 0:
        continue
      if a == x[-1]:
        y[-1] += 1
        continue
      x.append(a)
      y.append(1)
    return x, y

  @staticmethod
  def le(node, key):
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
  def lt(node, key):
    res = None
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  @staticmethod
  def ge(node, key):
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
  def gt(node, key):
    res = None
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  @staticmethod
  def index(node, key) -> int:
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
  def index_right(node, key) -> int:
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

