from __pypy__ import newlist_hint
from typing import List

class BSTSetNodeBase():

  @staticmethod
  def sort_unique(a: List) -> List:
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(a)
      b = [a[0]]
      for e in a:
        if b[-1] == e:
          continue
        b.append(e)
      a = b
    return a

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
  def index_right(node, key) -> int:
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
  def tolist(node, _len=0) -> List:
    stack = newlist_hint(_len)
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
  def kth_elm(node, k: int, _len: int):
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


