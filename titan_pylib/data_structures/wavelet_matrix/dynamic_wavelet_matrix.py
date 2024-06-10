from titan_pylib.data_structures.bit_vector.avl_tree_bit_vector import AVLTreeBitVector
from titan_pylib.data_structures.wavelet_matrix.wavelet_matrix import WaveletMatrix
from typing import Sequence
from array import array


class DynamicWaveletMatrix(WaveletMatrix):
    """動的ウェーブレット行列です。

    (静的)ウェーブレット行列でできる操作に加えて ``insert / pop / set`` 等ができます。
      - ``BitVector`` を平衡二分木にしています(``AVLTreeBitVector``)。あらゆる操作に平衡二分木の log がつきます。これヤバくね

    :math:`O(n\\log{(\\sigma)})` です。
    """

    def __init__(self, sigma: int, a: Sequence[int] = []) -> None:
        self.sigma: int = sigma
        self.log: int = (sigma - 1).bit_length()
        self.v: list[AVLTreeBitVector] = [AVLTreeBitVector()] * self.log
        self.mid: array[int] = array("I", bytes(4 * self.log))
        self.size: int = len(a)
        self._build(a)

    def _build(self, a: Sequence[int]) -> None:
        v = array("B", bytes(self.size))
        for bit in range(self.log - 1, -1, -1):
            # bit目の0/1に応じてvを構築 + aを安定ソート
            zero, one = [], []
            for i, e in enumerate(a):
                if e >> bit & 1:
                    v[i] = 1
                    one.append(e)
                else:
                    v[i] = 0
                    zero.append(e)
            self.mid[bit] = len(zero)  # 境界をmid[bit]に保持
            self.v[bit] = AVLTreeBitVector(v)
            a = zero + one

    def reserve(self, n: int) -> None:
        """``n`` 要素分のメモリを確保します。
        :math:`O(n)` です。
        """
        assert n >= 0, f"ValueError: {self.__class__.__name__}.reserve({n})"
        for v in self.v:
            v.reserve(n)

    def insert(self, k: int, x: int) -> None:
        """位置 ``k`` に ``x`` を挿入します。
        :math:`O(\\log{(n)}\\log{(\\sigma)})` です。
        """
        assert (
            0 <= k <= self.size
        ), f"IndexError: {self.__class__.__name__}.insert({k}, {x}), n={self.size}"
        assert (
            0 <= x < 1 << self.log
        ), f"ValueError: {self.__class__.__name__}.insert({k}, {x}), LIM={1<<self.log}"
        mid = self.mid
        for bit in range(self.log - 1, -1, -1):
            v = self.v[bit]
            # if x >> bit & 1:
            #   v.insert(k, 1)
            #   k = v.rank1(k) + mid[bit]
            # else:
            #   v.insert(k, 0)
            #   mid[bit] += 1
            #   k = v.rank0(k)
            if x >> bit & 1:
                s = v._insert_and_rank1(k, 1)
                k = s + mid[bit]
            else:
                s = v._insert_and_rank1(k, 0)
                k -= s
                mid[bit] += 1
        self.size += 1

    def pop(self, k: int) -> int:
        """位置 ``k`` の要素を削除し、その値を返します。
        :math:`O(\\log{(n)}\\log{(\\sigma)})` です。
        """
        assert (
            0 <= k < self.size
        ), f"IndexError: {self.__class__.__name__}.pop({k}), n={self.size}"
        mid = self.mid
        ans = 0
        for bit in range(self.log - 1, -1, -1):
            v = self.v[bit]
            # K = k
            # if v.access(k):
            #   ans |= 1 << bit
            #   k = v.rank1(k) + mid[bit]
            # else:
            #   mid[bit] -= 1
            #   k = v.rank0(k)
            # v.pop(K)
            sb = v._access_pop_and_rank1(k)
            s = sb >> 1
            if sb & 1:
                ans |= 1 << bit
                k = s + mid[bit]
            else:
                mid[bit] -= 1
                k -= s
        self.size -= 1
        return ans

    def set(self, k: int, x: int) -> None:
        """位置 ``k`` の要素を ``x`` に更新します。
        :math:`O(\\log{(n)}\\log{(\\sigma)})` です。
        """
        assert (
            0 <= k < self.size
        ), f"IndexError: {self.__class__.__name__}.set({k}, {x}), n={self.size}"
        assert (
            0 <= x < 1 << self.log
        ), f"ValueError: {self.__class__.__name__}.set({k}, {x}), LIM={1<<self.log}"
        self.pop(k)
        self.insert(k, x)

    def __setitem__(self, k: int, x: int):
        assert (
            0 <= k < self.size
        ), f"IndexError: {self.__class__.__name__}[{k}] = {x}, n={self.size}"
        assert (
            0 <= x < 1 << self.log
        ), f"ValueError: {self.__class__.__name__}[{k}] = {x}, LIM={1<<self.log}"
        self.set(k, x)

    def __str__(self):
        return f"{self.__class__.__name__}({[self[i] for i in range(self.size)]})"
