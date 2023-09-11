from typing import Callable, TypeVar, Generic
T = TypeVar('T')

class Doubling(Generic[T]):

  def __init__(self, n: int, lim: int, move_to: Callable[[T], T]):
    self.move_to = move_to
    self.n = n
    self.lim = lim
    self.log = lim.bit_length()
    self._build()

  def _build(self):
    db = [[0]*self.n for _ in range(self.log+1)]
    for i in range(n):
      db[0][i] = self.move_to(i)
    for k in range(self.log):
      for i in range(self.n):
        db[k+1][i] = db[k][db[k][i]]
    self.db = db

  def kth(self, start: T, k: int):
    now = start
    for i in range(self.log):
      if k & 1:
        now = self.db[i][now]
      k >>= 1
    return now

