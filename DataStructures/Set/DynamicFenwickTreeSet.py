from typing import Iterable, Set, TypeVar, Generic, Tuple, Optional
T = TypeVar("T")

class DynamicFenwickTreeSet(Generic[T]):

  # Build a new FenwickTreeSet. / O(1)
  # 整数[0, u)を、空間O(qlogu)/時間O(qlogu)
  def __init__(self, u: int, a: Iterable[T]=[], _multi=False):
    self._size = u
    self._len = 0
    self._cnt = {}
    self._fw = DynamicFenwickTree(self._size)
    for _a in a:
      self.add(_a)

  def add(self, key: T) -> bool:
    if key in self._cnt:
      return False
    self._len += 1
    self._cnt[key] = 1
    self._fw.add(key, 1)
    return True

  def remove(self, key: T) -> None:
    if self.discard(key): return
    raise KeyError(key)

  def discard(self, key: T) -> bool:
    if key in self._cnt:
      self._len -= 1
      del self._cnt[key]
      self._fw.add(key, -1)
      return True
    return False

  def le(self, key: T) -> Optional[T]:
    if key in self._cnt: return key
    pref = self._fw.pref(key) - 1
    return None if pref < 0 else self._fw.bisect_right(pref)

  def lt(self, key: T) -> Optional[T]:
    pref = self._fw.pref(key) - 1
    return None if pref < 0 else self._fw.bisect_right(pref)

  def ge(self, key: T) -> Optional[T]:
    if key in self._cnt: return key
    pref = self._fw.pref(key + 1)
    return None if pref >= self._len else self._fw.bisect_right(pref)

  def gt(self, key: T) -> Optional[T]:
    pref = self._fw.pref(key + 1)
    return None if pref >= self._len else self._fw.bisect_right(pref)

  def index(self, key: T) -> int:
    return self._fw.pref(key)

  def index_right(self, key: T) -> int:
    return self._fw.pref(key + 1)

  def __getitem__(self, k):
    if k < 0: k += self._len
    return self._fw.bisect_right(k)

  def __repr__(self):
    return f'DynamicFenwickTreeSet({self})'

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

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

  def __contains__(self, key: T):
    return key in self._cnt

  def __bool__(self):
    return self._len > 0

  def pop(self, k: int=-1):
    x = self.__getitem__(k)
    self.discard(x)
    return x

  def pop_min(self):
    x = self.__getitem__(0)
    self.discard(x)
    return x


class DynamicFenwickTreeMultiset(DynamicFenwickTreeSet, Generic[T]):

  def __init__(self, n: int, a: Iterable[T]=[]) -> None:
    super().__init__(n, a, _multi=True)

  def add(self, key: T, val: int=1) -> None:
    self._len += val
    if key in self._cnt:
      self._cnt[key] += val
    else:
      self._cnt[key] = val
    self._fw.add(key, val)

  def discard(self, key: T, val: int=1) -> bool:
    if key not in self._cnt:
      return False
    cnt = self._cnt[key]
    if val >= cnt:
      self._len -= cnt
      del self._cnt[key]
      self._fw.add(key, -cnt)
    else:
      self._len -= val
      self._cnt[key] -= val
      self._fw.add(key, -val)
    return True

  def discard_all(self, key: T) -> bool:
    return self.discard(key, val=self.count(key))

  def count(self, key: T) -> int:
    return self._cnt[key]

  def items(self) -> Iterable[Tuple[T, int]]:
    _iter = 0
    while _iter < self._len:
      res = self.__getitem__(_iter)
      cnt = self.count(res)
      _iter += cnt
      yield res, cnt

  def show(self) -> None:
    print('{' + ', '.join(f'{i[0]}: {i[1]}' for i in self.items()) + '}')

  def __repr__(self):
    return f'DynamicFenwickTreeMultiset({self})'

