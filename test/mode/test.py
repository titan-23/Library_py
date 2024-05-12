from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class StaticRangeModeQuery(Generic[T]):
    """静的な列に対する区間最頻値クエリに答えます。
    <構築 :math:`O(n\\sqrt{n})` , クエリ :math:`O(\\sqrt{n)})` >

    参考: https://noshi91.hatenablog.com/entry/2020/10/26/140105
    """

    @staticmethod
    def _sort_unique(a: list[T]) -> list[T]:
        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
            new_a = [a[0]]
            for elm in a:
                if new_a[-1] == elm:
                    continue
                new_a.append(elm)
            a = new_a
        return a

    def __init__(self, a: Iterable[T], compress: bool = True) -> None:
        """``a`` から ``StaticRangeModeQuery`` を構築します。
        :math:`O(n \\sqrt{n})` です。

        Args:
          a (Iterable[T]):
          compress (bool, optional): ``False`` なら座標圧縮しません。空間計算量に気を付けてください。
        """

        a: list[T] = list(a)
        self.to_origin: list[T] = []
        self.compress: bool = compress
        if compress:
            self.to_origin = StaticRangeModeQuery._sort_unique(a)
            to_zaatsu: dict[T, int] = {x: i for i, x in enumerate(self.to_origin)}
            self.a: list[int] = [to_zaatsu[x] for x in a]
        else:
            self.a: list[int] = a

        self.n: int = len(self.a)
        self.u: int = max(self.a) + 1
        self.size: int = int(self.n**0.5) + 1
        self.bucket_cnt: int = (self.n + self.size - 1) // self.size
        self.data: list[list[int]] = [
            self.a[k * self.size : (k + 1) * self.size] for k in range(self.bucket_cnt)
        ]

        # (freq, val)
        self.bucket_data: list[list[tuple[int, int]]] = [
            [(0, -1)] * (self.bucket_cnt + 1) for _ in range(self.bucket_cnt + 1)
        ]
        self._calc_all_blocks()

        self.indx: list[list[int]] = [[] for _ in range(self.u)]
        self.inv_indx: list[int] = [-1] * self.n
        self._calc_index()

    def _calc_all_blocks(self) -> None:
        """``bucket_data`` を計算します
        :math:`O(n \\sqrt{n})` です。

        bucket_data[i][j] := data[i:j] の (freq, val)
        """
        data, bucket_data = self.data, self.bucket_data
        freqs = [0] * self.u
        for i in range(self.bucket_cnt):
            freq, val = -1, -1
            for j in range(i + 1, self.bucket_cnt + 1):
                for x in data[j - 1]:
                    freqs[x] += 1
                    if freqs[x] > freq:
                        freq, val = freqs[x], x
                bucket_data[i][j] = (freq, val)
            for j in range(i + 1, self.bucket_cnt + 1):
                for x in data[j - 1]:
                    freqs[x] = 0

    def _calc_index(self):
        """``indx``, ``inv_indx`` を計算します
        :math:`O(n)` です。

        indx[x]: 値 x の、 a におけるインデックス(昇順)
        inv_indx[i]: aにおける位置i の、indx[a[i]] でのインデックス
        """
        indx, inv_indx = self.indx, self.inv_indx
        for i, e in enumerate(self.a):
            inv_indx[i] = len(indx[e])
            indx[e].append(i)

    def mode(self, l: int, r: int) -> tuple[T, int]:
        """区間 ``[l, r)`` の最頻値とその頻度を返します。

        Args:
          l (int):
          r (int):

        Returns:
          tuple[T, int]: (最頻値, 頻度) のタプルです。
        """
        assert 0 <= l < r <= self.n
        L, R = l, r
        k1 = l // self.size
        k2 = r // self.size
        l -= k1 * self.size
        r -= k2 * self.size

        freq, val = 0, -1

        if k1 == k2:
            a, indx, inv_indx = self.a, self.indx, self.inv_indx
            for i in range(L, R):
                x = a[i]
                k = inv_indx[i]
                freq_cand = freq + 1
                while (
                    k + freq_cand - 1 < len(indx[x]) and indx[x][k + freq_cand - 1] < R
                ):
                    freq, val = freq_cand, x
                    freq_cand += 1

        else:
            data, indx, inv_indx = self.data, self.indx, self.inv_indx

            freq, val = self.bucket_data[k1 + 1][k2]

            # left
            for i in range(l, len(data[k1])):
                x = data[k1][i]
                k = inv_indx[k1 * self.size + i]
                freq_cand = freq + 1
                while (
                    k + freq_cand - 1 < len(indx[x]) and indx[x][k + freq_cand - 1] < R
                ):
                    freq, val = freq_cand, x
                    freq_cand += 1

            # right
            for i in range(r):
                x = data[k2][i]
                k = inv_indx[k2 * self.size + i]
                freq_cand = freq + 1
                while 0 <= k - (freq_cand - 1) and L <= indx[x][k - (freq_cand - 1)]:
                    freq, val = freq_cand, x
                    freq_cand += 1

        val = self.to_origin[val] if self.compress else val
        return val, freq


from time import process_time


n, q = map(int, input().split())
A = list(map(int, input().split()))

start = process_time()
rmq = StaticRangeModeQuery(A)

for _ in range(q):
    l, r = map(int, input().split())
    val, freq = rmq.mode(l, r)

print(process_time() - start)
# 0.54
