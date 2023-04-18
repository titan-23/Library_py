from typing import Iterable, List, Any

class Deque():

  # コンセプト: ランダムアクセスO(1)でできるDeque
  # pop/popleft: O(1)
  # append/appendleft: O(1)
  # tolist: O(N)
  # getitem/setitem: O(1)
  # contains: O(N)

  def __init__(self, a: Iterable[Any]=[]):
    self.front = []
    self.back = list(a)

  def _rebuild(self) -> None:
    new = self.front[::-1] + self.back
    self.front = new[:len(new)//2][::-1]
    self.back = new[len(new)//2:]

  def pop(self) -> Any:
    if not self.back:
      self._rebuild()
    return self.back.pop() if self.back else self.front.pop()

  def popleft(self) -> Any:
    if not self.front:
      self._rebuild()
    return self.front.pop() if self.front else self.back.pop()

  def append(self, v: Any) -> None:
    self.back.append(v)

  def appendleft(self, v: Any) -> None:
    self.front.append(v)

  def tolist(self) -> List[Any]:
    return self.front[::-1] + self.back

  def __getitem__(self, k: int) -> Any:
    if k < 0: k += len(self)
    return self.front[len(self.front)-k-1] if k < len(self.front) else self.back[k-len(self.front)]

  def __setitem__(self, k: int, v: Any):
    if k < 0: k += len(self)
    if k < len(self.front):
      self.front[len(self.front)-k-1] = v
    else:
      self.back[k-len(self.front)] = v

  def __bool__(self):
    return self.front or self.back

  def __len__(self):
    return len(self.front) + len(self.back)

  def __contains__(self, v):
    return (v in self.front) or (v in self.back)

  def __str__(self):
    return str(self.tolist())

  def __repr__(self):
    return f'Deque({self})'

