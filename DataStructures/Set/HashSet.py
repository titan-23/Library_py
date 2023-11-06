import random
from typing import Iterable, List, Iterator

class HashSet():

  def __init__(self, a: Iterable[int]=[], not_seen: int=-1, deleted: int=-2):
    self._keys: List[int] = [not_seen]
    self._empty: int = not_seen
    self._deleted : int = deleted
    self._len: int = 0
    self._dellen: int = 0
    self._query_count: int = 0
    self._being_rebuild: bool = False
    self._xor: int = random.getrandbits(1)
    for e in a:
      self.add(e)

  def reserve(self, n: int) -> None:
    self._keys += [self._empty] * (3*n+4)
    self._xor = random.getrandbits(len(self._keys).bit_length())

  def _inner_rebuild(self, old_keys: List[int]) -> None:
    _empty, _deleted = self._empty, self._deleted
    self._len = 0
    self._dellen = 0
    self._being_rebuild = True
    self._xor = random.getrandbits(len(self._keys).bit_length())
    for k in old_keys:
      if k != _empty and k != _deleted:
        self.add(k)
    self._query_count = 0
    self._being_rebuild = False

  def _rebuild(self) -> None:
    old_keys, _empty = self._keys, self._empty
    self._keys = [_empty for _ in old_keys]
    self._inner_rebuild(old_keys)

  def _rebuild_extend(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty for _ in range(3*len(old_keys)+4)]
    self._inner_rebuild(old_keys)

  def _rebuid_shrink(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty for _ in range(len(old_keys)//3+4)]
    self._inner_rebuild(old_keys)

  def _query_check(self) -> None:
    if self._being_rebuild:
      return
    self._query_count += 1
    if self._len > 1000 and self._query_count*3 > self._len:
      self._rebuild()

  def _hash(self, key: int) -> int:
    return (key ^ self._xor) % len(self._keys)

  def add(self, key: int) -> bool:
    assert key != self._empty, \
        f'ValueError: HashSet.add({key}), {key} cannot be equal to {self._empty}'
    assert key != self._deleted, \
        f'ValueError: HashSet.add({key}), {key} cannot be equal to {self._deleted}'
    l, _keys, _empty, _deleted = len(self._keys), self._keys, self._empty, self._deleted
    self._query_check()
    H = self._hash(key)
    for h in range(H, H+l):
      if h >= l:
        h -= l
      if _keys[h] == _empty or _keys[h] == _deleted:
        _keys[h] = key
        self._len += 1
        if 3*self._len > len(self._keys):
          self._rebuild_extend()
        return True
      elif _keys[h] == key:
        return False
    assert False

  def discard(self, key: int) -> bool:
    assert key != self._empty, \
        f'ValueError: HashSet.discard({key}), {key} cannot be equal to {self._empty}'
    assert key != self._deleted, \
        f'ValueError: HashSet.discard({key}), {key} cannot be equal to {self._deleted}'
    l, _keys, _empty = len(self._keys), self._keys, self._empty
    self._query_check()
    H = self._hash(key)
    for h in range(H, H+l):
      if h >= l:
        h -= l
      if _keys[h] == _empty:
        return False
      elif _keys[h] == key:
        _keys[h] = self._deleted
        self._dellen += 1
        self._len -= 1
        if 3*3*self._len < len(self._keys):
          self._rebuid_shrink()
        if self._len > 1000 and self._dellen*20 > self._len:
          self._rebuild()
        return True
    assert False

  def __contains__(self, key: int):
    assert key != self._empty, \
        f'ValueError: {key} in HashSet, {key} cannot be equal to {self._empty}'
    assert key != self._deleted, \
        f'ValueError: {key} in HashSet, {key} cannot be equal to {self._deleted}'
    l, _keys, _empty = len(self._keys), self._keys, self._empty
    self._query_check()
    H = self._hash(key)
    for h in range(H, H+l):
      if h >= l:
        h -= l
      if _keys[h] == _empty:
        return False
      elif _keys[h] == key:
        return True

  def __iter__(self) -> Iterator[int]:
    _empty, _deleted = self._empty, self._deleted
    cnt = len(self)
    for k in self._keys:
      if k != _empty and k != _deleted:
        cnt -= 1
        yield k
      if cnt == 0:
        return

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __len__(self):
    return self._len

