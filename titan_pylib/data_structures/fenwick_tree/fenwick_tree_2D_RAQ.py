class FenwickTree2DRAQ:
    """2次元です。区間加算ができます"""

    def __init__(self, h: int, w: int, a: list[list[int]] = []) -> None:
        """O(HWlogHlogW)"""
        self._h = h + 1
        self._w = w + 1
        self._bit = [[0] * (self._w) for _ in range(self._h)]
        if a:
            assert len(a) == h
            if h == 0:
                return
            assert len(a[0]) == w
            self._build(a)

    def _build(self, a: list[list[int]]) -> None:
        for i in range(self._h - 1):
            for j in range(self._w - 1):
                if a[i][j] != 0:
                    self.add(i, j, a[i][j])

    def add(self, h: int, w: int, x: int) -> None:
        """Add x to a[h][w]. / O(logH * logW)"""
        h += 1
        w += 1
        _h, _w, _bit = self._h, self._w, self._bit
        while h < _h:
            j = w
            bit_h = _bit[h]
            while j < _w:
                bit_h[j] += x
                j += j & -j
            h += h & -h

    def set(self, h: int, w: int, x: int) -> None:
        self.add(h, w, x - self.get(h, w))

    def range_add(self, h1: int, w1: int, h2: int, w2: int, x: int) -> int:
        """Add x to [h1, h2) x [w1, w2) of a. / O(logH * logW)"""
        assert h1 <= h2 and w1 <= w2
        self.add(h1, w1, x)
        self.add(h2, w1, -x)
        self.add(h1, w2, -x)
        self.add(h2, w2, x)

    def get(self, h: int, w: int) -> int:
        """Return a[h][w]. / O(logH * logW)"""
        ret = 0
        while h > 0:
            j = w
            bit_h = self._bit[h]
            while j > 0:
                ret += bit_h[j]
                j -= j & -j
            h -= h & -h
        return ret

    def __str__(self) -> str:
        ret = []
        for i in range(self._h - 1):
            ret.append(
                ", ".join(map(str, ((self.get(i, j)) for j in range(self._w - 1))))
            )
        return "[\n  " + "\n  ".join(map(str, ret)) + "\n]"
