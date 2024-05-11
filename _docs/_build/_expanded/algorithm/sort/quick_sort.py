# from titan_pylib.algorithm.sort.quick_sort import quick_sort
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
from typing import Iterable, TypeVar, Callable, List
import random

T = TypeVar("T", bound=SupportsLessThan)


def quick_sort(
    a: Iterable[T], key: Callable[[T, T], bool] = lambda s, t: s < t
) -> List[T]:
    """クイックソートです。

    非破壊的です。
    期待 :math:`O(n\\log{n})` 時間です。

    Args:
      a (Iterable[T]): ソートする列です。
      key (Callable[[T, T], bool], optional): 比較関数 `key` にしたがって比較演算をします。
                                              (第1引数)<(第2引数) のとき、 ``True`` を返すようにしてください。
    """
    a = list(a)

    def sort(i: int, j: int):
        if i >= j:
            return
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
        sort(i, l - 1)
        sort(r + 1, j)

    sort(0, len(a) - 1)
    return a
