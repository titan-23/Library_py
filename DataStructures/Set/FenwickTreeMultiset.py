from Library_py.DataStructures.Set.FenwickTreeSet import FenwickTreeSet
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

