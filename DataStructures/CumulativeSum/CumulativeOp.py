from typing import List, TypeVar, Callable
T = TypeVar('T')

class CumulativeOp():

  def __init__(self, a: List[T], op: Callable[[T, T], T], e: T):
    if not isinstance(a, list):
      a = list(a)
    n = len(a)
    acc = [e for _ in range(n+1)]
    for i in range(n):
      acc[i+1] = op(acc[i],  a[i])
    self.n = n
    self.acc = acc
    self.a = a

  def all_prod(self) -> T:
    return self.acc[-1]

  def prod(self, l: int, r: int) -> int:
    return self.acc[r] - self.acc[l]

  def __getitem__(self, k: int):
    return self.a[k]
