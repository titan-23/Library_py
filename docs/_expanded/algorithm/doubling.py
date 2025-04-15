# from titan_pylib.algorithm.doubling import Doubling
from typing import Callable


class Doubling:
    """ダブリングテーブルを構築します。
    :math:`O(n\\log{lim})` です。

    Args:
        n (int): テーブルサイズです。
                すべての ``i`` に対して :math:`0 \leq ``move_to(i)`` < n` である必要があります。
        lim (int): クエリの最大数です。
        move_to (Callable[[int], int]): 遷移関数です。 ``u`` から ``v`` へ遷移します。
    """

    def __init__(self, n: int, lim: int, move_to: Callable[[int], int]) -> None:
        self.move_to = move_to
        self.n = n
        self.lim = lim
        self.log = max(1, lim.bit_length())
        db = [[] for _ in range(self.log + 1)]
        db[0] = [move_to(i) for i in range(self.n)]
        for k in range(self.log):
            db[k + 1] = [db[k][db[k][i]] for i in range(self.n)]
        self.db = db

    def kth(self, start: int, k: int) -> int:
        """``start`` から ``k`` 個進んだ状態を返します。
        :math:`O(\\log{k})` です。

        Args:
            start (int): スタートの状態です。
            k (int): 遷移関数を適用する回数です。
        """
        db = self.db
        now = start
        for i in range(self.log):
            if k & 1:
                now = db[i][now]
            k >>= 1
        return now
