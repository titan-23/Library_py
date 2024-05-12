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

    def __init__(self, u: int):
        self._n = (u >> 5) + 1
        self._data = array("I", bytes(self._n * 4))

    def add(self, k: int) -> None:
        self._data[k >> 5] |= Bitset.TABLE[k & 31]

    def discard(self, k: int) -> None:
        self._data[k >> 5] &= ~Bitset.TABLE[k & 31]

    def flip(self, k: int) -> None:
        self._data[k >> 5] ^= Bitset.TABLE[k & 31]

    def count(self) -> int:
        return sum(Bitset._popcount(b) for b in self._data)

    def __contains__(self, k: int) -> bool:
        return self._data[k >> 5] >> (k & 31) & 1 == 1

    def __getitem__(self, k: int):
        return self._data[k >> 5] >> (k & 31) & 1

    def __setitem__(self, k: int, bit: bool):
        if bit:
            self._data[k >> 5] |= Bitset.TABLE[k & 31]
        else:
            self._data[k >> 5] &= ~Bitset.TABLE[k & 31]

    def tolist(self) -> list[int]:
        return [
            (i << 5) + j
            for i, a in enumerate(self._data)
            for j in range(32)
            if a >> j & 1 == 1
        ]

    def __xor__(self, other) -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        res = Bitset(self._n)
        res_bit, self_bit, other_bit = res.bit, self.bit, other.bit
        for i in range(self.bsize):
            res_bit[i] = self_bit[i] ^ other_bit[i]
        return res

    def __or__(self, other) -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        res = Bitset(self._n)
        res_bit, self_bit, other_bit = res.bit, self.bit, other.bit
        for i in range(self.bsize):
            res_bit[i] = self_bit[i] | other_bit[i]
        return res

    def __ixor__(self, other) -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        self_bit, other_bit = self.bit, other.bit
        for i in range(self.bsize):
            self_bit[i] ^= other_bit[i]
        return self

    def __ior__(self, other) -> "Bitset":
        assert isinstance(other, Bitset)
        assert self._n == other._n
        self_bit, other_bit = self.bit, other.bit
        for i in range(self.bsize):
            self_bit[i] |= other_bit[i]
        return self

    def __rshift__(self, k: int):
        # x >> y: x.__rshift__(y)
        pass

    def __rrshift__(self, k: int):
        pass

    def __str__(self):
        return str(self.tolist())
