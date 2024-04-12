# from titan_pylib.data_structures.list.linked_list import LinkedList
from typing import Generic, TypeVar, List, Optional, Iterator, Iterable
T = TypeVar('T')

class LinkedList(Generic[T]):
  """双方向連結リストです。
  """

  ___slots__ = ('top', 'tail', 'it', '_len')

  class LinkedListNode():

    def __init__(self, key: T) -> None:
      self._key = key
      self._pre: Optional['LinkedList.LinkedListNode'] = None
      self._nxt: Optional['LinkedList.LinkedListNode'] = None

    def key(self) -> T:
      return self._key

    def set_key(self, key: T) -> None:
      self._key = key

    def __add__(self, _inc: int):
      assert _inc == 1
      return self._nxt

    def __iadd__(self, _inc: int):
      assert _inc == 1
      return self._nxt

    def __sub__(self, _dec: int):
      assert _dec == 1
      return self._pre

    def __isub__(self, _dec: int):
      assert _dec == 1
      return self._pre

    def __str__(self):
      return f'LinkedList.LinkedListNode({self._key})'

    __repr__ = __str__

  def __init__(self, a: Iterable[T]=[]):
    self.top: Optional[LinkedList.LinkedListNode] = None
    self.tail: Optional[LinkedList.LinkedListNode] = None
    self._len = 0
    for e in a:
      self.append(e)

  def extend(self, other: 'LinkedList') -> None:
    if self.top is None:
      self.top = other.top
    if other.tail is not None:
      self.tail = other.tail

  def append(self, key: T) -> LinkedListNode:
    node = self.make_node(key)
    self.append_iter(node)
    return node

  def append_iter(self, node: LinkedListNode) -> None:
    assert node._nxt is None
    self._len += 1
    if not self.top:
      self.top = node
    node._pre = self.tail
    if self.tail:
      self.tail._nxt = node
    self.tail = node

  def appendleft(self, key: T) -> LinkedListNode:
    self._len += 1
    node = self.make_node(key)
    if not self.tail:
      self.tail = node
    node._nxt = self.top
    if self.top:
      self.top._pre = node
    self.top = node
    return node

  def pop(self) -> T:
    self._len -= 1
    node = self.tail
    if node._pre:
      node._pre._nxt = node._nxt
    else:
      self.top = node._pre
    self.tail = node._pre
    return node.key()

  def popleft(self) -> T:
    self._len -= 1
    node = self.top
    if node._nxt:
      node._nxt._pre = node._pre
    else:
      self.tail = node._nxt
    self.top = node._nxt
    return node.key()

  def get_front_iter(self) -> Optional[LinkedListNode]:
    return self.top

  def get_back_iter(self) -> Optional[LinkedListNode]:
    return self.tail

  # pos -> new_node -> pos._nxt
  def insert_iter_nxt(self, pos_node: LinkedListNode, new_node: LinkedListNode) -> None:
    self._len += 1
    new_node._nxt = pos_node._nxt
    new_node._pre = pos_node
    if pos_node._nxt:
      pos_node._nxt._pre = new_node
    else:
      self.tail = new_node
    pos_node._nxt = new_node

  # nxt._pre -> new -> nxt
  def insert_iter_pre(self, nxt_node: LinkedListNode, new_node: LinkedListNode) -> None:
    self._len += 1
    if nxt_node._pre:
      nxt_node._pre._nxt = new_node
    else:
      self.top = new_node
    new_node._pre = nxt_node._pre
    new_node._nxt = nxt_node
    nxt_node._pre = new_node

  def remove_iter(self, node: LinkedListNode) -> None:
    self._len -= 1
    if node._pre:
      node._pre._nxt = node._nxt
    else:
      self.top = node._nxt
    if node._nxt:
      node._nxt._pre = node._pre
    else:
      assert self.tail is node
      self.tail = node._pre

  def iter_node(self) -> LinkedListNode:
    node = self.top
    while node:
      nxt = node._nxt
      yield node
      node = nxt

  def iter_node_rev(self):
    node = self.tail
    while node:
      pre = node._pre
      yield node
      node = pre

  def __reversed__(self) -> Iterator[T]:
    node = self.tail
    while node:
      pre = node._pre
      yield node.key()
      node = pre

  def tolist(self) -> List[T]:
    return [x for x in self]

  def make_node(self, key: T) -> LinkedListNode:
    return self.LinkedListNode(key)

  def __iter__(self) -> Iterator[T]:
    self.it = self.top
    return self

  def __len__(self):
    return self._len

  def __next__(self) -> T:
    if self.it is None:
      raise StopIteration
    key = self.it.key()
    self.it += 1
    return key

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'LinkedList({self})'


