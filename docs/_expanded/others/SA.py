# from titan_pylib.others.SA import SA
import sys
from time import process_time
from math import exp
from typing import TypeVar
# from titan_pylib.algorithm.random.random import Random
from typing import Any


class Random:
    """Random
    乱数系のライブラリです。
    標準ライブラリよりも高速なつもりでいます。
    """

    def __init__(self) -> None:
        self._x = 123456789
        self._y = 362436069
        self._z = 521288629
        self._w = 88675123

    def _xor(self) -> int:
        t = (self._x ^ ((self._x << 11) & 0xFFFFFFFF)) & 0xFFFFFFFF
        self._x, self._y, self._z = self._y, self._z, self._w
        self._w = (self._w ^ (self._w >> 19)) ^ (
            t ^ ((t >> 8)) & 0xFFFFFFFF
        ) & 0xFFFFFFFF
        return self._w

    def random(self) -> float:
        """0以上1以下の一様ランダムな値を1つ生成して返すはずです。
        :math:`O(1)` です。
        """
        return self._xor() / 0xFFFFFFFF

    def randint(self, begin: int, end: int) -> int:
        """``begin`` 以上 ``end`` **以下** のランダムな整数を返します。
        :math:`O(1)` です。

        制約:
            :math:`begin \\leq end`
        """
        assert begin <= end
        return begin + self._xor() % (end - begin + 1)

    def randrange(self, begin: int, end: int) -> int:
        """``begin`` 以上 ``end`` **未満** のランダムな整数を返します。
        :math:`O(1)` です。

        制約:
            :math:`begin < end`
        """
        assert begin < end
        return begin + self._xor() % (end - begin)

    def shuffle(self, a: list[Any]) -> None:
        """``a`` をインプレースにシャッフルします。
        :math:`O(n)` です。

        Args:
            a (list[Any]): ``a`` をシャッフルします。
        """
        n = len(a)
        for i in range(n - 1):
            j = self.randrange(i, n)
            a[i], a[j] = a[j], a[i]


class State:

    def __init__(self) -> None:
        pass

    def copy(self) -> "State":
        pass


class SA:

    Changed = TypeVar("Changed")

    def __init__(self):
        self.random = Random()

    def make_ans_init(self) -> tuple[State, int]:
        return

    def modify(self, state: State) -> tuple[int, Changed]:
        # state は変更される
        return

    def rollback(self, state: State, changed: Changed) -> None:
        return

    def sovle(
        self, START_TEMP: float = 100, END_TEMP: float = 10, TIME_LIMIT: float = 1.8
    ) -> tuple[State, int]:
        START_TIME = process_time()
        random = self.random
        ans, score = self.make_ans_init()
        vest_ans = ans.copy()
        vest_score = score
        cnt = 0
        while True:
            now_time = process_time() - START_TIME
            if now_time > TIME_LIMIT:
                break
            cnt += 1
            diff_score, changed = self.modify(ans)
            new_score = score + diff_score
            temp = START_TEMP + (END_TEMP - START_TEMP) * now_time / TIME_LIMIT
            arg = new_score - score
            if arg >= 1 or exp(arg / temp) > random.random():
                score = new_score
                if new_score > vest_score:
                    vest_score = new_score
                    vest_ans = ans.copy()
            else:
                self.rollback(ans, changed)
        print(f"{cnt=}", file=sys.stderr)
        return vest_ans, vest_score
