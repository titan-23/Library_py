from titan_pylib.data_structures.set.fenwick_tree_set import FenwickTreeSet
from typing import Iterable, TypeVar, Generic, Union, Tuple
T = TypeVar('T')

class FenwickTreeMultiset(FenwickTreeSet, Generic[T]):

  def __init__(self,
               used: Union[int, Iterable[T]],
               a: Iterable[T]=[],
               compress: bool=True
               ) -> None:
    """
    Args:
      used (Union[int, Iterable[T]]): 使用する要素の集合
      a (Iterable[T], optional): 初期集合
      compress (bool, optional): 座圧するかどうか( ``True`` : する)
    """
    super().__init__(used, a, compress=compress, _multi=True)

  def add(self, key: T, num: int=1) -> None:
    if num <= 0: return
    i = self._to_zaatsu[key]
    self._len += num
    self._cnt[i] += num
    self._fw.add(i, num)

  def remove(self, key: T, num: int=1) -> None:
    if not self.discard(key, num):
      raise KeyError(key)

  def discard(self, key: T, num: int=1) -> bool:
    i = self._to_zaatsu[key]
    num = min(num, self._cnt[i])
    if num <= 0: return False
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
        f'IndexError: {self.__class__.__name__}.pop({k}), len={self._len}'
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
