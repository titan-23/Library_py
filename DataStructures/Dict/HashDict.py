import random
from typing import List, Iterator, Tuple, Any

class HashDict():

  '''
  load factorの基準: 25%(え?)
  ↑pypyのdictのメモリ消費量がヤバいのでこれくらいでもギリ許されそう
  
  一応uintを想定しているので、eはint型の-1を設定している
  Hash関数やrehashの基準は適当。有識者求む
  (intを載せるのにeをNoneにすると、listのstrategyの問題で有意に遅くなる。注意)
  
  組み込みdictよりちょっと遅い
  存  在  意  義
  '''

  def __init__(self, e: int=-1, default: Any=0):
    # e: keyとして使わない値
    # default: valのdefault値
    self._keys: List[int] = [e]
    self._vals: List[Any] = [default]
    self._e: int = e
    self._default: Any = default
    self._len: int = 0
    self._xor: int = random.getrandbits(1)

  def reserve(self, n: int) -> None:
    self._keys += [self._e] * (4*n)
    self._vals += [self._default] * (4*n)
    self._xor = random.getrandbits(len(self._keys).bit_length())

  def _rebuild(self) -> None:
    old_keys, old_vals, _e = self._keys, self._vals, self._e
    self._keys = [_e] * (4*(len(old_keys)+3))
    self._vals = [self._default] * len(self._keys)
    self._len = 0
    self._xor = random.getrandbits(len(self._keys).bit_length())
    for i in range(len(old_keys)):
      if old_keys[i] != _e:
        self.set(old_keys[i], old_vals[i])

  def _hash(self, key: int) -> int:
    return (key ^ self._xor) % len(self._keys)

  def get(self, key: int, default: Any=None) -> Any:
    assert key != self._e, \
        f'ValueError: HashDict.get({key}, {default}), {key} cannot be equal to {self._e}'
    l, _keys, _e = len(self._keys), self._keys, self._e
    h = self._hash(key)
    while True:
      x = _keys[h]
      if x == _e:
        return self._vals[h] if default is None else default
      if x == key:
        return self._vals[h]
      h += 1
      if h == l:
        h = 0

  def set(self, key: int, val: Any) -> None:
    assert key != self._e, \
        f'ValueError: HashDict.set({key}, {val}), {key} cannot be equal to {self._e}'
    l, _keys, _e = len(self._keys), self._keys, self._e
    h = self._hash(key)
    while True:
      x = _keys[h]
      if x == _e:
        _keys[h] = key
        self._vals[h] = val
        self._len += 1
        if 4*self._len > len(self._keys):
          self._rebuild()
        return
      if x == key:
        self._vals[h] = val
        return
      h += 1
      if h == l:
        h = 0

  def __contains__(self, key: int):
    assert key != self._e, \
        f'ValueError: {key} in HashDict, {key} cannot be equal to {self._e}'
    l, _keys, _e = len(self._keys), self._keys, self._e
    h = self._hash(key)
    while True:
      x = _keys[h]
      if x == _e:
        return False
      if x == key:
        return True
      h += 1
      if h == l:
        h = 0

  __getitem__ = get
  __setitem__ = set

  def keys(self) -> Iterator[int]:
    _keys, _e = self._keys, self._e
    for i in range(len(_keys)):
      if _keys[i] != _e:
        yield _keys[i]

  def values(self) -> Iterator[Any]:
    _keys, _vals, _e = self._keys, self._vals, self._e
    for i in range(len(_keys)):
      if _keys[i] != _e:
        yield _vals[i]

  def items(self) -> Iterator[Tuple[int, Any]]:
    _keys, _vals, _e = self._keys, self._vals, self._e
    for i in range(len(_keys)):
      if _keys[i] != _e:
        yield _keys[i], _vals[i]

  def __str__(self):
    return '{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}'

  def __len__(self):
    return self._len

