# from Library_py.DataStructures.Set.FenwickTreeMultiset import FenwickTreeMultiset
# from Library_py.DataStructures.Set.FenwickTreeSet import FenwickTreeSet
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

# from Library_py.DataStructures.FenwickTree.FenwickTree import FenwickTree
from typing import List, Union, Iterable, Optional

class FenwickTree():

  def __init__(self, n_or_a: Union[Iterable[int], int]):
    if isinstance(n_or_a, int):
      self._size = n_or_a
      self._tree = [0] * (self._size + 1)
    else:
      a = n_or_a if isinstance(n_or_a, list) else list(n_or_a)
      self._size = len(a)
      self._tree = [0] + a
      for i in range(1, self._size):
        if i + (i & -i) <= self._size:
          self._tree[i + (i & -i)] += self._tree[i]
    self._s = 1 << (self._size - 1).bit_length()

  def pref(self, r: int) -> int:
    assert 0 <= r <= self._size, \
        f'IndexError: FenwickTree.pref({r}), n={self._size}'
    ret, _tree = 0, self._tree
    while r > 0:
      ret += _tree[r]
      r &= r - 1
    return ret

  def suff(self, l: int) -> int:
    assert 0 <= l < self._size, \
        f'IndexError: FenwickTree.suff({l}), n={self._size}'
    return self.pref(self._size) - self.pref(l)

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self._size, \
        f'IndexError: FenwickTree.sum({l}, {r}), n={self._size}'
    _tree = self._tree
    res = 0
    while r > l:
      res += _tree[r]
      r &= r - 1
    while l > r:
      res -= _tree[l]
      l &= l - 1
    return res

  prod = sum

  def __getitem__(self, k: int) -> int:
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTree.__getitem__({k}), n={self._size}'
    if k < 0:
      k += self._size
    return self.sum(k, k+1)

  def add(self, k: int, x: int) -> None:
    assert 0 <= k < self._size, \
        f'IndexError: FenwickTree.add({k}, {x}), n={self._size}'
    k += 1
    _tree = self._tree
    while k <= self._size:
      _tree[k] += x
      k += k & -k

  def __setitem__(self, k: int, x: int):
    assert -self._size <= k < self._size, \
        f'IndexError: FenwickTree.__setitem__({k}, {x}), n={self._size}'
    if k < 0: k += self._size
    pre = self.__getitem__(k)
    self.add(k, x - pre)

  def bisect_left(self, w: int) -> Optional[int]:
    i, s, _size, _tree = 0, self._s, self._size, self._tree
    while s:
      if i + s <= _size and _tree[i + s] < w:
        w -= _tree[i + s]
        i += s
      s >>= 1
    return i if w else None

  def bisect_right(self, w: int) -> int:
    i, s, _size, _tree = 0, self._s, self._size, self._tree
    while s:
      if i + s <= _size and _tree[i + s] <= w:
        w -= _tree[i + s]
        i += s
      s >>= 1
    return i

  def _pop(self, k: int) -> int:
    assert k >= 0
    i, acc, s, _size, _tree = 0, 0, self._s, self._size, self._tree
    while s:
      if i+s <= _size:
        if acc + _tree[i+s] <= k:
          acc += _tree[i+s]
          i += s
        else:
          _tree[i+s] -= 1
      s >>= 1
    return i

  def show(self) -> None:
    print('[' + ', '.join(map(str, (self.pref(i) for i in range(self._size+1)))) + ']')

  def tolist(self) -> List[int]:
    sub = [self.pref(i) for i in range(self._size+1)]
    return [sub[i+1]-sub[i] for i in range(self._size)]

  @staticmethod
  def get_inversion_num(a: List[int], compress: bool=False) -> int:
    inv = 0
    if compress:
      a_ = sorted(set(a))
      z = {e: i for i, e in enumerate(a_)}
      fw = FenwickTree(len(a_))
      for i, e in enumerate(a):
        inv += i - fw.pref(z[e])
        fw.add(z[e], 1)
    else:
      fw = FenwickTree(len(a))
      for i, e in enumerate(a):
        inv += i - fw.pref(e)
        fw.add(e, 1)
    return inv

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'FenwickTree({self})'

from typing import Dict, Iterable, TypeVar, Generic, Union, Optional
T = TypeVar('T', bound=SupportsLessThan)

class FenwickTreeSet(Generic[T]):

  def __init__(self, _used: Union[int, Iterable[T]], _a: Iterable[T]=[], compress=True, _multi=False):
    self._len = 0
    self._to_origin = list(range(_used)) if isinstance(_used, int) else sorted(set(_used))
    self._to_zaatsu: Dict[T, int] = {key: i for i, key in enumerate(self._to_origin)} if compress else self._to_origin
    self._size = len(self._to_origin)
    self._cnt = [0] * self._size
    _a = list(_a)
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
      self._fw = FenwickTree(a_)
    else:
      self._fw = FenwickTree(self._size)

  def add(self, key: T) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i]:
      return False
    self._len += 1
    self._cnt[i] = 1
    self._fw.add(i, 1)
    return True

  def remove(self, key: T) -> None:
    if not self.discard(key):
      raise KeyError(key)

  def discard(self, key: T) -> bool:
    i = self._to_zaatsu[key]
    if self._cnt[i]:
      self._len -= 1
      self._cnt[i] = 0
      self._fw.add(i, -1)
      return True
    return False

  def le(self, key: T) -> Optional[T]:
    i = self._to_zaatsu[key]
    if self._cnt[i]: return key
    pref = self._fw.pref(i) - 1
    return None if pref < 0 else self._to_origin[self._fw.bisect_right(pref)]

  def lt(self, key: T) -> Optional[T]:
    pref = self._fw.pref(self._to_zaatsu[key]) - 1
    return None if pref < 0 else self._to_origin[self._fw.bisect_right(pref)]

  def ge(self, key: T) -> Optional[T]:
    i = self._to_zaatsu[key]
    if self._cnt[i]: return key
    pref = self._fw.pref(i + 1)
    return None if pref >= self._len else self._to_origin[self._fw.bisect_right(pref)]

  def gt(self, key: T) -> Optional[T]:
    pref = self._fw.pref(self._to_zaatsu[key] + 1)
    return None if pref >= self._len else self._to_origin[self._fw.bisect_right(pref)]

  def index(self, key: T) -> int:
    return self._fw.pref(self._to_zaatsu[key])

  def index_right(self, key: T) -> int:
    return self._fw.pref(self._to_zaatsu[key] + 1)

  def pop(self, k: int=-1) -> T:
    assert -self._len <= k < self._len, \
        f'IndexError: FenwickTreeSet.pop({k}), Index out of range.'
    if k < 0: k += self._len
    self._len -= 1
    x = self._fw._pop(k)
    self._cnt[x] = 0
    return self._to_origin[x]

  def pop_min(self) -> T:
    assert self._len > 0, \
        f'IndexError: pop_min() from empty {self.__class__.__name__}.'
    return self.pop(0)

  def pop_max(self) -> T:
    assert self._len > 0, \
        f'IndexError: pop_max() from empty {self.__class__.__name__}.'
    return self.pop(-1)

  def get_min(self) -> Optional[T]:
    if not self: return
    return self[0]

  def get_max(self) -> Optional[T]:
    if not self: return
    return self[-1]

  def __getitem__(self, k):
    assert -self._len <= k < self._len, \
        f'IndexError: FenwickTreeSet[{k}], Index out of range.'
    if k < 0: k += self._len
    return self._to_origin[self._fw.bisect_right(k)]

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter == self._len:
      raise StopIteration
    res = self._to_origin[self._fw.bisect_right(self._iter)]
    self._iter += 1
    return res

  def __reversed__(self):
    _to_origin = self._to_origin
    for i in range(self._len):
      yield _to_origin[self._fw.bisect_right(self._len-i-1)]

  def __len__(self):
    return self._len

  def __contains__(self, key: T):
    return self._cnt[self._to_zaatsu[key]] > 0

  def __bool__(self):
    return self._len > 0

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return f'{self.__class__.__name__}({self})'

from typing import Iterable, TypeVar, Generic, Union, Tuple
T = TypeVar('T')

class FenwickTreeMultiset(FenwickTreeSet, Generic[T]):

  def __init__(self, used: Union[int, Iterable[T]], a: Iterable[T]=[], compress=True) -> None:
    super().__init__(used, a, compress=compress, _multi=True)

  def add(self, key: T, num: int=1) -> None:
    if num <= 0: return
    i = self._to_zaatsu[key]
    self._len += num
    self._cnt[i] += num
    self._fw.add(i, num)

  def discard(self, key: T, num: int=1) -> bool:
    cnt = self.count(key)
    if num > cnt:
      num = cnt
    if num <= 0: return False
    i = self._to_zaatsu[key]
    self._len -= num
    self._cnt[i] -= num
    self._fw.add(i, -num)
    return True

  def discard_all(self, key: T) -> bool:
    return self.discard(key, num=self.count(key))

  def count(self, key: T) -> int:
    return self._cnt[self._to_zaatsu[key]]

  def pop(self, k: int=-1) -> T:
    assert -self._len <= k < self._len, \
        f'IndexError: FenwickTreeMultiset.pop({k}), len={self._len}'
    x = self[k]
    self.discard(x)
    return x

  def pop_min(self) -> T:
    assert self._len > 0, \
        f'IndexError: pop_min() from empty {self.__class__.__name__}.'
    return self.pop(0)

  def pop_max(self) -> T:
    assert self._len > 0, \
        f'IndexError: pop_max() from empty {self.__class__.__name__}.'
    return self.pop(-1)

  def items(self) -> Iterable[Tuple[T, int]]:
    _iter = 0
    while _iter < self._len:
      res = self._to_origin[self._bisect_right(_iter)]
      cnt = self.count(res)
      _iter += cnt
      yield res, cnt

  def show(self) -> None:
    print('{' + ', '.join(f'{i[0]}: {i[1]}' for i in self.items()) + '}')


