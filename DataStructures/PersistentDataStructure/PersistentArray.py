from typing import Any, Iterable

class PersistentArray():

  class Node():

    def __init__(self, key):
      self.key = key
      self.left = None
      self.right = None
      self.size = 1

  def __init__(self, a: Iterable[Any]):
    self.root = [self._build(a)]

  def _build(self, a) -> None:
    Node = PersistentArray.Node
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
        node.size += node.left.size
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.size += node.right.size
      return node
    return sort(0, len(a))

  def set(self, t: int, k: int, v: Any):
    oldroot = self.root[t]
    newroot = Node(oldroot.key)
    




