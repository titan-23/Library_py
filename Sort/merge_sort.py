from typing import Iterable, TypeVar, Callable, List
from __pypy__ import newlist_hint
T = TypeVar('T')

def merge_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:
  def _sort(a: List[T]) -> List[T]:
    n = len(a)
    if n <= 1:
      return a
    if n == 2:
      if key(a[0], a[1]):
        return a
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
    while i < l:
      res.append(left[i])
      i += 1
    while j < r:
      res.append(right[j])
      j += 1
    return res
  return _sort(list(a))

