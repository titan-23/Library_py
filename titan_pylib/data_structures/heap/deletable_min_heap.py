from titan_pylib.data_structures.heap.min_heap import MinHeap
from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import TypeVar, Generic, Iterable

T = TypeVar("T", bound=SupportsLessThan)


class DeletableMinHeap(Generic[T]):

    def __init__(self, a: Iterable[T] = []) -> None:
        """削除可能Minヒープです。
        要素の 追加/削除/最小値取得 が効率よく行えます。
        """
        self.hq: MinHeap[T] = MinHeap(a)
        self.rem_hq: MinHeap[T] = MinHeap()
        self._len: int = len(self.hq)

    def push(self, key: T) -> None:
        """``key`` を追加します。
        :math:`O(\\log{n})` です。
        """
        self._len += 1
        if self.rem_hq and self.rem_hq.get_min() == key:
            self.rem_hq.pop_min()
            return
        self.hq.push(key)

    def remove(self, key: T) -> None:
        """``key`` を削除します。
        :math:`O(\\log{n})` です。
        """
        assert self._len > 0
        self._len -= 1
        if self.hq.get_min() == key:
            self.hq.pop_min()
        else:
            self.rem_hq.push(key)

    def _delete(self) -> None:
        while self.rem_hq and self.rem_hq.get_min() == self.hq.get_min():
            self.hq.pop_min()
            self.rem_hq.pop_min()

    def get_min(self) -> T:
        """最小の要素を返します。
        :math:`O(\\log{n})` です。
        """
        assert self._len > 0
        self._delete()
        return self.hq.get_min()

    def pop_min(self) -> T:
        """最小の要素を削除して返します。
        :math:`O(\\log{n})` です。
        """
        assert self._len > 0
        self._len -= 1
        self._delete()
        return self.hq.pop_min()

    def __len__(self) -> int:
        return self._len
