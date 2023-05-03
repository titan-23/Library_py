from typing import Iterable, TypeVar, Generic, Union, Tuple, Optional
T = TypeVar('T')

class FenwickTreeSet(Generic[T]):

  def __init__(self, _used: Union[int, Iterable[T]], _a: Iterable[T]=[], compress=False, _multi=False):
    _used = range(_used) if isinstance(_used, int) else sorted(set(_used))
    self._size = len(_used)
    self._len = 0
    self._to_zaatsu = {key: i for i, key in enumerate(_used)} if compress else _used
    self._to_origin = _used
    self._cnt = [0] * self._size
    if _a:
      a_ = [0] * self._size
      if _multi:
        self._len = len(_a)
        for v in _a:
          i = self._to_zaatsu[v]
          a_[i] += 1
          self._cnt[i] += 1
      else:
        for v in _a:
          i = self._to_zaatsu[v]
          if self._cnt[i] == 0:
            self._len += 1
            a_[i] = 1
            self._cnt[i] = 1
      a_.insert(0, 0)
      for i in range(1, self._size):
        if i + (i & -i) <= self._size:
          a_[i + (i & -i)] += a_[i]
      self._fw = a_
    else:
      self._fw = [0] * (self._size+1)
    self._fw_s = 1 << (self._size-1).bit_length()

  def _add(self, k: int, x: int) -> None:
    k += 1
    while k <= self._size:
      self._fw[k] += x
      k += k & -k

  def _pref(self, r: int) -> int:
    ret = 0
    while r:
      ret += self._fw[r]
      r -= r & -r
    return ret

  def _bisect_right(self, w: int) -> int:
    i, s = 0, self._fw_s
    while s:
      if i + s <= self._size and self._fw[i + s] <= w:
        w -= self._fw[i + s]
        i += s
      s >>= 1
    return i

  def add(self, key: T) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i]:
      return False
    self._len += 1
    self._cnt[i] = 1
    self._add(i, 1)
    return True

  def remove(self, key: T) -> None:
    if not self.discard(key):
      raise KeyError(key)

  def discard(self, key: T) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i]:
      self._len -= 1
      self._cnt[i] = 0
      self._add(i, -1)
      return True
    return False

  def le(self, key: T) -> Optional[T]:
    i = self._to_zaatsu[key]
    if self._cnt[i]: return key
    pref = self._pref(i) - 1
    return None if pref < 0 else self._to_origin[self._bisect_right(pref)]

  def lt(self, key: T) -> Optional[T]:
    pref = self._pref(self._to_zaatsu[key]) - 1
    return None if pref < 0 else self._to_origin[self._bisect_right(pref)]

  def ge(self, key: T) -> Optional[T]:
    i = self._to_zaatsu[key]
    if self._cnt[i]: return key
    pref = self._pref(i + 1)
    return None if pref >= self._len else self._to_origin[self._bisect_right(pref)]

  def gt(self, key: T) -> Optional[T]:
    pref = self._pref(self._to_zaatsu[key] + 1)
    return None if pref >= self._len else self._to_origin[self._bisect_right(pref)]

  def index(self, key: T) -> int:
    return self._pref(self._to_zaatsu[key])

  def index_right(self, key: T) -> int:
    return self._pref(self._to_zaatsu[key] + 1)

  def pop(self, k: int=-1) -> T:
    assert -self._len <= k < self._len, \
        f'IndexError: FenwickTreeSet.pop({k}), Index out of range.'
    if k < 0: k += self._len
    self._len -= 1
    i, acc, s = 0, 0, self._fw_s
    while s:
      if i+s <= self._size:
        if acc + self._fw[i+s] <= k:
          acc += self._fw[i+s]
          i += s
        else:
          self._fw[i+s] -= 1
      s >>= 1
    self._cnt[i] = 0
    return self._to_origin[i]

  def pop_min(self) -> T:
    assert self._len > 0, \
        f'IndexError: FenwickTreeSet.pop_min(), Index out of range.'
    return self.pop(0)

  def __getitem__(self, k):
    assert -self._len <= k < self._len, \
        f'IndexError: {self.classname}.__getitem__({k}), Index out of range.'
    if k < 0: k += self._len
    return self._to_origin[self._bisect_right(k)]

  def __repr__(self):
    return f'FenwickTreeSet({self})'

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter == self._len:
      raise StopIteration
    res = self._to_origin[self._bisect_right(self._iter)]
    self._iter += 1
    return res

  def __reversed__(self):
    _to_origin = self._to_origin
    for i in range(self._len):
      yield _to_origin[self._bisect_right(self._len-i-1)]

  def __len__(self):
    return self._len

  def __contains__(self, key: T):
    return self._cnt[self._to_zaatsu[key]] > 0

  def __bool__(self):
    return self._len > 0


from typing import Iterable, Set, TypeVar, Generic, Union, Tuple, Optional
T = TypeVar('T')

class FenwickTreeMultiset(FenwickTreeSet, Generic[T]):

  def __init__(self, used: Union[int, Iterable[T]], a: Iterable[T]=[], compress=True) -> None:
    super().__init__(used, a, compress=compress, _multi=True)

  def add(self, key: T, num: int=1) -> None:
    if num <= 0: return
    i = self._to_zaatsu[key]
    self._len += num
    self._cnt[i] += num
    self._add(i, num)

  def discard(self, key: T, num: int=1) -> bool:
    cnt = self.count(key)
    if num > cnt:
      num = cnt
    if num <= 0: return False
    i = self._to_zaatsu[key]
    self._len -= num
    self._cnt[i] -= num
    self._add(i, -num)
    return True

  def discard_all(self, key: T) -> bool:
    return self.discard(key, num=self.count(key))

  def count(self, key: T) -> int:
    return self._cnt[self._to_zaatsu[key]]

  def le(self, key: T) -> Optional[T]:
    i = self._to_zaatsu[key]
    if self._cnt[i] > 0: return key
    pref = self._pref(i) - 1
    return None if pref < 0 else self._to_origin[self._bisect_right(pref)]

  def ge(self, key: T) -> Optional[T]:
    i = self._to_zaatsu[key]
    if self._cnt[i] > 0: return key
    pref = self._pref(i + 1)
    return None if pref >= self._len else self._to_origin[self._bisect_right(pref)]

  def pop(self, k: int=-1) -> T:
    assert -self._len <= k < self._len, \
        f'IndexError: FenwickTreeMultiset.pop({k}), Index out of range.'
    if k < 0: k += self._len
    self._len -= 1
    i, acc, s = 0, 0, self._fw_s
    while s:
      if i+s <= self._size:
        if acc + self._fw[i+s] <= k:
          acc += self._fw[i+s]
          i += s
        else:
          self._fw[i+s] -= 1
      s >>= 1
    self._cnt[i] -= 1
    return self._to_origin[i]

  def pop_min(self) -> T:
    assert self._len > 0, \
        f'IndexError: FenwickTreeMultiset.pop_min(), Index out of range.'
    return self.pop(0)

  def items(self) -> Iterable[Tuple[T, int]]:
    _iter = 0
    while _iter < self._len:
      res = self._to_origin[self._bisect_right(_iter)]
      cnt = self.count(res)
      _iter += cnt
      yield res, cnt

  def show(self) -> None:
    print('{' + ', '.join(f'{i[0]}: {i[1]}' for i in self.items()) + '}')

  def __repr__(self):
    return f'FenwickTreeMultiset({self})'

