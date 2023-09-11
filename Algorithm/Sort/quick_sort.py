from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Iterable, TypeVar, Callable, List
import random
T = TypeVar('T', bound=SupportsLessThan)

def quick_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:
  a = list(a)
  def sort(i: int, j: int):
    if i >= j: return
    pivot = a[random.randint(i, j)]
    l, r = i, j
    while True:
      while key(a[l], pivot):
        l += 1
      while key(pivot, a[r]):
        r -= 1
      if l >= r:
        break
      a[l], a[r] = a[r], a[l]
      l += 1
      r -= 1
    sort(i, l-1)
    sort(r+1, j)
  sort(0, len(a)-1)
  return a
