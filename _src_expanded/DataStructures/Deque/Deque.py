from typing import Iterable, List, Generic, TypeVar
T = TypeVar('T')

class Deque(Generic[T]):

  # コンセプト: ランダムアクセスO(1)でできるDeque
  # pop / popleft: O(1)
  # append / appendleft: O(1)
  # tolist: O(N)
  # getitem / setitem: O(1)
  # contains: O(N)

  def __init__(self, a: Iterable[T]=[]):
    self.front: List[T] = []
    self.back: List[T] = list(a)

  def _rebuild(self) -> None:
    new = self.front[::-1] + self.back
    self.front = new[:len(new)//2][::-1]
    self.back = new[len(new)//2:]

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

  def tolist(self) -> List[T]:
    return self.front[::-1] + self.back

  def __getitem__(self, k: int) -> T:
    assert -len(self) <= k < len(self), \
        f'IndexError, Deque.__getitem__({k}), len={len(self)}'
    if k < 0:
      k += len(self)
    return self.front[len(self.front)-k-1] if k < len(self.front) else self.back[k-len(self.front)]

  def __setitem__(self, k: int, v: T):
    assert -len(self) <= k < len(self), \
        f'IndexError, Deque.__setitem__({k}, {v}), len={len(self)}'
    if k < 0:
      k += len(self)
    if k < len(self.front):
      self.front[len(self.front)-k-1] = v
    else:
      self.back[k-len(self.front)] = v

  def __bool__(self):
    return bool(self.front or self.back)

  def __len__(self):
    return len(self.front) + len(self.back)

  def __contains__(self, v: T):
    return (v in self.front) or (v in self.back)

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'Deque({self})'


