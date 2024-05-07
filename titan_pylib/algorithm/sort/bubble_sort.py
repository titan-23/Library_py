from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import TypeVar, Callable, List

T = TypeVar("T", bound=SupportsLessThan)


def bubble_sort(
    a: List[T], key: Callable[[T, T], bool] = lambda s, t: s < t, inplace: bool = True
) -> List[T]:
    """バブルソートです。

    非破壊的です。
    最悪 :math:`O(n^2)` 時間です。

    Args:
      a (Iterable[T]): ソートする列です。
      key (Callable[[T, T], bool], optional): 比較関数 `key` にしたがって比較演算をします。
                                              (第1引数)<(第2引数) のとき、 ``True`` を返すようにしてください。
    """
    a = a[:] if inplace else a
    n = len(a)
    for i in range(n):
        flag = True
        for j in range(n - 1, i - 1, -1):
            if not key(a[j - 1], a[j]):
                a[j], a[j - 1] = a[j - 1], a[j]
                flag = False
        if flag:
            break
    return a
