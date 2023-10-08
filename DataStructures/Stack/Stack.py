from typing import TypeVar, Generic, Iterable, List
T = TypeVar('T')

class Stack(Generic[T]):

  # コンセプト：popをしないStack

  def __init__(self, a: Iterable[T]=[]):
    self.data: List[T] = list(a)
    self.back: int = len(self.data)

  def pop(self) -> T:
    self.back -= 1
    return self.data[self.back]

  def append(self, val: T) -> None:
    if self.back < len(self.data):
      self.data[self.back] = val
    else:
      self.data.append(val)
    self.back += 1

  def top(self) -> T:
    return self.data[self.back-1]

  def __getitem__(self, k: int) -> T:
    if k < 0:
      k += self.back
    return self.data[k]

  def __contains__(self, val: T):
    return val in self.data

  def __iter__(self):
    self.__iter = -1
    return self

  def __next__(self):
    if self.__iter+1 >= self.back:
      raise StopIteration
    self.__iter += 1
    return self.data[self.__iter]

  def __len__(self):
    return self.back

  def __str__(self):
    return '[' + ', '.join(map(str, self)) + ']'

  def __repr__(self):
    return f'Stack({self})'

