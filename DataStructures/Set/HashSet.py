import random
from typing import Iterable, List, Iterator, Tuple, Any

class HashSet():

  def __init__(self, a: Iterable[int]=[], not_seen: int=-1, deleted: int=-2):
    self._keys: List[int] = [not_seen]
    self._empty: int = not_seen
    self._deleted : int = deleted
    self._len: int = 0
    self._xor: int = random.getrandbits(1)
    for e in a:
      self.add(e)

  def reserve(self, n: int) -> None:
    self._keys += [self._empty] * (3*n)
    self._xor = random.getrandbits(len(self._keys).bit_length())

  def _rebuild(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty] * (3*len(old_keys)+3)
    self._len = 0
    self._xor = random.getrandbits(len(self._keys).bit_length())
    for k in old_keys:
      if k != _empty and k != _deleted:
        self.add(k)

  def _hash(self, key: int) -> int:
    return (key ^ self._xor) % len(self._keys)

  def add(self, key: int) -> bool:
    assert key != self._empty, \
        f'ValueError: HashSet.add({key}), {key} cannot be equal to {self._empty}'
    assert key != self._deleted, \
        f'ValueError: HashSet.add({key}), {key} cannot be equal to {self._deleted}'
    l, _keys, _empty, _deleted = len(self._keys), self._keys, self._empty, self._deleted
    h = self._hash(key)
    while True:
      if _keys[h] == _empty or _keys[h] == _deleted:
        _keys[h] = key
        self._len += 1
        if 3*self._len > len(self._keys):
          self._rebuild()
        return True
      if _keys[h] == key:
        return False
      h += 1
      if h == l:
        h = 0

  def _rebuid_shrink(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty] * (len(old_keys)//3+3)
    self._len = 0
    self._xor = random.getrandbits(len(self._keys).bit_length())
    for k in old_keys:
      if k != _empty and k != _deleted:
        self.add(k)

  def discard(self, key: int) -> bool:
    assert key != self._empty, \
        f'ValueError: HashSet.discard({key}), {key} cannot be equal to {self._empty}'
    assert key != self._deleted, \
        f'ValueError: HashSet.discard({key}), {key} cannot be equal to {self._deleted}'
    l, _keys, _empty = len(self._keys), self._keys, self._empty
    h = self._hash(key)
    while True:
      if _keys[h] == _empty:
        return False
      if _keys[h] == key:
        _keys[h] = self._deleted
        self._len -= 1
        if 9*self._len < len(self._keys):
          # print(self._len, len(self._keys), flush=True)
          self._rebuid_shrink()
        return True
      h += 1
      if h == l:
        h = 0

  def __contains__(self, key: int):
    assert key != self._empty, \
        f'ValueError: {key} in HashSet, {key} cannot be equal to {self._empty}'
    assert key != self._deleted, \
        f'ValueError: {key} in HashSet, {key} cannot be equal to {self._deleted}'
    l, _keys, _empty = len(self._keys), self._keys, self._empty
    h = self._hash(key)
    while True:
      if _keys[h] == _empty:
        return False
      if _keys[h] == key:
        return True
      h += 1
      if h == l:
        h = 0

  def __iter__(self) -> Iterator[int]:
    _empty, _deleted = self._empty, self._deleted
    for k in self._keys:
      if k != _empty and k != _deleted:
        yield k

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __len__(self):
    return self._len

#  -----------------------  #

from time import time
start = time()

import sys
input = lambda: sys.stdin.readline().rstrip()
n = int(input())
A = list(map(lambda x: int(x)-1, input().split()))
# n = 2*10**5
# A = [random.randint(0, n-1) for _ in range(n)]
st = HashSet(range(n))
for i in range(n):
  if i in st:
    st.discard(A[i])
a = list(st)
a.sort()
print(len(a))
print(' '.join(map(lambda x: str(x+1), a)))
print(time() - start, file=sys.stderr)
