from .WordsizeTreeSet import WordsizeTreeSet
from typing import TypeVar, Iterable, Optional, Generic
T = TypeVar('T')

class WordsizeTreeSetZ(Generic[T]):

  def __init__(self, _used: Iterable[T], a: Iterable[T]=[]):
    if isinstance(_used, set):
      _used = sorted(_used)
    else:
      _used = sorted(set(_used))
    self._to_zaatsu = {key: i for i, key in enumerate(_used)}
    self._to_origin = _used
    self.data = WordsizeTreeSet(len(_used), (self._to_zaatsu[x] for x in a))

  def add(self, x: T) -> bool:
    return self.data.add(self._to_zaatsu[x])

  def discard(self, x: int) -> bool:
    return self.data.discard(self._to_zaatsu[x])

  def ge(self, x: T) -> Optional[T]:
    res = self.data.ge(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def gt(self, x: T) -> Optional[T]:
    res = self.data.gt(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def le(self, x: T) -> Optional[T]:
    res = self.data.le(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def lt(self, x: T) -> Optional[T]:
    res = self.data.lt(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def get_min(self) -> T:
    return self._to_origin[self.data.ge(0)]

  def get_max(self) -> T:
    return self._to_origin[self.data.le(self.data.u - 1)]

  def pop_min(self) -> T:
    v = self.get_min()
    self.discard(v)
    return v

  def pop_max(self) -> T:
    v = self.get_max()
    self.discard(v)
    return v

  def clear(self) -> None:
    for e in self:
      self.discard(e)

  def __len__(self):
    return len(self.data)

  def __contains__(self, x: T):
    x = self._to_zaatsu[x]
    return self.data.data[0][x>>5] >> (x&31) & 1 == 1

  def __iter__(self):
    if len(self) == 0:
      return
    v = self.ge(self._to_origin[0])
    while v is not None:
      yield v
      v = self.gt(v)

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return 'WordsizeTreeSetZ(' + str(self) + ')'

class WordsizeTreeMultisetZ(Generic[T]):

  def __init__(self, _used: Iterable[T], a: Iterable[T]=[]):
    if isinstance(_used, set):
      _used = sorted(_used)
    else:
      _used = sorted(set(_used))
    self._to_zaatsu = {key: i for i, key in enumerate(_used)}
    self._to_origin = _used
    self.data = WordsizeTreeMultiset(len(_used), (self._to_zaatsu[x] for x in a))

  def add(self, x: T, val: int=1) -> None:
    self.data.add(self._to_zaatsu[x], val)

  def discard(self, x: T, val: int=1) -> bool:
    return self.data.discard(self._to_zaatsu[x], val)

  def count(self, x: T) -> int:
    x = self._to_zaatsu[x]
    return self.data.cnt[x] if x in self.data.cnt else 0

  def ge(self, x: T) -> Optional[T]:
    res = self.data.ge(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def gt(self, x: T) -> Optional[T]:
    res = self.data.gt(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def le(self, x: T) -> Optional[T]:
    res = self.data.le(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def lt(self, x: T) -> Optional[T]:
    res = self.data.lt(self._to_zaatsu[x])
    return None if res is None else self._to_origin[res]

  def get_min(self) -> T:
    return self._to_origin[self.data.ge(0)]

  def get_max(self) -> T:
    return self._to_origin[self.data.le(self.data.u - 1)]

  def pop_min(self) -> T:
    return self._to_origin[self.data.pop_min()]

  def pop_max(self) -> T:
    return self._to_origin[self.data.pop_max()]

  def keys(self):
    if len(self) == 0:
      return
    v = self.get_min()
    while v is not None:
      yield v
      v = self.gt(v)

  def values(self):
    if len(self) == 0:
      return
    v = self.get_min()
    while v is not None:
      yield self.cnt[v]
      v = self.gt(v)

  def items(self):
    if len(self) == 0:
      return
    v = self.get_min()
    while v is not None:
      yield (v, self.data.cnt[v])
      v = self.gt(v)

  def clear(self) -> None:
    for e in self:
      self.discard(e)

  def __contains__(self, x: T):
    return x in self.data

  def __len__(self):
    return self.data.len

  def __iter__(self):
    if len(self) == 0:
      return
    v = self.get_min()
    while v is not None:
      for _ in range(self.count(v)):
        yield v
      v = self.gt(v)

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return 'WordsizeTreeMultisetZ([' + ', '.join(map(str, self)) + '])'

