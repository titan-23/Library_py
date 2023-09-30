from typing import Generic, TypeVar, Callable, Iterable
T = TypeVar('T')

class CumulativeOp(Generic[T]):

  def __init__(self, a: Iterable[T], op: Callable[[T, T], T], inv: Callable[[T], T], e: T):
    a = list(a)
    n = len(a)
    acc = [e for _ in range(n+1)]
    for i in range(n):
      acc[i+1] = op(acc[i],  a[i])
    self.n = n
    self.acc = acc
    self.a = a
    self.op = op
    self.inv = inv

  def pref(self, r: int) -> T:
    return self.acc[r]

  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self.n, f'IndexError'
    return self.op(self.acc[r], self.inv(self.acc[l]))

  def all_prod(self) -> T:
    return self.acc[-1]

  def __getitem__(self, k: int) -> T:
    return self.a[k]
  
  def __len__(self):
    return len(self.a)
  
  def __str__(self):
    return str(self.acc)
  
  __repr__ = __str__


