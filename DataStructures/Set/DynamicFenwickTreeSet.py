from ..FenwickTree.DynamicFenwickTree import DynamicFenwickTree
from typing import Dict, Iterable, Optional

class DynamicFenwickTreeSet():

  # 整数[0, u)を、空間O(qlogu)/時間O(qlogu)
  
  def __init__(self, u: int, a: Iterable[int]=[]):
    # Build a new FenwickTreeSet. / O(1)
    self._size: int = u
    self._len: int = 0
    self._cnt: Dict[int, int] = {}
    self._fw = DynamicFenwickTree(self._size)
    for _a in a:
      self.add(_a)

  def add(self, key: int) -> bool:
    if key in self._cnt:
      return False
    self._len += 1
    self._cnt[key] = 1
    self._fw.add(key, 1)
    return True

  def remove(self, key: int) -> None:
    if self.discard(key): return
    raise KeyError(key)

  def discard(self, key: int) -> bool:
    if key in self._cnt:
      self._len -= 1
      del self._cnt[key]
      self._fw.add(key, -1)
      return True
    return False

  def le(self, key: int) -> Optional[int]:
    if key in self._cnt: return key
    pref = self._fw.pref(key) - 1
    return None if pref < 0 else self._fw.bisect_right(pref)

  def lt(self, key: int) -> Optional[int]:
    pref = self._fw.pref(key) - 1
    return None if pref < 0 else self._fw.bisect_right(pref)

  def ge(self, key: int) -> Optional[int]:
    if key in self._cnt: return key
    pref = self._fw.pref(key + 1)
    return None if pref >= self._len else self._fw.bisect_right(pref)

  def gt(self, key: int) -> Optional[int]:
    pref = self._fw.pref(key + 1)
    return None if pref >= self._len else self._fw.bisect_right(pref)

  def index(self, key: int) -> int:
    return self._fw.pref(key)

  def index_right(self, key: int) -> int:
    return self._fw.pref(key + 1)

  def pop(self, k: int=-1) -> int:
    x = self.__getitem__(k)
    self.discard(x)
    return x

  def pop_max(self) -> int:
    assert self, f'IndexError'
    return self.pop()

  def pop_min(self) -> int:
    assert self, f'IndexError'
    return self.pop(0)

  def __getitem__(self, k: int) -> int:
    if k < 0:
      k += self._len
    return self._fw.bisect_right(k)

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter == self._len:
      raise StopIteration
    res = self.__getitem__(self._iter)
    self._iter += 1
    return res

  def __reversed__(self):
    for i in range(self._len):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return self._len

  def __contains__(self, key: int):
    return key in self._cnt

  def __bool__(self):
    return self._len > 0

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return f'DynamicFenwickTreeSet({self})'

