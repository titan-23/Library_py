from titan_pylib.data_structures.bit_vector.bit_vector import BitVector
from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
from array import array
from typing import List, Tuple, Sequence
from bisect import bisect_left


class FenwickTreeWaveletMatrix:

    def __init__(self, sigma: int, pos: List[Tuple[int, int, int]] = []):
        self.sigma: int = sigma
        self.log: int = (sigma - 1).bit_length()
        self.mid: array[int] = array("I", bytes(4 * self.log))
        self.xy: List[Tuple[int, int]] = self._sort_unique([(x, y) for x, y, _ in pos])
        self.y: List[int] = self._sort_unique([y for _, y, _ in pos])
        self.size: int = len(self.xy)
        self.v: List[BitVector] = [BitVector(self.size) for _ in range(self.log)]
        self._build([bisect_left(self.y, y) for _, y in self.xy])
        ws = [[0] * self.size for _ in range(self.log)]
        for x, y, w in pos:
            k = bisect_left(self.xy, (x, y))
            i_y = bisect_left(self.y, y)
            for bit in range(self.log - 1, -1, -1):
                if i_y >> bit & 1:
                    k = self.v[bit].rank1(k) + self.mid[bit]
                else:
                    k = self.v[bit].rank0(k)
                ws[bit][k] += w
        self.bit: List[FenwickTree] = [FenwickTree(a) for a in ws]

    def _build(self, a: Sequence[int]) -> None:
        # 列 a から wm を構築する
        for bit in range(self.log - 1, -1, -1):
            # bit目の0/1に応じてvを構築 + aを安定ソート
            v = self.v[bit]
            zero, one = [], []
            for i, e in enumerate(a):
                if e >> bit & 1:
                    v.set(i)
                    one.append(e)
                else:
                    zero.append(e)
            v.build()
            self.mid[bit] = len(zero)  # 境界をmid[bit]に保持
            a = zero + one

    def _sort_unique(self, a: List) -> List:
        if not a:
            return a
        a.sort()
        b = [a[0]]
        for e in a:
            if b[-1] == e:
                continue
            b.append(e)
        return b

    def add_point(self, x: int, y: int, w: int) -> None:
        k = bisect_left(self.xy, (x, y))
        i_y = bisect_left(self.y, y)
        for bit in range(self.log - 1, -1, -1):
            if i_y >> bit & 1:
                k = self.v[bit].rank1(k) + self.mid[bit]
            else:
                k = self.v[bit].rank0(k)
            self.bit[bit].add(k, w)

    def _sum(self, l: int, r: int, x: int) -> int:
        ans = 0
        for bit in range(self.log - 1, -1, -1):
            l0, r0 = self.v[bit].rank0(l), self.v[bit].rank0(r)
            if x >> bit & 1:
                l += self.mid[bit] - l0
                r += self.mid[bit] - r0
                ans += self.bit[bit].sum(l0, r0)
            else:
                l, r = l0, r0
        return ans

    def sum(self, w1: int, w2: int, h1: int, h2: int) -> int:
        # sum([w1, w2) x [h1, h2))
        l = bisect_left(self.xy, (w1, 0))
        r = bisect_left(self.xy, (w2, 0))
        return self._sum(l, r, bisect_left(self.y, h2)) - self._sum(
            l, r, bisect_left(self.y, h1)
        )
