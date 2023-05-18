from typing import Iterable, TypeVar, Callable, List
T = TypeVar('T')

def quick_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:
  def sort(i: int, j: int):
    if i >= j: return
    pivot = a[i]
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
  a = list(a)
  sort(0, len(a)-1)
  return a

