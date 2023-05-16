from typing import Generic, Iterable, TypeVar, List
T = TypeVar('T')

class MinMaxMultiset(Generic[T]):

  def __init__(self, a: Iterable[T]=[]):
    a = list(a)
    data = {}
    for x in a:
      if x in data:
        data[x] += 1
      else:
        data[x] = 1
    self.data = data
    self.heap = DoubleEndedHeap(a)
    self.len = len(a)

  def add(self, key: T, val: int=1) -> None:
    if val == 0: return
    self.heap.add(key)
    if key in self.data:
      self.data[key] += val
    else:
      self.data[key] = val
    self.len += val

  def discard(self, key: T, val: int=1) -> bool:
    if key not in self.data: return False
    cnt = self.data[key]
    if val < cnt:
      self.len -= val
      self.data[key] -= val
    else:
      self.len -= cnt
      del self.data[key]
    return True

  def pop_min(self) -> T:
    while True:
      v = self.heap.get_min()
      if v in self.data:
        if self.data[v] == 1:
          self.heap.pop_min()
          del self.data[v]
        else:
          self.data[v] -= 1
        self.len -= 1
        return v
      self.heap.pop_min()

  def pop_max(self) -> T:
    while True:
      v = self.heap.get_max()
      if v in self.data:
        self.len -= 1
        if self.data[v] == 1:
          self.heap.pop_max()
          del self.data[v]
        else:
          self.data[v] -= 1
        return v
      self.heap.pop_max()

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

  def count(self, key: T) -> int:
    return self.data[key]

  def tolist(self) -> List[T]:
    return sorted(k for k, v in self.data.items() for _ in range(v))

  def len_elm(self) -> int:
    return len(self.data)

  def __contains__(self, key: T):
    return key in self.data

  def __getitem__(self, k: int):  # 末尾と先頭のみ
    if k == -1 or k == self.len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __len__(self):
    return self.len

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'MinMaxMultiset([' + ', '.join(map(str, self.tolist())) + '])'

