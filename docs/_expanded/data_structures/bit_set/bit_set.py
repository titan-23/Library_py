# from titan_pylib.data_structures.bit_set.bit_set import Bitset
from array import array


class Bitset:

    TABLE = array("I", (1 << i for i in range(32)))

    @staticmethod
    def _popcount(x: int) -> int:
        x = x - ((x >> 1) & 0x55555555)
        x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
        x = x + (x >> 4) & 0x0F0F0F0F
        x += x >> 8
        x += x >> 16
        return x & 0x0000007F

    def __init__(self, n: int) -> int:
        self._n = n
        self._m = (n >> 5) + 1
        self._data = array("I", bytes(self._m * 4))

    def set(self, k: int) -> None:
        self._data[k >> 5] |= Bitset.TABLE[k & 31]

    def reset(self, k: int) -> None:
        self._data[k >> 5] &= ~Bitset.TABLE[k & 31]

    def flip(self, k: int) -> None:
        self._data[k >> 5] ^= Bitset.TABLE[k & 31]

    def count(self) -> int:
        return sum(Bitset._popcount(b) for b in self._data)

    def __contains__(self, k: int) -> bool:
        return self._data[k >> 5] >> (k & 31) & 1 == 1

    def __getitem__(self, k: int) -> int:
        return self._data[k >> 5] >> (k & 31) & 1

    def __setitem__(self, k: int, bit: bool) -> None:
        if bit:
            self._data[k >> 5] |= Bitset.TABLE[k & 31]
        else:
            self._data[k >> 5] &= ~Bitset.TABLE[k & 31]

    def tolist(self) -> list[int]:
        return [
            (i << 5) + j
            for i, a in enumerate(self._data)
            for j in range(32)
            if a >> j & 1
        ]

    def __xor__(self, other: "Bitset") -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        res = Bitset(self._n)
        res_data, self_data, other_data = res.data, self._data, other._data
        for i in range(self._m):
            res_data[i] = self_data[i] ^ other_data[i]
        return res

    def __or__(self, other: "Bitset") -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        res = Bitset(self._n)
        res_data, self_data, other_data = res.data, self._data, other._data
        for i in range(self._m):
            res_data[i] = self_data[i] | other_data[i]
        return res

    def __ixor__(self, other: "Bitset") -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        self_data, other_data = self._data, other._data
        for i in range(self._m):
            self_data[i] ^= other_data[i]
        return self

    def __ior__(self, other: "Bitset") -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        self_data, other_data = self._data, other._data
        for i in range(self._m):
            self_data[i] |= other_data[i]
        return self

    def __rshift__(self, k: int):
        raise NotImplementedError

    def __rrshift__(self, k: int):
        raise NotImplementedError

    def __len__(self) -> int:
        return self._n

    def __str__(self):
        return str(self.tolist())
