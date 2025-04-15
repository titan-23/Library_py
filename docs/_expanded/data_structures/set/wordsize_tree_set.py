# from titan_pylib.data_structures.set.wordsize_tree_set import WordsizeTreeSet
from array import array
from typing import Iterable, Optional


class WordsizeTreeSet:
    """``[0, u)`` の整数集合を管理する32分木です。
    空間 :math:`O(u)` であることに注意してください。
    """

    def __init__(self, u: int, a: Iterable[int] = []) -> None:
        """:math:`O(u)` です。"""
        assert u >= 0
        u += 1  # 念のため
        self.u = u
        data = []
        len_ = 0
        if a:
            u >>= 5
            A = array("I", bytes(4 * (u + 1)))
            for a_ in a:
                assert (
                    0 <= a_ < self.u
                ), f"ValueError: {self.__class__.__name__}.__init__, {a_}, u={u}"
                if A[a_ >> 5] >> (a_ & 31) & 1 == 0:
                    len_ += 1
                    A[a_ >> 5] |= 1 << (a_ & 31)
            data.append(A)
            while u:
                a = array("I", bytes(4 * ((u >> 5) + 1)))
                for i in range(u + 1):
                    if A[i]:
                        a[i >> 5] |= 1 << (i & 31)
                data.append(a)
                A = a
                u >>= 5
        else:
            while u:
                u >>= 5
                data.append(array("I", bytes(4 * (u + 1))))
        self.data: list[array[int]] = data
        self.len: int = len_
        self.len_data: int = len(data)

    def add(self, v: int) -> bool:
        """整数 ``v`` を個追加します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.add({v}), u={self.u}"
        if self.data[0][v >> 5] >> (v & 31) & 1:
            return False
        self.len += 1
        for a in self.data:
            a[v >> 5] |= 1 << (v & 31)
            v >>= 5
        return True

    def discard(self, v: int) -> bool:
        """整数 ``v`` を削除します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.discard({v}), u={self.u}"
        if self.data[0][v >> 5] >> (v & 31) & 1 == 0:
            return False
        self.len -= 1
        for a in self.data:
            a[v >> 5] &= ~(1 << (v & 31))
            v >>= 5
            if a[v]:
                break
        return True

    def remove(self, v: int) -> None:
        """整数 ``v`` を削除します。
        :math:`O(\\log{u})` です。

        Note: ``v`` が存在しないとき、例外を投げます。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.remove({v}), u={self.u}"
        assert self.discard(v), f"ValueError: {v} not in self."

    def ge(self, v: int) -> Optional[int]:
        """``v`` 以上で最小の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.ge({v}), u={self.u}"
        data = self.data
        d = 0
        while True:
            if d >= self.len_data or v >> 5 >= len(data[d]):
                return None
            m = data[d][v >> 5] & ((~0) << (v & 31))
            if m == 0:
                d += 1
                v = (v >> 5) + 1
            else:
                v = (v >> 5 << 5) + (m & -m).bit_length() - 1
                if d == 0:
                    break
                v <<= 5
                d -= 1
        return v

    def gt(self, v: int) -> Optional[int]:
        """``v`` より大きい値で最小の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.gt({v}), u={self.u}"
        if v + 1 == self.u:
            return
        return self.ge(v + 1)

    def le(self, v: int) -> Optional[int]:
        """``v`` 以下で最大の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.le({v}), u={self.u}"
        data = self.data
        d = 0
        while True:
            if v < 0 or d >= self.len_data:
                return None
            m = data[d][v >> 5] & ~((~1) << (v & 31))
            if m == 0:
                d += 1
                v = (v >> 5) - 1
            else:
                v = (v >> 5 << 5) + m.bit_length() - 1
                if d == 0:
                    break
                v <<= 5
                v += 31
                d -= 1
        return v

    def lt(self, v: int) -> Optional[int]:
        """``v`` より小さい値で最大の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.lt({v}), u={self.u}"
        if v - 1 == 0:
            return
        return self.le(v - 1)

    def get_min(self) -> Optional[int]:
        """`最小値を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        return self.ge(0)

    def get_max(self) -> Optional[int]:
        """最大値を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        return self.le(self.u - 1)

    def pop_min(self) -> int:
        """最小値を削除して返します。
        :math:`O(\\log{u})` です。
        """
        v = self.get_min()
        assert (
            v is not None
        ), f"IndexError: pop_min() from empty {self.__class__.__name__}."
        self.discard(v)
        return v

    def pop_max(self) -> int:
        """最大値を削除して返します。
        :math:`O(\\log{u})` です。
        """
        v = self.get_max()
        assert (
            v is not None
        ), f"IndexError: pop_max() from empty {self.__class__.__name__}."
        self.discard(v)
        return v

    def clear(self) -> None:
        """集合を空にします。
        :math:`O(n\\log{u})` です。
        """
        for e in self:
            self.discard(e)
        self.len = 0

    def tolist(self) -> list[int]:
        """リストにして返します。
        :math:`O(n\\log{u})` です。
        """
        return [x for x in self]

    def __bool__(self):
        return self.len > 0

    def __len__(self):
        return self.len

    def __contains__(self, v: int):
        assert (
            0 <= v < self.u
        ), f"ValueError: {v} in {self.__class__.__name__}, u={self.u}"
        return self.data[0][v >> 5] >> (v & 31) & 1 == 1

    def __iter__(self):
        self._val = self.ge(0)
        return self

    def __next__(self):
        if self._val is None:
            raise StopIteration
        pre = self._val
        self._val = self.gt(pre)
        return pre

    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.u}, {self})"
