from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Iterable, TypeVar, Callable

T = TypeVar("T", bound=SupportsLessThan)


def merge_sort(
    a: Iterable[T], key: Callable[[T, T], bool] = lambda s, t: s < t
) -> list[T]:
    """マージソートです。安定なはずです。
    最悪 :math:`O(n\\log{n})` 時間です。

    Args:
        a (Iterable[T]): ソートする列です。
        key (Callable[[T, T], bool], optional): 比較関数 `key` にしたがって比較演算をします。
                                                (第1引数)<=(第2引数) のとき、 ``True`` を返すようにしてください。
    """

    def _sort(l: int, r: int) -> None:
        if r - l <= 1:
            return
        if r - l == 2:
            if not key(a[l], a[l + 1]):
                a[l], a[l + 1] = a[l + 1], a[l]
            return
        mid = (l + r) // 2
        _sort(l, mid)
        _sort(mid, r)
        i, j = l, mid
        indx = 0
        while i < mid and j < r:
            if key(a[i], a[j]):
                buff[indx] = a[i]
                i += 1
            else:
                buff[indx] = a[j]
                j += 1
            indx += 1
        for k in range(i, mid):
            a[l + indx + k - i] = a[k]
        for k in range(l, l + indx):
            a[k] = buff[k - l]

    a = list(a)
    buff = [0] * len(a)
    _sort(0, len(a))
    return a
