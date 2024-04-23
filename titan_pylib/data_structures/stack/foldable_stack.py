from typing import Generic, Iterable, TypeVar, Callable, Union, List
T = TypeVar('T')

class FoldableStack(Generic[T]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               e: T) -> None:
    self._op = op
    self._e = e
    if isinstance(n_or_a, int):
      self._n = n_or_a
      self._a = [e] * self._n
    else:
      n_or_a = list(n_or_a)
      self._n = len(n_or_a)
      self._a = list(n_or_a)
    self._data = [e] * (self._n+1)
    for i in range(self._n):
      self._data[i+1] = op(self._data[i], self._a[i])

  def append(self, key: T) -> None:
    self._a.append(key)
    self._data.append(self._op(self._data[-1], key))

  def top(self) -> T:
    return self._a[-1]

  def pop(self) -> T:
    self._data.pop()
    return self._a.pop()

  def all_prod(self) -> T:
    return self._data[-1]

  def prod(self, r: int) -> T:
    return self._data[r]

  def tolist(self) -> List[T]:
    return list(self._a)

  def __len__(self):
    return len(self._a)

