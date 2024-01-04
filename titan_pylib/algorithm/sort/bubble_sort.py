from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import TypeVar, Callable, List
T = TypeVar('T', bound=SupportsLessThan)

def bubble_sort(a: List[T], key: Callable[[T, T], bool]=lambda s, t: s < t, inplace: bool=True) -> List[T]:
  n = len(a)
  for i in range(n):
    flag = True
    for j in range(n-1, i-1, -1):
      if not key(a[j-1], a[j]):
        a[j], a[j-1] = a[j-1], a[j]
        flag = False
    if flag:
      break
  return a

