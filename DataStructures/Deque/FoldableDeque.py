from Library_py.DataStructures.Stack.FoldableStack import FoldableStack
from typing import Generic, Iterable, TypeVar, Callable, Union, List
T = TypeVar('T')

class FoldableDeque(Generic[T]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               e: T) -> None:
    self._op = op
    self._e = e
    self.front: FoldableStack[T] = FoldableStack(0, op, e)
    self.back: FoldableStack[T] = FoldableStack(n_or_a, op, e)

  def _rebuild(self) -> None:
    new = self.front.tolist()[::-1] + self.back.tolist()
    self.front = FoldableStack(new[:len(new)//2][::-1], self._op, self._e)
    self.back = FoldableStack(new[len(new)//2:], self._op, self._e)

  def tolist(self) -> List[T]:
    return self.front.tolist()[::-1] + self.back.tolist()

  def append(self, v: T) -> None:
    self.back.append(v)

  def appendleft(self, v: T) -> None:
    self.front.append(v)

  def pop(self) -> T:
    if not self.back:
      self._rebuild()
    return self.back.pop() if self.back else self.front.pop()

  def popleft(self) -> T:
    if not self.front:
      self._rebuild()
    return self.front.pop() if self.front else self.back.pop()

  def all_prod(self) -> T:
    return self._op(self.front.all_prod(), self.back.all_prod())

  def __len__(self):
    return len(self.front) + len(self.back)

