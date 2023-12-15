from Library_py.DataStructures.Set.WordsizeTreeSet import WordsizeTreeSet
from typing import List, Iterable, Optional, Iterator, Tuple

class WordsizeTreeMultiset():

  def __init__(self, u: int, a: Iterable[int]=[]):
    assert u >= 0
    self.u = u
    self.len: int = 0
    self.st: WordsizeTreeSet = WordsizeTreeSet(u, a)
    cnt = [0] * (u+1)
    for a_ in a:
      self.len += 1
      cnt[a_] += 1
    self.cnt: List[int] = cnt

  def add(self, x: int, val: int=1) -> None:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.add({x}), u={self.u}'
    self.len += val
    if self.cnt[x]:
      self.cnt[x] += val
    else:
      self.cnt[x] = val
      self.st.add(x)

  def discard(self, x: int, val: int=1) -> bool:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.discard({x}), u={self.u}'
    if self.cnt[x] == 0: return False
    v = self.cnt[x]
    if v > val:
      self.cnt[x] -= val
      self.len -= val
    else:
      self.len -= v
      self.cnt[x] = 0
      self.st.discard(x)
    return True

  def count(self, x: int) -> int:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.count({x}), u={self.u}'
    return self.cnt[x]

  def ge(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.ge({x}), u={self.u}'
    return self.st.ge(x)

  def gt(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.gt({x}), u={self.u}'
    return self.ge(x + 1)

  def le(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.le({x}), u={self.u}'
    return self.st.le(x)

  def lt(self, x: int) -> Optional[int]:
    assert 0 <= x < self.u, \
        f'ValueError: WordsizeTreeMultiset.lt({x}), u={self.u}'
    return self.le(x - 1)

  def get_min(self) -> Optional[int]:
    return self.st.ge(0)

  def get_max(self) -> Optional[int]:
    return self.st.le(self.st.u - 1)

  def pop_min(self) -> int:
    assert self, 'IndexError: pop_min() from empty WordsizeTreeMultiset.'
    x = self.st.get_min()
    self.discard(x)
    return x

  def pop_max(self) -> int:
    assert self, 'IndexError: pop_max() from empty WordsizeTreeMultiset.'
    x = self.st.get_max()
    self.discard(x)
    return x

  def keys(self) -> Iterator[int]:
    v = self.st.get_min()
    while v is not None:
      yield v
      v = self.st.gt(v)

  def values(self) -> Iterator[int]:
    v = self.st.get_min()
    while v is not None:
      yield self.cnt[v]
      v = self.st.gt(v)

  def items(self) -> Iterator[Tuple[int, int]]:
    v = self.st.get_min()
    while v is not None:
      yield (v, self.cnt[v])
      v = self.st.gt(v)

  def clear(self) -> None:
    for e in self:
      self.st.discard(e)
    self.len = 0
    self.cnt = [0] * (self.u+1)

  def tolist(self) -> List[int]:
    return [x for x in self]

  def __contains__(self, x: int):
    return self.cnt[x] > 0

  def __bool__(self):
    return self.len > 0

  def __len__(self):
    return self.len

  def __iter__(self):
    self.__val = self.st.get_min()
    self.__valcnt = 1
    return self

  def __next__(self):
    if self.__val is None:
      raise StopIteration
    pre = self.__val
    self.__valcnt += 1
    if self.__valcnt > self.cnt[self.__val]:
      self.__valcnt = 1
      self.__val = self.gt(self.__val)
    return pre

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return f'WordsizeTreeMultiset({self.u}, [' + ', '.join(map(str, self)) + '])'

