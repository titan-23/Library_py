from titan_pylib.data_structures.set.wordsize_tree_set import WordsizeTreeSet
from typing import Iterable, Optional, Iterator


class WordsizeTreeMultiset:
    """``[0, u)`` の整数多重集合を管理する32分木です。
    空間 :math:`O(u)` であることに注意してください。
    """

    def __init__(self, u: int, a: Iterable[int] = []) -> None:
        """:math:`O(u)` です。"""
        u += 1  # 念のため
        assert u >= 0
        self.u = u
        self.len: int = 0
        self.st: WordsizeTreeSet = WordsizeTreeSet(u, a)
        cnt = [0] * (u + 1)
        for a_ in a:
            self.len += 1
            cnt[a_] += 1
        self.cnt: list[int] = cnt

    def add(self, v: int, cnt: int = 1) -> None:
        """整数 ``v`` を ``cnt`` 個追加します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.add({v}, {cnt}), u={self.u}"
        self.len += cnt
        if self.cnt[v]:
            self.cnt[v] += cnt
        else:
            self.cnt[v] = cnt
            self.st.add(v)

    def discard(self, v: int, cnt: int = 1) -> bool:
        """整数 ``v`` を ``cnt`` 個削除します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.discard({v}), u={self.u}"
        if self.cnt[v] == 0:
            return False
        c = self.cnt[v]
        if c > cnt:
            self.cnt[v] -= cnt
            self.len -= cnt
        else:
            self.len -= c
            self.cnt[v] = 0
            self.st.discard(v)
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

    def count(self, v: int) -> int:
        """整数 ``v`` の個数を返します。
        :math:`O(1)` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.count({v}), u={self.u}"
        return self.cnt[v]

    def ge(self, v: int) -> Optional[int]:
        """``v`` 以上で最小の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.ge({v}), u={self.u}"
        return self.st.ge(v)

    def gt(self, v: int) -> Optional[int]:
        """``v`` より大きい値で最小の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.gt({v}), u={self.u}"
        return self.ge(v + 1)

    def le(self, v: int) -> Optional[int]:
        """``v`` 以下で最大の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.le({v}), u={self.u}"
        return self.st.le(v)

    def lt(self, v: int) -> Optional[int]:
        """``v`` より小さい値で最大の要素を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        assert (
            0 <= v < self.u
        ), f"ValueError: {self.__class__.__name__}.lt({v}), u={self.u}"
        return self.le(v - 1)

    def get_min(self) -> Optional[int]:
        """`最小値を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        return self.st.ge(0)

    def get_max(self) -> Optional[int]:
        """最大値を返します。存在しないとき、 ``None``を返します。
        :math:`O(\\log{u})` です。
        """
        return self.st.le(self.st.u - 1)

    def pop_min(self) -> int:
        """最小値を削除して返します。
        :math:`O(\\log{u})` です。
        """
        assert self, f"IndexError: pop_min() from empty {self.__class__.__name__}."
        x = self.st.get_min()
        self.discard(x)
        return x

    def pop_max(self) -> int:
        """最大値を削除して返します。
        :math:`O(\\log{u})` です。
        """
        assert self, f"IndexError: pop_max() from empty {self.__class__.__name__}."
        x = self.st.get_max()
        self.discard(x)
        return x

    def keys(self) -> Iterator[int]:
        """集合に含まれている要素(重複無し)を昇順にイテレートします。
        :math:`O(n\\log{u})` です。
        """
        v = self.st.get_min()
        while v is not None:
            yield v
            v = self.st.gt(v)

    def values(self) -> Iterator[int]:
        """集合に含まれている要素の個数を、要素の昇順にイテレートします。
        :math:`O(n\\log{u})` です。
        """
        v = self.st.get_min()
        while v is not None:
            yield self.cnt[v]
            v = self.st.gt(v)

    def items(self) -> Iterator[tuple[int, int]]:
        """集合に含まれている要素とその個数を、要素の昇順にイテレートします。
        :math:`O(n\\log{u})` です。
        """
        v = self.st.get_min()
        while v is not None:
            yield (v, self.cnt[v])
            v = self.st.gt(v)

    def clear(self) -> None:
        """集合を空にします。
        :math:`O(n\\log{u})` です。
        """
        for e in self:
            self.cnt[e] = 0
            self.st.discard(e)
        self.len = 0

    def tolist(self) -> list[int]:
        """リストにして返します。
        :math:`O(n\\log{u})` です。
        """
        return [x for x in self]

    def __contains__(self, v: int):
        """:math:`O(1)` です。"""
        return self.cnt[v] > 0

    def __bool__(self):
        return self.len > 0

    def __len__(self):
        return self.len

    def __iter__(self):
        self.__val = self.st.get_min()
        self.__valcnt = 1
        return self

    def __next__(self):
        if self.__val is None:
            raise StopIteration
        pre = self.__val
        self.__valcnt += 1
        if self.__valcnt > self.cnt[self.__val]:
            self.__valcnt = 1
            self.__val = self.gt(self.__val)
        return pre

    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.u}, [" + ", ".join(map(str, self)) + "])"
        )
