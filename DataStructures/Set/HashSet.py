import random
random.seed(1000000000)
from typing import Iterable, List, Iterator, Tuple, Any

class HashSet():

  def __init__(self, a: Iterable[int]=[], not_seen: int=-1, deleted: int=-2):
    self._keys: List[int] = [not_seen]
    self._empty: int = not_seen
    self._deleted : int = deleted
    self._len: int = 0
    self._dellen: int = 0
    self._xor: int = random.getrandbits(1)
    for e in a:
      self.add(e)

  def reserve(self, n: int) -> None:
    self._keys += [self._empty] * (4*n)
    self._xor = random.getrandbits(len(self._keys).bit_length())

  def _rebuild(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty] * len(old_keys)
    self._len = 0
    self._dellen = 0
    self._xor = random.getrandbits(len(self._keys).bit_length())
    for k in old_keys:
      if k != _empty and k != _deleted:
        self.add(k)

  def _rebuild_extend(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty] * (4*len(old_keys)+3)
    self._len = 0
    self._dellen = 0
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
        if 4*self._len > len(self._keys):
          self._rebuild_extend()
        return True
      elif _keys[h] == key:
        return False
      h += 1
      if h == l:
        h = 0

  def _rebuid_shrink(self) -> None:
    old_keys, _empty, _deleted = self._keys, self._empty, self._deleted
    self._keys = [_empty] * (len(old_keys)//4+3)
    self._len = 0
    self._dellen = 0
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
      elif _keys[h] == key:
        _keys[h] = self._deleted
        self._dellen += 1
        self._len -= 1
        if 4*4*self._len < len(self._keys):
          self._rebuid_shrink()
        if len(self._keys) > 1000 and self._dellen*1000 > len(self._keys):
          # print('rebuild', file=sys.stderr)
          self._rebuild()
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
      elif _keys[h] == key:
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
# A = list(range(0, n//10)) * 10
# random.shuffle(A)
st = HashSet(range(n))
for i in range(n):
  if i in st:
    st.discard(A[i])
a = list(st)
a.sort()
print(len(a))
print(' '.join(map(lambda x: str(x+1), a)))
print(time() - start, file=sys.stderr)
exit()

import sys
from time import time
start = time()
n = 10**6
start = time()
st = HashSet()
# st = set()
for i in range(n):
  st.add(i)
for i in range(n-1, -1, -1):
  if i in st:
    st.discard(i)
print(time() - start, file=sys.stderr)
