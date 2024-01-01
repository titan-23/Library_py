# from Library_py.DataStructures.Set.HashedMultiset import HashedMultiset
from typing import Iterator, List, Hashable

class HashedMultiset():

  def __init__(self, a: List[Hashable]=[]):
    d = {}
    for e in a:
      if e in d:
        d[e] += 1
      else:
        d[e] = 1
    self._data = d
    self._len = len(a)

  def add(self, key: Hashable, val: int=1) -> None:
    if key in self._data:
      self._data[key] += val
    else:
      self._data[key] = val
    self._len += val

  def discard(self, key: Hashable, val: int=1) -> None:
    if key not in self._data: return
    if self._data[key] > val:
      self._len -= val
      self._data[key] -= val
    else:
      self._len -= self._data[key]
      del self._data[key]

  def discard_all(self, key: Hashable) -> None:
    if key not in self._data: return
    self._len -= self._data[key]
    del self._data[key]

  def count(self, key: Hashable) -> int:
    return self._data.get(key, 0)

  def len_elm(self) -> int:
    return len(self._data)

  def keys(self) -> Iterator[Hashable]:
    for k in self._data.keys():
      yield k

  def values(self) -> Iterator[int]:
    for v in self._data.values():
      yield v

  def items(self) -> Iterator[Hashable]:
    for item in self._data.items():
      yield item

  def clear(self) -> None:
    self._data = {}
    self._len = 0
    self._len_elm = 0

  def __eq__(self, other):
    if isinstance(other, HashedMultiset):
      d = other._data
    elif hasattr(other, 'items'):
      d = other
    else:
      raise TypeError
    for k, v in self._data.items():
      if k not in d or d[k] != v:
        return False
    for k, v in d.items():
      if k not in self._data or self._data[k] != v:
        return False
    return True

  def __contains__(self, key: Hashable):
    return key in self._data

  def __len__(self):
    return self._len


