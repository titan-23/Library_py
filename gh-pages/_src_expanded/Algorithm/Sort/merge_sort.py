# from Library_py.Algorithm.Sort.merge_sort import merge_sort
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from typing import Iterable, TypeVar, Callable, List
from __pypy__ import newlist_hint
T = TypeVar('T', bound=SupportsLessThan)

def merge_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:
  def _sort(a: List[T]) -> List[T]:
    n = len(a)
    if n <= 1:
      return a
    if n == 2:
      if not key(a[0], a[1]):
        a[0], a[1] = a[1], a[0]
      return a
    left = _sort(a[:n//2])
    right = _sort(a[n//2:])
    res = newlist_hint(n)
    i, j, l, r = 0, 0, len(left), len(right)
    while i < l and j < r:
      if key(left[i], right[j]):
        res.append(left[i])
        i += 1
      else:
        res.append(right[j])
        j += 1
    for i in range(i, l):
      res.append(left[i])
    for j in range(j, r):
      res.append(right[j])
    return res
  return _sort(list(a))


