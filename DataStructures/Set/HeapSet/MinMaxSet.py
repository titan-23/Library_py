from typing import Generic, Iterable, TypeVar, List
T = TypeVar('T')

class MinMaxSet(Generic[T]):

  def __init__(self, a: Iterable[T]=[]):
    a = set(a)
    self.data = a
    self.heap = IntervalHeap(a)

  def add(self, key: T) -> bool:
    if key not in self.data:
      self.heap.add(key)
      self.data.add(key)
      return True
    return False

  def discard(self, key: T) -> bool:
    if key in self.data:
      self.data.discard(key)
      return True
    return False

  def pop_min(self) -> T:
    while True:
      v = self.heap.pop_min()
      if v in self.data:
        self.data.discard(v)
        return v

  def pop_max(self) -> T:
    while True:
      v = self.heap.pop_max()
      if v in self.data:
        self.data.discard(v)
        return v

  def get_min(self) -> T:
    while True:
      v = self.heap.get_min()
      if v in self.data:
        return v
      else:
        self.heap.pop_min()

  def get_max(self) -> T:
    while True:
      v = self.heap.get_max()
      if v in self.data:
        return v
      else:
        self.heap.pop_max()

  def tolist(self) -> List[T]:
    return sorted(self.data)

  def __contains__(self, key: T):
    return key in self.data

  def __getitem__(self, k: int):  # 末尾と先頭のみ
    if k == -1 or k == len(self.data)-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __len__(self):
    return len(self.data)

  def __str__(self):
    return '{' + ', '.join(map(str, sorted(self.data))) + '}'

  def __repr__(self):
    return f'MinMaxSet({self})'

