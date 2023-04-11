import sys
from array import array
from typing import TypeVar, Generic, List
sys.setrecursionlimit(7*10**5)
T = TypeVar('T')

class RandomizedMeldableHeap(Generic[T]):

  _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123
  keys: List[T] = [0]
  child: array[int] = array('I', bytes(8))
  end = 1

  @classmethod
  def _randbit(cls) -> int:
    t = cls._x ^ (cls._x << 11) & 0xFFFFFFFF
    cls._x, cls._y, cls._z = cls._y, cls._z, cls._w
    cls._w = (cls._w ^ (cls._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
    return cls._w & 1

  @classmethod
  def _make_node(cls, key: T) -> int:
    if cls.end >= len(cls.keys):
      cls.keys.append(key)
      cls.child.append(0)
      cls.child.append(0)
    else:
      cls.keys[cls.end] = key
    cls.end += 1
    return cls.end - 1

  @classmethod
  def reserve(cls, n: int) -> None:
    if n <= 0: return
    cls.keys += [0] * n
    cls.child += array('I', bytes(8*n))

  def __init__(self):
    self.root = 0

  def _meld(self, x: int, y: int) -> int:
    if x == 0:
      return y
    if y == 0:
      return x
    if self.keys[x] > self.keys[y]:
      x, y = y, x
    rand = self._randbit()
    self.child[x<<1|rand] = self.meld(self.child[x<<1|rand], y)
    return x

  @classmethod
  def meld(cls, x: 'RandomizedMeldableHeap', y: 'RandomizedMeldableHeap') -> 'RandomizedMeldableHeap':
    new_heap = RandomizedMeldableHeap()
    new_heap.root = cls.meld(x.root, y.root)
    return new_heap

  def heappush(self, key: T):
    node = self._make_node(key)
    self.root = self.meld(self.root, node)

  def heappop(self) -> T:
    res = self.keys[self.root]
    self.root = self.meld(self.child[self.root<<1], self.child[self.root<<1|1])
    return res

  def top(self) -> T:
    return self.keys[self.root]

  def __bool__(self):
    return self.root != 0

